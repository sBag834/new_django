
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post, Category

def send_weekly_newsletters():
    print("5")
    now = timezone.now()
    week_ago = now - timezone.timedelta(weeks=1)

    categories = Category.objects.prefetch_related('subscribers')

    for category in categories:
        print("4")
        subscribers = category.subscribers.all()
        if subscribers.exists():
            print("3")
            new_posts = Post.objects.filter(categories=category, created_time__gte=week_ago)

            if new_posts.exists():
                print("2")
                subject = f'Новые статьи в категории {category.name}'
                html_content = render_to_string('weekly_newsletter.html', {
                    'category': category,
                    'new_posts': new_posts,
                })

                for user in subscribers:
                    print("1")
                    msg = EmailMultiAlternatives(subject, '', 'Snamix7@yandex.ru', [user.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=False)
