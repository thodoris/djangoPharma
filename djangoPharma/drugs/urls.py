from django.conf.urls import url
from drugs.views import CategoryDrugsList


from . import views

urlpatterns = [
    # ex: /drugs/
    url(r'^$', views.index, name='index'),
    # ex: /drugs/5/
    url(r'^(?P<drug_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^category/([\w-]+)/$', CategoryDrugsList.as_view()),
    # ex: /drugs/addDrug
    url(r'^addDrug$', views.add_drug, name='add_drug'),
    # ex: /drugs/updateDrug
    url(r'^updateDrug/(?P<drug_id>[0-9]+)/$', views.update_drug, name='update_drug'),
    # categories
    url(r'^drugCategories$', views.display_drug_categories, name='display_drug_categories'),
    url(r'^addDrugCategory$', views.add_drug_category, name='add_drug_category'),
    url(r'^drugCategories/(?P<drug_category_id>[0-9]+)/$', views.update_drug_category, name='update_drug_category'),
]
