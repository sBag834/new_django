from django.db import models

from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = sum(post.rating for post in Post.objects.filter(author=self)) * 3
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        post_comments_rating = sum(comment.rating for post in Post.objects.filter(author=self)
                                   for comment in Comment.objects.filter(post=post))

        self.rating = post_rating + comment_rating + post_comments_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NE'
    POST_TYPE_CHOICES = [
        (ARTICLE, 'Article'),
        (NEWS, 'News'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def __str__(self):
        return f'{self.title.title()}'

    def view(self):
        return f'{self.content}'

    def get_absolute_url(self):
        return reverse('NewDetail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user