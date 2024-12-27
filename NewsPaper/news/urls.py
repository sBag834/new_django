from django.urls import path
from django.views.decorators.cache import cache_page
from .views import NewsList, NewDetail, NewsSearchView,NewsCreateView, NewsEditView, NewsDeleteView, subscribe_to_category


urlpatterns = [
   path('', cache_page(60*10)(NewsList.as_view()), name='news_list'),
   path('<int:pk>', NewDetail.as_view(), name='NewDetail'),
   path('search/', NewsSearchView.as_view(), name='news_search'),
   path('create/', NewsCreateView.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEditView.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
   path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe_to_category'),
]