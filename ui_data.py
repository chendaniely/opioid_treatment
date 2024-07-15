from shiny import ui
from shinyswatch.theme import united as shiny_theme

from data import data_choices

ui_data = ui.nav_panel(
    "Data",
    ui.page_sidebar(
        ui.sidebar(
            "Assemble and Download",
            shiny_theme,  # FIXME: the way i split up the ui, this cannot be in ui.py
            ui.input_selectize(
                id="selectize_data",
                label="Select data to combine:",
                choices=data_choices,
                selected="demographics",
                multiple=True,
            ),
            ui.help_text("Data Filters"),
            ui.output_ui("data_filters"),
        ),
        ui.layout_columns(
            ui.value_box(
                title="Number of rows",
                value=ui.output_text("assembled_nrow"),
            ),
            ui.value_box(
                title="Number of columns",
                value=ui.output_text("assembled_ncol"),
            ),
            ui.value_box(
                title="Estimated CSV download size (Kb)",
                value=ui.output_text("assembled_csv_size"),
            ),
        ),
        ui.download_button("download_data", "Download Data"),
        ui.output_data_frame("assembled_data"),
    ),
)
