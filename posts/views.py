from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, F
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Post, Comment

"""To show all posts"""
class PostAPIView(APIView):
    # TODO сделать красивее
    """Return information about posts on API"""
    @staticmethod
    def get(request) -> Response:
        post_list = Post.objects.annotate(
            latest_comment_text=Subquery(
                Comment.objects.filter(post_id=OuterRef('id')
                ).values('comment_text').order_by('-comment_create_date')[:1]
            ) # этим вообще не горжусь, но как сплитить не придумал
        ).annotate(
            latest_comment_id=Subquery(
                Comment.objects.filter(post_id=OuterRef('id')
                ).values('id').order_by('-comment_create_date')[:1]
            )
        )
        return Response({'posts': list(post_list.values())})

""" To show one post """
class DetailPostAPIView(APIView):
    """ Get id post's and return them on api """
    @staticmethod
    def get(request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        Post.objects.filter(id=post_id).update(post_view=F('post_view') + 1)
        comments_list = post.comment_set.order_by('id')
        return Response({
            'post': model_to_dict(post),
            'comments': list(comments_list.values())
        })
