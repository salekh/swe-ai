#!/usr/bin/env python3
"""
Diagram rendering pipeline for "Software Engineering in the Age of AI"
Uses matplotlib to generate publication-quality PDF diagrams.

All diagrams use:
- Source Sans 3 / Source Code Pro fonts (matching the book)
- O'Reilly-inspired color palette
- Consistent sizing for LaTeX integration
- Anti-aliased rendering at 300 DPI

Usage:
    python3 render_diagrams.py              # Render all diagrams
    python3 render_diagrams.py ch02         # Render only ch02 diagrams
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe
import numpy as np
import os
import sys

# ============================================================================
# STYLE CONFIGURATION
# ============================================================================

# Try to load Source Sans Pro; fall back to system sans-serif
FONT_FAMILIES = ['Source Sans 3', 'Source Sans Pro', 'Helvetica Neue', 'Arial']
MONO_FONTS = ['Source Code Pro', 'Menlo', 'Consolas', 'monospace']

def find_font(families):
    """Find the first available font family."""
    import matplotlib.font_manager as fm
    available = {f.name for f in fm.fontManager.ttflist}
    for fam in families:
        if fam in available:
            return fam
    return families[-1]

FONT_MAIN = find_font(FONT_FAMILIES)
FONT_MONO = find_font(MONO_FONTS)

# O'Reilly-inspired palette
C = {
    'teal':       '#00758F',
    'blue':       '#2D6A8F',
    'red':        '#C4362A',
    'dark':       '#1A1A2E',
    'text':       '#2D3748',
    'subtext':    '#607D8B',
    # Node fills
    'fill_default':  '#F0F4F8',
    'fill_blue':     '#E3F2FD',
    'fill_green':    '#E8F5E9',
    'fill_orange':   '#FFF3E0',
    'fill_pink':     '#FCE4EC',
    'fill_purple':   '#F3E5F5',
    'fill_gray':     '#ECEFF1',
    'fill_yellow':   '#FFFDE7',
    'fill_teal':     '#E0F2F1',
    # Darker fills for emphasis
    'dark_green':    '#C8E6C9',
    'dark_blue':     '#BBDEFB',
    'dark_purple':   '#E1BEE7',
    'dark_orange':   '#FFE0B2',
    # Border colors
    'border_default':'#B0BEC5',
    'border_blue':   '#64B5F6',
    'border_green':  '#81C784',
    'border_orange': '#FFB74D',
    'border_red':    '#E57373',
    'border_purple': '#BA68C8',
    'border_teal':   '#4DB6AC',
    'border_yellow': '#FDD835',
    # Background
    'bg':            '#FFFFFF',
    'bg_cluster':    '#FAFAFA',
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': [FONT_MAIN],
    'font.size': 9,
    'axes.unicode_minus': False,
    'figure.facecolor': C['bg'],
    'savefig.facecolor': C['bg'],
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.15,
})


def _box(ax, x, y, w, h, label, fill, border, fontsize=8,
         fontweight='normal', radius=0.12, linewidth=1.2,
         text_color=None, shadow=True, mono=False):
    """Draw a rounded rectangle with centered text."""
    tc = text_color or C['text']
    font = FONT_MONO if mono else FONT_MAIN
    
    rect = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=border,
        linewidth=linewidth, zorder=2,
    )
    if shadow:
        rect.set_path_effects([
            pe.withSimplePatchShadow(offset=(1.5, -1.5),
                                     shadow_rgbFace='#00000010',
                                     alpha=0.15),
        ])
    ax.add_patch(rect)
    
    lines = label.split('\n')
    total_h = len(lines) * fontsize * 1.3 / 72  # approx line spacing in inches
    for i, line in enumerate(lines):
        ly = y + total_h/2 - (i + 0.5) * fontsize * 1.3 / 72
        fw = fontweight if i == 0 and len(lines) > 1 else 'normal'
        ax.text(x, ly, line, ha='center', va='center',
                fontsize=fontsize, fontweight=fw, color=tc,
                fontfamily=font, zorder=3)


def _arrow(ax, x1, y1, x2, y2, color=None, label='', style='-',
           linewidth=1.0, head_width=0.06, fontsize=7, curve=0,
           zorder=1):
    """Draw an arrow from (x1,y1) to (x2,y2)."""
    c = color or C['subtext']
    ls = '--' if style == 'dashed' else '-'
    
    if curve != 0:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(
                        arrowstyle='->', color=c,
                        lw=linewidth, ls=ls,
                        connectionstyle=f'arc3,rad={curve}',
                    ), zorder=zorder)
    else:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(
                        arrowstyle='->', color=c,
                        lw=linewidth, ls=ls,
                    ), zorder=zorder)
    
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.06, label, ha='center', va='bottom',
                fontsize=fontsize, color=c, fontstyle='italic',
                zorder=4)


def _cluster(ax, x, y, w, h, label, border_color, bg_color=None,
             style='dashed', fontsize=9):
    """Draw a cluster/group box with a label at top."""
    bg = bg_color or C['bg_cluster']
    ls = '--' if style == 'dashed' else '-'
    rect = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0,rounding_size=0.15",
        facecolor=bg, edgecolor=border_color,
        linewidth=1.0, linestyle=ls, zorder=0,
    )
    ax.add_patch(rect)
    ax.text(x, y + h/2 - 0.08, label, ha='center', va='top',
            fontsize=fontsize, fontweight='bold',
            color=border_color, zorder=1)


def _cylinder(ax, x, y, w, h, label, fill, border, fontsize=8):
    """Draw a database cylinder shape."""
    from matplotlib.patches import Ellipse
    # Body
    body = FancyBboxPatch(
        (x - w/2, y - h/2), w, h * 0.75,
        boxstyle="square,pad=0",
        facecolor=fill, edgecolor=border,
        linewidth=1.2, zorder=2,
    )
    ax.add_patch(body)
    # Top ellipse
    top = Ellipse((x, y + h*0.25), w, h*0.25,
                  facecolor=fill, edgecolor=border, linewidth=1.2, zorder=3)
    ax.add_patch(top)
    # Bottom ellipse
    bot = matplotlib.patches.Arc((x, y - h/2), w, h*0.25,
                                  theta1=180, theta2=360,
                                  edgecolor=border, linewidth=1.2, zorder=3)
    ax.add_patch(bot)
    # Label
    lines = label.split('\n')
    for i, line in enumerate(lines):
        ly = y - 0.02 + (len(lines)/2 - i - 0.5) * fontsize * 1.3 / 72
        ax.text(x, ly, line, ha='center', va='center',
                fontsize=fontsize, color=C['text'], zorder=4)


def _save(fig, path):
    """Save figure as PDF."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, format='pdf')
    plt.close(fig)
    print(f"  ✓ {path}")


