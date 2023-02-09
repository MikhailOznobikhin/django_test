from django.http import Http404
from .models import Post, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery
from django.forms.models import model_to_dict


class PostAPIView(APIView):
    # TODO сделать красивее
    def get(self, request):
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



class DetailPostAPIView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            raise Http404('Поста не существует!')

        comments_list = post.comment_set.order_by('id')
        # TODO доделать счётчик
        post.post_view = post.post_view + 1
        post.save()
        return Response({
            'post': model_to_dict(post),
            'comments': list(comments_list.values())
        })
