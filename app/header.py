from nicegui import ui

def create():
    """Create the application header with title and logo placeholder"""
    with ui.header().classes('bg-blue-900 text-white p-4'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.row().classes('items-center'):
                # Logo placeholder
                ui.icon('directions_car', size='2em').classes('mr-4')
                ui.label('Global Automotive Operations Dashboard').classes('text-2xl font-bold')
            
            # Current time display
            time_label = ui.label().classes('text-sm opacity-75')
            
            def update_time():
                from datetime import datetime
                time_label.set_text(f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            
            update_time()
            ui.timer(30.0, update_time)  # Update every 30 seconds