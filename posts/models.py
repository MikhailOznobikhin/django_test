from django.db import models


""" Model for posts """
class Post(models.Model):
    post_header = models.CharField('название поста', max_length=100)
    post_text = models.TextField('текст поста')
    post_view = models.IntegerField('количество просмотров')
    post_create_date = models.DateTimeField('дата создания поста')

    """ To display in Russian posts in the admin panel """
    # TODO Доделать падежи
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

""" Model for comments """
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField('текст комментария', max_length=300)
    comment_create_date = models.DateTimeField('дата создания коммента')

    """ To display in Russian comments in the admin panel """
    # TODO Доделать падежи
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
