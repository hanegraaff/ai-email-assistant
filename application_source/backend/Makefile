# This Makefile was created by OpenAI's ChatGPT

# Define source, target directories and parent directory
SOURCE_DIR := ./src
TARGET_DIR := ./target

# Default target executed when no arguments are given to make.
default: zip

# Target for creating the zip file.
zip: check_source_dir check_target_dir
	@cd $(SOURCE_DIR) && zip -r ../$(TARGET_DIR)/handlers.zip .
	@echo "Zip file created at $(TARGET_DIR)/handlers.zip"

# Target for checking if the source directory exists.
check_source_dir:
	@test -d $(SOURCE_DIR) || (echo "Source directory $(SOURCE_DIR) does not exist." && exit 1)

# Target for checking if the target directory exists and creating it if it doesn't.
check_target_dir:
	@test -d $(TARGET_DIR) || (echo "Target directory $(TARGET_DIR) does not exist. Creating it now." && mkdir -p $(TARGET_DIR))
