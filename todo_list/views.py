from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, DetailView, UpdateView, ListView

from .models import Task
from .forms import RegistrationUserForm, LoginUserForm, TaskForm
from .utilities import user_is_active


class TaskListView(ListView):
    paginate_by = 2
    model = Task
    template_name = 'todo_list/home_page.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        if self.request.user.is_active:
            todo_list = Task.objects.filter(author=self.request.user).order_by('deadline')
            return todo_list
        return ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = context | user_is_active(self.request)

        return context


class RegistrationUser(FormView):
    template_name = 'todo_list/register_page.html'
    form_class = RegistrationUserForm
    success_url = '/'

    def form_valid(self, form):
        cd = form.cleaned_data
        username, email, password = (
            cd['username'],
            cd['email'],
            cd['password'],
        )
        print(username, email, password)
        User.objects.create_user(username=username, email=email, password=password)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = context | user_is_active(self.request)

        return context


class LoginUser(FormView):
    template_name = 'todo_list/login_page.html'
    form_class = LoginUserForm
    success_url = '/'

    def form_valid(self, form):
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


class TaskFormCreate(FormView):
    template_name = 'todo_list/task_form_create.html'
    form_class = TaskForm
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        author = self.request.user
        Task.objects.create(
            author=author,
            deadline=data.get('deadline'),
            title=data.get('title'),
            body=data.get('body')
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = context | user_is_active(self.request)

        return context


class TaskDetail(DetailView):
    model = Task
    template_name = 'todo_list/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = context | user_is_active(self.request)

        return context


def task_delete(request, pk, title, author, year, month, day):
    Task.objects.get(pk=pk).delete()
    return redirect('/')


class TaskUpdateView(UpdateView):
    form_class = TaskForm
    template_name = 'todo_list/task_update.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = context | user_is_active(self.request)

        return context
