from django.test import TestCase
from unittest.mock import patch
from .tasks import perform_calculation
from .models import Calculation, CalculationStatus

class CalculationTaskTestCase(TestCase):

    @patch('calculator.tasks.time.sleep')  # Mock sleep to skip the delay
    def test_perform_calculation_success(self, mock_sleep):
        # Setup - create a calculation instance
        calc = Calculation.objects.create(expression="10 + 2")
        
        # Execute the task directly
        perform_calculation(calc.id)
        
        # Refresh from DB
        calc.refresh_from_db()
        
        # Asserts
        self.assertEqual(calc.status, CalculationStatus.SUCCESS)
        self.assertEqual(calc.result, "12")
        self.assertIsNotNone(calc.started_at)
        self.assertIsNotNone(calc.finished_at)

    @patch('calculator.tasks.time.sleep')
    def test_perform_calculation_bad_expression(self, mock_sleep):
        calc = Calculation.objects.create(expression="10 0 - 34 /")
        perform_calculation(calc.id)
        calc.refresh_from_db()

        self.assertEqual(calc.status, CalculationStatus.ERROR)

        print(calc.status)
        self.assertTrue("invalid syntax" in calc.result)

    @patch('calculator.tasks.time.sleep')
    def test_perform_calculation_division_by_zero(self, mock_sleep):
        calc = Calculation.objects.create(expression="1 / 0")
        perform_calculation(calc.id)
        calc.refresh_from_db()

        self.assertEqual(calc.status, CalculationStatus.ERROR)
        self.assertIn("division by zero", calc.result)

    @patch('calculator.tasks.time.sleep')
    def test_perform_calculation_complex_expression(self, mock_sleep):
        calc = Calculation.objects.create(expression="(2 + 3) * 5")
        perform_calculation(calc.id)
        calc.refresh_from_db()

        self.assertEqual(calc.status, CalculationStatus.SUCCESS)
        self.assertEqual(calc.result, "25")

    @patch('calculator.tasks.time.sleep')
    def test_perform_calculation_unsupported_operator(self, mock_sleep):
        calc = Calculation.objects.create(expression="2 ^ 3")
        perform_calculation(calc.id)
        calc.refresh_from_db()

        self.assertEqual(calc.status, CalculationStatus.ERROR)
        self.assertIn("Unsafe expression", calc.result)

    @patch('calculator.tasks.time.sleep')
    def test_perform_calculation_with_characters(self, mock_sleep):
        calc = Calculation.objects.create(expression="a + b")
        perform_calculation(calc.id)
        calc.refresh_from_db()

        self.assertEqual(calc.status, CalculationStatus.ERROR)
        self.assertIn("Unsafe expression", calc.result)


    @patch('calculator.tasks.time.sleep')
    def test_perform_calculation_malicious_input(self, mock_sleep):
        # An attempt to use Python's built-in functions to perform malicious actions
        # For example, trying to list directory contents, which should not be allowed
        malicious_expression = "__import__('os').listdir('/')"

        calc = Calculation.objects.create(expression=malicious_expression)
        perform_calculation(calc.id)
        calc.refresh_from_db()

        self.assertNotEqual(calc.status, CalculationStatus.SUCCESS)
        self.assertIn(calc.status, [CalculationStatus.ERROR])

        self.assertTrue("unsafe" in calc.result.lower())