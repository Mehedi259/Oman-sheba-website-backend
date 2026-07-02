from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import News, NewsComment
from .serializers import NewsSerializer, NewsCommentSerializer


class NewsListView(generics.ListAPIView):
    """List all published news"""
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['published_at', 'views']


class NewsDetailView(generics.RetrieveAPIView):
    """Retrieve news details"""
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class NewsCommentListCreateView(generics.ListCreateAPIView):
    """List and create comments for a news article"""
    serializer_class = NewsCommentSerializer
    
    def get_queryset(self):
        news_slug = self.kwargs.get('slug')
        return NewsComment.objects.filter(news__slug=news_slug, parent=None)
    
    def perform_create(self, serializer):
        news_slug = self.kwargs.get('slug')
        news = News.objects.get(slug=news_slug)
        serializer.save(user=self.request.user, news=news)
