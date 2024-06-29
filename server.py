from pathlib import Path
from itertools import chain

import altair as alt
import pandas as pd
import plotly.express as px
import plotnine as p9
from plotnine import ggplot, aes
import seaborn as sns
from shiny import render, reactive, ui
from shinywidgets import render_widget
import skimpy as sk

import data
import helper

# shiny server -----


def server(input, output, session):

    @render.text
    def cnt_patients():
        return f"{data.patient_count}"

    # @render.text()
    # def pct_reason_missed():
    #     return f"{data.has_reason_missed / data.total_visits:4.1%}"

    @render.text
    def num_visit_miss_14():
        return f"{data.num_visit_miss_14}"

    # @render.plot(alt="Self reported drug use counts over time")
    # def drug_use_opioids_time():
    #     g = (
    #         ggplot(
    #             data.drug_usage_opioids,
    #             aes(x="when", y="who", color="treatment"),
    #         )
    #         + p9.geom_line()
    #         + p9.geom_vline(aes(xintercept=0))
    #         + p9.theme_bw()
    #     )
    #     return g

    # @render_widget()
    # def drug_use_opioids_time_alt():
    #     line = (
    #         alt.Chart(data.drug_usage_opioids)
    #         .mark_line()
    #         .encode(x="when", y="who", color="treatment")
    #     )

    #     # Create the vertical line at x=0
    #     vertical_line = (
    #         alt.Chart(pd.DataFrame({"x": [0]}))
    #         .mark_rule(color="red")
    #         .encode(x="x:Q")
    #     )

    #     chart = line + vertical_line
    #     return chart

    @render_widget()
    def drug_use_opioids_time_px():
        fig = px.line(
            data.total_drug_over_study_opioids,
            x="when",
            y="who",
            color="treatment",
            symbol="treatment",
            markers=True,
            labels={
                "when": "Study Day",
                "who": "Count",
                "treatment": "Treatment",
            },
        ).add_vline(x=0, line_color="black", line_width=1)

        fig.update_layout(
            yaxis_range=[0, data.max_y_for_plot],
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        return fig

    @render_widget()
    def urine_drug_use_opioids_time_px():
        fig = px.line(
            data.urine_drug_usage_opioid,
            x="when",
            y="who",
            color="treatment",
            symbol="treatment",
            markers=True,
            labels={
                "when": "Study Day",
                "who": "Count",
                "treatment": "Treatment",
            },
        ).add_vline(x=0, line_color="black", line_width=1)

        fig.update_layout(
            yaxis_range=[0, data.max_y_for_plot],
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        return fig

    @render.plot()
    def age_hist_sns():
        ax = sns.histplot(data=data.demographics, x="age").set(ylabel=None)
        return ax

    @render_widget
    def age_hist_px():
        p = px.histogram(data.demographics, x="age")
        p
        p.update_xaxes(title="Age")
        p.update_yaxes(title=None)
        return p

    @reactive.calc
    @reactive.event(input.selectize_data)
    def joined_data():
        return helper.join_data(input.selectize_data())

    @render.image
    def skimpy_results_img():
        pth = Path.cwd() / "skimpy.svg"
        sk.skim_get_figure(joined_data(), pth, "svg")
        img = {"src": pth}
        return img

    @render.text
    def skimpy_results_txt():
        pth = Path.cwd() / "skimpy.txt"
        sk.skim_get_figure(joined_data(), pth, "text")
        with open(pth, "r") as f:
            skimpy_contents = f.read()
        print(skimpy_contents)
        return skimpy_contents

    @reactive.calc
    def joined_subset():
        joined_data_col_ids = [
            f"joined_data_{col}" for col in joined_data().columns
        ]

        joined_subset = joined_data()

        for input_id in joined_data_col_ids:
            col = input_id.split("_")[2]
            input_val = getattr(input, input_id)()
            if input_val:
                joined_subset = joined_subset.loc[
                    joined_subset[col].isin(input_val)
                ]
        return joined_subset

    @render.ui
    def data_filters():
        ui_elements = [
            ui.input_selectize(
                f"joined_data_{col}",
                f"{col}",
                joined_data()[col].unique().tolist(),
                multiple=True,
            )
            for col in joined_data().columns
        ]
        return ui_elements

    @render.data_frame
    def assembled_data():
        return render.DataGrid(joined_subset(), selection_mode="rows")

    @render.download(filename="data.csv")
    async def download_data():
        # This version uses a function to generate the filename.
        yield joined_subset().to_csv()
