from .models import Booking
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import FeedbackSerializer,FeedbackListSerializer
from .models import Feedback
from django.db.models import Avg


class FeedbackAddingView(APIView):
    def post(self, request):
        user = request.data.get("user")  
        booking_id = request.data.get("booking")
        try:
            booking = Booking.objects.get(user_id=user, id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found for the given user and booking_id."},status=status.HTTP_404_NOT_FOUND)
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # employee = serializer.validated_data['employee']
            # employee.update_average_rating()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FeedbackListView(ListAPIView):
    serializer_class = FeedbackListSerializer

    def get_queryset(self):
        employee = self.kwargs['employee']
        return Feedback.objects.filter(employee=employee)



