from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор

from .models import Post, Category, User, PostCategory

from django.core.mail import send_mail



@receiver(m2m_changed, sender=PostCategory)
def post(sender, instance, *args, **kwargs):
    for cat_id in instance.postCategory.all():
        print(cat_id)
        users = Category.objects.filter(name=cat_id).values("subscribers")
        for user_id in users:
            send_mail(
                subject=f"{instance.title}",
                message=f"Здравствуй, {User.objects.get(pk=user_id['subscribers']).username}."
                        f"Новая статья в твоём любимом разделе! \n"
                        f"Заголовок статьи: {instance.title} \n"
                        f"Текст статьи: {instance.text[:50]} \n"
                        f"Ссылка на статью: http://127.0.0.1:8000/news/{instance.pk}",
                from_email='vintazh-m@yandex.ru',
                recipient_list=[User.objects.get(pk=user_id['subscribers']).email]
            )