#!/bin/bash

# Define source and target directories
SOURCE_DIR="./backend/handlers"
TARGET_DIR="./target"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Source directory $SOURCE_DIR does not exist."
    exit 1
fi

# Check if target directory exists, if not, create it
if [ ! -d "$TARGET_DIR" ]; then
    echo "Target directory $TARGET_DIR does not exist. Creating it now."
    mkdir -p "$TARGET_DIR"
fi

# Create the zip file
# -r means to recurse into directories
# This command will create a zip file named handlers.zip in the /target directory
zip -r "$TARGET_DIR/handlers.zip" "$SOURCE_DIR"

echo "Zip file created at $TARGET_DIR/handlers.zip"