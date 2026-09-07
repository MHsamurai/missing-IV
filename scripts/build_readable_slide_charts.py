"""Build 14 x 5 cm slide charts from saved results; never rerun simulation.

Run: python scripts/build_readable_slide_charts.py
Dependencies: matplotlib, pandas. Output PDFs retain their exact physical size.
Sources: simulation/plot_presentation_recovery.py and the bias/RMSE plotting
cell of simulation/allman_latent_mnar_simulation.ipynb. Only orientation,
layout, and labels change; CSV selection/ordering/aggregation are unchanged.
The four-panel marginal plot is split so every label can remain at 11 pt.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "simulation/results"
OUTPUT = ROOT / "manuscript/figures/readable"
SIZE = (14 / 2.54, 5 / 2.54)
FONT = 11
METHODS = [
    "full_data_oracle", "mar", "selection_likelihood_correct",
    "selection_likelihood_misspecified", "proposed_stage1_bridge",
]
LABELS = ["Oracle", "MAR", "Selection correct", "Selection misspec.", "Proposed Stage 1"]
STYLE = {
    "font.family": "DejaVu Sans", "font.size": FONT,
    "axes.titlesize": FONT, "axes.labelsize": FONT,
    "xtick.labelsize": FONT, "ytick.labelsize": FONT,
    "legend.fontsize": FONT, "figure.titlesize": FONT,
    "pdf.fonttype": 42, "savefig.bbox": None,
    "figure.autolayout": False, "figure.constrained_layout.use": False,
}


def save(fig, name):
    """Reject undersized/clipped text; never crop or resize the PDF canvas."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for text in fig.findobj(Text):
        if not text.get_visible() or not text.get_text():
            continue
        if text.get_fontsize() < FONT:
            raise ValueError(f"Undersized text: {text.get_text()}")
        box = text.get_window_extent(renderer)
        if (box.x0 < -0.5 or box.y0 < -0.5 or
                box.x1 > fig.bbox.width + 0.5 or box.y1 > fig.bbox.height + 0.5):
            raise ValueError(f"Clipped text: {text.get_text()}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / name
    fig.savefig(path, bbox_inches=None, metadata={"CreationDate": None})
    plt.close(fig)
    print(f"{path.relative_to(ROOT)}: 14.0 x 5.0 cm; minimum text {FONT} pt")


def method_panels(labels):
    fig, axes = plt.subplots(1, 2, figsize=SIZE, sharey=True)
    fig.subplots_adjust(left=.285, right=.95, bottom=.28, top=.80, wspace=.32)
    for ax in axes:
        ax.set_yticks(range(5), labels)
        ax.set_ylim(4.3, -.3)
        ax.grid(axis="x", alpha=.2)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
    return fig, axes


def marginal():
    data = pd.read_csv(RESULTS / "allman_observed_law_inference_summary.csv")
    data = data[data["scope"] == "overall_marginal"]
    pairs = [
        ("bias_sd", [("bias", "Bias", 0), ("empirical_sd", "Empirical SD", None)]),
        ("se_coverage", [("mean_estimated_se", "Mean estimated SE", None),
                         ("coverage", "95% coverage", 95)]),
    ]
    for suffix, specs in pairs:
        fig, axes = method_panels(LABELS)
        for ax, (metric, title, reference) in zip(axes, specs):
            for parameter, label, color, marker, style in [
                ("mu_Y2", "P(Y2 = 1)", "#1F5AA6", "o", "-"),
                ("mu_Y3", "P(Y3 = 1)", "#B86510", "s", "--"),
            ]:
                values = data[data["parameter"] == parameter].set_index("method").loc[METHODS, metric].to_numpy()
                if metric == "coverage":
                    values = values * 100
                ax.plot(values, range(5), color=color, marker=marker,
                        linestyle=style, linewidth=1.3, markersize=4, label=label)
            if reference is not None:
                ax.axvline(reference, color="#777777", linestyle=":", linewidth=1)
            ax.set_title(title, pad=9)
            if metric in ("empirical_sd", "mean_estimated_se"):
                ax.set_xlim(.015, .06)
                ax.set_xticks([.02, .04, .06])
            if metric == "coverage":
                ax.set_xlim(0, 105)
                ax.set_xticks([0, 50, 95], ["0%", "50%", "95%"])
        fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center",
                   bbox_to_anchor=(.60, 0), ncol=2, frameon=False)
        save(fig, f"allman_outcome_marginal_inference_{suffix}_chart.pdf")


def joint():
    data = pd.read_csv(RESULTS / "allman_y_joint_distribution.csv", dtype={"cell": str})
    data["cell"] = data["cell"].str.zfill(3)
    cells = [f"{cell:03b}" for cell in range(8)]
    fig, ax = plt.subplots(figsize=SIZE)
    fig.subplots_adjust(left=.13, right=.98, top=.98, bottom=.53)
    for method, label, color, marker, style in [
        ("population_truth", "Population truth", "#222222", "o", "-"),
        ("mar", "MAR", "#D97706", "s", "--"),
        ("selection_likelihood_correct", "Selection correct", "#2A7F62", "D", "-."),
        ("selection_likelihood_misspecified", "Selection misspecified", "#B83A3A", "v", ":"),
        ("proposed_saturated_bridge", "Proposed (Stages 1 + 2)", "#1F5AA6", "^", "-"),
    ]:
        values = data[data["method"] == method].groupby("cell")["probability"].mean().loc[cells]
        ax.plot(range(8), values, label=label, color=color, marker=marker,
                linestyle=style, linewidth=1.6 if method.startswith("proposed") else 1.2,
                markersize=4)
    ax.set_xticks(range(8), cells)
    ax.set_ylabel("Probability")
    ax.set_xlabel("Outcome cell (Y1, Y2, Y3)", labelpad=1)
    ax.set_ylim(0, .33)
    ax.set_yticks([0, .15, .3])
    ax.grid(axis="y", alpha=.2)
    ax.spines[["top", "right"]].set_visible(False)
    fig.legend(*ax.get_legend_handles_labels(), loc="lower center", ncol=2,
               frameon=False, bbox_to_anchor=(.52, -.015),
               labelspacing=.15, columnspacing=1, handlelength=1.6)
    save(fig, "allman_y_joint_distribution_chart.pdf")


def latent():
    methods = METHODS[:-1] + ["proposed_saturated_bridge"]
    data = pd.read_csv(RESULTS / "allman_summary.csv").set_index("method").loc[methods]
    fig, axes = method_panels(LABELS[:-1] + ["Saturated bridge"])
    fig.subplots_adjust(top=.72)
    for ax, (title, bias, rmse) in zip(axes, [
        ("Measurement kernels", "M_bias", "M_RMSE"),
        ("Latent class proportion", "p_f1_bias", "p_f1_RMSE"),
    ]):
        ax.plot(data[bias], range(5), marker="o", linewidth=1.3, markersize=4, label="Bias")
        ax.plot(data[rmse], range(5), marker="s", linewidth=1.3, markersize=4, label="RMSE")
        ax.axvline(0, color="black", linewidth=.8)
        ax.set_title(title.replace(" ", "\n", 1), pad=9)
        ax.set_xticks([-.05, 0, .05, .1] if bias == "M_bias" else [0, .025, .05])
    fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center",
               bbox_to_anchor=(.6, 0), ncol=2, frameon=False)
    save(fig, "allman_bias_rmse_comparison_chart.pdf")


if __name__ == "__main__":
    with plt.rc_context(STYLE):
        marginal()
        joint()
        latent()
