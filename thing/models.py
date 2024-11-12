from django.db import models
from k_auth.models import HomeUsers, UserTypes

# A board that contains a list of things
class Board(models.Model):
    name = models.CharField(max_length=100)
    vid = models.CharField(max_length=6)
    pid = models.CharField(max_length=6)
    port = models.CharField(max_length=100) # get unique id of the board
    baudrate = models.IntegerField(default=115200)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Board: {self.name}:: Port: {self.port} VID: {self.vid} PID: {self.pid}"

# An IoT thing that each represents a device in the system
class Thing(models.Model):
    name = models.CharField(max_length=100)
    is_digital = models.BooleanField(default=False)
    value = models.IntegerField(default=0)
    is_writable = models.BooleanField(default=False)
    # which group can change the value of this thing
    permission_to = models.ForeignKey(UserTypes, on_delete=models.CASCADE, default=1)
    belongs_to = models.ForeignKey(Board, on_delete=models.CASCADE) # board this thing is connected to
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Device: {self.name} Value: {self.value}"
