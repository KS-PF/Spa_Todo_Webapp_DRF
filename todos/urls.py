from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from todos import views


app_name = 'todos'
urlpatterns = [
    path('', views.TodoListView.as_view()),
    path('<int:pk>/', views.TodoDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# .json