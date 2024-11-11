from django.db import models
from k_auth.models import HomeUsers, UserTypes

# An IoT thing that each represents a device in the system
class Thing(models.Model):
    name = models.CharField(max_length=100)
    is_digital = models.BooleanField(default=False)
    value = models.IntegerField(default=0)
    is_writable = models.BooleanField(default=False)
    # which group can change the value of this thing
    permission_to = models.ForeignKey(UserTypes, on_delete=models.CASCADE, default=1)
    belongs_to = models.ForeignKey(HomeUsers, on_delete=models.CASCADE)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Device: {self.name} Value: {self.value}"
