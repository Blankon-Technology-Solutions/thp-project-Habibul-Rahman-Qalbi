from django.test import TestCase
from django.utils import timezone

from api.models import CustomUser, UserTodo
from django.contrib.auth import get_user_model


class CustomUserManagerTestCase(TestCase):
    def test_create_user(self):
        """
        Test creating a new user.
        """
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """
        Test creating a new superuser.
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="admin123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("admin123"))
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)


class CustomUserCRUDTestCase(TestCase):
    def test_create_custom_user(self):
        """
        Test creating a new CustomUser instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.assertEqual(user.email, "test@example.com")

    def test_read_custom_user(self):
        """
        Test reading an existing CustomUser instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        fetched_user = CustomUser.objects.get(email="test@example.com")
        self.assertEqual(user, fetched_user)

    def test_update_custom_user(self):
        """
        Test updating an existing CustomUser instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        user.email = "updated@example.com"
        user.save()
        updated_user = CustomUser.objects.get(email="updated@example.com")
        self.assertEqual(user, updated_user)

    def test_delete_custom_user(self):
        """
        Test deleting an existing CustomUser instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        user.delete()
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(email="test@example.com")


class UserTodoCRUDTestCase(TestCase):
    def test_create_user_todo(self):
        """
        Test creating a new UserTodo instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        todo = UserTodo.objects.create(
            user=user, todo="Test Todo", deadline=timezone.now()
        )
        self.assertEqual(todo.todo, "Test Todo")

    def test_read_user_todo(self):
        """
        Test reading an existing UserTodo instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        todo = UserTodo.objects.create(
            user=user, todo="Test Todo", deadline=timezone.now()
        )
        fetched_todo = UserTodo.objects.get(todo="Test Todo")
        self.assertEqual(todo, fetched_todo)

    def test_update_user_todo(self):
        """
        Test updating an existing UserTodo instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        todo = UserTodo.objects.create(
            user=user, todo="Test Todo", deadline=timezone.now()
        )
        todo.todo = "Updated Todo"
        todo.save()
        updated_todo = UserTodo.objects.get(todo="Updated Todo")
        self.assertEqual(todo, updated_todo)

    def test_delete_user_todo(self):
        """
        Test deleting an existing UserTodo instance.
        """
        user = CustomUser.objects.create_user(
            email="test@example.com", password="password123"
        )
        todo = UserTodo.objects.create(
            user=user, todo="Test Todo", deadline=timezone.now()
        )
        todo.delete()
        with self.assertRaises(UserTodo.DoesNotExist):
            UserTodo.objects.get(todo="Test Todo")
