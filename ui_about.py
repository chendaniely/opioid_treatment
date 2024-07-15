from shiny import ui

from data import about_markdown

ui_about = (
    ui.nav_panel(
        "About",
        ui.page_fixed(
            ui.markdown(about_markdown),
        ),
    ),
)
