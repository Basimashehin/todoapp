from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("todos",views.TodoView,basename="todos")

urlpatterns = [

]+router.urls
