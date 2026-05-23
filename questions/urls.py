from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "generate/",                        #Here is where javascript will send post request so it can be viewed.
        views.generate_questions,
        name="generate_questions"
    ),
]