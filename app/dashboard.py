from nicegui import ui
from app import header, kpi_overview, controls, factory_operations, logistics, financial

def create():
    """Create the main dashboard page"""
    
    @ui.page('/')
    def dashboard():
        # Set page title and styling
        ui.page_title('Global Automotive Operations Dashboard')
        
        # Create header
        header.create()
        
        # Main content area
        with ui.column().classes('p-6 max-w-full'):
            # KPI Overview
            kpi_overview.create()
            
            # Controls
            controls.create()
            
            # Factory Operations Section
            with ui.expansion('Factory Operations & Production', icon='factory').classes('w-full mb-4').props('default-opened'):
                factory_operations.create()
            
            # Logistics Section
            with ui.expansion('Logistics & Supply Chain', icon='local_shipping').classes('w-full mb-4').props('default-opened'):
                logistics.create()
            
            # Financial Section
            with ui.expansion('Financial Impact & Performance', icon='attach_money').classes('w-full mb-4').props('default-opened'):
                financial.create()
        
        # Add some custom CSS for better styling
        ui.add_head_html('''
            <style>
                .nicegui-content { max-width: 100% !important; }
                .q-expansion-item__content { padding: 16px !important; }
            </style>
        ''')