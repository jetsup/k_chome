from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Thing
from k_api.serializers import ThingSerializer

# Create your views here.
class ThingListCreate(generics.ListCreateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Thing.objects.filter(belongs_to=user)
    
    def perform_create(self, serializer: ThingSerializer):
        if serializer.is_valid():
            serializer.save(belongs_to=self.request.user)
        else:
            print(f"Thing create error: {serializer.errors}")
        return super().perform_create(serializer)

class ThingDelete(generics.DestroyAPIView):
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Thing.objects.filter(belongs_to=user)
    
    def perform_destroy(self, instance):
        instance.delete()
        return super().perform_destroy(instance)
