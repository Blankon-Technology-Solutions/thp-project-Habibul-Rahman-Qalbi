import json

from api.models import UserTodo
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from django_redis import get_redis_connection


@receiver(post_save, sender=UserTodo)
def todo_created_updated(instance: UserTodo, created, **kwargs):
    message = (
        "New todo created successfully" if created else "Todo updated successfully"
    )
    event = {
        "message": message,
        "id": instance.pk,
        "user": instance.user.email,
        "content": instance.todo,
        "updated_at": instance.updated_at.isoformat(),
    }
    connection = get_redis_connection("default")
    payload = json.dumps(event)
    connection.publish("events", payload)


@receiver(post_delete, sender=UserTodo)
def todo_deleted(instance: UserTodo, **kwargs):
    event = {
        "message": "Todo Deleted",
        "id": instance.pk,
        "user": instance.user.email,
        "content": instance.todo,
        "deleted_at": now().isoformat(),
    }
    connection = get_redis_connection("default")
    payload = json.dumps(event)
    connection.publish("events", payload)
