from django.db import models


# модель для постов
class Post(models.Model):
    post_header = models.CharField('название поста', max_length=100)
    post_text = models.TextField('текст поста')
    post_view = models.IntegerField('количество просмотров')
    post_create_date = models.DateTimeField('дата создания поста')

    def __str__(self):
        return self.post_header

    # TODO Доделать падежи
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


# модель для комментов
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_text = models.CharField('текст комментария', max_length=300)
    comment_create_date = models.DateTimeField('дата создания коммента')

    def __str__(self):
        return self.comment_text

    # TODO Доделать падежи
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'