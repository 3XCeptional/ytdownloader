#!./venv/bin/python
import argparse
from yt_dlp import YoutubeDL
from multiprocessing import Pool
import os
from fake_useragent import UserAgent  # Import fake-useragent

def download_video(args):
    url, quality, output_dir = args
    try:
        # Generate a random user-agent
        ua = UserAgent()
        user_agent = ua.random

        ydl_opts = {
            'outtmpl': os.path.join(output_dir, "%(title)s.%(ext)s"),
            'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'merge_output_format': 'mp4',
            'nocheckcertificate': False,
            'quiet': True,
            'progress_hooks': [lambda d: print(f"Progress: {d['_percent_str']} - {d['_speed_str']}")],
            'cookiefile': 'cookies.txt',  # Optional: Add cookies file
            'http_headers': {
                'User-Agent': user_agent,  # Use the random user-agent
            },
        }
        with YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url} with User-Agent: {user_agent}")
            ydl.download([url])
            print(f"Finished downloading: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main(urls, quality, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Use multiprocessing to download videos in parallel
    with Pool(processes=4) as pool:  # Adjust the number of processes as needed
        pool.map(download_video, [(url, quality, output_dir) for url in urls])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos using yt-dlp and multiprocessing.")
    parser.add_argument("-u", "--urls", nargs="+", required=True, help="List of YouTube video URLs to download.")
    parser.add_argument("-q", "--quality", type=str, required=True, help="Video quality (e.g., 1080, 720).")
    parser.add_argument("-o", "--output", type=str, default="YTdownloads", help="Output directory for downloaded videos (default: YTdownloads).")
    args = parser.parse_args()

    main(args.urls, args.quality, args.output)