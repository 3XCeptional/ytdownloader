# Use a specific slim image version for reproducibility
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim-bullseye as base

LABEL maintainer="3XCeptional" \
      description="Runs the enhanced yt-dlp downloader script (ytdl_pro.py) with ffmpeg. Saves to /app by default."

# --- System Setup ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        ca-certificates \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- Python Dependencies ---
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Application Setup ---
# Create a non-root user and group
RUN groupadd --system appuser && \
    useradd --system --gid appuser --shell /bin/bash --create-home appuser

# Copy the application script and set ownership
# No need to pre-create YTdownloads dir anymore
COPY ytdl_pro.py .
RUN chown appuser:appuser ytdl_pro.py

# Switch to the non-root user
USER appuser

# --- Runtime ---
# Entrypoint remains the same
ENTRYPOINT ["python", "ytdl_pro.py"]
# Default command shows help
CMD ["--help"]