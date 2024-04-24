from rest_framework.exceptions import ValidationError
from django.test import TestCase
from api.models import CustomUser, UserTodo
from api.serializers import RegisterSerializer, TodoSerializer, UserSerializer


class UserSerializerCRUDTestCase(TestCase):
    def test_create_user(self):
        """
        Test creating a new user using UserSerializer.
        """
        data = {"email": "test@example.com", "username": "testuser"}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "test@example.com")

    def test_read_user(self):
        """
        Test reading an existing user using UserSerializer.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        serializer = UserSerializer(instance=user)
        self.assertEqual(serializer.data["email"], "test@example.com")

    def test_update_user(self):
        """
        Test updating an existing user using UserSerializer.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        data = {"email": "updated@example.com"}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.email, "updated@example.com")

    def test_delete_user(self):
        """
        Test deleting an existing user using UserSerializer.
        """
        user: CustomUser = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        serializer = UserSerializer(instance=user)  # noqa
        user.delete()
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(email="test@example.com")


class RegisterSerializerTestCase(TestCase):
    def test_register_serializer_valid(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password2": "password456",
        }
        serializer = RegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_register_serializer_email_exists(self):
        CustomUser.objects.create_user(email="test@example.com", password="password123")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123",
        }
        serializer = RegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TodoSerializerCRUDTestCase(TestCase):
    def test_create_todo(self):
        """
        Test creating a new todo using TodoSerializer.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        data = {"user": user.id, "todo": "Test Todo"}
        serializer = TodoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        todo = serializer.save()
        self.assertEqual(todo.todo, "Test Todo")

    def test_read_todo(self):
        """
        Test reading an existing todo using TodoSerializer.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        todo = UserTodo.objects.create(user=user, todo="Test Todo")
        serializer = TodoSerializer(instance=todo)
        self.assertEqual(serializer.data["todo"], "Test Todo")

    def test_update_todo(self):
        """
        Test updating an existing todo using TodoSerializer.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        todo = UserTodo.objects.create(user=user, todo="Test Todo")
        data = {"todo": "Updated Todo"}
        serializer = TodoSerializer(instance=todo, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_todo = serializer.save()
        self.assertEqual(updated_todo.todo, "Updated Todo")

    def test_delete_todo(self):
        """
        Test deleting an existing todo using TodoSerializer.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        todo = UserTodo.objects.create(user=user, todo="Test Todo")
        serializer = TodoSerializer(instance=todo)  # noqa
        todo.delete()
        with self.assertRaises(UserTodo.DoesNotExist):
            UserTodo.objects.get(todo="Test Todo")
