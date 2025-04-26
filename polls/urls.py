from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_poll, name="create_poll"),
    path("vote/<int:poll_id>/", views.vote, name="vote"),
    path("results/<int:poll_id>/", views.results, name="results"),
    path("register/", views.register, name="register"),
    path("my-polls/", views.MyPollsView.as_view(), name="my_polls"),
    path("edit-poll/<int:pk>/", views.PollUpdateView.as_view(), name="edit_poll"),
    path("share/<uuid:share_id>/", views.shared_poll, name="shared_poll"),
]