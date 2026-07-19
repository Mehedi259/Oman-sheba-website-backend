from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, Like, Classified, ClassifiedCategory, ForumPost, ForumCategory, ForumComment, ForumLike
from .serializers import PostSerializer, CommentSerializer, ClassifiedSerializer, ClassifiedCategorySerializer, ForumPostSerializer, ForumCategorySerializer, ForumCommentSerializer


class PostListCreateView(generics.ListCreateAPIView):
    """List and create community posts"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    """List and create comments for a post"""
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)


class PostLikeView(APIView):
    """Like or unlike a post"""
    
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)


class ClassifiedCategoryListView(generics.ListAPIView):
    """List all classified categories"""
    queryset = ClassifiedCategory.objects.all()
    serializer_class = ClassifiedCategorySerializer
    permission_classes = [] # Allow any


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ClassifiedListCreateView(generics.ListCreateAPIView):
    """List and create classified ads"""
    queryset = Classified.objects.all()
    serializer_class = ClassifiedSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition', 'price_negotiable']
    search_fields = ['title', 'title_bn', 'description', 'description_bn']
    ordering_fields = ['price', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a classified listing"""
    queryset = Classified.objects.all()
    serializer_class = ClassifiedSerializer
    
class ForumCategoryListView(generics.ListAPIView):
    """List all forum categories"""
    queryset = ForumCategory.objects.all()
    serializer_class = ForumCategorySerializer
    permission_classes = [] # Allow any


class ForumPostListCreateView(generics.ListCreateAPIView):
    """List and create forum posts"""
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'views', 'likes', 'pinned']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ForumPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a forum post"""
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class ForumCommentListCreateView(generics.ListCreateAPIView):
    """List and create comments for a forum post"""
    serializer_class = ForumCommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return ForumComment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = ForumPost.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)


class ForumPostLikeView(APIView):
    """Like or unlike a forum post"""
    
    def post(self, request, post_id):
        post = ForumPost.objects.get(id=post_id)
        
        # Check if user already liked the post
        like, created = ForumLike.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            # User already liked, so unlike it
            like.delete()
            post.likes = max(0, post.likes - 1)
            post.save(update_fields=['likes'])
            return Response({'message': 'Forum post unliked', 'likes': post.likes}, status=status.HTTP_200_OK)
            
        # New like
        post.likes += 1
        post.save(update_fields=['likes'])
        return Response({'message': 'Forum post liked', 'likes': post.likes}, status=status.HTTP_200_OK)
