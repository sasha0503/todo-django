from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse

from base.models import Task


class TaskList(ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'


class TaskDetail(DetailView):
    model = Task
    template_name = 'base/task_detail.html'
    context_object_name = 'task'


class TaskCreate(CreateView):
    model = Task
    template_name = 'base/task_create.html'
    context_object_name = 'task'
    fields = '__all__'
