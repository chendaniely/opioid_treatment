from shiny import ui

from ui_overview import ui_overview
from ui_data import ui_data
from ui_about import ui_about

ui.include_css("styles.css")

app_ui = ui.page_navbar(
    ui_overview,
    ui_data,
    ui_about,
    title="Opioid Treatment",
    id="page",
)
