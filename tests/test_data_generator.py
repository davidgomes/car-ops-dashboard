import pytest
from app.data_generator import DataGenerator
from app.models import Factory, FactoryStatus, AssemblyLine, DelayCategory

def test_data_generator_initialization():
    """Test that DataGenerator initializes correctly"""
    data_gen = DataGenerator()
    assert len(data_gen.factories) == 10
    assert len(data_gen.assembly_lines) > 0
    assert data_gen.start_date < data_gen.end_date

def test_factory_generation():
    """Test that factories are generated with correct properties"""
    data_gen = DataGenerator()
    
    for factory in data_gen.factories:
        assert isinstance(factory, Factory)
        assert factory.id > 0
        assert factory.name
        assert factory.location
        assert -90 <= factory.latitude <= 90
        assert -180 <= factory.longitude <= 180
        assert factory.production_capacity > 0
        assert factory.current_production >= 0
        assert 0 <= factory.efficiency <= 1
        assert factory.status in [FactoryStatus.RUNNING, FactoryStatus.DELAYED, FactoryStatus.MAINTENANCE]

def test_assembly_lines_generation():
    """Test that assembly lines are generated correctly"""
    data_gen = DataGenerator()
    
    for line in data_gen.assembly_lines:
        assert isinstance(line, AssemblyLine)
        assert line.id > 0
        assert line.factory_id in [f.id for f in data_gen.factories]
        assert line.name
        assert line.output_rate > 0
        assert line.target_rate > 0
        assert line.status in [FactoryStatus.RUNNING, FactoryStatus.DELAYED, FactoryStatus.MAINTENANCE]

def test_kpi_data_generation():
    """Test that KPI data is generated correctly"""
    data_gen = DataGenerator()
    kpi_data = data_gen.get_kpi_data()
    
    assert kpi_data.total_cars_produced > 0
    assert kpi_data.total_factories == 10
    assert 0 <= kpi_data.on_time_delivery_rate <= 1
    assert kpi_data.lost_revenue >= 0
    assert 0 <= kpi_data.production_efficiency <= 1

def test_kpi_data_with_delay_multiplier():
    """Test that KPI data responds to delay multiplier"""
    data_gen = DataGenerator()
    
    kpi_normal = data_gen.get_kpi_data(delay_multiplier=1.0)
    kpi_high_delay = data_gen.get_kpi_data(delay_multiplier=2.0)
    
    assert kpi_high_delay.lost_revenue >= kpi_normal.lost_revenue
    assert kpi_high_delay.on_time_delivery_rate <= kpi_normal.on_time_delivery_rate

def test_production_data_generation():
    """Test that production data is generated correctly"""
    data_gen = DataGenerator()
    production_data = data_gen.get_production_data()
    
    assert len(production_data) > 0
    for record in production_data:
        assert 'factory_name' in record
        assert 'factory_id' in record
        assert 'date' in record
        assert 'cars_produced' in record
        assert 'target_production' in record
        assert record['cars_produced'] >= 0
        assert record['target_production'] > 0

def test_inventory_data_generation():
    """Test that inventory data is generated correctly"""
    data_gen = DataGenerator()
    inventory_data = data_gen.get_inventory_data()
    
    assert len(inventory_data) > 0
    for item in inventory_data:
        assert item.part_name
        assert item.current_stock >= 0
        assert item.target_stock > 0
        assert item.reorder_point >= 0
        assert item.factory_id in [f.id for f in data_gen.factories]

def test_quality_metrics_generation():
    """Test that quality metrics are generated correctly"""
    data_gen = DataGenerator()
    quality_metrics = data_gen.get_quality_metrics()
    
    assert len(quality_metrics) > 0
    for metric in quality_metrics:
        assert metric.factory_id in [f.id for f in data_gen.factories]
        assert metric.passed >= 0
        assert metric.failed >= 0
        assert metric.total == metric.passed + metric.failed

def test_delay_data_generation():
    """Test that delay data is generated correctly"""
    data_gen = DataGenerator()
    delay_data = data_gen.get_delay_data(days=7)
    
    assert len(delay_data) >= 0  # Could be empty if no delays
    for record in delay_data:
        assert 'date' in record
        assert 'factory_id' in record
        assert 'category' in record
        assert 'duration_hours' in record
        assert 'financial_impact' in record
        assert record['duration_hours'] > 0
        assert record['financial_impact'] >= 0

def test_financial_data_generation():
    """Test that financial data is generated correctly"""
    data_gen = DataGenerator()
    financial_data = data_gen.get_financial_data()
    
    assert len(financial_data) > 0
    for record in financial_data:
        assert 'date' in record
        assert 'revenue_lost' in record
        assert 'cost_expedited_shipping' in record
        assert 'cost_idle_labor' in record
        assert 'cost_penalties' in record
        assert all(value >= 0 for value in record.values() if isinstance(value, (int, float)))

def test_product_lines_generation():
    """Test that product lines are generated correctly"""
    data_gen = DataGenerator()
    product_lines = data_gen.get_product_lines()
    
    assert len(product_lines) > 0
    for product in product_lines:
        assert product.name
        assert product.profit_margin >= 0
        assert product.units_sold >= 0
        assert product.revenue >= 0

def test_bottleneck_data_generation():
    """Test that bottleneck data is generated correctly"""
    data_gen = DataGenerator()
    bottleneck_data = data_gen.get_bottleneck_data()
    
    assert len(bottleneck_data) > 0
    for record in bottleneck_data:
        assert 'category' in record
        assert 'incidents' in record
        assert record['incidents'] >= 0