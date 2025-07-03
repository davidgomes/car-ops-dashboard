import pytest
from app.models import (
    Factory, AssemblyLine, InventoryItem, QualityMetric, DelayRecord,
    ProductionData, FinancialData, ProductLine, KPIData,
    FactoryStatus, DelayCategory
)
from datetime import datetime

def test_factory_model():
    """Test Factory model validation"""
    factory = Factory(
        id=1,
        name="Test Factory",
        location="Test Location",
        latitude=40.7128,
        longitude=-74.0060,
        production_capacity=1000,
        current_production=800,
        efficiency=0.85,
        status=FactoryStatus.RUNNING
    )
    
    assert factory.id == 1
    assert factory.name == "Test Factory"
    assert factory.efficiency == 0.85
    assert factory.status == FactoryStatus.RUNNING

def test_assembly_line_model():
    """Test AssemblyLine model validation"""
    line = AssemblyLine(
        id=1,
        factory_id=1,
        name="Line A",
        status=FactoryStatus.RUNNING,
        output_rate=25,
        target_rate=30
    )
    
    assert line.id == 1
    assert line.factory_id == 1
    assert line.name == "Line A"
    assert line.output_rate == 25
    assert line.target_rate == 30

def test_inventory_item_model():
    """Test InventoryItem model validation"""
    item = InventoryItem(
        part_name="Engine",
        current_stock=500,
        target_stock=800,
        reorder_point=200,
        factory_id=1
    )
    
    assert item.part_name == "Engine"
    assert item.current_stock == 500
    assert item.target_stock == 800
    assert item.reorder_point == 200
    assert item.factory_id == 1

def test_quality_metric_model():
    """Test QualityMetric model validation"""
    metric = QualityMetric(
        factory_id=1,
        passed=950,
        failed=50,
        total=1000
    )
    
    assert metric.factory_id == 1
    assert metric.passed == 950
    assert metric.failed == 50
    assert metric.total == 1000

def test_kpi_data_model():
    """Test KPIData model validation"""
    kpi = KPIData(
        total_cars_produced=1500000,
        total_factories=10,
        on_time_delivery_rate=0.95,
        lost_revenue=15000000.0,
        production_efficiency=0.88
    )
    
    assert kpi.total_cars_produced == 1500000
    assert kpi.total_factories == 10
    assert kpi.on_time_delivery_rate == 0.95
    assert kpi.lost_revenue == 15000000.0
    assert kpi.production_efficiency == 0.88

def test_delay_record_model():
    """Test DelayRecord model validation"""
    delay = DelayRecord(
        date=datetime.now(),
        factory_id=1,
        category=DelayCategory.SUPPLIER_ISSUES,
        duration_hours=4,
        financial_impact=50000.0
    )
    
    assert delay.factory_id == 1
    assert delay.category == DelayCategory.SUPPLIER_ISSUES
    assert delay.duration_hours == 4
    assert delay.financial_impact == 50000.0

def test_product_line_model():
    """Test ProductLine model validation"""
    product = ProductLine(
        name="Sedan",
        profit_margin=0.15,
        units_sold=450000,
        revenue=13500000000.0
    )
    
    assert product.name == "Sedan"
    assert product.profit_margin == 0.15
    assert product.units_sold == 450000
    assert product.revenue == 13500000000.0

def test_factory_status_enum():
    """Test FactoryStatus enum values"""
    assert FactoryStatus.RUNNING == "running"
    assert FactoryStatus.DELAYED == "delayed"
    assert FactoryStatus.MAINTENANCE == "maintenance"

def test_delay_category_enum():
    """Test DelayCategory enum values"""
    assert DelayCategory.SUPPLIER_ISSUES == "supplier_issues"
    assert DelayCategory.TRANSPORT_BREAKDOWN == "transport_breakdown"
    assert DelayCategory.CUSTOMS == "customs"
    assert DelayCategory.WEATHER == "weather"
    assert DelayCategory.EQUIPMENT_FAILURE == "equipment_failure"