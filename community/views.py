from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, Like, Classified, ClassifiedCategory, ForumPost, ForumCategory
from .serializers import PostSerializer, CommentSerializer, ClassifiedSerializer, ClassifiedCategorySerializer, ForumPostSerializer, ForumCategorySerializer


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
    
class ForumPostListCreateView(generics.ListCreateAPIView):
    """List and create forum posts"""
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ForumPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a forum post"""
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
