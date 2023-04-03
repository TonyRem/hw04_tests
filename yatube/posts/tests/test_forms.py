from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post
from http import HTTPStatus

from . import constants as const


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = const.create_test_user()
        cls.group = const.create_test_group()
        cls.post = const.create_test_post(cls.user)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_valid_form(self):
        """
        Тестирование формы создания поста.
        Проверяется, что пост не создан до отправки формы,
        форма заполняется корректно, данные сохраняются в БД и появляется
        запись в БД о новом посте.
        """
        form_data_create = {
            'text': 'Текст поста для проверки формы содания поста',
            'group': self.group.id
        }

        self.assertFalse(
            Post.objects.filter(
                text=form_data_create['text'], group=self.group).exists()
        )

        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data_create)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            Post.objects.filter(text=form_data_create['text'],
                                group=self.group).exists()
        )

    def test_edit_post_valid_form(self):
        """
        Тестирование формы редактирования поста.
        Проверяется, что поля заполнены корректно,
        изменения сохраняются в БД и измененные данные соответствуют введенным.
        """
        form_data_edit = {
            'text': 'Текст поста для проверки формы редактирования поста',
            'group': self.group.id
        }
        self.assertNotEqual(self.post.text, form_data_edit['text'])
        self.assertIsNone(self.post.group)

        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data_edit
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, form_data_edit['text'])
        self.assertEqual(self.post.group.id, form_data_edit['group'])

    def test_create_post_invalid_form(self):
        """Тестирование формы создания поста с некорректными данными."""
        form_data_create_invalid_text = {
            'text': '',
            'group': self.group.id
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data_create_invalid_text,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(
            Post.objects.filter(
                text=form_data_create_invalid_text['text'], group=self.group
            ).exists()
        )

    def test_edit_post_invalid_form(self):
        """Тестирование формы редактирования поста с некорректными данными."""
        form_data_edit_invalid_text = {
            'text': '',
            'group': self.group.id
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data_edit_invalid_text,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.text,
                            form_data_edit_invalid_text['text'])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        const.delete_test_group(cls.group)
        const.delete_test_user(cls.user)
