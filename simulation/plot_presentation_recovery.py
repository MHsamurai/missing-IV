"""Render presentation figures from the saved Monte Carlo results."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
METHODS = [
    "full_data_oracle", "mar", "selection_likelihood_correct",
    "selection_likelihood_misspecified", "proposed_stage1_bridge",
]
LABELS = ["Oracle", "MAR", "Selection\ncorrect", "Selection\nmisspecified", "Proposed\nStage 1"]


def save_figure(figure, stem):
    for suffix in ("pdf", "png"):
        figure.savefig(
            ROOT / "figures" / f"{stem}.{suffix}", dpi=200,
            bbox_inches="tight", metadata={"CreationDate": None} if suffix == "pdf" else None,
        )
    plt.close(figure)


def plot_marginal_inference():
    data = pd.read_csv(ROOT / "results" / "allman_observed_law_inference_summary.csv")
    data = data[data["scope"] == "overall_marginal"]
    specs = [
        ("bias", "Bias", 0), ("empirical_sd", "Empirical SD", None),
        ("mean_estimated_se", "Mean estimated SE", None),
        ("coverage", "95% coverage", .95),
    ]
    figure, axes = plt.subplots(2, 2, figsize=(12.8, 5.2), sharex=True)
    figure.subplots_adjust(left=.07, right=.99, top=.97, bottom=.23, hspace=.38, wspace=.22)
    for axis, (metric, title, reference) in zip(axes.flat, specs):
        for parameter, label, color, marker, style in [
            ("mu_Y2", r"$\mu_2=P(Y_2=1)$", "#1F5AA6", "o", "-"),
            ("mu_Y3", r"$\mu_3=P(Y_3=1)$", "#B86510", "s", "--"),
        ]:
            rows = data[data["parameter"] == parameter].set_index("method").loc[METHODS]
            values = rows[metric].to_numpy()
            if metric == "coverage":
                values = values * 100
            axis.plot(range(5), values, color=color, marker=marker,
                      linestyle=style, linewidth=2, markersize=6, label=label)
        if reference is not None:
            axis.axhline(reference * (100 if metric == "coverage" else 1),
                         color="#777777", linestyle=":", linewidth=1.3)
        axis.set_title(title, fontsize=13, loc="left", pad=7)
        axis.grid(axis="y", alpha=.2)
        axis.spines[["top", "right"]].set_visible(False)
        axis.tick_params(labelsize=10)
        axis.set_xticks(range(5), LABELS)
        axis.set_xlim(-.18, 4.18)
        if metric in ("empirical_sd", "mean_estimated_se"):
            axis.set_ylim(.015, .06)
        if metric == "coverage":
            axis.set_ylim(0, 105)
            axis.set_yticks([0, 50, 95], ["0%", "50%", "95%"])
    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", bbox_to_anchor=(.5, .015),
                  ncol=2, frameon=False, fontsize=13)
    save_figure(figure, "allman_outcome_marginal_inference_slides")


def plot_joint_distribution():
    data = pd.read_csv(ROOT / "results" / "allman_y_joint_distribution.csv", dtype={"cell": str})
    data["cell"] = data["cell"].str.zfill(3)
    cells = [f"{cell:03b}" for cell in range(8)]
    figure, axis = plt.subplots(figsize=(12.8, 4.9))
    figure.subplots_adjust(left=.07, right=.99, top=.97, bottom=.27)
    for method, label, color, marker, style in [
        ("population_truth", "Population truth", "#222222", "o", "-"),
        ("mar", "MAR", "#D97706", "s", "--"),
        ("selection_likelihood_correct", "Selection correct", "#2A7F62", "D", "-."),
        ("selection_likelihood_misspecified", "Selection misspecified", "#B83A3A", "v", ":"),
        ("proposed_saturated_bridge", "Proposed (Stages 1 + 2)", "#1F5AA6", "^", "-"),
    ]:
        means = data[data["method"] == method].groupby("cell")["probability"].mean().loc[cells]
        axis.plot(range(8), means, label=label, color=color, marker=marker,
                  linestyle=style, linewidth=2.3 if method.startswith("proposed") else 1.7,
                  markersize=6)
    axis.set_xticks(range(8), cells, fontsize=12)
    axis.tick_params(axis="y", labelsize=11)
    axis.set_ylabel("Probability", fontsize=13)
    axis.set_xlabel(r"Outcome cell $(Y_1,Y_2,Y_3)$", fontsize=13, labelpad=8)
    axis.set_ylim(0, .33)
    axis.grid(axis="y", alpha=.2)
    axis.spines[["top", "right"]].set_visible(False)
    figure.legend(*axis.get_legend_handles_labels(), loc="lower center", ncol=3,
                  frameon=False, fontsize=11, bbox_to_anchor=(.52, 0))
    save_figure(figure, "allman_y_joint_distribution_slides")


if __name__ == "__main__":
    with plt.rc_context({"font.family": "DejaVu Sans"}):
        plot_marginal_inference()
        plot_joint_distribution()
