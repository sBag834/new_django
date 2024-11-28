from django.urls import path

from .views import ArticleCreateView, ArticleEditView, ArticleDeleteView


urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleEditView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]