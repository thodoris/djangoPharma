from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /drugs/
    url(r'^$', views.index, name='index'),
    # ex: /drugs/5/
    url(r'^(?P<drug_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /drugs/test
    url(r'^test$', views.test, name='test'),
    # ex: add drug
    url(r'^addDrug$', views.add_drug, name='add_drug'),
    url(r'^updateDrug/(?P<drug_id>[0-9]+)/$', views.update_drug, name='update_drug'),
    ]