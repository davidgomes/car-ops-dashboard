from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class FactoryStatus(str, Enum):
    RUNNING = "running"
    DELAYED = "delayed"
    MAINTENANCE = "maintenance"

class DelayCategory(str, Enum):
    SUPPLIER_ISSUES = "supplier_issues"
    TRANSPORT_BREAKDOWN = "transport_breakdown"
    CUSTOMS = "customs"
    WEATHER = "weather"
    EQUIPMENT_FAILURE = "equipment_failure"

class Factory(BaseModel):
    id: int
    name: str
    location: str
    latitude: float
    longitude: float
    production_capacity: int
    current_production: int
    efficiency: float
    status: FactoryStatus

class AssemblyLine(BaseModel):
    id: int
    factory_id: int
    name: str
    status: FactoryStatus
    output_rate: int  # cars per hour
    target_rate: int

class InventoryItem(BaseModel):
    part_name: str
    current_stock: int
    target_stock: int
    reorder_point: int
    factory_id: int

class QualityMetric(BaseModel):
    factory_id: int
    passed: int
    failed: int
    total: int

class DelayRecord(BaseModel):
    date: datetime
    factory_id: int
    category: DelayCategory
    duration_hours: int
    financial_impact: float

class ProductionData(BaseModel):
    factory_id: int
    date: datetime
    cars_produced: int
    target_production: int

class FinancialData(BaseModel):
    date: datetime
    revenue_lost: float
    cost_expedited_shipping: float
    cost_idle_labor: float
    cost_penalties: float

class ProductLine(BaseModel):
    name: str
    profit_margin: float
    units_sold: int
    revenue: float

class KPIData(BaseModel):
    total_cars_produced: int
    total_factories: int
    on_time_delivery_rate: float
    lost_revenue: float
    production_efficiency: float