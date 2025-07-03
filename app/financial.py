from nicegui import ui, app
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.data_generator import DataGenerator

def create():
    """Create financial impact and performance visualization"""
    
    def update_financial():
        data_gen = DataGenerator()
        delay_multiplier = app.storage.user.get('delay_multiplier', 1.0)
        
        # Lost Revenue Over Time
        financial_data = data_gen.get_financial_data(delay_multiplier)
        df_financial = pd.DataFrame(financial_data)
        
        if not df_financial.empty:
            fig_revenue = go.Figure()
            fig_revenue.add_trace(go.Scatter(
                x=df_financial['date'],
                y=df_financial['revenue_lost'],
                mode='lines+markers',
                name='Lost Revenue',
                line=dict(color='#EF4444'),
                fill='tonexty'
            ))
            
            fig_revenue.update_layout(
                title='Lost Revenue Due to Delays Over Time',
                xaxis_title='Date',
                yaxis_title='Lost Revenue ($)',
                height=400,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            revenue_chart.update_figure(fig_revenue)
            
            # Cost Breakdown
            cost_categories = ['Expedited Shipping', 'Idle Labor', 'Penalties']
            cost_values = [
                df_financial['cost_expedited_shipping'].sum(),
                df_financial['cost_idle_labor'].sum(),
                df_financial['cost_penalties'].sum()
            ]
            
            fig_costs = go.Figure()
            fig_costs.add_trace(go.Bar(
                x=cost_categories,
                y=cost_values,
                marker_color=['#3B82F6', '#F59E0B', '#EF4444']
            ))
            
            fig_costs.update_layout(
                title='Cost Breakdown by Category (Monthly)',
                xaxis_title='Cost Category',
                yaxis_title='Cost ($)',
                height=400,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            cost_chart.update_figure(fig_costs)
        else:
            cost_values = [0, 0, 0]
        
        # Profit Margin by Product Line
        product_lines = data_gen.get_product_lines()
        df_products = pd.DataFrame([{
            'name': p.name,
            'profit_margin': p.profit_margin * 100,
            'revenue': p.revenue / 1000000  # Convert to millions
        } for p in product_lines])
        
        fig_profit = go.Figure()
        fig_profit.add_trace(go.Bar(
            x=df_products['name'],
            y=df_products['profit_margin'],
            marker_color='#10B981'
        ))
        
        fig_profit.update_layout(
            title='Profit Margin by Product Line',
            xaxis_title='Product Line',
            yaxis_title='Profit Margin (%)',
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        profit_chart.update_figure(fig_profit)
        
        # Financial Summary Table
        total_revenue = sum(p.revenue for p in product_lines)
        total_lost = df_financial['revenue_lost'].sum() if not df_financial.empty else 0
        total_costs = sum(cost_values)
        
        summary_data = [
            {'metric': 'Total Revenue', 'value': f"${total_revenue/1000000:.1f}M"},
            {'metric': 'Lost Revenue', 'value': f"${total_lost/1000000:.1f}M"},
            {'metric': 'Total Delay Costs', 'value': f"${total_costs/1000000:.1f}M"},
            {'metric': 'Net Impact', 'value': f"${(total_lost + total_costs)/1000000:.1f}M"},
        ]
        
        summary_table.update_rows(summary_data)
    
    with ui.row().classes('w-full gap-4 mb-6'):
        # Left column - Revenue and costs
        with ui.column().classes('flex-1'):
            with ui.card().classes('mb-4'):
                with ui.card_section():
                    revenue_chart = ui.plotly({}).classes('w-full')
            
            with ui.card():
                with ui.card_section():
                    cost_chart = ui.plotly({}).classes('w-full')
        
        # Right column - Profit margins and summary
        with ui.column().classes('flex-1'):
            with ui.card().classes('mb-4'):
                with ui.card_section():
                    profit_chart = ui.plotly({}).classes('w-full')
            
            with ui.card():
                with ui.card_section():
                    ui.label('Financial Summary').classes('text-lg font-semibold mb-4')
                    summary_table = ui.table(
                        columns=[
                            {'name': 'metric', 'label': 'Metric', 'field': 'metric'},
                            {'name': 'value', 'label': 'Value', 'field': 'value'},
                        ],
                        rows=[],
                        row_key='metric'
                    ).classes('w-full')
    
    # Initialize financial
    update_financial()
    
    # Add to update chain
    if 'update_charts' not in app.storage.user:
        app.storage.user['update_charts'] = update_financial
    else:
        existing_update = app.storage.user['update_charts']
        app.storage.user['update_charts'] = lambda: (existing_update(), update_financial())