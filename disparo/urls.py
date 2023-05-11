from django.urls import path

from . import views

urlpatterns = [
    path('enviar_disparo/', views.enviar_disparo, name='enviar_disparo'),
    path('confirmar_disparo/', views.confirmar_disparo, name='confirmar_disparo'),
    path('add_authorization/', views.add_authorization, name='add_authorization'),
    path('auth_aceita_disparador/', views.auth_aceita_disparador,
         name='auth_aceita_disparador'),
    path('auth_deleta_disparador/', views.auth_deleta_disparador,
         name='auth_deleta_disparador'),
    path('rec_authorization_tit/', views.rec_authorization_tit,
         name='rec_authorization_tit'),
    path('rec_authorization_ass/', views.rec_authorization_ass,
         name='rec_authorization_ass'),
    path('auth_deleta_titular/<int:titular_id>',
         views.auth_deleta_titular, name='auth_deleta_titular'),
    path('auth_deleta_assessor/<int:assessor_id>',
         views.auth_deleta_assessor, name='auth_deleta_assessor'),
    path('editautholist/', views.editautholist, name='editautholist'),

]
