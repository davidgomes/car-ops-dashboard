from nicegui import ui
from app import dashboard

def startup() -> None:
    # Create the main dashboard
    dashboard.create()