import logging
import datetime

from django.conf import settings
from ...models import Post, User, Category
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    startdate = datetime.date.today() - datetime.timedelta(days=6)
    posts = Post.objects.filter(dateCreation__gt=startdate).values('postCategory', 'title', 'pk')

    for cat in Category.objects.values('pk', 'name'):
        id_posts_cat = []
        for post in posts:
            if post['postCategory'] == cat['pk']:
                id_posts_cat.append(post['pk'])
        if not id_posts_cat == []:
            for user in User.objects.values('subscribers', 'email', 'username'):
                if user['subscribers'] == cat['pk']:
                    send_mail(
                        subject=f"Еженедельная рассылка новостей!",
                        message=f"Здравствуй, {user['username']}."
                                f"Новый список статьей в твоём любимом разделе - {cat['name']}! \n"                                
                                f"Ссылка на статьи: http://127.0.0.1:8000/news/search?dateCreation__gt="
                                f"{startdate}&postCategory={cat['pk']}",
                        from_email='vintazh-m@yandex.ru',
                        recipient_list=[user['email']]
                    )

# функция, которая будет удалять неактуальные задачи posts
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second='*/10'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")