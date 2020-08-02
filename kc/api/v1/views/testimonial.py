from rest_framework import viewsets
from rest_framework import permissions
from kc.api.v1.serializers.testimonial import TestimonialSerializer
from kc.core.models import Testimonial


class TestimonialView(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    permission_classes = [permissions.AllowAny]