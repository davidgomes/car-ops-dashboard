from nicegui import ui, app
from datetime import datetime, timedelta
from app.data_generator import DataGenerator

def create():
    """Create interactive controls for filtering and simulation"""
    
    def update_delay_multiplier(value):
        app.storage.user['delay_multiplier'] = value
        # Update KPIs when delay multiplier changes
        update_kpis = app.storage.user.get('update_kpis')
        if update_kpis:
            update_kpis()
        
        # Update charts
        update_charts = app.storage.user.get('update_charts')
        if update_charts:
            update_charts()
    
    def update_factory_filter(value):
        app.storage.user['selected_factory'] = value
        # Update charts when factory filter changes
        update_charts = app.storage.user.get('update_charts')
        if update_charts:
            update_charts()
    
    def update_time_range(start_date, end_date):
        app.storage.user['start_date'] = start_date
        app.storage.user['end_date'] = end_date
        # Update charts when time range changes
        update_charts = app.storage.user.get('update_charts')
        if update_charts:
            update_charts()
    
    with ui.card().classes('w-full mb-6'):
        with ui.card_section():
            ui.label('Dashboard Controls').classes('text-lg font-semibold mb-4')
            
            with ui.row().classes('w-full gap-6 items-end'):
                # Time Range Selector
                with ui.column().classes('flex-1'):
                    ui.label('Time Range').classes('text-sm font-medium mb-2')
                    with ui.row().classes('gap-2'):
                        start_date = ui.date(
                            value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                            on_change=lambda e: update_time_range(e.value, end_date.value)
                        ).classes('flex-1')
                        end_date = ui.date(
                            value=datetime.now().strftime('%Y-%m-%d'),
                            on_change=lambda e: update_time_range(start_date.value, e.value)
                        ).classes('flex-1')
                
                # Factory Selector
                with ui.column().classes('flex-1'):
                    ui.label('Factory Filter').classes('text-sm font-medium mb-2')
                    data_gen = DataGenerator()
                    factory_options = [{'label': 'All Factories', 'value': None}] + [
                        {'label': f.name, 'value': f.id} for f in data_gen.factories
                    ]
                    ui.select(
                        options=factory_options,
                        value=None,
                        on_change=lambda e: update_factory_filter(e.value)
                    ).classes('w-full')
                
                # Delay Impact Multiplier
                with ui.column().classes('flex-1'):
                    ui.label('Delay Impact Multiplier').classes('text-sm font-medium mb-2')
                    with ui.row().classes('items-center gap-2'):
                        multiplier_slider = ui.slider(
                            min=0.5, max=3.0, step=0.1, value=1.0,
                            on_change=lambda e: update_delay_multiplier(e.value)
                        ).classes('flex-1')
                        multiplier_label = ui.label('1.0x').classes('text-sm font-mono')
                        
                        def update_multiplier_label():
                            multiplier_label.set_text(f'{multiplier_slider.value:.1f}x')
                        
                        multiplier_slider.on('update:model-value', update_multiplier_label)
                
                # Refresh Button
                with ui.column().classes('flex-0'):
                    ui.button('Refresh Data', icon='refresh', 
                             on_click=lambda: app.storage.user.get('update_charts', lambda: None)(),
                             color='primary').classes('h-10')
    
    # Initialize default values
    app.storage.user.setdefault('delay_multiplier', 1.0)
    app.storage.user.setdefault('selected_factory', None)
    app.storage.user.setdefault('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    app.storage.user.setdefault('end_date', datetime.now().strftime('%Y-%m-%d'))