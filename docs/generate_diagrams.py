import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)


def add_label(ax, x, y, text, *, fontsize=11, box=True, box_fc="#ffffff", box_ec="#2b3a55", text_color="#1f2937"):
    if box:
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fontsize, color=text_color,
            bbox=dict(boxstyle="round,pad=0.35", fc=box_fc, ec=box_ec, lw=1.2)
        )
    else:
        ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, color=text_color)


def add_box(ax, x, y, w, h, label, color="#e8f0fe", edge="#3b82f6"):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=1.5, edgecolor=edge, facecolor=color
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=10.5, color="#111827")
    return patch


def add_arrow(ax, x1, y1, x2, y2, text=None):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=14,
        linewidth=1.3, color="#374151"
    )
    ax.add_patch(arrow)
    if text:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, text, fontsize=8.2, ha="center", va="center", color="#111827")


def add_footer(ax):
    ax.text(
        0.5, 0.03,
        "© 2026 Devesh Kumar • devesh2178@gmail.com",
        ha="center", va="center",
        fontsize=8.5, color="#4b5563",
        transform=ax.transAxes
    )


def draw_architecture():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    add_box(ax, 0.5, 5.6, 1.9, 1.0, "User /\nExternal Input", color="#e0f2fe", edge="#0284c7")
    add_box(ax, 3.0, 5.6, 2.1, 1.0, "Input Guardrail\nRegex Validate", color="#dbeafe", edge="#2563eb")
    add_box(ax, 6.0, 5.6, 2.2, 1.0, "Untrusted LLM\nExtract JSON", color="#ede9fe", edge="#7c3aed")
    add_box(ax, 9.0, 5.6, 2.2, 1.0, "Sanitized\nEmailSummary", color="#dcfce7", edge="#16a34a")
    add_box(ax, 3.0, 2.8, 2.3, 1.0, "Trusted LLM\nExecute Task", color="#fef3c7", edge="#d97706")
    add_box(ax, 6.1, 2.8, 2.1, 1.0, "Candidate\nResponse", color="#fee2e2", edge="#ef4444")
    add_box(ax, 9.0, 2.8, 2.2, 1.0, "Regex\nGuardrail", color="#f1f5f9", edge="#475569")
    add_box(ax, 11.7, 2.8, 2.2, 1.0, "Semantic\nGuardrail", color="#f5f3ff", edge="#8b5cf6")
    add_box(ax, 8.2, 0.7, 3.0, 1.0, "Final Safe Response", color="#dcfce7", edge="#15803d")

    add_arrow(ax, 2.4, 6.1, 3.0, 6.1, "raw input")
    add_arrow(ax, 5.1, 6.1, 6.0, 6.1, "validate")
    add_arrow(ax, 8.2, 6.1, 9.0, 6.1, "JSON")
    add_arrow(ax, 4.1, 5.6, 4.1, 3.8, "sanitized context")
    add_arrow(ax, 5.3, 3.3, 6.1, 3.3)
    add_arrow(ax, 8.2, 3.3, 9.0, 3.3)
    add_arrow(ax, 11.2, 3.3, 11.7, 3.3, "policy")
    add_arrow(ax, 9.8, 2.8, 9.8, 1.7)
    add_arrow(ax, 11.6, 2.8, 11.6, 1.7)
    add_arrow(ax, 8.3, 1.2, 7.6, 1.2)

    ax.text(7, 7.3, "AI Security Pipeline Architecture", fontsize=16, fontweight="bold", ha="center", color="#111827")
    add_footer(ax)
    fig.tight_layout()
    fig.savefig(OUT / "architecture_diagram.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_call_flow():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")

    boxes = {
        "user": (0.5, 8.5, 1.8, 1.0),
        "orchestrator": (3.2, 8.5, 2.2, 1.0),
        "input_guard": (6.3, 8.5, 2.0, 1.0),
        "untrusted": (9.2, 8.5, 2.2, 1.0),
        "trusted": (3.0, 5.8, 2.3, 1.0),
        "regex": (6.5, 5.8, 2.0, 1.0),
        "semantic": (9.6, 5.8, 2.3, 1.0),
        "final": (6.4, 2.8, 2.5, 1.0),
    }

    for name, (x, y, w, h) in boxes.items():
        color = {
            "user": "#dbeafe",
            "orchestrator": "#ede9fe",
            "input_guard": "#e0f2fe",
            "untrusted": "#dcfce7",
            "trusted": "#fef3c7",
            "regex": "#f1f5f9",
            "semantic": "#f5f3ff",
            "final": "#dcfce7",
        }[name]
        edge = {
            "user": "#2563eb",
            "orchestrator": "#7c3aed",
            "input_guard": "#0284c7",
            "untrusted": "#16a34a",
            "trusted": "#d97706",
            "regex": "#475569",
            "semantic": "#8b5cf6",
            "final": "#15803d",
        }[name]
        add_box(ax, x, y, w, h, {
            "user": "User",
            "orchestrator": "Main\nOrchestrator",
            "input_guard": "Input\nGuardrail",
            "untrusted": "Untrusted LLM",
            "trusted": "Trusted LLM",
            "regex": "Regex\nGuardrail",
            "semantic": "Semantic\nGuardrail",
            "final": "Final\nResponse",
        }[name], color=color, edge=edge)

    add_arrow(ax, 2.3, 9.0, 3.2, 9.0, "goal + raw input")
    add_arrow(ax, 5.4, 9.0, 6.3, 9.0, "validate")
    add_arrow(ax, 8.3, 9.0, 9.2, 9.0, "allow / block")
    add_arrow(ax, 10.4, 8.5, 10.4, 6.8)
    add_arrow(ax, 10.4, 6.8, 5.3, 6.8, "EmailSummary\nJSON")
    add_arrow(ax, 5.3, 6.3, 6.5, 6.3)
    add_arrow(ax, 8.5, 6.3, 9.6, 6.3, "candidate response")
    add_arrow(ax, 8.5, 5.8, 8.5, 4.3)
    add_arrow(ax, 10.9, 5.8, 10.9, 4.3)
    add_arrow(ax, 7.8, 3.3, 8.1, 3.3)
    add_arrow(ax, 9.2, 3.3, 7.5, 3.3, "safe output")

    ax.text(7, 9.9, "Call Flow of the Security Pipeline", fontsize=16, fontweight="bold", ha="center", color="#111827")
    add_footer(ax)
    fig.tight_layout()
    fig.savefig(OUT / "call_flow_diagram.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_guardrail_activity():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    states = [
        (0.8, 6.3, 2.2, 0.9, "Start\nPipeline", "#dbeafe", "#2563eb"),
        (3.8, 6.3, 2.6, 0.9, "Input non-empty\nand valid?", "#ecfeff", "#0891b2"),
        (7.3, 6.3, 2.4, 0.9, "Regex Input\nGuardrail", "#e0f2fe", "#0284c7"),
        (10.6, 6.3, 2.5, 0.9, "Block\nPrompt Injection", "#fee2e2", "#ef4444"),
        (1.4, 4.1, 2.8, 0.9, "Extract\nStructured Data", "#dcfce7", "#16a34a"),
        (5.0, 4.1, 2.6, 0.9, "Generate\nCandidate Output", "#fef3c7", "#d97706"),
        (8.5, 4.1, 2.5, 0.9, "Regex Output\nValidation", "#f1f5f9", "#475569"),
        (11.6, 4.1, 2.0, 0.9, "Blocked?", "#f5f3ff", "#8b5cf6"),
        (4.7, 1.8, 3.5, 0.9, "Semantic\nSafety Check", "#ede9fe", "#7c3aed"),
        (9.3, 1.8, 3.5, 0.9, "Return Safe\nResponse", "#dcfce7", "#15803d"),
    ]

    for x, y, w, h, label, color, edge in states:
        add_box(ax, x, y, w, h, label, color=color, edge=edge)

    add_arrow(ax, 3.0, 6.8, 3.8, 6.8)
    add_arrow(ax, 6.4, 6.8, 7.3, 6.8)
    add_arrow(ax, 9.7, 6.8, 10.6, 6.8)
    add_arrow(ax, 4.6, 4.1, 5.0, 4.1)
    add_arrow(ax, 7.6, 4.1, 8.5, 4.1)
    add_arrow(ax, 11.0, 4.1, 11.6, 4.1)
    add_arrow(ax, 6.2, 2.8, 6.2, 3.9)
    add_arrow(ax, 9.3, 2.7, 9.3, 3.9)
    add_arrow(ax, 4.8, 1.8, 5.8, 1.8)
    add_arrow(ax, 8.6, 2.7, 9.3, 2.7)

    ax.text(7, 7.7, "Guardrail Activity Flow", fontsize=16, fontweight="bold", ha="center", color="#111827")
    add_footer(ax)
    fig.tight_layout()
    fig.savefig(OUT / "guardrail_activity_diagram.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    draw_architecture()
    draw_call_flow()
    draw_guardrail_activity()
    print(f"Diagrams generated in {OUT}")
