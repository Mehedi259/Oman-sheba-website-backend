from rest_framework import serializers
from .models import News, NewsComment


class NewsCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsComment
        fields = ['id', 'user', 'user_name', 'content', 'parent', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return NewsCommentSerializer(obj.replies.all(), many=True).data
        return []


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'category', 
                  'author', 'author_name', 'featured_image', 'is_featured', 
                  'views', 'comments_count', 'published_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'views', 'created_at', 'updated_at']
