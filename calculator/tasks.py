import time
from .models import Calculation, CalculationStatus
from celery import shared_task
from django.utils import timezone
import re
from simpleeval import SimpleEval, NameNotDefined

def is_safe_expression(expression):
    # A basic check to ensure the expression only contains numbers and math operators
    return re.match(r'^[\d\+\-\*/\(\)\s]+$', expression) is not None

@shared_task
def perform_calculation(calculation_id):
    calculation = Calculation.objects.get(id=calculation_id)
    calculation.status = CalculationStatus.PROCESSING
    calculation.started_at = timezone.now()
    calculation.save()

    time.sleep(5)  # Delay for testing
    
    try:
        if not is_safe_expression(calculation.expression):
            raise ValueError("Unsafe expression")

        evaluator = SimpleEval()
        result = evaluator.eval(calculation.expression)
        
        calculation.result = str(result)
        calculation.status = CalculationStatus.SUCCESS
    except (ValueError, NameNotDefined, Exception) as e:
        calculation.status = CalculationStatus.ERROR
        calculation.result = str(e)
    finally:
        calculation.finished_at = timezone.now()
        calculation.save()
