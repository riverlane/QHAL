ifeq ($(OS),Windows_NT)
include ../Makefile.win
else
include ../Makefile.unix
endif

BUILDDIR=_build
SPHINXBUILD=sphinx-build -v -n -a

.PHONY: clean-build
clean-build: 
	$(RMCMD) $(BUILDDIR)

.PHONY: clean
clean: clean-build


# --------------- DOCS -------------------------------------------------------#


.PHONY: all
all: html pdf epub release

.PHONY: html
html: 
	$(SPHINXBUILD) -b html -w sphinx-build-html.log . $(BUILDDIR)/html/
	@echo "Build finished: HTML"

.PHONY: pdf
pdf: 
	$(SPHINXBUILD) -b rinoh -w sphinx-build-pdf.log . $(BUILDDIR)/pdf/
	@echo "Build finished: PDF"

.PHONY: epub
epub:
	$(SPHINXBUILD) -b epub -w sphinx-build-epub.log . $(BUILDDIR)/epub/
	@echo "Build finished: EPUB"

.PHONY: release:
release: pdf
	cp $(BUILDDIR)/pdf/*.pdf ../
	@echo "PDF Ready to be released"


