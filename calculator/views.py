from rest_framework import generics
from .models import Calculation
from .serializers import CalculationSerializer
from .tasks import perform_calculation  # Make sure to import your task

class CalculationListCreate(generics.ListCreateAPIView):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()  # Save the instance first to get an ID
        print(instance.id)
        perform_calculation.delay(instance.id)  # Use .delay() to run the task asynchronously

# Single calculation view
class CalculationDetail(generics.RetrieveAPIView):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer
