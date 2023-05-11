from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('cadastrar_disparador/', views.cadastrar_disparador,
         name='cadastrar_disparador'),
    path('listar_disparador/', views.listar_disparador, name='listar_disparador'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('exluir_disparador/<str:id>/',
         views.exluir_disparador, name='exluir_disparador'),
    path('editar_disparador/<str:id>/',
         views.editar_disparador, name='editar_disparador'),
    path('cadastrar_disparador_ext', views.cadastrar_disparador_ext,
         name='cadastrar_disparador_ext'),
    # ... outras URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
]
