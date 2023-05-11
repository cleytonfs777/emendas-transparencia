from django.urls import path

from . import views

urlpatterns = [
    path('', views.cadastrar, name='cadastrar'),
    path('listar/', views.listar, name='listar'),
    path('processar_titular/', views.processar_titular, name='processar_titular'),
    path('processar_assessor/', views.processar_assessor,
         name='processar_assessor'),
    path('processar_viatura/', views.processar_viatura, name='processar_viatura'),
    path('editar_titular/<int:id>', views.editar_titular, name='editar_titular'),
    path('editar_assessor/<int:id>', views.editar_assessor, name='editar_assessor'),
    path('editar_viatura/<int:id>', views.editar_viatura, name='editar_viatura'),
    path('deleta_titular/<int:titular_id>',
         views.deleta_titular, name='deleta_titular'),
    path('deleta_assessor/<int:id>', views.deleta_assessor, name='deleta_assessor'),
    path('deleta_viatura/<int:id>', views.deleta_viatura, name='deleta_viatura'),
    path('add_categoria/', views.add_categoria, name='add_categoria'),
    path('sync_database/', views.sync_database, name='sync_database'),
    path('log_disparo/', views.log_disparo, name='log_disparo'),
    path('ajuda_manager/', views.ajuda_manager, name='ajuda_manager'),
    path('responde_user/', views.responde_user, name='responde_user'),

]
