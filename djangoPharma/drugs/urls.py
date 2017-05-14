from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /drugs/
    url(r'^$', views.index, name='index'),
    # ex: /drugs/5/
    url(r'^(?P<drug_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: add drug
    url(r'^addDrug$', views.add_drug, name='add_drug'),
    ]