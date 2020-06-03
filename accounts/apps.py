from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('accounts')

    # def ready(self):
    #     print("importing")
    #     import accounts.signals
    #     print("imported")