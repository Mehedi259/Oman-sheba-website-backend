from rest_framework import serializers
from .models import Post, Comment, Like, Classified, ClassifiedCategory, ForumPost, ForumCategory, ForumComment
from classifieds.models import ClassifiedImage


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    def get_user_name(self, obj):
        return obj.user.name or f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    def get_user_name(self, obj):
        return obj.user.name or f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'user_name', 'content', 'image', 
                  'comments_count', 'likes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class ClassifiedCategorySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='classifieds.count', read_only=True)
    
    class Meta:
        model = ClassifiedCategory
        fields = '__all__'


class ClassifiedSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    
    def get_owner_name(self, obj):
        return obj.owner.name or f"{obj.owner.first_name} {obj.owner.last_name}".strip() or obj.owner.username
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
    author_name = serializers.SerializerMethodField()
    author_profile_picture = serializers.SerializerMethodField()
    
    def get_author_name(self, obj):
        return obj.author.name or f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username

    def get_author_profile_picture(self, obj):
        request = self.context.get('request')
        if hasattr(obj.author, 'profile_picture') and obj.author.avatar:
            return request.build_absolute_uri(obj.author.avatar.url) if request else obj.author.avatar.url
        return None
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    
    class Meta:
        model = ForumComment
        fields = ['id', 'content', 'author', 'author_name', 'author_first_name', 'author_profile_picture', 'post', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'post', 'created_at', 'updated_at']

class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = '__all__'


class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_profile_picture = serializers.SerializerMethodField()
    
    def get_author_name(self, obj):
        return obj.author.name or f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username

    def get_author_profile_picture(self, obj):
        request = self.context.get('request')
        if hasattr(obj.author, 'profile_picture') and obj.author.avatar:
            return request.build_absolute_uri(obj.author.avatar.url) if request else obj.author.avatar.url
        return None
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
        # Convert tags from comma-separated string to JSON string if necessary
        import json
        mutable_data = data.copy() if hasattr(data, 'copy') else data
        tags = mutable_data.get('tags')
        if isinstance(tags, str):
            try:
                json.loads(tags)
            except ValueError:
                tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                mutable_data['tags'] = json.dumps(tags_list)
        return super().to_internal_value(mutable_data)
