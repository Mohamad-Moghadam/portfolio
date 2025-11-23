from django.shortcuts import render
from django.db import transaction
from django.db.models import F
from rest_framework.permissions import BasePermission
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
        
        # Delete the blog
        self.perform_destroy(instance)
        
        # Renumber all remaining blogs to have sequential IDs starting from 1
        with transaction.atomic():
            self._renumber_blogs()
        
        return Response(
            {
                'message': 'Blog deleted successfully',
                'id': blog_id,
                'title': blog_title,
            },
            status=status.HTTP_200_OK
        )
    
    def _renumber_blogs(self):
        """
        Renumber all blogs to have sequential IDs starting from 1.
        This preserves all blog data including timestamps.
        """
        from django.db import connection
        from django.utils import timezone
        
        # Get all blogs ordered by current ID
        blogs = list(Blog.objects.all().order_by('id'))
        
        if not blogs:
            # If no blogs remain, reset the SQLite sequence
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='blog_blog'")
            return
        
        # Store all blog data
        blog_data = []
        for blog in blogs:
            blog_data.append({
                'title': blog.title,
                'content': blog.content,
                'created_at': blog.created_at,
                'updated_at': blog.updated_at,
                'status': blog.status,
                'author_id': blog.author_id,
            })
        
        # Delete all blogs
        Blog.objects.all().delete()
        
        # Reset the SQLite sequence to 0
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='blog_blog'")
        
        # Recreate blogs with sequential IDs starting from 1
        # Using bulk_create for efficiency, but need to handle timestamps manually
        blog_objects = []
        for index, data in enumerate(blog_data, start=1):
            blog = Blog(
                id=index,
                title=data['title'],
                content=data['content'],
                status=data['status'],
                author_id=data['author_id'],
            )
            # Manually set timestamps to preserve original values
            blog.created_at = data['created_at']
            blog.updated_at = data['updated_at']
            blog_objects.append(blog)
        
        # Use bulk_create and then update timestamps with raw SQL to preserve them
        Blog.objects.bulk_create(blog_objects)
        
        # Update timestamps using raw SQL since auto_now and auto_now_add prevent setting them directly
        with connection.cursor() as cursor:
            for index, data in enumerate(blog_data, start=1):
                cursor.execute(
                    """
                    UPDATE blog_blog 
                    SET created_at = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    [data['created_at'], data['updated_at'], index]
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