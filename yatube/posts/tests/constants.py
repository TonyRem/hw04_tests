"""
Модуль содержит вспомогательные функции для тестирования приложения Yatube.
"""

from django.contrib.auth import get_user_model
from django.db.models import Model
from ..models import Group, Post
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


def create_test_image():
    with open('posts/tests/test_image.jpg', 'rb') as f:
        image_data = f.read()
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_data,
            content_type='image/jpeg'
        )
    return image


def create_test_user(username: str = 'NoName') -> User:
    """Создает тестового пользователя."""
    return User.objects.create(username=username)


def create_test_group(title: str = 'Тестовая группа',
                      slug: str = 'Test-slug') -> Group:
    """Создает тестовую группу."""
    return Group.objects.create(
        title=title,
        slug=slug,
        description='Тестовое описание',
    )


def create_test_post(user: User, group: Group = None, image=None) -> Post:
    """Создает тестовый пост от заданного пользователя в указанной группе."""
    return Post.objects.create(
        author=user,
        text='Тестовый пост, больше 15 символов',
        group=group,
        image=image
    )


def delete_test_group(group: Model) -> None:
    """Удаляет тестовую группу."""
    group.delete()


def delete_test_user(user: Model) -> None:
    """Удаляет тестового пользователя."""
    user.delete()
