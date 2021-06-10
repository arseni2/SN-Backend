from django.urls import path, include

from Profile.views import userDetail, reviewsCurrentPost, CreatePostOnWall, changeStatus, changeCountry, SnippetDetail, \
    deletePost, updatePost, createReviews, DeleteReviewsView, addLikePost, deleteLike

urlpatterns = [
    path('info/', userDetail),
    path('reviews/', reviewsCurrentPost),
    path('createReviews/', createReviews),
    path('createPostOnWall/', CreatePostOnWall),
    path('changeStatus/', changeStatus),
    path('changeCountry/', changeCountry),
    path('deleteReviews/', DeleteReviewsView.as_view()),
    path('deletePost/<int:pk>', deletePost.as_view()),
    path('updatePost/<int:pk>', updatePost.as_view()),
    path('addLike/', addLikePost),
    path('delLike/<int:pk>/', deleteLike),
]