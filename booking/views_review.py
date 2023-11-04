from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializer import ReviewRatingSerializer,ReviewListingSerializer
from .models import Booking,ReviewRating


class AddReview(APIView):
    def post(self, request):
        serializer = ReviewRatingSerializer(data=request.data)
        if serializer.is_valid():
            
            user = serializer.validated_data['user']
            product = serializer.validated_data['product']
            if Booking.objects.filter(user=user, booked_product=product, status='completed').exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": "You can only review products you've booked and completed the service."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListReviewsForProduct(ListAPIView):
    serializer_class = ReviewListingSerializer

    def get_queryset(self):
        product_id = self.kwargs['productId'] 
        return ReviewRating.objects.filter(product=product_id)


class ReviewListForAdmin(ListAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewListingSerializer

class ReviewDeleteForAdmin(DestroyAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewListingSerializer
    