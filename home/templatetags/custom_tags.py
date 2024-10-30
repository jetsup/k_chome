from django import template
from django.contrib.messages.storage.base import Message

from random import randint

register = template.Library()

@register.filter(name="to_lowercase")
def to_lowercase(value: Message):
    return value.message.lower()

@register.filter(name="truncate_chars")
def truncate_chars(value: str, char_count: int):
    if len(value) > char_count:
        return value[:char_count] + "..."
    return value