# ============================================================================
# DIAGRAM DEFINITIONS
# ============================================================================

def ch02_kv_cache():
    """KV-Cache: Prefill vs Decode phases and memory breakdown."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 4.5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # --- Prefill Phase cluster ---
    _cluster(ax, 2, 2.2, 4.6, 3.5, 'Prefill Phase', C['teal'], C['fill_teal'])
    
    _box(ax, 0.8, 2.8, 1.5, 0.7, 'Input Prompt\n(N tokens)', C['fill_yellow'], C['border_yellow'])
    _box(ax, 2.8, 2.8, 1.5, 0.7, 'Parallel\nAttention', C['fill_purple'], C['border_purple'])
    _cylinder(ax, 2.8, 1.3, 1.3, 0.8, 'KV Cache\n(populate)', C['fill_blue'], C['border_blue'])
    
    _arrow(ax, 1.55, 2.8, 2.05, 2.8, C['teal'], 'all at once')
    _arrow(ax, 2.8, 2.4, 2.8, 1.75, C['teal'], 'store K,V')

    # --- Decode Phase cluster ---
    _cluster(ax, 6.5, 2.2, 4.6, 3.5, 'Decode Phase', C['red'], C['fill_pink'])
    
    _box(ax, 5.3, 2.8, 1.3, 0.7, 'New Token\n(1 token)', C['fill_yellow'], C['border_yellow'])
    _box(ax, 7.0, 2.8, 1.5, 0.7, 'Attend to\nALL past K,V', C['fill_purple'], C['border_purple'])
    _box(ax, 8.7, 2.8, 1.3, 0.7, 'Next Token\nPrediction', C['fill_green'], C['border_green'])
    _cylinder(ax, 7.0, 1.3, 1.3, 0.8, 'KV Cache\n(grows +1)', C['fill_blue'], C['border_blue'])
    
    _arrow(ax, 5.95, 2.8, 6.25, 2.8, C['red'])
    _arrow(ax, 7.75, 2.8, 8.05, 2.8, C['red'])
    _arrow(ax, 7.0, 2.4, 7.0, 1.75, C['red'], 'append', style='dashed')
    
    # Cross-link: KV cache from prefill feeds decode
    _arrow(ax, 3.45, 1.3, 6.3, 1.3, C['teal'], 'read all past K,V', linewidth=1.5)
    
    # Memory callout
    ax.text(5.2, 0.3, '💡 Memory: 70B model → 140GB weights + ~5GB KV-cache per request',
            ha='center', va='center', fontsize=8, color=C['text'],
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=C['fill_orange'],
                      edgecolor=C['border_orange'], linewidth=1))
    
    _save(fig, 'diagrams/compiled/ch02/kv-cache.pdf')


def ch03_post_training_landscape():
    """Full post-training pipeline: SFT → RLHF/DPO → Safety → Aligned."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-0.5, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Base model
    _box(ax, 5, 7.3, 2.5, 0.7, 'Pre-trained Base Model\n(raw next-token predictor)',
         C['fill_gray'], C['border_default'], fontsize=8, fontweight='bold')
    
    # SFT cluster
    _cluster(ax, 5, 5.8, 8, 1.6, 'Stage 1: Supervised Fine-Tuning', C['teal'], C['fill_teal'])
    _box(ax, 2.5, 5.5, 2, 0.6, 'Curated (instruction,\nresponse) pairs', C['fill_yellow'], C['border_yellow'], fontsize=7)
    _box(ax, 5, 5.5, 1.8, 0.6, 'SFT Training\n(assistant loss only)', C['fill_purple'], C['border_purple'], fontsize=7)
    _box(ax, 7.5, 5.5, 1.6, 0.6, 'SFT Model\n(follows instructions)', C['fill_green'], C['border_green'], fontsize=7)
    
    _arrow(ax, 5, 6.95, 5, 6.7, C['teal'])
    _arrow(ax, 3.5, 5.5, 4.1, 5.5, C['teal'])
    _arrow(ax, 5.9, 5.5, 6.7, 5.5, C['teal'])
    
    # Preference data
    _box(ax, 5, 4.3, 2.8, 0.6, 'Human Preference Data\n(prompt, chosen, rejected)',
         C['fill_yellow'], C['border_yellow'], fontsize=7, fontweight='bold')
    _arrow(ax, 7.5, 5.17, 5, 4.63, C['subtext'])
    
    # RLHF path
    _cluster(ax, 2.5, 3, 4, 1.5, 'Path A: RLHF', C['red'], C['fill_pink'])
    _box(ax, 1.5, 2.7, 1.6, 0.6, 'Train Reward\nModel', C['dark_orange'], C['border_orange'], fontsize=7)
    _box(ax, 3.5, 2.7, 1.6, 0.6, 'PPO\nOptimization\n(4 models)', C['fill_purple'], C['border_purple'], fontsize=7)
    _arrow(ax, 2.3, 2.7, 2.7, 2.7, C['red'])
    
    # DPO path
    _cluster(ax, 7.5, 3, 3.5, 1.5, 'Path B: DPO', '#2E7D32', C['fill_green'])
    _box(ax, 7.5, 2.7, 2, 0.6, 'Direct Policy\nOptimization\n(2 models)', C['fill_purple'], C['border_purple'], fontsize=7)
    
    _arrow(ax, 3.8, 4, 2.5, 3.8, C['red'], 'RLHF')
    _arrow(ax, 6.2, 4, 7.5, 3.8, '#2E7D32', 'DPO')
    
    # Safety
    _cluster(ax, 5, 1.2, 8, 1.3, 'Stage 3: Safety Training', C['border_orange'], C['fill_orange'])
    _box(ax, 2.5, 0.9, 1.5, 0.5, 'Red-Team\nTesting', C['fill_pink'], C['border_red'], fontsize=7)
    _box(ax, 5, 0.9, 1.5, 0.5, 'Safety SFT\n(refusal data)', C['dark_orange'], C['border_orange'], fontsize=7)
    _box(ax, 7.5, 0.9, 1.5, 0.5, 'Safety RLHF\n(harmless prefs)', C['dark_orange'], C['border_orange'], fontsize=7)
    
    _arrow(ax, 3.5, 2.37, 2.5, 1.9, C['red'])
    _arrow(ax, 7.5, 2.37, 7.5, 1.9, '#2E7D32')
    _arrow(ax, 3.25, 0.9, 4.25, 0.9, C['border_orange'])
    _arrow(ax, 5.75, 0.9, 6.75, 0.9, C['border_orange'])
    
    # Aligned model
    _box(ax, 5, -0.2, 2.5, 0.6, '✅ Aligned Model\n(helpful, harmless, honest)',
         C['dark_green'], '#2E7D32', fontsize=8, fontweight='bold', linewidth=2)
    _arrow(ax, 5, 0.6, 5, 0.13, '#2E7D32', linewidth=1.5)
    
    _save(fig, 'diagrams/compiled/ch03/post-training-landscape.pdf')


