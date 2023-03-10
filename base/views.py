from django.forms import Form
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin, DeletionMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from base.forms import UpdateForm, CreateForm, LoginForm
from base.models import Task


class RegisterView(FormView):
    model = User
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        for task in context['tasks']:
            task.create = task.create.strftime("%B, %d at %H:%M")
        context['count'] = context['tasks'].filter(complete=False).count()
        count = str(context['count'])
        context['count_plural'] = not (
                count.endswith('1') or count.endswith('2') or count.endswith('3') or count.endswith('4'))
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/task_detail.html'
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateForm
    template_name = 'base/task_create.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = UpdateForm
    template_name = 'base/task_update.html'
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class DeleteAll(LoginRequiredMixin, View, DeletionMixin, FormMixin):
    success_url = reverse_lazy('tasks')
    template_name = 'base/confirm_delete_all.html'
    form_class = Form

    def post(self, request, *args, **kwargs):
        self.object = Task.objects.filter(user=request.user)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

    def get(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)
        return render(request, self.template_name, {'form': self.form_class})

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def mark_complete(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.complete = not task.complete
        task.save()
        return redirect('tasks')
