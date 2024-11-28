from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Post, Category
from datetime import datetime
from .filters import PostFilter
from .forms import NewsForm

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

class NewsCreateView(View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'news_form.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.post_type = 'NE'
            news.save()
            return redirect('news_list')
        return render(request, 'news_form.html', {'form': form})

class NewsEditView(View):
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

class NewsDeleteView(View):
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