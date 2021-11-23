from django.urls import path
from tasks.views import TaskView, TaskDetailView, TaskUpdateListView, TaskSearchView

urlpatterns = [
    path('', TaskView.as_view()),
    path('/list', TaskUpdateListView.as_view()),
    path('/search', TaskSearchView.as_view()),
    path('/<int:task_id>', TaskDetailView.as_view()),
]