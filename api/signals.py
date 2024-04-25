import json

from api.models import UserTodo
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django_redis import get_redis_connection


@receiver([post_save, pre_delete], sender=UserTodo)
def publish_event(instance: UserTodo, **kwargs):
    event = {
        "message": "New Todo List Updated",
        "id": instance.pk,
        "user": instance.user.email,
        "content": instance.todo,
        "updated_at": instance.updated_at.isoformat(),
    }
    connection = get_redis_connection("default")
    payload = json.dumps(event)
    connection.publish("events", payload)
