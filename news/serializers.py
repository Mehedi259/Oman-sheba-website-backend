from rest_framework import serializers
from .models import News, NewsComment, Article, ArticleCategory


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


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True)
    featured_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'title_bn', 'slug', 'excerpt', 'excerpt_bn',
            'content', 'content_bn', 'type', 'category', 'category_name',
            'category_name_bn', 'featured_image', 'images', 'tags',
            'meta_title', 'meta_description', 'author_name', 'status',
            'featured', 'views', 'source', 'source_url',
            'published_at', 'created_at', 'updated_at'
        ]
    
    def get_featured_image(self, obj):
        if obj.featured_image:
            return obj.featured_image.url
        return None