def ch04_lora_architecture():
    """LoRA weight decomposition: frozen base + low-rank bypass."""
    fig, ax = plt.subplots(1, 1, figsize=(9, 4))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.2, 4.2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Input
    _box(ax, 0.8, 2, 1.2, 0.7, 'Input x\n[batch, d]', C['fill_yellow'], C['border_yellow'])
    
    # Frozen path (top)
    _cluster(ax, 4, 3.3, 3.5, 1.4, 'Frozen Path (no gradient) ❄️', C['border_default'], C['bg_cluster'], style='dashed')
    _box(ax, 4, 3, 2.5, 0.7, 'W (frozen)\n~billions of params\nNOT updated', C['fill_gray'], C['border_default'], fontsize=7)
    
    # LoRA path (bottom)
    _cluster(ax, 4, 1, 5, 1.2, 'LoRA Bypass (trainable) 🔥', C['teal'], C['fill_teal'])
    _box(ax, 2.8, 0.7, 1.5, 0.6, 'A (down-project)\n[d × r]  r=16', C['fill_purple'], C['border_purple'], fontsize=7)
    _box(ax, 5.2, 0.7, 1.5, 0.6, 'B (up-project)\n[r × d]  init=0', C['fill_purple'], C['border_purple'], fontsize=7)
    
    # Sum
    _box(ax, 7.2, 2, 0.6, 0.6, '+', C['fill_green'], C['border_green'], fontsize=14, fontweight='bold')
    
    # Output
    _box(ax, 8.7, 2, 1.2, 0.7, 'Output\nW·x + BA·x', C['fill_green'], C['border_green'])
    
    # Arrows
    _arrow(ax, 1.4, 2.3, 2.7, 3.0, C['subtext'], linewidth=1.2)  # input → W
    _arrow(ax, 1.4, 1.7, 2.05, 0.7, C['teal'], linewidth=1.2)  # input → A
    _arrow(ax, 3.55, 0.7, 4.45, 0.7, C['teal'], 'r ≪ d')  # A → B
    _arrow(ax, 5.25, 3.0, 6.9, 2.15, C['subtext'], 'W·x')  # W → sum
    _arrow(ax, 5.95, 0.7, 6.95, 1.7, C['teal'], 'α/r · BA·x')  # B → sum
    _arrow(ax, 7.5, 2, 8.1, 2, C['border_green'], linewidth=1.5)  # sum → output
    
    # Annotations
    ax.text(4, 3.95, '~99.9% of parameters', ha='center', fontsize=7,
            color=C['subtext'], fontstyle='italic')
    ax.text(4, 0.05, '~0.1% of parameters — only this is trained',
            ha='center', fontsize=7, color=C['teal'], fontweight='bold')
    
    _save(fig, 'diagrams/compiled/ch04/lora-architecture.pdf')


