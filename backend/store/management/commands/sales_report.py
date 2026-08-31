"""
Management command to generate sales and revenue analytics report for Nexus Tech Store.
"""
import json
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db.models import Sum, Avg
from store.models import Order, OrderItem

class Command(BaseCommand):
    help = 'Generate sales, order volume, and revenue analytics summary.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--json',
            action='store_true',
            dest='json_output',
            help='Output report format as raw JSON',
        )

    def handle(self, *args, **options):
        total_orders = Order.objects.count()
        paid_orders = Order.objects.filter(payment_status='paid').count()
        pending_orders = Order.objects.filter(status='pending').count()
        completed_orders = Order.objects.filter(status='delivered').count()

        revenue_agg = Order.objects.filter(payment_status='paid').aggregate(
            total_rev=Sum('total_amount'),
            avg_order=Avg('total_amount')
        )
        total_revenue = revenue_agg['total_rev'] or Decimal('0.00')
        avg_order_value = revenue_agg['avg_order'] or Decimal('0.00')

        items_sold = OrderItem.objects.aggregate(total_units=Sum('quantity'))['total_units'] or 0

        report_data = {
            'total_orders': total_orders,
            'paid_orders': paid_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'total_revenue_usd': float(total_revenue),
            'average_order_value_usd': float(round(avg_order_value, 2)),
            'total_units_sold': items_sold,
        }

        if options['json_output']:
            self.stdout.write(json.dumps(report_data, indent=2))
            return

        self.stdout.write(self.style.SUCCESS('====================================='))
        self.stdout.write(self.style.SUCCESS('>>> NEXUS TECH STORE SALES REPORT <<<'))
        self.stdout.write(self.style.SUCCESS('====================================='))
        self.stdout.write(f"Total Orders:          {total_orders}")
        self.stdout.write(f"Paid Orders:           {paid_orders}")
        self.stdout.write(f"Pending Orders:        {pending_orders}")
        self.stdout.write(f"Delivered Orders:      {completed_orders}")
        self.stdout.write(f"Total Revenue:         ${total_revenue:,.2f}")
        self.stdout.write(f"Avg Order Value:       ${avg_order_value:,.2f}")
        self.stdout.write(f"Total Units Sold:      {items_sold}")
        self.stdout.write(self.style.SUCCESS('====================================='))
