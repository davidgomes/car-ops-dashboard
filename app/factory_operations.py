from nicegui import ui, app
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.data_generator import DataGenerator

def create():
    """Create factory operations and production insights"""
    
    def update_factory_operations():
        data_gen = DataGenerator()
        selected_factory = app.storage.user.get('selected_factory')
        
        # Production Volume by Factory
        production_data = data_gen.get_production_data(selected_factory)
        df_production = pd.DataFrame(production_data)
        
        if not df_production.empty:
            # Group by factory and sum production
            factory_production = df_production.groupby('factory_name')['cars_produced'].sum().reset_index()
            
            fig_production = go.Figure()
            fig_production.add_trace(go.Bar(
                x=factory_production['factory_name'],
                y=factory_production['cars_produced'],
                name='Cars Produced',
                marker_color='#3B82F6'
            ))
            
            fig_production.update_layout(
                title='Monthly Production by Factory',
                xaxis_title='Factory',
                yaxis_title='Cars Produced',
                height=400,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            production_chart.update_figure(fig_production)
        
        # Assembly Line Status
        assembly_lines = data_gen.assembly_lines
        if selected_factory:
            assembly_lines = [line for line in assembly_lines if line.factory_id == selected_factory]
        
        # Update assembly line table
        assembly_data = []
        for line in assembly_lines[:8]:  # Show first 8 lines
            factory_name = next(f.name for f in data_gen.factories if f.id == line.factory_id)
            efficiency = (line.output_rate / line.target_rate) * 100
            assembly_data.append({
                'factory': factory_name,
                'line': line.name,
                'status': line.status.value.title(),
                'output_rate': f"{line.output_rate} cars/hour",
                'target_rate': f"{line.target_rate} cars/hour",
                'efficiency': f"{efficiency:.1f}%"
            })
        
        assembly_table.update_rows(assembly_data)
        
        # Parts Inventory Levels
        inventory_data = data_gen.get_inventory_data(selected_factory)
        df_inventory = pd.DataFrame([{
            'part_name': item.part_name,
            'current_stock': item.current_stock,
            'target_stock': item.target_stock,
            'factory_id': item.factory_id
        } for item in inventory_data])
        
        if not df_inventory.empty:
            # Group by part name and sum stocks
            inventory_summary = df_inventory.groupby('part_name').agg({
                'current_stock': 'sum',
                'target_stock': 'sum'
            }).reset_index()
            
            fig_inventory = go.Figure()
            fig_inventory.add_trace(go.Scatter(
                x=inventory_summary['part_name'],
                y=inventory_summary['current_stock'],
                mode='lines+markers',
                name='Current Stock',
                line=dict(color='#10B981')
            ))
            fig_inventory.add_trace(go.Scatter(
                x=inventory_summary['part_name'],
                y=inventory_summary['target_stock'],
                mode='lines+markers',
                name='Target Stock',
                line=dict(color='#F59E0B', dash='dash')
            ))
            
            fig_inventory.update_layout(
                title='Parts Inventory Levels',
                xaxis_title='Part Type',
                yaxis_title='Stock Level',
                height=400,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            inventory_chart.update_figure(fig_inventory)
        
        # Quality Control Metrics
        quality_data = data_gen.get_quality_metrics(selected_factory)
        total_passed = sum(q.passed for q in quality_data)
        total_failed = sum(q.failed for q in quality_data)
        
        fig_quality = go.Figure(data=[go.Pie(
            labels=['Passed', 'Failed'],
            values=[total_passed, total_failed],
            marker_colors=['#10B981', '#EF4444']
        )])
        
        fig_quality.update_layout(
            title='Quality Control Pass/Fail Rate',
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        quality_chart.update_figure(fig_quality)
    
    with ui.row().classes('w-full gap-4 mb-6'):
        # Left column - Production chart and assembly line status
        with ui.column().classes('flex-1'):
            with ui.card().classes('mb-4'):
                with ui.card_section():
                    production_chart = ui.plotly({}).classes('w-full')
            
            with ui.card():
                with ui.card_section():
                    ui.label('Assembly Line Status').classes('text-lg font-semibold mb-4')
                    assembly_table = ui.table(
                        columns=[
                            {'name': 'factory', 'label': 'Factory', 'field': 'factory'},
                            {'name': 'line', 'label': 'Line', 'field': 'line'},
                            {'name': 'status', 'label': 'Status', 'field': 'status'},
                            {'name': 'output_rate', 'label': 'Output Rate', 'field': 'output_rate'},
                            {'name': 'target_rate', 'label': 'Target Rate', 'field': 'target_rate'},
                            {'name': 'efficiency', 'label': 'Efficiency', 'field': 'efficiency'},
                        ],
                        rows=[],
                        row_key='line'
                    ).classes('w-full')
        
        # Right column - Inventory and quality charts
        with ui.column().classes('flex-1'):
            with ui.card().classes('mb-4'):
                with ui.card_section():
                    inventory_chart = ui.plotly({}).classes('w-full')
            
            with ui.card():
                with ui.card_section():
                    quality_chart = ui.plotly({}).classes('w-full')
    
    # Initialize factory operations
    update_factory_operations()
    
    # Store update function for use by controls
    if 'update_charts' not in app.storage.user:
        app.storage.user['update_charts'] = update_factory_operations
    else:
        # Chain multiple update functions
        existing_update = app.storage.user['update_charts']
        app.storage.user['update_charts'] = lambda: (existing_update(), update_factory_operations())