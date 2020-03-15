from . import views, viewsets
from rest_framework.routers import DefaultRouter


app_name = "rooms"

router = DefaultRouter()
router.register("", views.RoomViewSet)

urlpatterns = router.urls


# router = DefaultRouter()
# router.register("", viewsets.RoomViewset, basename="room")
#
# urlpatterns = router.urls

# urlpatterns = [path("list/", views.list_rooms)]
# urlpatterns = [
    # path("", views.rooms_view),
    # path("", views.RoomsView.as_view()),
    # # path("<int:pk>/", views.SeeRoomView.as_view()),  # as_view() : 클래스 함수를 통해 인스턴스 생성
    # path("search/", views.room_search),
    # path("<int:pk>/", views.RoomView.as_view()),  # as_view() : 클래스 함수를 통해 인스턴스 생성
    # ]

