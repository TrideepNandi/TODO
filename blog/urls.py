from django.urls import path

from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("posts", views.posts, name="posts-page"),
    path("posts/<slug:slug>", views.post_detail,
         name="post-detail-page"), # /posts/my-first-post
    path ("signup/", views.RegisterView.as_view(), name = "Sign-up"),
    path('create_task/', views.create_task, name='create_task'),
    path("complete_task/<slug:slug>/", views.complete_task, name="complete_task"),
    path('completed-tasks/', views.completed_tasks, name='completed-tasks'),
    path('delete-task/<slug:slug>/', views.delete_task, name='delete_task'),
    path('completed-tasks/', views.completed_tasks, name='completed_tasks'),
]
