from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Things, Boards
from k_api.serializers import ThingSerializer
from django.http import HttpRequest, JsonResponse
from celery_background.tasks import listen_usb_serial_ports


# Create your views here.
class ThingListCreate(generics.ListCreateAPIView):
    queryset = Things.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Things.objects.filter(belongs_to=user)

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
        return Things.objects.filter(belongs_to=user)

    def perform_destroy(self, instance):
        instance.delete()
        return super().perform_destroy(instance)


def get_connected_boards(request: HttpRequest):
    connected_boards: dict = listen_usb_serial_ports()
    database_boards = Boards.objects.all()
    found_and_in_database = {}
    for board in database_boards:
        if f"{board.vid},{board.pid}" in connected_boards:
            found_and_in_database[f"{board.vid},{board.pid}"] = connected_boards[
                f"{board.vid},{board.pid}"
            ]
    return JsonResponse(found_and_in_database, status=200)
