from django.conf.urls import url
from drugs.views import CategoryDrugsList


from . import views

urlpatterns = [
    # ex: /drugs/
    url(r'^$', views.index, name='index'),
    # ex: /drugs/5/
    url(r'^(?P<drug_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^category/([\w-]+)/$', CategoryDrugsList.as_view()),
    # ex: /drugs/test
    url(r'^test$', views.test, name='test'),
    # ex: add drug
    url(r'^addDrug$', views.add_drug, name='add_drug'),
    url(r'^updateDrug/(?P<drug_id>[0-9]+)/$', views.update_drug, name='update_drug'),
    url(r'^migrate$', views.manage_migrations, name='manage_migrations'),
]
