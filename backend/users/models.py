from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserCreate(AbstractUser):
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Адрес электронной почты')
    username = models.CharField(max_length=150, unique=True,
                                verbose_name='Уникальный юзернейм')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    password = models.CharField(max_length=150, verbose_name='Пароль')
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUserCreate, on_delete=models.CASCADE,
        related_name='follower', verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        CustomUserCreate, on_delete=models.CASCADE,
        related_name='following', verbose_name='Автор'
    )
    created = models.DateTimeField(
        'Дата подписки', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_followers'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='prevent_self_follow'
            )
        ]
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
