from rest_framework import serializers
from .models import Post, Comment, Like, Classified, ClassifiedCategory


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'user_name', 'content', 'image', 
                  'comments_count', 'likes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class ClassifiedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedCategory
        fields = '__all__'


class ClassifiedSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=ClassifiedCategory.objects.all(),
        allow_null=True,
        required=False
    )
    
    class Meta:
        model = Classified
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'slug']
