from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name="search"),
    path("new_page",views.newpage, name="new-page"),
    path("edit_page",views.editpage, name="edit-page"),
    path("<str:name>",views.entry, name="show-entry")
]
