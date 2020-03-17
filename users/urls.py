from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "users"

router = DefaultRouter()
router.register("", views.UsersViewSet)

urlpatterns = router.urls
# urlpatterns = [
#     path("", views.UsersView.as_view()),
#     path("token/", views.login),  #로그인
#     path("me/", views.MeView.as_view()),
#     path("me/favs/", views.FavsView.as_view()),
#     path("<int:pk>", views.user_detail),
# ]
