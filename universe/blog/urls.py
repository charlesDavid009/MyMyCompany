from django.urls import path, include
from blog import views

urlpatterns = [
    path('Blog/',  views.items_list),
    path('Blog/create', views.create_blog),
    path('Blog/action', views.action),
    path('Blog/<int:id>/comment/',  views.comment),
    path('Blog/<int:id>/subcomment/', views.sub_comment),
    path('Blog/<int:pk>/details',  views.items_details),
    path('Blog/<int:id>/comment_details/', views.comment_details),
    path('Blog/<int:pk>/delete', views.items_delete),
    path('Blog/<int:pk>/comment_delete/', views.comment_delete),
]
