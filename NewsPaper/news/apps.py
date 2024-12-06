from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'


class MyConfig(AppConfig):
    name = 'news'

    def ready(self):

        from django_apscheduler.jobstores import DjangoJobStore
        from apscheduler.schedulers.background import BackgroundScheduler
        from .tasks import send_weekly_newsletters

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_newsletters,
            trigger='cron',
            day_of_week='mon',
            hour=8,
            minute=0,
            id='send_weekly_newsletters',
            replace_existing=True,
        )

        scheduler.start()
