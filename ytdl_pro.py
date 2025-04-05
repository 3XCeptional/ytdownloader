#!/usr/bin/env python3
import argparse
import os
import logging
import traceback
from multiprocessing import Pool, cpu_count
from typing import List, Tuple, Optional

# Third-party imports - Install these!
# pip install yt-dlp fake-useragent tqdm
try:
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError  # Fixed exception usage
    from fake_useragent import UserAgent
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries not found.")
    print("Please install them using: pip install yt-dlp fake-useragent tqdm")
    exit(1)

# --- Configuration ---
DEFAULT_OUTPUT_DIR = "."
DEFAULT_PROCESSES = cpu_count()

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(processName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

# --- User Agent ---
try:
    ua = UserAgent()
except Exception:
    log.warning("Could not initialize fake-useragent. Falling back to default yt-dlp UA.")
    ua = None

# Define postprocessor arguments separately
POSTPROCESSOR_ARGS = {
    'metadata': ['-map', '0', '-map', '1', '-c', 'copy', '-disposition:v:1', 'attached_pic']
}

# --- Download Function ---
def download_video(args_tuple: Tuple[str, str, str, Optional[str], bool]) -> Tuple[str, bool, Optional[str]]:
    """Downloads a single YouTube video using yt-dlp."""
    url, quality, output_dir, cookiefile, quiet_ydl = args_tuple
    video_title = url
    try:
        user_agent = ua.random if ua else "Mozilla/5.0"  # Fallback UA

        # Construct the full output path template
        output_template = os.path.abspath(os.path.join(output_dir, "%(title)s [%(id)s].%(ext)s"))

        ydl_opts = {
            'outtmpl': output_template,
            'format': f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'merge_output_format': 'mp4',
            'nocheckcertificate': False,
            'quiet': quiet_ydl,
            'progress_hooks': [],
            'http_headers': {'User-Agent': user_agent},
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'writethumbnail': True,
            # Include postprocessor_args if writethumbnail is enabled
            'postprocessor_args': POSTPROCESSOR_ARGS if True else None,
        }

        if cookiefile and os.path.exists(cookiefile):
            ydl_opts['cookiefile'] = cookiefile
            log.debug(f"Using cookie file: {cookiefile} for {url}")
        elif cookiefile:
            log.warning(f"Cookie file specified but not found: {cookiefile}")

        with YoutubeDL(ydl_opts) as ydl:
            log.debug(f"Starting download: {url} with UA: {user_agent}")
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', url)
            log.info(f"Downloading: '{video_title}' ({url}) to '{os.path.dirname(output_template)}'")
            ydl.download([url])
            log.info(f"Finished: '{video_title}' ({url})")
            return url, True, None

    except DownloadError as e:
        log.error(f"yt-dlp error downloading '{video_title}' ({url}): {e}")
        return url, False, str(e)
    except Exception as e:
        log.error(f"Unexpected error downloading '{video_title}' ({url}): {e}")
        log.debug(traceback.format_exc())
        return url, False, f"Unexpected error: {e}"

# --- Main Orchestration ---
def main(urls: List[str], quality: str, output_dir: str, processes: int, cookiefile: Optional[str], quiet_ydl: bool):
    """Manages the download process using a process pool."""
    log.info(f"Starting download process for {len(urls)} videos.")
    log.info(f"Quality: {quality}p")
    abs_output_dir = os.path.abspath(output_dir)
    log.info(f"Output directory: {abs_output_dir}")
    log.info(f"Using {processes} parallel processes.")
    if cookiefile:
        log.info(f"Using cookie file: {cookiefile}")

    try:
        os.makedirs(abs_output_dir, exist_ok=True)
        if output_dir != ".":
            log.info(f"Ensured output directory exists: {abs_output_dir}")
    except OSError as e:
        log.error(f"Failed to create output directory '{abs_output_dir}': {e}")
        return

    download_args = [(url, quality, output_dir, cookiefile, quiet_ydl) for url in urls]

    success_count = 0
    fail_count = 0
    failed_urls = []

    try:
        with Pool(processes=processes) as pool:
            results = list(tqdm(pool.imap_unordered(download_video, download_args),
                                total=len(urls),
                                desc="Overall Progress",
                                unit="video"))
        for url, success, error_msg in results:
            if success:
                success_count += 1
            else:
                fail_count += 1
                failed_urls.append((url, error_msg))
    except KeyboardInterrupt:
        log.warning("\nDownload interrupted by user.")
    except Exception as e:
        log.error(f"An critical error occurred during multiprocessing: {e}")
        log.debug(traceback.format_exc())
    finally:
        log.info("--- Download Summary ---")
        log.info(f"Output directory: {abs_output_dir}")
        log.info(f"Successfully downloaded: {success_count} video(s)")
        log.info(f"Failed to download: {fail_count} video(s)")
        if failed_urls:
            log.warning("Failed URLs:")
            for url, reason in failed_urls:
                log.warning(f"  - {url} (Reason: {reason})")
        log.info("------------------------")

# --- Argument Parsing and Script Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download YouTube videos concurrently using yt-dlp. Defaults to saving in the current directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-u", "--urls", nargs="+", help="List of YouTube video URLs.")
    input_group.add_argument("-f", "--file", type=str, help="Path to a file containing YouTube video URLs (one per line).")

    parser.add_argument("-q", "--quality", type=str, required=True, help="Max video quality/height (e.g., 1080, 720).")
    parser.add_argument("-o", "--output",
                        type=str,
                        default=DEFAULT_OUTPUT_DIR,
                        help="Output directory for downloaded videos. Defaults to the current directory.")
    parser.add_argument("-p", "--processes", type=int, default=DEFAULT_PROCESSES, help="Number of parallel downloads.")
    parser.add_argument("-c", "--cookiefile", type=str, default=None, help="Path to a cookies file (optional).")
    parser.add_argument("--quiet-ydl", action='store_true', help="Suppress yt-dlp's own console output.")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose logging for this script.")

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        log.debug("Verbose logging enabled.")

    video_urls = []
    if args.urls:
        video_urls = args.urls
    elif args.file:
        try:
            file_path = os.path.abspath(args.file)
            with open(file_path, 'r') as f:
                video_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            if not video_urls:
                log.error(f"No valid URLs found in file: {file_path}")
                exit(1)
            log.info(f"Loaded {len(video_urls)} URLs from {file_path}")
        except FileNotFoundError:
            log.error(f"URL file not found: {file_path}")
            exit(1)
        except Exception as e:
            log.error(f"Error reading URL file '{file_path}': {e}")
            exit(1)

    if args.processes <= 0:
        log.warning(f"Invalid process count ({args.processes}). Using default: {DEFAULT_PROCESSES}")
        args.processes = DEFAULT_PROCESSES

    cookie_path = None
    if args.cookiefile:
        cookie_path = os.path.abspath(args.cookiefile)
        if not os.path.exists(cookie_path):
            log.warning(f"Specified cookie file does not exist: {cookie_path}")

    main(video_urls, args.quality, args.output, args.processes, cookie_path, args.quiet_ydl)
