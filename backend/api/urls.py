from django.conf.urls import include, url

#Django Rest Framework
from rest_framework import routers

from api import controllers
from django.views.decorators.csrf import csrf_exempt

#REST API routes
router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^childs', csrf_exempt(controllers.ChildList.as_view())),
    url(r'^groups', csrf_exempt(controllers.GroupList.as_view())),
    url(r'^profiles', csrf_exempt(controllers.ProfileList.as_view())),
    url(r'^events', csrf_exempt(controllers.EventList.as_view())),
    url(r'^session', csrf_exempt(controllers.Session.as_view())),
    url(r'^register', csrf_exempt(controllers.Register.as_view())),
    url(r'^events', csrf_exempt(controllers.Events.as_view())),
    url(r'^dogs/(?P<pk>[0-9]+)$', csrf_exempt(controllers.DogDetail.as_view())),
    url(r'^dogs', csrf_exempt(controllers.DogList.as_view())),
    url(r'^breeds/(?P<pk>[0-9]+)$', csrf_exempt(controllers.BreedDetail.as_view())),
    url(r'^breeds', csrf_exempt(controllers.BreedList.as_view())),
    url(r'^activateifttt', csrf_exempt(controllers.ActivateIFTTT.as_view())),
    url(r'^', include(router.urls)),
]
