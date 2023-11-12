from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Complaints, Booking
from .serializer import ComplaintsSerializer,ComplaintListSerializer
from .signals import complaint_update_signal


class ComplaintsRegisterView(APIView):
    def post(self, request):
        user = request.data.get("user")  
        booking_id = request.data.get("booking_id")
        
        try:
            booking = Booking.objects.get(user_id=user, booking_id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found for the given user and booking_id."},status=status.HTTP_404_NOT_FOUND)
        serializer = ComplaintsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplaintsListView(ListAPIView):
    queryset = Complaints.objects.all()
    serializer_class = ComplaintListSerializer


class ComplaintStatusUpdate(APIView):
    def patch(self, request, BookingId):
        try:
            complaint = Complaints.objects.get(booking_id=BookingId)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status', None)

        if new_status is None or new_status not in dict(Complaints.ROLE_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        complaint.status = new_status
        complaint.save()
        
        serializer = ComplaintListSerializer(complaint)
        return Response(serializer.data, status=status.HTTP_200_OK)


