from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Post, Category, Author
from datetime import datetime
from django.utils import timezone
from .filters import PostFilter
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .mixins import AuthorRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.cache import cache


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        new_au = Author.objects.create(user_id=request.user.id)
        new_au.save()
    return redirect('/news/')

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        if request.user in category.subscribers.all():
            category.subscribers.remove(request.user)
            print(f"{request.user.username} отписался от {category.name}")
        else:
            category.subscribers.add(request.user)
            print(f"{request.user.username} подписался на {category.name}")
    return redirect('news_list')

class MyPage(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class AuthRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'

class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

class NewDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = cache.get(f'news-{self.kwargs["pk"]}', None)
        if not context:
            context = super().get_context_data(**kwargs)
            context['categories'] = self.object.categories.all()
            cache.set(f'news-{self.kwargs["pk"]}', context)
        return context

class NewsSearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        category = request.GET.get('category', '')
        date_after = request.GET.get('date_after', '')

        news_queryset = Post.objects.all()

        if query:
            news_queryset = news_queryset.filter(title__icontains=query)

        if category:
            news_queryset = news_queryset.filter(categories__name__icontains=category)

        if date_after:
            news_queryset = news_queryset.filter(created_time__gte=date_after)

        categories = Category.objects.all()

        context = {
            'news_list': news_queryset,
            'query': query,
            'category': category,
            'date_after': date_after,
            'categories': categories,
        }

        return render(request, 'posts_search.html', context)

class NewsCreateView(AuthorRequiredMixin, AuthRequiredMixin, View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'news_form.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST)
        today = timezone.now().date()
        author = Author.objects.get(user_id=request.user.id)
        author_id = author.id
        news_count_today = Post.objects.filter(author_id=author_id, created_time__date=today).count()

        if news_count_today >= 3:
            return render(request, 'news_form.html', {'form': form, 'error': 'Вы уже опубликовали 3 новости сегодня.'})


        if form.is_valid():
            news = form.save(commit=False)
            news.post_type = 'NE'
            author = Author.objects.get(user_id=request.user.id)
            author_id = author.id
            news.author_id = author_id
            news.save()
            form.save_m2m()

            categories = news.categories.all()
            subscribers = set()

            for category in categories:
                subscribers.update(category.subscribers.all())

            for user in subscribers:
                subject = news.title
                text_content = f"Здравствуй, {user.username}. Новая статья: {news.title}. Содержимое: {news.content[:50]}..."
                html_content = render_to_string('email_template.html', {
                    'title': news.title,
                    'content': news.content[:50],
                    'username': user.username,
                })

                msg = EmailMultiAlternatives(subject, text_content, 'Snamix7@yandex.ru', [user.email])
                msg.attach_alternative(html_content, "text/html")

                msg.send(fail_silently=False)

            return redirect('news_list')
        return render(request, 'news_form.html', {'form': form})

class NewsEditView(AuthorRequiredMixin, AuthRequiredMixin, View):
    def get(self, request, pk):
        news = get_object_or_404(Post, pk=pk)
        form = NewsForm(instance=news)
        return render(request, 'news_form.html', {'form': form})

    def post(self, request, pk):
        news = get_object_or_404(Post, pk=pk)
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_list')
        return render(request, 'news_form.html', {'form': form})

class NewsDeleteView(AuthorRequiredMixin, AuthRequiredMixin, View):
    def get(self, request, pk):
        news = get_object_or_404(Post, pk=pk)
        return render(request, 'news_confirm_delete.html', {'news': news})

    def post(self, request, pk):
        news = get_object_or_404(Post, pk=pk)
        news.delete()
        return redirect('news_list')

class ArticleCreateView(NewsCreateView):
    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.post_type = 'AR'
            article.save()
            return redirect('news_list')

class ArticleEditView(NewsEditView):

    def post(self, request, pk):
        article = get_object_or_404(Post, pk=pk)
        form = NewsForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news_list')

class ArticleDeleteView(NewsDeleteView):

    def post(self, request, pk):
        article = get_object_or_404(Post, pk=pk)
        article.delete()
        return redirect('news_list')