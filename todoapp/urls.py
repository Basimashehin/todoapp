from django.urls import path
from todoapp import views
urlpatterns=[
    path("signup",views.SignUpView.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="index"),
    path ("signout",views.SignOutView.as_view(),name="signout"),
    path("todos/add",views.ToDoAddView.as_view(),name="add-todo"),
    path("todos/all",views.ToDoListView.as_view(),name="list-todo"),
    path("todos/remove/<int:id>",views.delete_todo,name="remove-todo"),
    path("todos/detail/<int:id>",views.ToDoDetailView.as_view(),name="todo-detail"),
    path("todos/change/<int:id>", views.ToDoEditView.as_view(), name="edit-todo"),

]