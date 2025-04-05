# Concurrent YouTube Downloader (using yt-dlp)

A Python script and Docker setup to download YouTube videos concurrently using the powerful `yt-dlp` library. It supports quality selection, reading URLs from files, using cookies for restricted content, and flexible output locations, defaulting to the current directory for simplicity.

## Features

*   **Concurrent Downloads:** Uses Python's `multiprocessing` to download multiple videos in parallel, significantly speeding up batch downloads.
*   **Quality Selection:** Specify the maximum desired video quality (e.g., 1080p, 720p).
*   **Flexible Input:** Provide video URLs directly via command line or list them in a text file.
*   **Cookie Support:** Use browser cookies (e.g., `cookies.txt` format) to download age-restricted or members-only content (requires exporting cookies from your browser).
*   **Configurable Output:** Download videos to the current directory (default) or specify a custom output path.
*   **Progress Tracking:** Uses `tqdm` for a clean overall progress bar.
*   **Metadata & Thumbnails:** Embeds video metadata (title, uploader) and thumbnail into the output MP4 file (requires `ffmpeg`).
*   **Random User-Agents:** Uses `fake-useragent` to vary the User-Agent header for downloads.
*   **Dockerized:** Includes a `Dockerfile` for easy setup and dependency management, running as a non-root user for better security.

## Prerequisites

### For Running the Script Directly:

1.  **Python:** Version 3.8 or higher recommended.
2.  **pip:** Python package installer (usually comes with Python).
3.  **ffmpeg:** Essential for merging video/audio streams and embedding metadata/thumbnails. `yt-dlp` relies heavily on it. Ensure `ffmpeg` is installed and accessible in your system's PATH. ([Download ffmpeg](https://ffmpeg.org/download.html))
4.  **Git (Optional):** To clone the repository.

### For Using Docker:

1.  **Docker Engine:** Install Docker for your operating system. ([Install Docker](https://docs.docker.com/engine/install/))
    *   _(ffmpeg and Python dependencies are handled *inside* the container)_

## Installation / Setup

### Option 1: Run the Script Directly

1.  **Clone or Download:**
    ```bash
    git clone https://github.com/3XCeptional/ytdownloader.git # Or download the ZIP and extract
    cd ytdownloader
    ```
2.  **(Optional but Recommended) Create a Virtual Environment:**
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Verify `ffmpeg`:** Make sure the `ffmpeg` command works in your terminal.

### Option 2: Use Docker (Recommended for Isolation & Simplicity)

1.  **Clone or Download:**
    ```bash
    git clone <repository_url> # Or download the ZIP and extract
    cd <repository_directory>
    ```
2.  **Build the Docker Image:**
    ```bash
    docker build -t yt-downloader .
    ```
    *(This command builds an image named `yt-downloader` based on the `Dockerfile` in the current directory.)*

## Usage

The script (`ytdl_pro.py`) downloads files to the current working directory by default.

### Running the Script Directly

*(Make sure you are in the repository directory and have activated the virtual environment if you created one)*

*   **Download specific URLs (max 1080p) to current directory:**
    ```bash
    python ytdl_pro.py -q 1080 -u https://www.youtube.com/watch?v=VIDEO_ID_1 https://www.youtube.com/watch?v=VIDEO_ID_2
    ```
*   **Download from a file (max 720p) to a specific directory:**
    *(Create `urls.txt` with one URL per line)*
    ```bash
    python ytdl_pro.py -q 720 -f urls.txt -o ./my_video_downloads
    ```
*   **Use cookies (for restricted content):**
    *(Requires a `cookies.txt` file exported from your browser)*
    ```bash
    python ytdl_pro.py -q 1080 -c cookies.txt -u https://www.youtube.com/watch?v=RESTRICTED_VIDEO_ID
    ```
*   **Increase parallel downloads (e.g., 8 processes):**
    ```bash
    python ytdl_pro.py -q 720 -p 8 -f urls.txt
    ```
*   **Get help:**
    ```bash
    python ytdl_pro.py --help
    ```

### Running with Docker

The key advantage here is easy dependency management and the ability to map your host directory directly into the container's working directory (`/app`).

*   **Download URLs (max 1080p), saving to your current host directory:**
    ```bash
    # Linux/macOS
    docker run --rm -v "$(pwd):/app" yt-downloader -q 1080 -u https://www.youtube.com/watch?v=VIDEO_ID

    # Windows (PowerShell)
    docker run --rm -v "${PWD}:/app" yt-downloader -q 1080 -u https://www.youtube.com/watch?v=VIDEO_ID

    # Windows (CMD)
    docker run --rm -v "%CD%:/app" yt-downloader -q 1080 -u https://www.youtube.com/watch?v=VIDEO_ID
    ```
    *   `-v "$(pwd):/app"` (or `${PWD}`, `%CD%`) mounts your current directory on the host to `/app` inside the container.
    *   Since the script saves to its current directory (`/app` inside the container), the files appear directly on your host.
    *   `--rm` automatically removes the container when it exits.

*   **Download from file / use cookies (files must be in your current host directory):**
    *(Assuming `urls.txt` and/or `cookies.txt` are in the directory where you run `docker run`)*
    ```bash
    # Linux/macOS
    docker run --rm -v "$(pwd):/app" yt-downloader -q 720 -f urls.txt -c cookies.txt

    # Windows (PowerShell)
    docker run --rm -v "${PWD}:/app" yt-downloader -q 720 -f urls.txt -c cookies.txt
    ```

*   **Save to a specific *sub-directory* within your current host directory:**
    ```bash
    # Linux/macOS (will create 'specific_output' on host if it doesn't exist)
    docker run --rm -v "$(pwd):/app" yt-downloader -q 1080 -u <url> -o specific_output
    ```

*   **Get help:**
    ```bash
    docker run --rm yt-downloader --help
    ```

## Command-Line Arguments

Run `python ytdl_pro.py --help` or `docker run --rm yt-downloader --help` to see all available options:

*   `-u URLS [URLS ...]` / `--urls URLS [URLS ...]`: List of YouTube URLs.
*   `-f FILE` / `--file FILE`: Path to a file containing URLs (one per line).
*   `-q QUALITY` / `--quality QUALITY`: **(Required)** Max video quality/height (e.g., 1080, 720, 480).
*   `-o OUTPUT` / `--output OUTPUT`: Output directory (default: "." - current directory).
*   `-p PROCESSES` / `--processes PROCESSES`: Number of parallel downloads (default: system CPU count).
*   `-c COOKIEFILE` / `--cookiefile COOKIEFILE`: Path to cookies file (optional).
*   `--quiet-ydl`: Suppress yt-dlp's own console output.
*   `--verbose`: Enable verbose logging for this script.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (You should create a `LICENSE` file, e.g., containing the MIT license text).

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.
