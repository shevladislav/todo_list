from django.urls import path

from .views import (
    RegistrationUser,
    LoginUser,
    logout_view,
    TaskFormCreate,
    TaskDetail,
    task_delete,
    TaskUpdateView,
    TaskListView,
)

urlpatterns = [
    path('', TaskListView.as_view(), name='home_page'),
    path('auth/register/', RegistrationUser.as_view(), name='registration'),
    path('auth/login/', LoginUser.as_view(), name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('create_task/', TaskFormCreate.as_view(), name='task_create'),
    path('detail/<int:pk>/<str:title>/<str:author>/<int:year>/<int:month>/<int:day>/', TaskDetail.as_view(),
         name='task_detail'),
    path('delete/<int:pk>/<str:title>/<str:author>/<int:year>/<int:month>/<int:day>/', task_delete,
         name='task_delete'),
    path('task_update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
]
