from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterView, \
    mark_complete, DeleteAll

urlpatterns = [
    path('mark_complete/<int:task_id>', mark_complete, name='mark-complete'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='tasks'), name='logout'),
    path('', TaskList.as_view(), name='tasks'),
    path('<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-udpate/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('delete-all/', DeleteAll.as_view(), name='delete-all'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete')
    ]
