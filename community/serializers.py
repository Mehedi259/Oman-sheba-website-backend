from rest_framework import serializers
from .models import Post, Comment, Like, Classified, ClassifiedCategory, ForumPost, ForumCategory, ForumComment
from classifieds.models import ClassifiedImage


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
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Classified
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'slug']

    def get_images(self, obj):
        request = self.context.get('request')
        images = ClassifiedImage.objects.filter(content_type='others', content_id=obj.id)
        if not images:
            return []
        return [request.build_absolute_uri(img.image.url) if request else img.image.url for img in images]


class ForumCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    
    class Meta:
        model = ForumComment
        fields = ['id', 'content', 'author', 'author_name', 'author_first_name', 'post', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'post', 'created_at', 'updated_at']

class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = '__all__'


class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=ForumCategory.objects.all(),
        allow_null=True,
        required=False
    )
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = ForumPost
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'slug', 'views', 'likes']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        # category is a slug string because of SlugRelatedField. 
        # Frontend expects an object with name, nameBn etc.
        if instance.category:
            repr['category'] = {
                'id': instance.category.id,
                'name': instance.category.name,
                'nameBn': instance.category.name_bn,
                'slug': instance.category.slug
            }
        return repr

    def to_internal_value(self, data):
        # Convert tags from comma-separated string to list if necessary
        mutable_data = data.copy() if hasattr(data, 'copy') else data
        tags = mutable_data.get('tags')
        if isinstance(tags, str):
            mutable_data['tags'] = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return super().to_internal_value(mutable_data)