def ch05_model_routing():
    """Multi-model routing with semantic cache and tiered models."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Request
    _box(ax, 4, 8, 1.8, 0.6, 'Incoming Request', C['fill_yellow'], C['border_yellow'], fontweight='bold')
    
    # Semantic cache
    _cylinder(ax, 4, 7, 1.6, 0.7, 'Semantic Cache', C['fill_blue'], C['border_blue'])
    _arrow(ax, 4, 7.67, 4, 7.4, C['subtext'])
    
    # Classifier
    _box(ax, 4, 5.8, 2, 0.6, 'Complexity Classifier', C['fill_orange'], C['border_orange'], fontweight='bold')
    _arrow(ax, 4, 6.55, 4, 6.13, C['subtext'], 'cache miss')
    
    # Cache hit shortcut
    _arrow(ax, 5.2, 7, 7.5, 7, '#2E7D32', 'cache hit', style='dashed')
    
    # Three tiers
    # Tier 1: Fast
    _cluster(ax, 1.5, 4.3, 2.6, 1.4, 'Tier 1: Fast', C['border_green'], C['fill_green'])
    _box(ax, 1.5, 4, 2, 0.6, 'GPT-4o-mini / Haiku\n$0.15/1M  •  50ms', C['dark_green'], C['border_green'], fontsize=7)
    
    # Tier 2: Standard
    _cluster(ax, 4, 4.3, 2.6, 1.4, 'Tier 2: Standard', C['border_blue'], C['fill_blue'])
    _box(ax, 4, 4, 2, 0.6, 'GPT-4o / Sonnet\n$2.50/1M  •  200ms', C['dark_blue'], C['border_blue'], fontsize=7)
    
    # Tier 3: Reasoning
    _cluster(ax, 6.5, 4.3, 2.6, 1.4, 'Tier 3: Reasoning', C['border_purple'], C['fill_purple'])
    _box(ax, 6.5, 4, 2, 0.6, 'o3 / Opus\n$15/1M  •  5-30s', C['dark_purple'], C['border_purple'], fontsize=7)
    
    # Routing arrows
    _arrow(ax, 3, 5.5, 1.5, 5.05, '#2E7D32', '~70%', linewidth=1.2)
    _arrow(ax, 4, 5.5, 4, 5.05, C['border_blue'], '~25%', linewidth=1.2)
    _arrow(ax, 5, 5.5, 6.5, 5.05, C['border_purple'], '~5%', linewidth=1.2)
    
    # Output validation
    _box(ax, 4, 2.8, 2.2, 0.6, 'Output Validation\n& Guardrails', C['fill_gray'], C['border_default'], fontweight='bold')
    
    _arrow(ax, 1.5, 3.55, 3.5, 3.05, C['subtext'])
    _arrow(ax, 4, 3.55, 4, 3.13, C['subtext'])
    _arrow(ax, 6.5, 3.55, 4.5, 3.05, C['subtext'])
    
    # Fallback
    _box(ax, 7, 2.8, 1.4, 0.5, 'Retry with\nhigher tier', C['fill_pink'], C['border_red'], fontsize=7)
    _arrow(ax, 5.1, 2.8, 6.3, 2.8, C['red'], 'fail', style='dashed')
    
    # Response
    _box(ax, 4, 1.5, 1.8, 0.6, 'Response', C['fill_green'], C['border_green'], fontweight='bold', linewidth=2)
    _arrow(ax, 4, 2.47, 4, 1.83, '#2E7D32', linewidth=1.5)
    
    # Cache hit also goes to response
    _box(ax, 7.5, 7, 0.01, 0.01, '', C['bg'], C['bg'], shadow=False)  # invisible anchor
    
    _save(fig, 'diagrams/compiled/ch05/model-routing.pdf')


def ch06_stripe_fraud():
    """Stripe's tiered fraud detection cascade."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Transaction input
    _box(ax, 5, 7, 2, 0.6, '💳 Payment Transaction', C['fill_yellow'], C['border_yellow'], fontweight='bold')
    
    # Tier 1: Fast ML
    _cluster(ax, 5, 5.3, 9, 2, 'Tier 1: Fast ML  •  < 10ms  •  100% of transactions', C['border_green'], C['fill_green'])
    _box(ax, 2.2, 5, 1.8, 0.6, 'Feature\nExtraction', C['dark_green'], C['border_green'], fontsize=7)
    _box(ax, 4.5, 5, 1.8, 0.6, 'XGBoost\nEnsemble', C['dark_green'], C['border_green'], fontsize=7)
    _box(ax, 7, 5, 1.5, 0.7, 'Risk\nScore', C['dark_green'], C['border_green'], fontsize=8, fontweight='bold')
    
    _arrow(ax, 5, 6.67, 5, 6.4, C['subtext'])
    _arrow(ax, 3.1, 5, 3.6, 5, C['border_green'])
    _arrow(ax, 5.4, 5, 6.25, 5, C['border_green'])
    
    # Tier 1 outcomes
    _box(ax, 1, 3.5, 1.4, 0.5, '✅ Allow\nscore < 0.05\n~85%', C['fill_green'], '#2E7D32', fontsize=7)
    _box(ax, 9, 3.5, 1.4, 0.5, '🚫 Block\nscore > 0.95\n~7%', C['fill_pink'], C['border_red'], fontsize=7)
    
    _arrow(ax, 6.6, 4.6, 1.5, 3.8, '#2E7D32', 'low risk')
    _arrow(ax, 7.5, 4.6, 9, 3.8, C['red'], 'high risk')
    
    # Tier 2: LLM
    _cluster(ax, 5, 2.5, 7, 1.6, 'Tier 2: LLM Analysis  •  50-100ms  •  ~8% of transactions',
             C['border_blue'], C['fill_blue'])
    _box(ax, 2.8, 2.2, 1.5, 0.5, 'Context\nAssembly', C['dark_blue'], C['border_blue'], fontsize=7)
    _box(ax, 5, 2.2, 1.5, 0.5, 'LLM\nAnalysis', C['fill_purple'], C['border_purple'], fontsize=7)
    _box(ax, 7.2, 2.2, 1.5, 0.5, 'Ensemble\nCombiner', C['dark_blue'], C['border_blue'], fontsize=7)
    
    _arrow(ax, 7, 4.5, 5, 3.4, C['border_blue'], 'gray zone', linewidth=1.5)
    _arrow(ax, 3.55, 2.2, 4.25, 2.2, C['border_blue'])
    _arrow(ax, 5.75, 2.2, 6.45, 2.2, C['border_blue'])
    
    # Tier 3: Human
    _cluster(ax, 7.5, 0.7, 3.5, 1, 'Tier 3: Human Review  •  ~0.5%', C['border_orange'], C['fill_orange'])
    _box(ax, 7.5, 0.4, 2, 0.5, 'Fraud Analyst\n(with AI pre-analysis)', C['dark_orange'], C['border_orange'], fontsize=7)
    
    _arrow(ax, 7.2, 1.92, 7.5, 1.25, C['border_orange'], 'uncertain')
    
    # Final allow from Tier 2
    _box(ax, 3, 0.7, 1.4, 0.5, '✅ Allow\ncombined < 0.5', C['fill_green'], '#2E7D32', fontsize=7)
    _arrow(ax, 7.2, 1.92, 3.5, 1, '#2E7D32', 'confident', curve=-0.2)
    
    _save(fig, 'diagrams/compiled/ch06/stripe-hybrid-fraud.pdf')


