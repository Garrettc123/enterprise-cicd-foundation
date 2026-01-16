"""Custom Prometheus Metrics Exporter.

Exposes custom business and application metrics.
"""

from prometheus_client import start_http_server, Gauge, Counter, Histogram, Info
import time
import random
from typing import Dict, Any


class EnterpriseMetricsExporter:
    """Export custom enterprise metrics to Prometheus."""
    
    def __init__(self, port: int = 9100):
        self.port = port
        
        # Service metrics
        self.service_health = Gauge(
            'service_health_status',
            'Service health status (1=healthy, 0=unhealthy)',
            ['service_name']
        )
        
        self.service_uptime = Gauge(
            'service_uptime_percentage',
            'Service uptime percentage',
            ['service_name']
        )
        
        self.service_response_time = Gauge(
            'service_response_time_ms',
            'Service response time in milliseconds',
            ['service_name']
        )
        
        # Pilot program metrics
        self.pilot_customers_total = Gauge(
            'pilot_customers_total',
            'Total number of pilot customers'
        )
        
        self.pilot_customer_health_score = Gauge(
            'pilot_customer_health_score',
            'Customer health score',
            ['customer_id', 'company_name', 'phase']
        )
        
        self.pilot_arr_potential = Gauge(
            'pilot_arr_potential_dollars',
            'ARR potential in dollars',
            ['customer_id']
        )
        
        # Bond metrics
        self.bond_portfolio_value = Gauge(
            'bond_portfolio_value_dollars',
            'Total bond portfolio value'
        )
        
        self.bond_current_value = Gauge(
            'bond_current_value',
            'Current bond value',
            ['bond_id', 'asset_id']
        )
        
        self.bond_days_to_maturity = Gauge(
            'bond_days_to_maturity',
            'Days until bond maturity',
            ['bond_id']
        )
        
        # Business metrics
        self.monthly_recurring_revenue = Gauge(
            'monthly_recurring_revenue_dollars',
            'Monthly recurring revenue in dollars'
        )
        
        self.daily_active_users = Gauge(
            'daily_active_users',
            'Number of daily active users'
        )
        
        self.api_calls_total = Counter(
            'api_calls_total',
            'Total API calls',
            ['service', 'endpoint', 'method']
        )
        
        # Performance metrics
        self.request_duration = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['service', 'endpoint', 'method'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
        )
    
    def update_service_metrics(self, services: Dict[str, Any]) -> None:
        """Update service metrics.
        
        Args:
            services: Dictionary of service metrics
        """
        for service_name, metrics in services.items():
            self.service_health.labels(service_name=service_name).set(
                1 if metrics['status'] == 'healthy' else 0
            )
            self.service_uptime.labels(service_name=service_name).set(
                metrics['uptime_percentage']
            )
            self.service_response_time.labels(service_name=service_name).set(
                metrics['response_time_ms']
            )
    
    def update_pilot_metrics(self, customers: Dict[str, Any]) -> None:
        """Update pilot program metrics.
        
        Args:
            customers: Dictionary of customer data
        """
        self.pilot_customers_total.set(len(customers))
        
        for customer_id, customer in customers.items():
            self.pilot_customer_health_score.labels(
                customer_id=customer_id,
                company_name=customer['company_name'],
                phase=customer['phase']
            ).set(customer['health_score'])
            
            self.pilot_arr_potential.labels(
                customer_id=customer_id
            ).set(customer['arr_potential'])
    
    def update_bond_metrics(self, bonds: Dict[str, Any]) -> None:
        """Update bond portfolio metrics.
        
        Args:
            bonds: Dictionary of bond data
        """
        total_value = sum(bond['current_value'] for bond in bonds.values())
        self.bond_portfolio_value.set(total_value)
        
        for bond_id, bond in bonds.items():
            self.bond_current_value.labels(
                bond_id=bond_id,
                asset_id=bond['asset_id']
            ).set(bond['current_value'])
            
            self.bond_days_to_maturity.labels(
                bond_id=bond_id
            ).set(bond['days_to_maturity'])
    
    def simulate_metrics(self) -> None:
        """Simulate metrics for demo purposes."""
        # Simulate service metrics
        services = {
            'ai-agent-platform': {'status': 'healthy', 'uptime_percentage': 99.97, 'response_time_ms': 125.5},
            'ai-ops-studio': {'status': 'healthy', 'uptime_percentage': 99.99, 'response_time_ms': 89.3},
            'nwu-data-monetization': {'status': 'healthy', 'uptime_percentage': 100.0, 'response_time_ms': 95.7},
        }
        self.update_service_metrics(services)
        
        # Simulate pilot customers
        customers = {
            'ALPHA-001': {
                'company_name': 'FinanceFlow',
                'phase': 'integration',
                'health_score': 92.0,
                'arr_potential': 500000
            },
            'ALPHA-002': {
                'company_name': 'MedTech',
                'phase': 'testing',
                'health_score': 88.0,
                'arr_potential': 750000
            }
        }
        self.update_pilot_metrics(customers)
        
        # Simulate bonds
        bonds = {
            'BOND-001': {
                'asset_id': 'ENT-DATA-001',
                'current_value': 252000,
                'days_to_maturity': 175
            }
        }
        self.update_bond_metrics(bonds)
        
        # Business metrics
        self.monthly_recurring_revenue.set(50000 + random.randint(-5000, 5000))
        self.daily_active_users.set(1200 + random.randint(-100, 100))
    
    def start(self) -> None:
        """Start metrics server."""
        start_http_server(self.port)
        print(f"Metrics server started on port {self.port}")
        
        # Continuously update metrics
        while True:
            self.simulate_metrics()
            time.sleep(15)  # Update every 15 seconds


if __name__ == "__main__":
    exporter = EnterpriseMetricsExporter()
    print("Starting Enterprise Metrics Exporter...")
    exporter.start()
