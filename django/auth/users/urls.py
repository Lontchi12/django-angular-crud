from django.urls import path 
from .views import ResgisterView, LoginView, UserView, LogoutView, TodoView, TodoDetailView, TodoCreateView, TodoUpdateView, TodoDeleteView
# TodoView, TodoDetailView,TodoCreateView, TodoUpdateView, TodoDeleteView 

urlpatterns = [
    path('register', ResgisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('todos', TodoView.as_view()),
    path('todo/<str:pk>', TodoDetailView.as_view()),
    path('addtodo', TodoCreateView.as_view()),
    path('update/<str:pk>', TodoUpdateView.as_view()),
    path('delete/<str:pk>', TodoDeleteView.as_view()),

    
]