def ch06_uber_gateway():
    """Uber's centralized GenAI Gateway architecture."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.2, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Internal services
    _cluster(ax, 1.3, 3, 2.2, 3.4, 'Internal Services', C['border_default'], C['bg_cluster'], style='dashed')
    services = ['Customer\nSupport', 'Fraud\nDetection', 'Uber Eats\nRecs', 'Code\nAgent']
    for i, svc in enumerate(services):
        _box(ax, 1.3, 4.2 - i * 0.85, 1.5, 0.55, svc, C['fill_yellow'], C['border_yellow'], fontsize=7)
    
    # GenAI Gateway
    _cluster(ax, 5, 3, 3.5, 3.4, 'GenAI Gateway (Go)', C['teal'], C['fill_teal'])
    gw_items = [
        ('Auth &\nBudgeting', C['fill_teal'], C['border_teal']),
        ('Model\nRouter', C['fill_teal'], C['border_teal']),
        ('Prompt\nVersioning', C['fill_teal'], C['border_teal']),
        ('Observability\n& Tracing', C['fill_teal'], C['border_teal']),
    ]
    for i, (label, fill, border) in enumerate(gw_items):
        _box(ax, 5, 4.2 - i * 0.85, 1.8, 0.55, label, fill, border, fontsize=7)
    
    # LLM Providers
    _cluster(ax, 8.7, 3.5, 2.2, 2.5, 'LLM Providers', C['border_purple'], C['fill_purple'], style='dashed')
    providers = [('OpenAI\nGPT-4o', 'complex'), ('Google\nVertex AI', 'multimodal'), ('Self-Hosted\nLlama 3 70B', 'high-vol')]
    for i, (name, route) in enumerate(providers):
        _box(ax, 8.7, 4.3 - i * 0.85, 1.5, 0.55, name, C['dark_purple'], C['border_purple'], fontsize=7)
    
    # Toolshed
    _box(ax, 5, 0.8, 2, 0.5, 'Toolshed (MCP)\n400+ internal tools', C['fill_orange'], C['border_orange'], fontsize=7, fontweight='bold')
    
    # Arrows: services → gateway
    for i in range(4):
        _arrow(ax, 2.1, 4.2 - i * 0.85, 4.1, 4.2 - i * 0.85, C['subtext'])
    
    # Arrows: gateway → providers
    _arrow(ax, 5.9, 4.2, 7.95, 4.3, C['border_purple'])
    _arrow(ax, 5.9, 3.35, 7.95, 3.45, C['border_purple'])
    _arrow(ax, 5.9, 2.5, 7.95, 2.6, C['border_purple'])
    
    _save(fig, 'diagrams/compiled/ch06/uber-genai-gateway.pdf')


def ch07_document_pipeline():
    """Document processing pipeline: sources → extraction → chunking → indexing."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 7.5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Sources
    _cluster(ax, 5, 7, 9, 1.2, 'Document Sources', C['border_default'], C['bg_cluster'], style='dashed')
    sources = [
        ('PDFs\n(40%)', C['fill_pink'], C['border_red']),
        ('Confluence', C['fill_yellow'], C['border_yellow']),
        ('GitHub', C['fill_gray'], C['border_default']),
        ('Slack', C['fill_yellow'], C['border_yellow']),
        ('API Docs', C['fill_gray'], C['border_default']),
    ]
    for i, (name, fill, border) in enumerate(sources):
        _box(ax, 1.5 + i * 1.8, 6.7, 1.3, 0.5, name, fill, border, fontsize=7)
    
    # Classifier
    _box(ax, 5, 5.6, 1.8, 0.5, 'Format Classifier', C['fill_orange'], C['border_orange'], fontweight='bold')
    for i in range(5):
        _arrow(ax, 1.5 + i * 1.8, 6.42, 5, 5.88, C['subtext'])
    
    # Format-specific extraction
    _cluster(ax, 5, 4.3, 9, 1.3, 'Format-Specific Extraction', C['border_blue'], C['fill_blue'])
    extractors = ['Text\n(PyMuPDF)', 'OCR\n(Tesseract)', 'Table\n→ Markdown', 'HTML/MD\nParser', 'Code\n(AST-aware)']
    labels = ['digital', 'scanned', 'tables', 'HTML', 'code']
    for i, (ext, lbl) in enumerate(zip(extractors, labels)):
        x = 1.5 + i * 1.8
        _box(ax, x, 4, 1.3, 0.5, ext, C['dark_blue'], C['border_blue'], fontsize=7)
        _arrow(ax, 5, 5.33, x, 4.28, C['border_blue'], lbl, fontsize=6)
    
    # Universal processing
    _cluster(ax, 5, 2.5, 9, 1.3, 'Universal Processing', C['border_orange'], C['fill_orange'])
    procs = [
        ('Clean & Normalize\n(fix ligatures, headers)', C['dark_orange'], C['border_orange']),
        ('Semantic Chunking\n(boundary-aware)', C['dark_orange'], C['border_orange']),
        ('Metadata Enrichment\n(title, section, date)', C['dark_orange'], C['border_orange']),
    ]
    for i, (name, fill, border) in enumerate(procs):
        _box(ax, 2 + i * 3, 2.2, 2.2, 0.5, name, fill, border, fontsize=7)
    
    # Merge arrows from extraction to cleaning
    for i in range(5):
        _arrow(ax, 1.5 + i * 1.8, 3.72, 2, 2.48, C['subtext'])
    _arrow(ax, 3.1, 2.2, 4.4, 2.2, C['border_orange'])
    _arrow(ax, 6.1, 2.2, 7, 2.2, C['border_orange'])
    
    # Embedding & Indexing
    _cluster(ax, 5, 0.7, 7, 1.3, 'Embedding & Indexing', C['border_purple'], C['fill_purple'])
    _box(ax, 3, 0.4, 1.8, 0.5, 'Embedding Model\n(text-embedding-3)', C['dark_purple'], C['border_purple'], fontsize=7)
    _cylinder(ax, 5.5, 0.4, 1.5, 0.6, 'Vector DB', C['fill_blue'], C['border_blue'], fontsize=7)
    _cylinder(ax, 7.5, 0.4, 1.5, 0.6, 'Full-Text\nIndex (BM25)', C['fill_blue'], C['border_blue'], fontsize=7)
    
    _arrow(ax, 8, 1.92, 3, 1.05, C['border_purple'])
    _arrow(ax, 3.9, 0.4, 4.7, 0.4, C['border_purple'])
    _arrow(ax, 8, 1.92, 7.5, 1.05, C['border_blue'], style='dashed')
    
    _save(fig, 'diagrams/compiled/ch07/document-processing-pipeline.pdf')


