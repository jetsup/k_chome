from rest_framework import serializers
from k_auth.models import HomeUsers
from thing.models import Things, Boards


class HomeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeUsers
        fields = ["id", "first_name", "last_name", "email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = HomeUsers.objects.create_user(**validated_data)
        return user
    

class BoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = [
            "id",
            "name",
            "description",
            "vid",
            "pid",
            "baudrate",
            "data_format",
            "data_headers",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        board = Boards.objects.create(**validated_data)
        return board
    
    def get_all_boards(self):
        return Boards.objects.all()


class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Things
        fields = [
            "id",
            "name",
            "is_digital",
            "value",
            "is_writable",
            "permission_to",
            "description",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "is_writable": {"read_only": True},
            "permission_to": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        thing = Things.objects.create(**validated_data)
        return thing
