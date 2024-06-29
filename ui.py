import faicons
from shiny import ui
from shinywidgets import output_widget

from data import data_choices, gt, about_markdown

ui.include_css("styles.css")

# shiny UI -----

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Overview",
        ui.layout_columns(
            ui.value_box(
                title="Randomized Patients",
                value=ui.output_ui("cnt_patients"),
                showcase=faicons.icon_svg("person", width="50px"),
            ),
            ui.value_box(
                title="Missing 14 Consecutive Visits",
                value=ui.output_ui("num_visit_miss_14"),
                showcase=faicons.icon_svg("hand", width="50px"),
            ),
            ui.card(
                output_widget("age_hist_px"),
                height="100px",
                class_=".card-margin-small",
            ),
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Self-Reported Opioid Use Over Treatment"),
                output_widget("drug_use_opioids_time_px"),
            ),
            ui.card(
                ui.card_header("Urine Test Opioid Use Over Treatment"),
                output_widget("urine_drug_use_opioids_time_px"),
            ),
            ui.card(ui.HTML(gt.as_raw_html())),
            col_widths=(4, 4, 4),
        ),
    ),
    ui.nav_panel(
        "Data",
        ui.page_sidebar(
            ui.sidebar(
                "Assemble and Filter Data",
                ui.input_selectize(
                    id="selectize_data",
                    label="Select data to assemble:",
                    choices=data_choices,
                    selected="demographics",
                    multiple=True,
                ),
                ui.output_ui("data_filters"),
            ),
            ui.download_button("download_data", "Download Data"),
            ui.output_data_frame("assembled_data"),
            # ui.output_image("skimpy_results_img"),
            ui.output_text_verbatim("skimpy_results_txt"),
        ),
    ),
    # ui.nav_panel(
    #     "Testing",
    #     ui.output_plot("drug_use_opioids_time"),
    #     output_widget("drug_use_opioids_time_alt"),
    # ),
    ui.nav_panel(
        "About",
        ui.page_fixed(
            ui.markdown(about_markdown),
        ),
    ),
    title="Opioid Treatment",
    id="page",
)
