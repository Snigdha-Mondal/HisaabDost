import unittest
from pydantic import ValidationError
from app.agent.schemas import (
    ExpenseItem,
    VendorProfile,
    CustomerCreditItem,
    GougingAlert,
    DailyAuditSummary
)

class TestFinancialSchemas(unittest.TestCase):
    def test_expense_item_valid(self):
        item = ExpenseItem(
            item="mustard oil",
            raw_name="sarson ka tel",
            quantity=2.0,
            unit="cans",
            total_cost=1900.0,
            unit_price=950.0
        )
        self.assertEqual(item.item, "mustard oil")
        self.assertEqual(item.unit_price, 950.0)

    def test_expense_item_auto_unit_price(self):
        # Omit unit_price and let validator derive it
        item = ExpenseItem(
            item="milk",
            raw_name="doodh",
            quantity=10.0,
            unit="liters",
            total_cost=600.0
        )
        self.assertEqual(item.unit_price, 60.0)

    def test_expense_item_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            ExpenseItem(
                item="milk",
                raw_name="doodh",
                quantity=0.0,  # quantity must be gt 0
                unit="liters",
                total_cost=600.0
            )

    def test_expense_item_negative_cost(self):
        with self.assertRaises(ValidationError):
            ExpenseItem(
                item="milk",
                raw_name="doodh",
                quantity=10.0,
                unit="liters",
                total_cost=-50.0  # cost must be ge 0
            )

    def test_vendor_profile(self):
        profile = VendorProfile()
        self.assertEqual(profile.vendor_id, "VEND_001")
        self.assertEqual(profile.stall_id, "STALL_004")
        self.assertEqual(profile.daily_closing_time, "20:30")
        self.assertEqual(profile.currency, "INR")

    def test_daily_audit_summary_auto_computations(self):
        milk = ExpenseItem(item="milk", raw_name="doodh", quantity=10.0, unit="liters", total_cost=600.0)
        oil = ExpenseItem(item="mustard oil", raw_name="sarson ka tel", quantity=2.0, unit="cans", total_cost=1900.0)
        veg = ExpenseItem(item="vegetables", raw_name="sabzi", quantity=1.0, unit="basket", total_cost=450.0)

        # Revenue = 4200, Total Expenses = 600 + 1900 + 450 = 2950
        # Net profit = 4200 - 2950 = 1250
        # Margin = 1250 / 4200 * 100 = 29.8%
        summary = DailyAuditSummary(
            revenue=4200.0,
            expenses=[milk, oil, veg]
        )
        self.assertEqual(summary.total_expenses, 2950.0)
        self.assertEqual(summary.net_profit, 1250.0)
        self.assertEqual(summary.profit_margin_pct, 29.8)

    def test_gouging_alert_model(self):
        alert = GougingAlert(
            item="mustard oil",
            baseline_price=850.0,
            current_price=950.0,
            pct_increase=11.7,
            extra_cost=200.0,
            warning_message="Mustard oil is 11.7% higher than baseline"
        )
        self.assertEqual(alert.extra_cost, 200.0)
        self.assertEqual(alert.pct_increase, 11.7)

    def test_customer_credit_item(self):
        credit = CustomerCreditItem(
            customer_name="Ramesh Mechanic",
            amount=110.0,
            action="add",
            days_unpaid=3,
            note="Morning chai and bun maska"
        )
        self.assertEqual(credit.amount, 110.0)
        self.assertEqual(credit.days_unpaid, 3)

if __name__ == "__main__":
    unittest.main()
