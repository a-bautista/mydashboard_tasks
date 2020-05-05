from django.contrib import admin
from accounts.models import Account, EmailConfirmed

admin.site.register(Account)
admin.site.register(EmailConfirmed)
