from Profile.models import Reviews
from Profile.serializer import ReviewsSerializer


def getReviewsCurrentPost(post_id):
    reviews = Reviews.objects.filter(post_id=post_id)
    serializer = ReviewsSerializer(reviews, many=True)
    obj = {
        'reviews': serializer.data,
    }
    return obj