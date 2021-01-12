from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api.views import MovieViewSet, RatingViewSet, for_neta

router = routers.DefaultRouter()
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checking_neta', for_neta)
]
