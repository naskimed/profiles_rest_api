from django.conf.urls import url

from . import views

from django.conf.urls import include
from rest_framework.routers import DefaultRouter

#this for the ViewSet
router = DefaultRouter()
#router.register('hello-viewset',views.HelloViewSet, base_name='hello-viewset')
router.register('profile',views.UserProfileViewSet)
router.register('login',views.LoginViewSet,base_name='login')
router.register('subject',views.SubjectsViewSet, base_name='subject')
router.register('group',views.GroupViewSet, base_name = 'group')
#router.register('subjects',views.SubjectsViewSet, base_name='subjects')
#this for APIView
urlpatterns = [

    url(r'',include(router.urls))
    
]


