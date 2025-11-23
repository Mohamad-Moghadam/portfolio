from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAuthorOrSuperuser



class BlogCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDestroyView(DestroyAPIView):
    permission_classes = [IsAuthorOrSuperuser]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        blog_id = instance.id
        blog_title = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': 'Blog deleted successfully',
                'id': blog_id,
                'title': blog_title,
            },
            status=status.HTTP_200_OK
        )

class BlogListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogUpdateView(UpdateAPIView):
    permission_classes = [IsAuthorOrSuperuser]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer