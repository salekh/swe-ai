# Makefile for "Software Engineering in the Age of AI"
# All LaTeX compilation runs inside Docker (texlive/texlive:latest)

DOCKER_IMAGE  = texlive/texlive:latest
DOCKER_RUN    = docker run --rm -v "$(CURDIR)":/workdir -w /workdir $(DOCKER_IMAGE)
XELATEX       = $(DOCKER_RUN) xelatex -interaction=nonstopmode -halt-on-error -shell-escape
BIBER         = $(DOCKER_RUN) biber
DOT           = dot
MAIN          = main
BUILD_DIR     = build

# Find all .dot files in diagrams/
DOT_SRCS      = $(shell find diagrams -name '*.dot' -not -path '*/compiled/*' 2>/dev/null)
DOT_PDFS      = $(patsubst diagrams/%.dot,diagrams/compiled/%.pdf,$(DOT_SRCS))

.PHONY: all build diagrams clean check help quick

help: ## Show this help
	@echo "Available targets:"
	@echo "  make build     - Full build (diagrams + 3-pass XeLaTeX + Biber)"
	@echo "  make quick     - Quick build (single XeLaTeX pass, no Biber)"
	@echo "  make diagrams  - Compile all Graphviz diagrams to PDF"
	@echo "  make check     - Validate LaTeX syntax (dry run)"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make help      - Show this help"

all: build ## Default target

build: diagrams ## Full build: diagrams → XeLaTeX (3 passes) → Biber → final
	@echo "=== Pass 1: XeLaTeX ==="
	$(XELATEX) $(MAIN).tex
	@echo "=== Pass 2: Biber ==="
	$(BIBER) $(MAIN) || true
	@echo "=== Pass 3: XeLaTeX ==="
	$(XELATEX) $(MAIN).tex
	@echo "=== Pass 4: XeLaTeX (final) ==="
	$(XELATEX) $(MAIN).tex
	@echo ""
	@echo "✅ Build complete: $(MAIN).pdf"
	@if command -v pdfinfo >/dev/null 2>&1; then \
		echo "Pages: $$(pdfinfo $(MAIN).pdf 2>/dev/null | grep Pages | awk '{print $$2}')"; \
	fi

quick: ## Quick single-pass build (for drafts)
	$(XELATEX) $(MAIN).tex
	@echo "✅ Quick build complete: $(MAIN).pdf"

diagrams: $(DOT_PDFS) ## Compile all Graphviz .dot files to PDF
	@echo "✅ All diagrams compiled"

# Pattern rule: diagrams/chXX/foo.dot → diagrams/compiled/chXX/foo.pdf
diagrams/compiled/%.pdf: diagrams/%.dot
	@mkdir -p $(dir $@)
	$(DOT) -Tpdf $< -o $@

check: ## Validate LaTeX (draft mode, no output)
	$(DOCKER_RUN) xelatex -interaction=nonstopmode -draftmode -halt-on-error $(MAIN).tex
	@echo "✅ LaTeX syntax check passed"

clean: ## Remove all build artifacts
	rm -f $(MAIN).pdf $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc
	rm -f $(MAIN).lof $(MAIN).lot $(MAIN).bbl $(MAIN).bcf $(MAIN).blg
	rm -f $(MAIN).run.xml $(MAIN).fls $(MAIN).fdb_latexmk
	rm -f chapters/*.aux frontmatter/*.aux
	rm -rf diagrams/compiled/*
	@echo "✅ Cleaned"
