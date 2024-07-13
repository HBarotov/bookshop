from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = "payments"
urlpatterns = [
    path(_("process/"), views.payment_process, name="process"),
    path(_("completed/"), views.payment_completed, name="completed"),
    path(_("cancelled/"), views.payment_cancelled, name="cancelled"),
]
