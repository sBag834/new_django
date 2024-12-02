from django.urls import path

from .views import MyPage, upgrade_me


urlpatterns = [
   path('', MyPage.as_view(), name='profile'),
   path('upgrade/', upgrade_me, name = 'upgrade')
]