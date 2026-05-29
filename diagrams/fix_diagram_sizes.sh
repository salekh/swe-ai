#!/bin/bash
# fix_diagram_sizes.sh — Add size constraints to all DOT files and recompile
#
# Book text width: 6.4 inches (8.5 - 1.2 - 0.9)
# Max diagram height: ~8 inches (leave room for caption)
#
# Strategy per diagram type:
#   - Wide/landscape diagrams (LR): size="6.4,4!" to prevent overflow
#   - Tall/portrait diagrams (TB): size="6.4,8!" to fill width
#   - Multi-column diagrams: size="6.4,3!" to keep compact

set -e
cd "$(dirname "$0")/.."

echo "=== Fixing diagram sizes ==="

# ============================================================================
# Fix each DOT file with appropriate size and increased font sizes
# ============================================================================

fix_dot() {
    local file="$1"
    local size="$2"         # e.g., "6.4,4"
    local graph_font="$3"   # graph label fontsize
    local node_font="$4"    # node fontsize
    local edge_font="$5"    # edge fontsize
    
    echo "  Fixing $(basename $file): size=$size, fonts=$graph_font/$node_font/$edge_font"
    
    # Replace the graph attributes line to add size and increase fonts
    # Match: graph [fontname="Helvetica Neue", fontsize=NN, bgcolor="white",
    sed -i '' \
        -e "s|graph \[fontname=\"Helvetica Neue\", fontsize=[0-9]*, bgcolor=\"white\",|graph [fontname=\"Helvetica Neue\", fontsize=${graph_font}, bgcolor=\"white\", size=\"${size}\", ratio=compress,|" \
        -e "s|node  \[fontname=\"Helvetica Neue\", fontsize=[0-9]*,|node  [fontname=\"Helvetica Neue\", fontsize=${node_font},|" \
        -e "s|edge  \[fontname=\"Helvetica Neue\", fontsize=[0-9]*,|edge  [fontname=\"Helvetica Neue\", fontsize=${edge_font},|" \
        "$file"
}

# Ch01 — new-software-stack: TB layout, moderate height
fix_dot "diagrams/ch01/new-software-stack.dot" "6.4,5" 13 12 10

# Ch02 — transformer-arch: TB, complex
fix_dot "diagrams/ch02/transformer-arch.dot" "6.4,7" 13 11 10

# Ch02 — training-pipeline: LR, wide pipeline  
fix_dot "diagrams/ch02/training-pipeline.dot" "6.4,3" 13 11 10

# Ch02 — distributed-training: TB, moderate
fix_dot "diagrams/ch02/distributed-training.dot" "6.4,5" 13 11 10

# Ch02 — kv-cache: LR, wide with 3 clusters
fix_dot "diagrams/ch02/kv-cache.dot" "6.4,3.5" 13 11 10

# Ch03 — rlhf-pipeline: LR, wide pipeline
fix_dot "diagrams/ch03/rlhf-pipeline.dot" "6.4,4" 13 11 10

# Ch03 — post-training-landscape: TB, tall with many nodes
fix_dot "diagrams/ch03/post-training-landscape.dot" "6.4,8" 13 11 10

# Ch04 — finetune-decision: TB, decision tree
fix_dot "diagrams/ch04/finetune-decision.dot" "6.4,5" 12 11 10

# Ch04 — lora-architecture: LR, wide
fix_dot "diagrams/ch04/lora-architecture.dot" "6.4,3" 13 11 10

# Ch05 — canonical-stack: TB, moderate
fix_dot "diagrams/ch05/canonical-stack.dot" "6.4,5" 13 11 10

# Ch05 — rag-pipeline: LR or TB, moderate
fix_dot "diagrams/ch05/rag-pipeline.dot" "6.4,4" 13 11 10

# Ch05 — model-routing: TB, many tiers
fix_dot "diagrams/ch05/model-routing.dot" "6.4,7" 13 11 10

# Ch06 — stripe-hybrid-fraud: TB, many tiers + wide
fix_dot "diagrams/ch06/stripe-hybrid-fraud.dot" "6.4,7" 13 11 10

# Ch06 — uber-genai-gateway: LR, wide with 3 clusters
fix_dot "diagrams/ch06/uber-genai-gateway.dot" "6.4,4" 13 11 10

# Ch07 — document-processing-pipeline: TB, tall
fix_dot "diagrams/ch07/document-processing-pipeline.dot" "6.4,8" 13 11 10

# Ch08 — eval-pyramid: BT, moderate height
fix_dot "diagrams/ch08/eval-pyramid.dot" "6.4,5" 13 11 10

# Ch12 — agent-loop: TB, complex with sidebars
fix_dot "diagrams/ch12/agent-loop.dot" "6.4,6" 13 11 10

# Ch12 — multi-agent: LR, 3 side-by-side patterns
fix_dot "diagrams/ch12/multi-agent.dot" "6.4,3" 13 11 10


echo ""
echo "=== Recompiling all diagrams ==="

for f in diagrams/ch*/*.dot; do
    base=$(basename "$f" .dot)
    dir=$(dirname "$f" | sed 's|diagrams/|diagrams/compiled/|')
    mkdir -p "$dir"
    echo "  Compiling $base..."
    dot -Tpdf "$f" -o "$dir/$base.pdf" 2>&1 || echo "    WARNING: $base had issues"
done

echo ""
echo "=== All diagrams recompiled ==="
echo ""

# Verify: check that no PDF is wider than ~7 inches (504 pts)
echo "=== Size verification (requires Ghostscript) ==="
for f in diagrams/compiled/*/*.pdf; do
    # Use ghostscript to get bounding box
    bbox=$(gs -q -dNODISPLAY -dBATCH -dNOPAUSE -c "($f) (r) file runpdfbegin 1 pdfgetpage /MediaBox pdfgetpageattr pop ==" 2>/dev/null || true)
    echo "  $(basename $(dirname $f))/$(basename $f .pdf): $bbox"
done
