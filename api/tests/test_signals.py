from django.test import TestCase
from api.models import CustomUser, UserTodo
import json
from unittest.mock import patch


class SignalTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )

    @patch("api.signals.get_redis_connection")
    def test_todo_created_updated_signal(self, mock_get_redis_connection):
        """
        Test post_save signal for todo creation and update.
        """
        # Create a UserTodo instance
        todo = UserTodo.objects.create(user=self.user, todo="Test Todo")

        # Ensure that the signal publishes the correct event to Redis
        self.assertTrue(mock_get_redis_connection.return_value.publish.called)
        published_message = mock_get_redis_connection.return_value.publish.call_args[0][
            1
        ]
        event = json.loads(published_message)

        self.assertEqual(event["message"], "New todo created successfully")
        self.assertEqual(event["id"], todo.pk)
        self.assertEqual(event["user"], self.user.email)
        self.assertEqual(event["content"], "Test Todo")

        # Update the UserTodo instance
        todo.todo = "Updated Todo"
        todo.save()

        # Ensure that the signal publishes the correct updated event to Redis
        self.assertTrue(mock_get_redis_connection.return_value.publish.called)
        published_message = mock_get_redis_connection.return_value.publish.call_args[0][
            1
        ]
        event = json.loads(published_message)

        self.assertEqual(event["message"], "Todo updated successfully")
        self.assertEqual(event["id"], todo.pk)
        self.assertEqual(event["user"], self.user.email)
        self.assertEqual(event["content"], "Updated Todo")

    @patch("api.signals.get_redis_connection")
    def test_todo_deleted_signal(self, mock_get_redis_connection):
        """
        Test pre_delete signal for todo deletion.
        """
        # Create a UserTodo instance
        todo = UserTodo.objects.create(user=self.user, todo="Test Todo")
        todo_pk = todo.pk

        # Delete the UserTodo instance
        todo.delete()

        # Ensure that the signal publishes the correct event to Redis
        self.assertTrue(mock_get_redis_connection.return_value.publish.called)
        published_message = mock_get_redis_connection.return_value.publish.call_args[0][
            1
        ]
        event = json.loads(published_message)

        self.assertEqual(event["message"], "Todo Deleted")
        self.assertEqual(event["id"], todo_pk)
        self.assertEqual(event["user"], self.user.email)
        self.assertEqual(event["content"], "Test Todo")
