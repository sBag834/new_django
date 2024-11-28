from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           'title': ['icontains'],
           'created_time': [
               'lt',  # цена должна быть меньше или равна указанной
               'gt',  # цена должна быть больше или равна указанной
           ],
       }