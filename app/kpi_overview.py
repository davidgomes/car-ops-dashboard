from nicegui import ui, app
from app.data_generator import DataGenerator

def create():
    """Create KPI overview cards"""
    
    def format_number(value):
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        return str(int(value))
    
    def format_currency(value):
        if value >= 1000000:
            return f"${value/1000000:.1f}M"
        elif value >= 1000:
            return f"${value/1000:.1f}K"
        return f"${value:.0f}"
    
    def format_percentage(value):
        return f"{value*100:.1f}%"
    
    def update_kpis():
        data_gen = DataGenerator()
        delay_multiplier = app.storage.user.get('delay_multiplier', 1.0)
        kpi_data = data_gen.get_kpi_data(delay_multiplier)
        
        # Update KPI values
        app.storage.user['kpi_data'] = {
            'total_cars': format_number(kpi_data.total_cars_produced),
            'total_factories': kpi_data.total_factories,
            'on_time_delivery': format_percentage(kpi_data.on_time_delivery_rate),
            'lost_revenue': format_currency(kpi_data.lost_revenue),
            'production_efficiency': format_percentage(kpi_data.production_efficiency)
        }
        
        # Update UI elements
        total_cars_label.set_text(app.storage.user['kpi_data']['total_cars'])
        total_factories_label.set_text(str(app.storage.user['kpi_data']['total_factories']))
        on_time_delivery_label.set_text(app.storage.user['kpi_data']['on_time_delivery'])
        lost_revenue_label.set_text(app.storage.user['kpi_data']['lost_revenue'])
        production_efficiency_label.set_text(app.storage.user['kpi_data']['production_efficiency'])
    
    with ui.row().classes('w-full gap-4 mb-6'):
        # Total Cars Produced
        with ui.card().classes('flex-1 bg-green-50'):
            with ui.card_section():
                ui.label('Total Cars Produced').classes('text-sm text-gray-600 mb-2')
                total_cars_label = ui.label('0').classes('text-3xl font-bold text-green-600')
                ui.label('Monthly Production').classes('text-xs text-gray-500')
        
        # Total Factories
        with ui.card().classes('flex-1 bg-blue-50'):
            with ui.card_section():
                ui.label('Total Factories').classes('text-sm text-gray-600 mb-2')
                total_factories_label = ui.label('0').classes('text-3xl font-bold text-blue-600')
                ui.label('Global Operations').classes('text-xs text-gray-500')
        
        # On-Time Deliveries
        with ui.card().classes('flex-1 bg-yellow-50'):
            with ui.card_section():
                ui.label('On-Time Deliveries').classes('text-sm text-gray-600 mb-2')
                on_time_delivery_label = ui.label('0%').classes('text-3xl font-bold text-yellow-600')
                ui.label('Delivery Performance').classes('text-xs text-gray-500')
        
        # Lost Revenue
        with ui.card().classes('flex-1 bg-red-50'):
            with ui.card_section():
                ui.label('Lost Revenue (Delays)').classes('text-sm text-gray-600 mb-2')
                lost_revenue_label = ui.label('$0').classes('text-3xl font-bold text-red-600')
                ui.label('Due to Delays').classes('text-xs text-gray-500')
        
        # Production Efficiency
        with ui.card().classes('flex-1 bg-purple-50'):
            with ui.card_section():
                ui.label('Production Efficiency').classes('text-sm text-gray-600 mb-2')
                production_efficiency_label = ui.label('0%').classes('text-3xl font-bold text-purple-600')
                ui.label('Overall Performance').classes('text-xs text-gray-500')
    
    # Initialize KPIs
    update_kpis()
    
    # Store update function for use by controls
    app.storage.user['update_kpis'] = update_kpis