from django.db import models
from k_auth.models import UserTypes


# A board that contains a list of things
class Boards(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    vid = models.CharField(max_length=6)
    pid = models.CharField(max_length=6)
    baudrate = models.IntegerField(default=115200)
    data_format = models.CharField(max_length=100, default="")  # regular expression to parse data, CSV
    data_headers = models.CharField(
        max_length=100
    )  # the label for the stringified data, CSV
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Board: {self.name}:: VID: {self.vid} PID: {self.pid}"


# An IoT thing that each represents a device in the system
class Things(models.Model):
    name = models.CharField(max_length=100) # e.g. Kitchen Light
    is_digital = models.BooleanField(default=False)
    value = models.IntegerField(default=0)
    is_writable = models.BooleanField(default=False)
    # which group can change the value of this thing
    permission_to = models.ForeignKey(UserTypes, on_delete=models.CASCADE, default=1)
    belongs_to = models.ForeignKey(
        Boards, on_delete=models.CASCADE
    )  # board this thing is connected to
    data_index = models.IntegerField(default=0)  # index of the data in the string
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device: {self.name} Value: {self.value}"
