
# YouTube Video Downloader

A Python-based tool to download YouTube videos using `yt-dlp` with support for multiprocessing, custom quality settings, and output directories. The tool is containerized using Docker for easy deployment.

---

## Features

- **Multiprocessing Support**: Download multiple videos in parallel.
- **Custom Quality**: Specify the video quality (e.g., 1080p, 720p).
- **Custom Output Directory**: Save downloaded videos to a specified directory.
- **Random User-Agent**: Uses `fake-useragent` to bypass restrictions.
- **Docker Support**: Run the tool in a Docker container for portability.
- **Cookies Support**: Use a `cookies.txt` file to download age-restricted or private videos.

---

## Prerequisites

- **Python 3.9+**: Required to run the script.
- **Docker**: Optional, for running the tool in a containerized environment.
- **ffmpeg**: Required for merging video and audio streams (included in the Docker image).

---

## Installation

### Without Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/3XCeptional/yt_downloader.git
   cd yt-dlp-downloader
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python app.py -u "https://youtu.be/5uQjEdfHog4" -q 1080 -o "downloads"
   ```

### With Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/3XCeptional/yt_downloader.git
   cd yt-dlp-downloader
   ```

2. Build the Docker image:
   ```bash
   docker build -t yt_downloader .
   ```

3. Run the Docker container:
   ```bash
   docker run --rm -v $(pwd)/downloads:/app/YTdownloads yt_downloader -u "https://youtu.be/5uQjEdfHog4" -q 1080
   ```

---

## Usage

### Command-Line Arguments

| Argument       | Description                                                                 | Example                          |
|----------------|-----------------------------------------------------------------------------|----------------------------------|
| `-u`, `--urls` | List of YouTube video URLs to download.                                     | `-u "https://youtu.be/example1"` |
| `-q`, `--quality` | Desired video quality (e.g., 1080, 720).                                | `-q 1080`                        |
| `-o`, `--output` | Output directory for downloaded videos (default: `YTdownloads`).         | `-o "MyDownloads"`               |

### Examples

1. Download a single video at 1080p quality:
   ```bash
   python app.py -u "https://youtu.be/5uQjEdfHog4" -q 1080
   ```

2. Download multiple videos at 720p quality to a custom directory:
   ```bash
   python app.py -u "https://youtu.be/example1" "https://youtu.be/example2" -q 720 -o "MyDownloads"
   ```

3. Run using Docker:
   ```bash
   docker run --rm -v $(pwd)/downloads:/app/YTdownloads yt_downloader -u "https://youtu.be/5uQjEdfHog4" -q 1080
   ```

---

## Configuration

### Cookies File (Optional)

To download age-restricted or private videos, you can use a `cookies.txt` file:

1. Export cookies from your browser using an extension like [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid).
2. Save the file as `cookies.txt` in the project root.
3. The script will automatically use the cookies if the file exists.

---

## Directory Structure

```
yt-dlp-downloader/
│
├── app.py                # Main Python script
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── README.md             # Project documentation
├── cookies.txt           # Optional cookies file for authentication
└── downloads/            # Default output directory (created automatically)
```

---

## Troubleshooting

### HTTP 403 Forbidden Error

If you encounter a `403 Forbidden` error:

1. **Update `yt-dlp`**:
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Use Cookies**:
   Export cookies from your browser and save them as `cookies.txt` in the project root.

3. **Enable Verbose Logging**:
   Modify the script to enable verbose logging for more details:
   ```python
   ydl_opts = {
       'verbose': True,
   }
   ```

---

### `ffmpeg` Not Installed Error

If you encounter the error `ERROR: You have requested merging of multiple formats but ffmpeg is not installed`:

1. **Install `ffmpeg`**:
   - If running locally, install `ffmpeg` using your package manager:
     ```bash
     sudo apt-get install ffmpeg  # For Debian/Ubuntu
     brew install ffmpeg          # For macOS
     ```
   - If using Docker, ensure the `Dockerfile` includes the installation of `ffmpeg` (already included in the provided `Dockerfile`).

2. **Rebuild the Docker Image**:
   If using Docker, rebuild the image after updating the `Dockerfile`:
   ```bash
   docker build -t yt_downloader .
   ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): A feature-rich YouTube downloader.
- [fake-useragent](https://github.com/hellysmile/fake-useragent): For generating random user-agent strings.

---

## Creating a `cookies.txt` File

To download age-restricted or private videos, you need to create a `cookies.txt` file:

1. **Install a Browser Extension**:
   - For **Google Chrome** or **Microsoft Edge**, use the [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid) extension.
   - For **Firefox**, use the [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) extension.

2. **Log in to YouTube**:
   - Open your browser and log in to your YouTube account.

3. **Export Cookies**:
   - Navigate to YouTube (`https://www.youtube.com`).
   - Click on the extension icon in your browser toolbar.
   - Select the option to export cookies.
   - Save the file as `cookies.txt` in the root directory of your project.

---

### Example `cookies.txt` Format

The `cookies.txt` file should look something like this:

```plaintext
.youtube.com	TRUE	/	TRUE	1712345678	VISITOR_INFO1_LIVE	abc123xyz456
.youtube.com	TRUE	/	TRUE	1712345678	PREF	f1=50000000
.youtube.com	TRUE	/	TRUE	1712345678	YSC	ABCdefGHIjkLMNop
```

Each line represents a cookie with the following fields (tab-separated):
1. **Domain**: The domain the cookie belongs to (e.g., `.youtube.com`).
2. **Include Subdomains**: `TRUE` or `FALSE`.
3. **Path**: The path the cookie is valid for (e.g., `/`).
4. **Secure**: `TRUE` or `FALSE`.
5. **Expiration**: The expiration date in Unix timestamp format.
6. **Name**: The name of the cookie (e.g., `VISITOR_INFO1_LIVE`).
7. **Value**: The value of the cookie.

---

### Using `cookies.txt` in Your Script

Once you have the `cookies.txt` file, place it in the root directory of your project. The script will automatically use it if the file exists.

For example, in your `app.py` script, the `ydl_opts` dictionary includes the `cookiefile` option:

```python
ydl_opts = {
    'cookiefile': 'cookies.txt',  # Use cookies.txt if it exists
}
```

---

### Notes:
- **Privacy Warning**: The `cookies.txt` file contains sensitive information (e.g., session cookies). Do not share this file publicly.
- **Expiration**: Cookies expire after a certain period. If the `cookies.txt` file stops working, you may need to export a new one.
- **Browser Compatibility**: Ensure you use a browser extension that supports the format required by `yt-dlp`.

---

