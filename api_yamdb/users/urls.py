from django.urls import include, path
from rest_framework import routers

import users.views as views

router_v1 = routers.DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')

authpatterns = [
    path('token/', views.get_jwt_token),
    path('signup/', views.obtain_confirmation_code),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(authpatterns)),
]
