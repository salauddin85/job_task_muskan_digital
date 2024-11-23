from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet,
      ModuleViewSet,
      AdminViewset,
      UserLoginApiView,
      LogoutView)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'admin-users', AdminViewset,basename='admin_users')
router.register(r'custom-users', CustomUserViewSet,basename='custom_users')
router.register(r'modules', ModuleViewSet,basename='module')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('login/',UserLoginApiView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout')
] 

# +router.urls