def ch08_eval_pyramid():
    """AI evaluation pyramid: structural → LLM-judge → human/statistical."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Level 1: Structural (base - widest)
    _cluster(ax, 5, 1.3, 9.5, 2, 'Level 1: Structural Validation', C['border_green'], C['fill_green'])
    l1_items = ['Schema\nCompliance\n(JSON, Pydantic)', 'Constraint\nChecks\n(length, format)', 'Refusal\nDetection\n("I cannot…")']
    for i, item in enumerate(l1_items):
        _box(ax, 2 + i * 3, 1, 2.2, 0.7, item, C['dark_green'], C['border_green'], fontsize=7)
    ax.text(9.2, 1.8, 'Cost: ~$0\nCoverage: 100%\nSpeed: < 1ms', fontsize=7,
            color='#2E7D32', va='top', ha='right', fontfamily=FONT_MONO)
    
    # Level 2: LLM-as-Judge (middle)
    _cluster(ax, 5, 3.6, 8, 1.8, 'Level 2: LLM-as-Judge', C['border_blue'], C['fill_blue'])
    l2_items = ['Absolute\nScoring\n(1-5 per criterion)', 'Pairwise\nComparison\n(A vs B, both orders)', 'Reference-Based\n(vs gold standard)']
    for i, item in enumerate(l2_items):
        _box(ax, 2.5 + i * 2.5, 3.3, 2, 0.7, item, C['dark_blue'], C['border_blue'], fontsize=7)
    ax.text(8.5, 4.1, 'Cost: ~$0.01/eval\nCoverage: 5-10%\nSpeed: 1-3s', fontsize=7,
            color='#1565C0', va='top', ha='right', fontfamily=FONT_MONO)
    
    # Level 3: Human + Statistical (top - narrowest)
    _cluster(ax, 5, 5.5, 6.5, 1.5, 'Level 3: Human + Statistical', C['border_purple'], C['fill_purple'])
    l3_items = ['Regression\nTest Suite', 'A/B Testing\n(prod traffic)', 'Expert Human\nReview']
    for i, item in enumerate(l3_items):
        _box(ax, 3 + i * 2, 5.2, 1.6, 0.6, item, C['dark_purple'], C['border_purple'], fontsize=7)
    ax.text(7.7, 5.9, 'Cost: $$$\nCoverage: 1-2%\nSpeed: hours', fontsize=7,
            color='#7B1FA2', va='top', ha='right', fontfamily=FONT_MONO)
    
    # Arrows between levels
    _arrow(ax, 3.5, 1.5, 3.5, 2.85, C['border_green'], 'pass')
    _arrow(ax, 5, 1.5, 5, 2.85, C['border_green'])
    _arrow(ax, 5, 3.8, 5, 4.7, C['border_blue'], 'sampled')
    
    _save(fig, 'diagrams/compiled/ch08/eval-pyramid.pdf')


def ch12_agent_loop():
    """Core agent execution loop: observe → reason → act."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Goal input
    _box(ax, 5, 7, 2.5, 0.6, '🎯 User Goal\n"Add pagination to /users"',
         C['fill_yellow'], C['border_yellow'], fontweight='bold')
    
    # Core loop
    _cluster(ax, 4, 4.5, 7, 3.5, 'Agent Execution Loop', C['teal'], C['fill_teal'])
    
    _box(ax, 1.8, 5, 2, 0.8, '① Observe\nRead environment:\nfiles, tool output,\nerror messages',
         C['fill_blue'], C['border_blue'], fontsize=7)
    _box(ax, 4.5, 5, 2, 0.8, '② Reason\nLLM: analyze state,\nplan next step,\nchoose tool',
         C['fill_purple'], C['border_purple'], fontsize=7)
    _box(ax, 4.5, 3.3, 2, 0.8, '③ Act\nExecute tool:\nread, write,\nrun tests',
         C['fill_orange'], C['border_orange'], fontsize=7)
    
    _arrow(ax, 5, 6.67, 5, 6.3, C['subtext'])
    _arrow(ax, 2.8, 5, 3.5, 5, C['teal'], linewidth=1.5)
    _arrow(ax, 5.5, 5, 5.5, 4.55, C['teal'], linewidth=1.5)  # reason → act (offset right)
    _arrow(ax, 3.5, 3.3, 1.8, 4.57, C['teal'], 'loop with\nresult', linewidth=1.5)  # act → observe
    
    # Memory
    _cluster(ax, 8.5, 5.5, 2.5, 1.5, 'Memory', C['border_default'], C['bg_cluster'], style='dashed')
    _box(ax, 8.5, 5.7, 1.8, 0.4, 'Short-term\n(conversation)', C['fill_gray'], C['border_default'], fontsize=7)
    _cylinder(ax, 8.5, 4.9, 1.5, 0.5, 'Long-term\n(vector store)', C['fill_gray'], C['border_default'], fontsize=6)
    
    _arrow(ax, 2.8, 5.3, 7.2, 5.7, C['subtext'], style='dashed')
    
    # Tools
    _cluster(ax, 8.5, 2.8, 2.5, 2, 'Tool Registry', C['border_orange'], C['fill_orange'], style='dashed')
    tools = ['read_file', 'write_file', 'search_code', 'run_tests', 'shell_exec']
    for i, tool in enumerate(tools):
        _box(ax, 8.5, 3.5 - i * 0.35, 1.8, 0.25, tool, C['dark_orange'], C['border_orange'],
             fontsize=6, mono=True)
    
    _arrow(ax, 5.5, 3.3, 7.2, 3.3, C['border_orange'], style='dashed')
    
    # Guardrails
    _box(ax, 1.5, 2, 2.2, 0.8, '🛡️ Guardrails\n• Max steps: 20\n• Budget: $2.00\n• Sandbox limits',
         C['fill_pink'], C['border_red'], fontsize=7)
    
    # Terminal states
    _box(ax, 5, 1, 1.8, 0.5, '✅ Goal Complete', C['fill_green'], '#2E7D32', fontweight='bold')
    _box(ax, 8, 1, 1.8, 0.5, '❌ Failed\n(limit exceeded)', C['fill_pink'], C['border_red'], fontsize=7)
    
    _arrow(ax, 4.5, 2.87, 1.5, 2.43, C['border_red'], style='dashed')
    _arrow(ax, 5.5, 4.57, 5, 1.28, '#2E7D32', '"done"')
    _arrow(ax, 2.5, 1.57, 8, 1.28, C['red'], 'limit hit', style='dashed')
    
    _save(fig, 'diagrams/compiled/ch12/agent-loop.pdf')


# ============================================================================
# EXISTING DIAGRAMS TO RE-RENDER
# ============================================================================

