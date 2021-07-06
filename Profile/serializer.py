from rest_framework import serializers
from django.contrib.auth import get_user_model
from Profile.models import PostWall, Reviews, LikePost
from rest_flex_fields import FlexFieldsModelSerializer

User = get_user_model()

class UserSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name')

class ReviewsParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('text', 'image')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude= ('password', 'last_login')

class ReviewsSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(required=False)
    post_id = serializers.ReadOnlyField(source='post.id', read_only=True)
    parent_id = serializers.ReadOnlyField(source='parent.id', read_only=True)
    class Meta:
        model = Reviews
        fields = ('user', 'text', 'post_id', 'image', 'id', 'parent_id')
    def create(self, validated_data):
        album = Reviews.objects.create(
            user = validated_data.get('user', None),
            text = validated_data.get('text', None),
            image = validated_data.get('image', None),
            post_id = validated_data.get('post_id', None),
            parent_id = validated_data.get('parent_id', None),
        )
        return album

class createReviewsSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(required=False)
    class Meta:
        model = Reviews
        fields = ('user', 'parent', 'text', 'image')

        def create(self, validated_data):
            album = Reviews.objects.create(
                user=validated_data.get('user', None),
                parent=validated_data.get('parent', None),
                image=validated_data.get('image', None),
                text=validated_data.get('text', None),
            )
            return album
class LikeSerializerPost(serializers.ModelSerializer):
    #def to_representation(self, instance): #вызывается перед сериализацей данных
        #return {'user': instance.user, 'likes': instance.likes}
    user = UserSubSerializer(required=False)
    class Meta:
        model = LikePost
        fields = ('user', 'likes', 'id')
    def create(self, validated_data):
        album = LikePost.objects.create(
            user = validated_data.get('user', None),
            likes = int(validated_data.get('likes', None)) + 1
        )
        return album

class PostWallSerializer(FlexFieldsModelSerializer, serializers.ModelSerializer):
    user = UserDetailSerializer(required=False)
    reviews = ReviewsSerializer(many=True, read_only=True, required=False)
    like = LikeSerializerPost(many=True, read_only=True, required=False, allow_empty=True, allow_null=True)
    likes_count = serializers.IntegerField(read_only=True, required=False)
    image = serializers.ImageField(required=False)
    class Meta:
        model = PostWall
        fields = ('user', 'des', 'image', 'like', 'date', 'id', 'editMode', 'reviews', 'likes_count')

    def create(self, validated_data):
        album = PostWall.objects.create(
            user = validated_data.get('user', None),
            des = validated_data.get('des', None),
            image = validated_data.get('image', None),
        )
        return album
