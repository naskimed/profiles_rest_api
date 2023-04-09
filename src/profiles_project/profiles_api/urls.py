from django.conf.urls import url

from . import views

from django.conf.urls import include
from rest_framework.routers import DefaultRouter

#this for the ViewSet
router = DefaultRouter()
#router.register('hello-viewset',views.HelloViewSet, base_name='hello-viewset')
router.register('profile',views.UserProfileViewSet)
#this for APIView
urlpatterns = [
    #url(r'^hello-view/', views.HelloApiView.as_view()),
    url(r'',include(router.urls))
]