def ch01_new_software_stack():
    """Traditional vs AI-augmented software stack."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    for ax_idx, (ax, title, layers) in enumerate(zip(axes, [
        'Traditional Software Stack', 'AI-Augmented Stack'
    ], [
        [('User Interface', C['fill_yellow'], C['border_yellow']),
         ('Business Logic', C['fill_orange'], C['border_orange']),
         ('Data Access Layer', C['fill_blue'], C['border_blue']),
         ('Database', C['fill_gray'], C['border_default'])],
        [('User Interface', C['fill_yellow'], C['border_yellow']),
         ('AI Orchestration Layer', C['fill_purple'], C['border_purple']),
         ('Business Logic', C['fill_orange'], C['border_orange']),
         ('Context Assembly / RAG', C['fill_teal'], C['border_teal']),
         ('LLM API / Self-hosted Model', C['fill_purple'], C['border_purple']),
         ('Data Access Layer', C['fill_blue'], C['border_blue']),
         ('Database + Vector Store', C['fill_gray'], C['border_default'])],
    ])):
        ax.set_xlim(-1, 5)
        n = len(layers)
        ax.set_ylim(-0.5, n + 0.5)
        ax.set_aspect('auto')
        ax.axis('off')
        ax.set_title(title, fontsize=10, fontweight='bold', color=C['text'], pad=10)
        
        for i, (name, fill, border) in enumerate(reversed(layers)):
            y = i
            rect = FancyBboxPatch((0, y), 4, 0.7,
                                   boxstyle="round,pad=0,rounding_size=0.1",
                                   facecolor=fill, edgecolor=border,
                                   linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            fw = 'bold' if 'AI' in name or 'LLM' in name or 'Context' in name or 'Vector' in name else 'normal'
            ax.text(2, y + 0.35, name, ha='center', va='center',
                    fontsize=8, fontweight=fw, color=C['text'], zorder=3)
    
    fig.suptitle('', fontsize=1)
    plt.tight_layout()
    _save(fig, 'diagrams/compiled/ch01/new-software-stack.pdf')


def ch02_training_pipeline():
    """End-to-end training data pipeline."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 3.5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.2, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    stages = [
        ('Raw Crawl\n(100+ TB)', C['fill_pink'], C['border_red']),
        ('Dedup &\nFilter', C['fill_orange'], C['border_orange']),
        ('Quality\nScoring', C['fill_orange'], C['border_orange']),
        ('Domain\nMixing', C['fill_blue'], C['border_blue']),
        ('Tokenization\n(BPE)', C['fill_purple'], C['border_purple']),
        ('Training\nCorpus\n(15T tokens)', C['fill_green'], C['border_green']),
    ]
    
    for i, (name, fill, border) in enumerate(stages):
        x = 0.5 + i * 1.8
        _box(ax, x, 1.8, 1.4, 0.7, name, fill, border, fontsize=7)
        if i > 0:
            _arrow(ax, x - 1.1, 1.8, x - 0.7, 1.8, C['teal'], linewidth=1.2)
    
    # Data composition bar at bottom
    ax.text(5, 0.6, 'Typical Mix: Web 60% • Code 15% • Books 10% • Academic 8% • Conversational 5% • Other 2%',
            ha='center', va='center', fontsize=7, color=C['subtext'], fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=C['bg_cluster'], edgecolor=C['border_default']))
    
    ax.set_title('Pre-Training Data Pipeline', fontsize=10, fontweight='bold',
                 color=C['text'], pad=8)
    
    _save(fig, 'diagrams/compiled/ch02/training-pipeline.pdf')


def ch02_distributed_training():
    """3D parallelism: Data × Tensor × Pipeline."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    ax.set_title('Three Axes of Distributed Training Parallelism', fontsize=10,
                 fontweight='bold', color=C['text'], pad=10)
    
    # Data Parallelism (horizontal copies)
    _cluster(ax, 2, 5, 3.5, 2, 'Data Parallelism', '#2E7D32', C['fill_green'])
    ax.text(2, 5.5, 'Same model on each GPU\nDifferent data batches\nSync gradients via AllReduce',
            ha='center', va='center', fontsize=7, color='#2E7D32')
    for i in range(3):
        _box(ax, 1 + i * 1, 4.3, 0.7, 0.4, f'GPU {i}\nFull Model', C['dark_green'], C['border_green'], fontsize=6)
    
    # Tensor Parallelism (vertical splits)
    _cluster(ax, 5.5, 2.5, 3, 2.5, 'Tensor Parallelism', C['border_blue'], C['fill_blue'])
    ax.text(5.5, 3.5, 'Split weight matrices\nacross GPUs\nHigh bandwidth needed',
            ha='center', va='center', fontsize=7, color='#1565C0')
    _box(ax, 4.5, 1.7, 0.7, 0.5, 'Col A', C['dark_blue'], C['border_blue'], fontsize=6)
    _box(ax, 5.5, 1.7, 0.7, 0.5, 'Col B', C['dark_blue'], C['border_blue'], fontsize=6)
    _box(ax, 6.5, 1.7, 0.7, 0.5, 'Col C', C['dark_blue'], C['border_blue'], fontsize=6)
    
    # Pipeline Parallelism (sequential stages)
    _cluster(ax, 8.5, 5, 2.8, 2, 'Pipeline Parallelism', C['border_purple'], C['fill_purple'])
    ax.text(8.5, 5.5, 'Different layers\non different GPUs\nMicrobatch scheduling',
            ha='center', va='center', fontsize=7, color='#7B1FA2')
    stages = ['Layers 1-8', 'Layers 9-16', 'Layers 17-24']
    for i, s in enumerate(stages):
        _box(ax, 8.5, 4.5 - i * 0.5, 1.8, 0.35, s, C['dark_purple'], C['border_purple'], fontsize=6)
        if i > 0:
            _arrow(ax, 8.5, 4.5 - (i-1) * 0.5 - 0.2, 8.5, 4.5 - i * 0.5 + 0.2, C['border_purple'])
    
    _save(fig, 'diagrams/compiled/ch02/distributed-training.pdf')


def ch05_rag_pipeline():
    """RAG pipeline: offline ingestion + online query."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.2, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    ax.set_title('RAG Pipeline: Offline Ingestion + Online Query', fontsize=10,
                 fontweight='bold', color=C['text'], pad=8)
    
    # Offline path (top)
    _cluster(ax, 3, 4.3, 5.5, 1.5, 'Offline: Ingestion Pipeline', C['border_default'], C['bg_cluster'], style='dashed')
    _box(ax, 1.2, 4, 1.2, 0.5, 'Documents', C['fill_gray'], C['border_default'], fontsize=7)
    _box(ax, 2.8, 4, 1.2, 0.5, 'Chunk &\nClean', C['fill_orange'], C['border_orange'], fontsize=7)
    _box(ax, 4.4, 4, 1.2, 0.5, 'Embed', C['fill_purple'], C['border_purple'], fontsize=7)
    _arrow(ax, 1.8, 4, 2.2, 4, C['subtext'])
    _arrow(ax, 3.4, 4, 3.8, 4, C['subtext'])
    
    # Vector DB (shared)
    _cylinder(ax, 6.5, 3, 1.5, 0.8, 'Vector\nDatabase', C['fill_blue'], C['border_blue'])
    _arrow(ax, 5, 4, 5.7, 3.35, C['border_blue'])
    
    # Online path (bottom)
    _cluster(ax, 5, 1.2, 9, 1.5, 'Online: Query Pipeline', C['teal'], C['fill_teal'])
    
    _box(ax, 1.2, 0.9, 1.2, 0.5, 'User\nQuery', C['fill_yellow'], C['border_yellow'], fontsize=7)
    _box(ax, 3, 0.9, 1.2, 0.5, 'Embed\nQuery', C['fill_purple'], C['border_purple'], fontsize=7)
    _box(ax, 5, 0.9, 1.2, 0.5, 'Retrieve\n(top-K)', C['fill_blue'], C['border_blue'], fontsize=7)
    _box(ax, 6.8, 0.9, 1.2, 0.5, 'Re-rank\n(cross-enc)', C['fill_orange'], C['border_orange'], fontsize=7)
    _box(ax, 8.8, 0.9, 1.4, 0.5, 'LLM\nGenerate', C['fill_purple'], C['border_purple'], fontsize=7, fontweight='bold')
    
    _arrow(ax, 1.8, 0.9, 2.4, 0.9, C['teal'])
    _arrow(ax, 3.6, 0.9, 4.4, 0.9, C['teal'])
    _arrow(ax, 5.6, 0.9, 6.2, 0.9, C['teal'])
    _arrow(ax, 7.4, 0.9, 8.1, 0.9, C['teal'])
    
    # Vector DB to retrieve
    _arrow(ax, 6.5, 2.55, 5, 1.18, C['border_blue'], style='dashed')
    
    _save(fig, 'diagrams/compiled/ch05/rag-pipeline.pdf')


