from django.urls import path
from . import views
from django.contrib.staticfiles.views import serve

#me
urlpatterns = [
    path("", views.index, name="index"),
    #path("changeday", views.change_day, name="changeday"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("login", views.login_view, name="login"),
    path("changeobs", views.training_observation_change, name="changeobs"),
    path("available", views.class_available, name="available"),
    path("class", views.class_room, name="class"),
    path("reserved", views.reserved_trainings, name="reserved"),
    path("trainingdays", views.training_observation, name="trainingdays"),
    path("add_classroom", views.add_classroom, name="add_classroom"),
    path("<int:page>", views.class_room, name="class"),
    path("trainingdays/<int:page>/<int:trainingday>", views.training_observation, name="trainingdays"),
    #path("trainingdays/<int:page>", views.training_observation, name="observation"),
    path('favicon.ico', serve, {'path': 'favicon.ico'}),
]