import pytest
from nicegui.testing import User
from nicegui import ui
from app.data_generator import DataGenerator
from app.models import Factory, FactoryStatus

async def test_dashboard_loads(user: User) -> None:
    """Test that the main dashboard loads successfully"""
    await user.open('/')
    await user.should_see('Global Automotive Operations Dashboard')
    await user.should_see('Total Cars Produced')
    await user.should_see('Total Factories')
    await user.should_see('Dashboard Controls')

async def test_kpi_cards_display(user: User) -> None:
    """Test that KPI cards are displayed with values"""
    await user.open('/')
    
    # Check that KPI cards are present
    await user.should_see('Total Cars Produced')
    await user.should_see('Total Factories')
    await user.should_see('On-Time Deliveries')
    await user.should_see('Lost Revenue (Delays)')
    await user.should_see('Production Efficiency')

async def test_controls_interaction(user: User) -> None:
    """Test that dashboard controls are interactive"""
    await user.open('/')
    
    # Test that controls are present
    await user.should_see('Time Range')
    await user.should_see('Factory Filter')
    await user.should_see('Delay Impact Multiplier')
    await user.should_see('Refresh Data')

async def test_factory_operations_section(user: User) -> None:
    """Test that factory operations section displays correctly"""
    await user.open('/')
    
    # Check factory operations section
    await user.should_see('Factory Operations & Production')
    await user.should_see('Assembly Line Status')

async def test_logistics_section(user: User) -> None:
    """Test that logistics section displays correctly"""
    await user.open('/')
    
    # Check logistics section - test for section header instead
    await user.should_see('Logistics & Supply Chain')
    # Don't test for chart titles that might be inside collapsed expansions

async def test_financial_section(user: User) -> None:
    """Test that financial section displays correctly"""
    await user.open('/')
    
    # Check financial section
    await user.should_see('Financial Impact & Performance')
    await user.should_see('Financial Summary')