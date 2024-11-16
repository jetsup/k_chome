from django import template
from django.contrib.messages.storage.base import Message
from k_auth.models import HomeUsers
from thing.models import Boards

register = template.Library()
DEFAULT_PROFILE_IMAGE_PATH = "/static/images/web-assets/profile-icon.png"


@register.filter(name="to_lowercase")
def to_lowercase(value: Message):
    return value.message.lower()


@register.filter(name="truncate_chars")
def truncate_chars(value: str, char_count: int):
    if len(value) > char_count:
        return value[:char_count] + "..."
    return value


@register.filter(name="get_profile_image")
def get_profile_image(user: HomeUsers):
    if user.dp:
        return user.dp.url
    return DEFAULT_PROFILE_IMAGE_PATH


@register.filter(name="get_board_attribute")
def get_board_attribute(data: dict, key: str):
    board: Boards = data.get("board")
    if key == "port":
        return data.get(key, "N/A")
    if key == "online":
        return data.get(key, False)
    if key == "name":
        return board.name
    if key == "description":
        return board.description
    if key == "baudrate":
        return board.baudrate
