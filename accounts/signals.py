from django.db.models.signals import post_save
from .models import EmailConfirmed
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()

# def user_created(sender, instance, created, *args, **kwargs):
#     user = instance
#     if created:
#         email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
#         if email_is_created:
#             short_hash = hashlib.sha256(str(os.urandom(256)).encode('utf-8')).hexdigest()[:10]
#             username, domain = str(user.email).split("@")
#             activation_key = hashlib.sha256(str(short_hash+username).encode('utf-8')).hexdigest()
#             email_confirmed.activation_key = activation_key
#             email_confirmed.save()
#             email_confirmed.activate_user_email()
            
#             #UserRegisterForm.activate_user_email(UserRegisterForm,context) 

# post_save.connect(user_created, sender=User)