
from django.urls import path

from account.apis import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('user/data/', views.UserListingView.as_view(), name="users"),
    # path('user/data/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
    path('user/<int:pk>/projects/', views.UserDetail.as_view(), name="user-detail"),
]

