import re
import os
from random import choice
from django.forms.forms import Form
from markdown2 import *
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from . import util


class FormNuevaEntrada(forms.Form):
    titulo = forms.CharField(max_length=80,required=True)
    entrada= forms.CharField(required=True,widget=forms.Textarea)


class FormEditarPagina(FormNuevaEntrada):
    def clean_title(self):
        titulo = self.cleaned_data.get('titulo')
        return titulo

    def actualizar_archivo(self, titulo, entrada):
        with open(f'./entries/{titulo}.md', 'w') as ef:
            ef.write(f'# {titulo}\n' + entrada)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "titulo": "All Pages",
    })

def mostrar_entradas(request, entrada):
    entrada_obtenida = util.get_entry(entrada)
    if entrada_obtenida != None:
        entrada_html = markdown(entrada_obtenida)
    else:
        return render(request, "encyclopedia/no_encontrada.html",{
            "entrada":"Page Not Found"
        })
        

    return render(request, "encyclopedia/entradas.html",{
        "entrada": entrada_html,
        "titulo": entrada
    })

def search_box(request):
    lista_busqueda = []
    no_resultado = True
    busqueda = request.GET.get('q')
    for entry in util.list_entries():
        if entry.upper() == busqueda.upper():
            return render(request, "encyclopedia/entradas.html",{
                "entrada": markdown(util.get_entry(entry)),
                "titulo": entry
            })
        else:
            if busqueda.upper() in entry.upper() or entry.upper() in busqueda.upper():
                lista_busqueda.append(entry)
                no_resultado = False
                   
    if no_resultado:
        return render(request, "encyclopedia/entradas.html",{
            "entrada": "<h1> Does not match any results!</h1>",
            "titulo": "Search Result",
    })
    
    
    return render(request, "encyclopedia/index.html", {
        "entries": lista_busqueda,
        "titulo": "Search Result",
    })


def random_page(request):
    entrada_random = choice(util.list_entries())
    return redirect('entrada', entrada=entrada_random)

def nueva_entrada(request):
    if request.method == 'POST':
        form = FormNuevaEntrada(request.POST)

        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            entrada = form.cleaned_data.get('entrada')

            for entry in util.list_entries():
                if entry.upper() == titulo.upper():
                    return render(request, "encyclopedia/nueva_entrada.html", {
                        "form": FormNuevaEntrada(request.POST),
                        "error": "The entry already exists, choose another title."
                    })
            
            util.save_entry(titulo, f'# {titulo}\n\n{entrada}')
            return redirect('entrada',entrada=titulo)

    return render(request, "encyclopedia/nueva_entrada.html", {
            "form": FormNuevaEntrada()
    })

def editar_pagina(request, titulo):
    if request.method == 'POST':
        titulo_nuevo = titulo
        form = FormEditarPagina(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            entrada = form.cleaned_data['entrada']

            os.rename(f'./entries/{titulo_nuevo}.md', f'./entries/{titulo}.md')

            util.save_entry(titulo, f'# {titulo}\n\n{entrada}')
            return redirect('entrada',entrada=titulo)

    else:
        entrada_editada = ""
        lista = str(util.get_entry(titulo)).split(sep='\n')
        for i in lista[2:]:
            entrada_editada = i + entrada_editada
        
        form = FormEditarPagina({"titulo":titulo, "entrada":entrada_editada})
        return render(request, "encyclopedia/editar_pagina.html", {
            "form": form,
            })
