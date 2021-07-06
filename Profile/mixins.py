from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from Profile.serializer import PostWallSerializer


class EnablePartialUpdateMixin:
    """Enable partial updates

    Override partial kwargs in UpdateModelMixin class
    https://github.com/encode/django-rest-framework/blob/91916a4db14cd6a06aca13fb9a46fc667f6c0682/rest_framework/mixins.py#L64
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class DeleteReviewsMixin:
    reviewsModel = None
    postModel = None
    def post(self, request, *args, **kwargs):
        self.reviewsModel.filter(id=request.POST.get('reviews_id')).delete()
        postRaw = self.postModel.filter(id=request.POST.get('post_id'))
        s = PostWallSerializer(postRaw, many=True)
        return Response(s.data)
