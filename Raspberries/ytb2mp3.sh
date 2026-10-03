#!/bin/bash

# Check if a URL was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <youtube-url>"
    exit 1
fi

# Target directory set to your Music folder
OUTPUT_DIR="$HOME/Movies"
PROFILE_DIR="$HOME/Library/Application Support/Firefox/Profiles/wuaceuim.default-esr"

echo "Downloading and converting to MP3..."
yt-dlp --no-check-certificate \
       --rm-cache-dir -4 \
       --extractor-args "youtube:player_client=android" \
       -x --audio-format mp3 -f "ba/b" \
       -o "$OUTPUT_DIR/%(title)s.%(ext)s" \
       "$1"

echo "Done! File saved to $OUTPUT_DIR"