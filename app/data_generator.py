import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.models import (
    Factory, AssemblyLine, InventoryItem, QualityMetric, DelayRecord,
    ProductionData, FinancialData, ProductLine, KPIData,
    FactoryStatus, DelayCategory
)

class DataGenerator:
    def __init__(self):
        self.factories = self._generate_factories()
        self.assembly_lines = self._generate_assembly_lines()
        self.start_date = datetime.now() - timedelta(days=30)
        self.end_date = datetime.now()
        
    def _generate_factories(self) -> List[Factory]:
        factory_data = [
            {"name": "Detroit Assembly", "location": "Detroit, MI", "lat": 42.3314, "lng": -83.0458},
            {"name": "Munich Production", "location": "Munich, Germany", "lat": 48.1351, "lng": 11.5820},
            {"name": "Tokyo Manufacturing", "location": "Tokyo, Japan", "lat": 35.6762, "lng": 139.6503},
            {"name": "São Paulo Plant", "location": "São Paulo, Brazil", "lat": -23.5505, "lng": -46.6333},
            {"name": "Shanghai Factory", "location": "Shanghai, China", "lat": 31.2304, "lng": 121.4737},
            {"name": "Mumbai Assembly", "location": "Mumbai, India", "lat": 19.0760, "lng": 72.8777},
            {"name": "Mexico City Plant", "location": "Mexico City, Mexico", "lat": 19.4326, "lng": -99.1332},
            {"name": "Seoul Production", "location": "Seoul, South Korea", "lat": 37.5665, "lng": 126.9780},
            {"name": "Birmingham Factory", "location": "Birmingham, UK", "lat": 52.4862, "lng": -1.8904},
            {"name": "Barcelona Assembly", "location": "Barcelona, Spain", "lat": 41.3851, "lng": 2.1734},
        ]
        
        factories = []
        for i, data in enumerate(factory_data):
            capacity = random.randint(800, 1500)
            current = int(capacity * random.uniform(0.7, 0.95))
            factories.append(Factory(
                id=i+1,
                name=data["name"],
                location=data["location"],
                latitude=data["lat"],
                longitude=data["lng"],
                production_capacity=capacity,
                current_production=current,
                efficiency=random.uniform(0.82, 0.95),
                status=random.choices([FactoryStatus.RUNNING, FactoryStatus.DELAYED, FactoryStatus.MAINTENANCE], 
                                    weights=[0.8, 0.15, 0.05])[0]
            ))
        return factories
    
    def _generate_assembly_lines(self) -> List[AssemblyLine]:
        lines = []
        line_id = 1
        for factory in self.factories:
            num_lines = random.randint(2, 4)
            for i in range(num_lines):
                target = random.randint(15, 30)
                current = int(target * random.uniform(0.8, 1.0))
                lines.append(AssemblyLine(
                    id=line_id,
                    factory_id=factory.id,
                    name=f"Line {chr(65+i)}",
                    status=random.choices([FactoryStatus.RUNNING, FactoryStatus.DELAYED, FactoryStatus.MAINTENANCE], 
                                        weights=[0.85, 0.12, 0.03])[0],
                    output_rate=current,
                    target_rate=target
                ))
                line_id += 1
        return lines
    
    def get_kpi_data(self, delay_multiplier: float = 1.0) -> KPIData:
        total_cars = sum(f.current_production for f in self.factories) * 30  # Monthly production
        on_time_rate = max(0.7, 0.95 - (delay_multiplier - 1.0) * 0.2)
        lost_revenue = 15000000 * delay_multiplier
        avg_efficiency = sum(f.efficiency for f in self.factories) / len(self.factories)
        
        return KPIData(
            total_cars_produced=int(total_cars),
            total_factories=len(self.factories),
            on_time_delivery_rate=on_time_rate,
            lost_revenue=lost_revenue,
            production_efficiency=avg_efficiency
        )
    
    def get_production_data(self, factory_id: Optional[int] = None) -> List[Dict]:
        data = []
        factories = [f for f in self.factories if f.id == factory_id] if factory_id else self.factories
        
        for factory in factories:
            daily_production = factory.current_production
            variation = daily_production * 0.2
            for i in range(30):
                date = self.start_date + timedelta(days=i)
                produced = max(0, int(daily_production + random.uniform(-variation, variation)))
                data.append({
                    'factory_name': factory.name,
                    'factory_id': factory.id,
                    'date': date,
                    'cars_produced': produced,
                    'target_production': factory.production_capacity
                })
        return data
    
    def get_inventory_data(self, factory_id: Optional[int] = None) -> List[InventoryItem]:
        parts = ["Engines", "Transmissions", "Chassis", "Electronics", "Tires", "Batteries"]
        inventory = []
        factories = [f for f in self.factories if f.id == factory_id] if factory_id else self.factories
        
        for factory in factories:
            for part in parts:
                target = random.randint(500, 1500)
                current = int(target * random.uniform(0.6, 1.2))
                inventory.append(InventoryItem(
                    part_name=part,
                    current_stock=current,
                    target_stock=target,
                    reorder_point=int(target * 0.3),
                    factory_id=factory.id
                ))
        return inventory
    
    def get_quality_metrics(self, factory_id: Optional[int] = None) -> List[QualityMetric]:
        metrics = []
        factories = [f for f in self.factories if f.id == factory_id] if factory_id else self.factories
        
        for factory in factories:
            total_checks = random.randint(800, 1200)
            pass_rate = random.uniform(0.92, 0.98)
            passed = int(total_checks * pass_rate)
            failed = total_checks - passed
            
            metrics.append(QualityMetric(
                factory_id=factory.id,
                passed=passed,
                failed=failed,
                total=total_checks
            ))
        return metrics
    
    def get_delay_data(self, days: int = 30) -> List[Dict]:
        data = []
        categories = list(DelayCategory)
        
        for i in range(days):
            date = self.start_date + timedelta(days=i)
            # Generate 0-5 delays per day
            num_delays = random.randint(0, 5)
            
            for _ in range(num_delays):
                factory = random.choice(self.factories)
                category = random.choice(categories)
                duration = random.randint(1, 24)  # hours
                impact = duration * random.uniform(50000, 200000)  # cost per hour
                
                data.append({
                    'date': date,
                    'factory_id': factory.id,
                    'factory_name': factory.name,
                    'category': category.value,
                    'duration_hours': duration,
                    'financial_impact': impact
                })
        return data
    
    def get_financial_data(self, delay_multiplier: float = 1.0) -> List[Dict]:
        data = []
        base_lost_revenue = 500000
        
        for i in range(30):
            date = self.start_date + timedelta(days=i)
            daily_lost = base_lost_revenue * delay_multiplier * random.uniform(0.8, 1.2)
            
            data.append({
                'date': date,
                'revenue_lost': daily_lost,
                'cost_expedited_shipping': daily_lost * 0.3,
                'cost_idle_labor': daily_lost * 0.4,
                'cost_penalties': daily_lost * 0.3
            })
        return data
    
    def get_product_lines(self) -> List[ProductLine]:
        products = [
            {"name": "Sedan", "profit_margin": 0.15, "units_sold": 450000, "revenue": 13500000000},
            {"name": "SUV", "profit_margin": 0.22, "units_sold": 380000, "revenue": 19000000000},
            {"name": "Truck", "profit_margin": 0.18, "units_sold": 280000, "revenue": 14000000000},
            {"name": "Electric", "profit_margin": 0.12, "units_sold": 120000, "revenue": 6000000000},
            {"name": "Hybrid", "profit_margin": 0.16, "units_sold": 200000, "revenue": 8000000000},
        ]
        
        return [ProductLine(**product) for product in products]
    
    def get_bottleneck_data(self) -> List[Dict]:
        categories = {
            "Supplier Issues": random.randint(25, 35),
            "Transport Breakdown": random.randint(15, 25),
            "Customs Delays": random.randint(10, 20),
            "Weather": random.randint(5, 15),
            "Equipment Failure": random.randint(20, 30)
        }
        
        return [{"category": k, "incidents": v} for k, v in categories.items()]