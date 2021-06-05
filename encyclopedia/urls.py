from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_box, name="search_box"),
    path("wiki/<str:entrada>", views.mostrar_entradas, name="entrada"),
    path('random_page/', views.random_page, name='random_page'),
    path('nueva_entrada/', views.nueva_entrada, name='nueva_entrada'),
    path('wiki/<str:titulo>/editar', views.editar_pagina, name='editar_pagina'),
]
