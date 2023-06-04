APP_DIR := ./src
TARGET_DIR := ./target

# The name of the output file
OUTPUT_FILE := front_end_app

# The zip command
ZIP := zip

# The target that is run when you run `make` with no arguments
default: package

# This rule ensures the target directory exists before we try to put files in it
$(TARGET_DIR):
	mkdir -p $@

# This rule tells make how to 'build' a .zip from all the files in your src directory
$(TARGET_DIR)/$(OUTPUT_FILE).zip: $(TARGET_DIR) $(wildcard $(APP_DIR)/**/*)
	$(ZIP) -r $@ $(APP_DIR)

# This rule tells make how to 'clean' your project
clean:
	rm -rf $(TARGET_DIR)

# This rule tells make how to 'package' your project
package: clean $(TARGET_DIR)/$(OUTPUT_FILE).zip
