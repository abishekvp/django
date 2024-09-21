from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index,name="index"),
    path('signup', views.signup,name="signup"),
    path('signin', views.signin,name="signin"),
    path('signout', views.signout,name="signout"),
    path('dashboard', views.dashboard,name="dashboard"),
    path("test", csrf_exempt(views.test), name="test")
]
