from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from django.db.models import Count

from Profile.mixins import EnablePartialUpdateMixin, DeleteReviewsMixin
from Profile.models import PostWall, Reviews, LikePost
from Profile.serializer import UserDetailSerializer, PostWallSerializer, ReviewsSerializer, createReviewsSerializer, LikeSerializerPost
from Profile.servises.views_logic import getReviewsCurrentPost

User = get_user_model()
# easy-thumbal need use for image
#photo large and small
# сделать так чтобы в reviews был массив children думаю надо добавлять массив children в queryset а не в serializer
@api_view(('GET',))
def userDetail(request):
    #like = PostWall.objects.all().annotate(likes_count=Count('like'))
    #print(like[1].likes_count)
    #likeForPost = LikeSerializerPost(like, many=True)
    #print(likeForPost.data)
    if not request.GET.get('limit'):
        posts = PostWall.objects.filter(user_id=request.user.id).annotate(likes_count=Count('like'))
    else:
        limit = int(request.GET.get('limit'))
        posts = PostWall.objects.filter(user_id=request.user.id).annotate(likes_count=Count('like'))[:limit]
    user = User.objects.filter(email=request.user)
    serializerUser = UserDetailSerializer(user, many=True)
    serializerPostaWall= PostWallSerializer(posts, many=True)
    obj = {
        'profile': serializerUser.data,
        'posts': serializerPostaWall.data,
        'success': 1,
    }
    return Response(obj)

class deletePost(APIView):
    def post(self, request, pk, format=None):
        snippet = PostWall.objects.filter(id=pk)
        snippet.delete()
        posts = PostWall.objects.filter(user=request.user).annotate(likes_count=Count('like')) #можно было глянуть и сделать как в movieapi
        serializer = PostWallSerializer(posts, many=True)
        return Response(serializer.data)#2 - delete successfuly

@api_view(('POST', ))
def addLikePost(request):
    '''
    post_id,
    likes
    '''
    user = request.user
    post_id = request.POST.get('post_id')
    s = LikeSerializerPost(data=request.data)
    if s.is_valid():
        s.save(user=user)
    currentPost = PostWall.objects.filter(id=post_id).annotate(likes_count=Count('like'))# кеширующее поля глянуть
    likeCreated = LikePost.objects.last()
    currentPost[0].like.add(likeCreated)
    s_post = PostWallSerializer(currentPost, many=True)
    return Response(s_post.data)
@api_view(('POST', ))
def deleteLike(request, pk):
    post = PostWall.objects.get(id=pk)
    post.like.filter(user=request.user).delete()
    s = PostWallSerializer(post)
    return Response(s.data)

@api_view(('GET','POST'))
def reviewsCurrentPost(request):
    """отзывы для текущего поста
    Get
    post_id -- type:int
    Post
    image?
    text -- type:str
    parent_id? -- type:int id отзыва на который надо ответить
    """
    obj = getReviewsCurrentPost(request.GET.get('post_id'))
    if request.method == 'POST':
        s = ReviewsSerializer(data=request.data)
        if s.is_valid():
            s.save(user=request.user, post_id=request.POST.get('post_id'), parent_id=request.POST.get('parent_id'))
            return Response(getReviewsCurrentPost(request.POST.get('post_id')))
        else:
            print(s.errors)
    #на клиенте можно сделать как с удалением комментария в мувике
    return Response(obj)
@api_view(('GET','POST'))
def CreatePostOnWall(request):
    global postsS
    """создвние поста на профиле
        ? - не обязательный параметр
        des - type:str
        image? -
        id_comment_parent? - type:int id коментария на который нужно ответить
    """
    if request.method == 'GET':
        # отзывы получать отдельным запросом или подгружать их после загрузки постов
        posts = PostWall.objects.filter(user=request.user)
        postsS = PostWallSerializer(posts, many=True)
        obj = {
            'posts': postsS.data,
        }
        return Response(obj)
    serializer = PostWallSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        posts = PostWall.objects.filter(user=request.user).annotate(likes_count=Count('like'))
        postsS = PostWallSerializer(posts, many=True)
        obj = {
            'posts': postsS.data,
        }
        return Response(obj)
    else:
        print(serializer.errors)
        return Response({'success': 0, 'message': ['eror']}) #status code
CreatePostOnWall = sync_to_async(CreatePostOnWall)
@api_view(('POST', ))
def changeStatus(request):
    user = User.objects.get(id=request.user.id)
    user.status = request.POST.get('statusText', '')
    user.save()
    serializer = UserDetailSerializer(user)
    obj = {
        'profile': [serializer.data]
    }
    return Response(obj)
@api_view(('POST', ))
def changeCountry(request):
    if request.POST.get('country', '').isspace():
        return Response({'success': 0, 'message': ['enter correct value country']})
    user = User.objects.get(id=request.user.id)
    user.country = request.POST.get('country', '')
    user.save()
    serializer = UserDetailSerializer(user)
    obj = {
        'profile': [serializer.data]
    }
    return Response(obj)

class SnippetDetail(APIView):
    def delete(self, request, pk, format=None):
        snippet = Reviews.objects.filter(id=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class updatePost(EnablePartialUpdateMixin, generics.RetrieveUpdateAPIView):
    queryset = PostWall.objects.all()
    serializer_class = PostWallSerializer

    def get_queryset(self):
        return PostWall.objects.filter(user=self.request.user)

@api_view(['POST', ]) #можно с комментом возвращать массив детей тоесть у каждого коммента будет массив детей и при создании сетать коммент в дети родителя
def createReviews(request):
    serializer = createReviewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
    createdComment = Reviews.objects.all().last()
    if request.POST.get('parent_id'):
        createdComment.parent_id = request.POST.get('parent_id')
        createdComment.save()
    currentPost = PostWall.objects.get(id=request.POST.get('post_id', None))
    currentPost.reviews.add(createdComment)
    s = PostWallSerializer(currentPost, many=False)
    return Response(s.data)

from rest_framework.generics import GenericAPIView
class DeleteReviewsView(DeleteReviewsMixin, GenericAPIView):
    reviewsModel = Reviews.objects
    postModel = PostWall.objects
# удаление отзыва можно ниписать миксин который будет принимать модель и юзера и айди поста и айди записи котрую нужно удалить и возвращать ысе отзывы к посту

"""
асинхронно мы не дожидаемся а синхронно мы дожыдаемся
писать как можно меньше логики во вьюхах и выносить её в папку servises.
писать тесты для более сложных вьюшек, моделей по возможности использовать сторонние либы, больше коментариев
если во вьюшке не большая логика которая тратит не много ресурсов то имеет смысл написать её асихронно
await говорит в питоне сделай это одновременно и дождись выполнения
"""
"""
на клиенте более строго типизировать данные как можно меньше писать тс игноры больше детальных тестов, больше коментариев
писать код качетсвеннее и думать как одну задачу моржно решить несколькими способами
"""
"""
смотреть в заметке ресурся длоя изучения и там смотреть интересные материалы и пилить этот проект используя лучшие практики
насчёт комментов можно при запросе получать все комменты и там смотреть на айди и парент айди и сетать в свойство чилдрен
а ппри создании коммента можно смотреть на парент айди и сетать его к детям комента с таким-же айдишником
"""