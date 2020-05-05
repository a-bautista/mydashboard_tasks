from django.db.models.signals import post_save
from .models import EmailConfirmed
from django.contrib.auth import get_user_model

User = get_user_model()


def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    print(user.emailedconfirmed.send_mail())
    if created:
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            # create hash
            # send email

post_save.connect(user_created, sender=User)