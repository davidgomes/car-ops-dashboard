from nicegui import ui, app
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.data_generator import DataGenerator

def create():
    """Create logistics and supply chain visualization"""
    
    def update_logistics():
        data_gen = DataGenerator()
        selected_factory = app.storage.user.get('selected_factory')
        
        # Factory locations map
        factories = data_gen.factories
        if selected_factory:
            factories = [f for f in factories if f.id == selected_factory]
        
        # Create map with factory locations
        fig_map = go.Figure()
        
        # Add factory markers
        factory_names = [f.name for f in factories]
        factory_lats = [f.latitude for f in factories]
        factory_lons = [f.longitude for f in factories]
        factory_status = [f.status.value for f in factories]
        
        # Color code by status
        colors = []
        for status in factory_status:
            if status == 'running':
                colors.append('#10B981')  # Green
            elif status == 'delayed':
                colors.append('#F59E0B')  # Yellow
            else:
                colors.append('#EF4444')  # Red
        
        fig_map.add_trace(go.Scattermapbox(
            lat=factory_lats,
            lon=factory_lons,
            mode='markers',
            marker=dict(
                size=12,
                color=colors
            ),
            text=factory_names,
            hovertemplate='<b>%{text}</b><br>Status: %{customdata}<extra></extra>',
            customdata=factory_status,
            name='Factories'
        ))
        
        fig_map.update_layout(
            title='Global Factory Locations',
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=30, lon=0),
                zoom=1
            ),
            height=500,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        factory_map.update_figure(fig_map)
        
        # Parts Delay Analysis
        delay_data = data_gen.get_delay_data(30)
        df_delays = pd.DataFrame(delay_data)
        
        if not df_delays.empty:
            # Group by date and sum financial impact
            daily_delays = df_delays.groupby('date')['financial_impact'].sum().reset_index()
            
            fig_delay_trend = go.Figure()
            fig_delay_trend.add_trace(go.Scatter(
                x=daily_delays['date'],
                y=daily_delays['financial_impact'],
                mode='lines+markers',
                name='Daily Impact',
                line=dict(color='#EF4444')
            ))
            
            fig_delay_trend.update_layout(
                title='Daily Delay Impact Over Time',
                xaxis_title='Date',
                yaxis_title='Financial Impact ($)',
                height=400,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            delay_trend_chart.update_figure(fig_delay_trend)
        
        # Bottleneck Analysis
        bottleneck_data = data_gen.get_bottleneck_data()
        df_bottlenecks = pd.DataFrame(bottleneck_data)
        
        fig_bottlenecks = go.Figure()
        fig_bottlenecks.add_trace(go.Bar(
            x=df_bottlenecks['incidents'],
            y=df_bottlenecks['category'],
            orientation='h',
            marker_color='#F59E0B'
        ))
        
        fig_bottlenecks.update_layout(
            title='Most Common Delay Causes',
            xaxis_title='Number of Incidents',
            yaxis_title='Category',
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        bottleneck_chart.update_figure(fig_bottlenecks)
    
    with ui.row().classes('w-full gap-4 mb-6'):
        # Left column - Map
        with ui.column().classes('flex-1'):
            with ui.card():
                with ui.card_section():
                    factory_map = ui.plotly({}).classes('w-full')
        
        # Right column - Delay analysis
        with ui.column().classes('flex-1'):
            with ui.card().classes('mb-4'):
                with ui.card_section():
                    delay_trend_chart = ui.plotly({}).classes('w-full')
            
            with ui.card():
                with ui.card_section():
                    bottleneck_chart = ui.plotly({}).classes('w-full')
    
    # Initialize logistics
    update_logistics()
    
    # Add to update chain
    if 'update_charts' not in app.storage.user:
        app.storage.user['update_charts'] = update_logistics
    else:
        existing_update = app.storage.user['update_charts']
        app.storage.user['update_charts'] = lambda: (existing_update(), update_logistics())