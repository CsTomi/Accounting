from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.accounting_proba, name='accounting_proba'),
]