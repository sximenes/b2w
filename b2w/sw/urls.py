from django.conf.urls import url, include
from dynamic_rest.routers import DynamicRouter

from sw import views

router = DynamicRouter()
router.register('planet', views.PlanetViewSet)

urlpatterns = [
    url(r'^',include(router.urls)),
]