import faicons

from shiny import ui
from shinywidgets import output_widget

from data import gt

ui_overview = ui.nav_panel(
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
)
