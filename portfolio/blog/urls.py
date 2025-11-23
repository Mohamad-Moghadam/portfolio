from django.urls import path
from .views import BlogCreateView, BlogDestroyView, BlogListView, BlogDetailView, BlogUpdateView

urlpatterns = [
    path('create', BlogCreateView.as_view(), name='blog-create'),
    path('delete/<int:pk>', BlogDestroyView.as_view(), name='blog-destroy'),
    path('list', BlogListView.as_view(), name='blog-list'),
    path('detail/<int:pk>', BlogDetailView.as_view(), name='blog-detail'),
    path('update/<int:pk>', BlogUpdateView.as_view(), name='blog-update'),
]