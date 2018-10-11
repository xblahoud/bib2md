BIB_DIR=example_use
MD_FILES=README.header.md $(BIB_DIR)/cite.md $(BIB_DIR)/full_ref.md 

$(BIB_DIR)/%.md: $(BIB_DIR)/%.tex
	$(MAKE) -C $(BIB_DIR) $(patsubst $(BIB_DIR)/%,%,$@)

README.md: $(MD_FILES)
	pandoc -o $@ $(MD_FILES)
	$(MAKE) -C $(BIB_DIR) clean
