from rest_framework import viewsets
from rest_framework import permissions
from api.v1.serializers.testimonial import TestimonialSerializer
from core.models import Testimonial


class TestimonialView(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    permission_classes = [permissions.AllowAny]