from django.db.models.functions import JSONObject
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, F
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Post, Comment

"""To show all posts"""
class PostAPIView(APIView):
    """Return information about posts on API"""
    def get(self, request) -> Response:
        post_list = Post.objects.annotate(
            latest_comment=Subquery(
                Comment.objects.filter(post_id=OuterRef('id')).order_by('-create_date').values(
                    data=JSONObject(
                        id='id', comment_text='text'
                    )
                )[:1]
            )
        )
        return Response({'posts': post_list.values()})

""" To show one post """
class DetailPostAPIView(APIView):
    """ Get id post's and return them on api """
    def get(self, request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        Post.objects.filter(id=post_id).update(view=F('view') + 1)
        comments_list = post.comment_set.order_by('id')
        return Response({
            'post': model_to_dict(post),
            'comments': list(comments_list.values())
        })
