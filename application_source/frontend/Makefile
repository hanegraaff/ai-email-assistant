APP_DIR := ./src
TARGET_DIR := ./target

# The name of the output file
OUTPUT_FILE := frontend_application

# The zip command
ZIP := zip

# The target that is run when you run `make` with no arguments
default: package

# This rule ensures the target directory exists before we try to put files in it
$(TARGET_DIR):
	mkdir -p $@

# This rule tells make how to 'build' a .zip from all the files in your src directory
$(TARGET_DIR)/$(OUTPUT_FILE).zip: $(TARGET_DIR) install
	cd $(APP_DIR) && $(ZIP) -r ../$@ *

# This rule tells make how to 'clean' your project
clean:
	rm -rf $(TARGET_DIR)
	rm -rf $(APP_DIR)/node_modules

# This rule tells make how to 'install' your project
install: 
	cd $(APP_DIR) && npm install

# This rule tells make how to 'package' your project
package: clean $(TARGET_DIR)/$(OUTPUT_FILE).zip
