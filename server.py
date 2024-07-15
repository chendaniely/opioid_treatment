from pathlib import Path
from itertools import chain
import io

import pandas as pd
import plotly.express as px
import plotnine as p9
from plotnine import ggplot, aes
import seaborn as sns
from shiny import render, reactive, ui
from shinywidgets import render_widget, output_widget

import data
import helper


def server(input, output, session):
    @render.text
    def cnt_patients():
        return f"{data.patient_count}"

    @render.text
    def num_visit_miss_14():
        return f"{data.num_visit_miss_14}"

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

    @reactive.calc
    def joined_subset():
        joined_data_col_ids = [
            f"joined_data___{col}" for col in joined_data().columns
        ]

        joined_data_sub = joined_data()

        # go through each column in the joined dataframe so a filter can be created
        for input_id in joined_data_col_ids:
            col = input_id.split("___")[1]
            input_val = getattr(input, input_id)()

            # if the initial filter value is empty just move on to next column
            if not input_val:
                joined_data_sub = joined_data_sub
                continue

            # selectize is returning a string, we need int to compare
            elif col == "who":
                joined_data_sub = joined_data_sub.loc[
                    joined_data_sub["who"].isin(pd.to_numeric(input_val))
                ]

            # special case for age: want it to be a slider, not selectize
            elif col == "age":
                joined_data_sub["age"] = pd.to_numeric(joined_data_sub["age"])
                joined_data_sub = joined_data_sub.loc[
                    joined_data_sub["age"].between(
                        input_val[0], input_val[1], inclusive="both"
                    )
                ]

            # default UI filter is selectize
            else:
                # check if the input value has a missing value
                if "nan" in input_val:
                    has_nan = True
                else:
                    has_nan = False

                # need to handle the nan as NaN missing value
                # and filter separately
                if has_nan:
                    joined_data_sub = joined_data_sub.loc[
                        (joined_data_sub[col].isin(input_val))
                        | (joined_data_sub[col].isna())
                    ]
                else:
                    joined_data_sub = joined_data_sub.loc[
                        joined_data_sub[col].isin(input_val)
                    ]

        return joined_data_sub

    @render.ui
    def data_filters():
        """Create the filter components based on the combined dataframe columns"""
        ui_elements = []

        for col in joined_data().columns:
            if col == "age":
                min_age = joined_data()["age"].min()
                max_age = joined_data()["age"].max()

                new_element = ui.input_slider(
                    id=f"joined_data___{col}",
                    label=f"{col}",
                    min=min_age,
                    max=max_age,
                    value=[min_age, max_age],
                    step=1,
                    ticks=True,
                    drag_range=True,
                )
            else:
                new_element = ui.input_selectize(
                    id=f"joined_data___{col}",
                    label=f"{col}",
                    choices=joined_data()[col].unique().tolist(),
                    multiple=True,
                    remove_button=True,
                )

            ui_elements.append(new_element)

        return ui_elements

    @reactive.calc
    def _render_px_missing_widgets():
        FXN_BODY_RENDER_PX_MISSING = """
@render_widget
def plot_miss_{col}():
    return helper.px_missing(joined_subset(), x="{col}")
"""
        for col in joined_subset().columns:
            fx = FXN_BODY_RENDER_PX_MISSING.strip().format(col=col)
            exec(fx)

    @render.data_frame
    def assembled_data():
        _render_px_missing_widgets()
        plots = {}
        for col in joined_subset().columns:
            plots[col] = output_widget(f"plot_miss_{col}")
        plots_df = pd.DataFrame(plots, index=[""])

        df = pd.concat([plots_df, joined_subset()])
        df = joined_subset()  # TODO: manually not put in the plots for now
        return render.DataGrid(df, selection_mode="rows")

    @render.text
    def assembled_nrow():
        return len(joined_subset().index)

    @render.text
    def assembled_ncol():
        return len(joined_subset().columns)

    @render.text
    def assembled_csv_size():
        csv_buffer = io.StringIO()
        joined_subset().to_csv(csv_buffer, index=False)
        csv_size = len(csv_buffer.getvalue().encode("utf-8"))
        return f"{csv_size / 1000:,.2f}"  # return in kilobytes

    @render.download(filename="data.csv")
    async def download_data():
        # This version uses a function to generate the filename.
        yield joined_subset().to_csv()
