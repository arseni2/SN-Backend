from rest_framework import generics
from django.contrib.auth import get_user_model

from users.serializers import getUsersSerializer
from users.servises.pagination.pagination_classes import StandardResultsSetPagination

User = get_user_model()
#from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Q

#написать тесты и делать фронтенд + смотреть django school
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = getUsersSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_params = self.request.GET.get('search', '')
        return User.objects.filter(Q(full_name__icontains=search_params) | Q(first_name__icontains=search_params))  #User.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')