import datetime
from celery import shared_task
from django.core.mail import send_mail
from .models import Post, Category, User


@shared_task
def post_now(pid):
    for cat_id in Post.objects.get(pk=pid).postCategory.all():
        users = Category.objects.filter(name=cat_id).values("subscribers")
        for user_id in users:
            send_mail(
                subject=f"{Post.objects.get(pk=pid).title}",
                message=f"Здравствуй, {User.objects.get(pk=user_id['subscribers']).username}."
                        f"Новая статья в твоём любимом разделе! \n"
                        f"Заголовок статьи: {Post.objects.get(pk=pid).title} \n"
                        f"Текст статьи: {Post.objects.get(pk=pid).text[:50]} \n"
                        f"Ссылка на статью: http://127.0.0.1:8000/news/{pid}",
                from_email='vintazh-m@yandex.ru',
                recipient_list=[User.objects.get(pk=user_id['subscribers']).email]
            )

@shared_task
def post_week():
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