def ch12_multi_agent():
    """Three multi-agent patterns: Supervisor, Peer, Hierarchical."""
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
    
    patterns = [
        ('Supervisor', [
            ('Supervisor', 5, 3, C['fill_purple'], C['border_purple'], True),
            ('Worker A', 2, 1, C['fill_blue'], C['border_blue'], False),
            ('Worker B', 5, 1, C['fill_blue'], C['border_blue'], False),
            ('Worker C', 8, 1, C['fill_blue'], C['border_blue'], False),
        ], [(5, 2.6, 2, 1.4), (5, 2.6, 5, 1.4), (5, 2.6, 8, 1.4)]),
        
        ('Peer-to-Peer', [
            ('Agent A', 2, 2.5, C['fill_green'], C['border_green'], False),
            ('Agent B', 8, 2.5, C['fill_green'], C['border_green'], False),
            ('Agent C', 5, 0.8, C['fill_green'], C['border_green'], False),
        ], [(2.5, 2.5, 7.5, 2.5), (8, 2.1, 5.5, 1.1), (4.5, 1.1, 2, 2.1)]),
        
        ('Hierarchical', [
            ('Orchestrator', 5, 3.2, C['fill_purple'], C['border_purple'], True),
            ('Lead A', 2.5, 2, C['fill_orange'], C['border_orange'], False),
            ('Lead B', 7.5, 2, C['fill_orange'], C['border_orange'], False),
            ('Worker', 1.5, 0.8, C['fill_blue'], C['border_blue'], False),
            ('Worker', 3.5, 0.8, C['fill_blue'], C['border_blue'], False),
            ('Worker', 6.5, 0.8, C['fill_blue'], C['border_blue'], False),
            ('Worker', 8.5, 0.8, C['fill_blue'], C['border_blue'], False),
        ], [(5, 2.8, 2.5, 2.4), (5, 2.8, 7.5, 2.4),
            (2.5, 1.6, 1.5, 1.2), (2.5, 1.6, 3.5, 1.2),
            (7.5, 1.6, 6.5, 1.2), (7.5, 1.6, 8.5, 1.2)]),
    ]
    
    for ax, (title, nodes, edges) in zip(axes, patterns):
        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-0.2, 4)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=9, fontweight='bold', color=C['text'])
        
        for name, x, y, fill, border, bold in nodes:
            fw = 'bold' if bold else 'normal'
            _box(ax, x, y, 2, 0.5, name, fill, border, fontsize=6, fontweight=fw, shadow=False)
        
        for x1, y1, x2, y2 in edges:
            _arrow(ax, x1, y1, x2, y2, C['subtext'], linewidth=0.8)
    
    plt.tight_layout()
    _save(fig, 'diagrams/compiled/ch12/multi-agent.pdf')


# ============================================================================
# MAIN
# ============================================================================

ALL_DIAGRAMS = {
    'ch01': [ch01_new_software_stack],
    'ch02': [ch02_kv_cache, ch02_training_pipeline, ch02_distributed_training],
    'ch03': [ch03_post_training_landscape],
    'ch04': [ch04_lora_architecture],
    'ch05': [ch05_model_routing, ch05_rag_pipeline],
    'ch06': [ch06_stripe_fraud, ch06_uber_gateway],
    'ch07': [ch07_document_pipeline],
    'ch08': [ch08_eval_pyramid],
    'ch12': [ch12_agent_loop, ch12_multi_agent],
}

if __name__ == '__main__':
    filter_ch = sys.argv[1] if len(sys.argv) > 1 else None
    
    total = 0
    for ch, funcs in ALL_DIAGRAMS.items():
        if filter_ch and ch != filter_ch:
            continue
        print(f"\n{'='*50}")
        print(f"Rendering {ch} ({len(funcs)} diagrams)")
        print(f"{'='*50}")
        for func in funcs:
            try:
                func()
                total += 1
            except Exception as e:
                print(f"  ✗ {func.__name__}: {e}")
    
    print(f"\n✅ Rendered {total} diagrams successfully")
    print(f"Font: {FONT_MAIN} / {FONT_MONO}")
