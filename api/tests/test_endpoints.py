from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import UserTodo

User = get_user_model()


class EndpointCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.user_todo = UserTodo.objects.create(user=self.user, todo="Test Todo")

    def test_user_create(self):
        url = reverse("api:user-list")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_todo_create(self):
        url = reverse("api:todo-list")
        data = {"user": self.user.id, "todo": "New Todo"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_retrieve(self):
        url = reverse("api:user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_retrieve(self):
        url = reverse("api:todo-detail", args=[self.user_todo.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        url = reverse("api:user-detail", args=[self.user.id])
        data = {"first_name": "firstname"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_update(self):
        url = reverse("api:todo-detail", args=[self.user_todo.id])
        data = {"todo": "Updated Todo"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        url = reverse("api:user-detail", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_todo_delete(self):
        url = reverse("api:todo-detail", args=[self.user_todo.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
