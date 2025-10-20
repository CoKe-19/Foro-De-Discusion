from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import HiloForm, UsuarioForm, RespuestaForm ,CategoriaForm , PerfilForm
from .models import Hilo , Respuesta , Categoria , Like , Perfil , Video
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q, Count , Exists, OuterRef
from django.contrib import messages 
import re

User = get_user_model() 

def pagina_principal(request):
    categorias = Categoria.objects.prefetch_related('hilos__usuario').all()
    usuarios_destacados = User.objects.annotate(
        total_hilos=Count('hilos')
    ).order_by('-total_hilos')[:10]
    hilos_recientes = Hilo.objects.select_related('usuario', 'categoria').order_by('-fecha')[:10]
    videos = Video.objects.order_by('-fecha_publicacion')[:2]  

    return render(request, 'hilos/index.html', {
        'categorias': categorias,
        'usuarios_destacados': usuarios_destacados,
        'hilos_recientes': hilos_recientes,
        'videos': videos
    })
def toggle_like(request, respuesta_id):
    if not request.user.is_authenticated:
        return redirect('login')
    respuesta = get_object_or_404(Respuesta, id=respuesta_id)
    like_existente = Like.objects.filter(usuario=request.user, respuesta=respuesta)
    if like_existente.exists():
        like_existente.delete() 
    else:
        Like.objects.create(usuario=request.user, respuesta=respuesta)  
    return redirect('detalle_hilo', hilo_id=respuesta.hilo.id)

@login_required
def registrar_hilo(request):
    if request.method == "POST":
        form = HiloForm(request.POST, request.FILES)
        if form.is_valid():
            hilo = form.save(commit=False)
            hilo.usuario = request.user
            hilo.save()
            messages.success(request, "Hilo creado correctamente.")
            return redirect("mis_hilos")
        else:
            messages.error(request, "No se pudo crear el hilo. Revisa los campos e inténtalo nuevamente.")
    else:
        form = HiloForm()

    categorias = Categoria.objects.all()
    return render(request, "hilos/form.html", {"form": form, "categorias": categorias})

@login_required(login_url="login")
def lista_hilos(request):
    query = request.GET.get("q")
    hilos = Hilo.objects.all()
    if query:
        hilos = hilos.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)
        )
    return render(request, 'hilos/lista_hilos.html', {
        'hilos': hilos,
        'query': query
    })

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.") 
            return redirect('login')
        else:
            messages.error(request, "Hubo un error al registrar el usuario.")  
    else:
        form = UsuarioForm()
    return render(request, 'hilos/form.html', {
        'form': form,
        'titulo': 'Registro de Usuario' 
    })

def detalle_hilo(request, hilo_id):
    hilo = Hilo.objects.select_related('categoria', 'usuario').prefetch_related('respuestas__usuario').get(id=hilo_id)
    respuestas = hilo.respuestas.all().order_by('fecha')
    if request.user.is_authenticated:
        respuestas = respuestas.annotate(
            ya_dio_like=Exists(
                Like.objects.filter(usuario=request.user, respuesta=OuterRef('pk'))
            )
        )
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            Respuesta.objects.create(
                hilo=hilo,
                usuario=request.user,
                contenido=contenido
            )
            return redirect('detalle_hilo', hilo_id=hilo.id)
    return render(request, 'hilos/detalle_hilo.html', {
        'hilo': hilo,
        'respuestas': respuestas
    })

@login_required(login_url="login")
def lista_usuarios(request):
    usuarios = (
        User.objects
        .select_related('perfil')
        .annotate(
            total_hilos=Count('hilos', distinct=True),
            total_respuestas=Count('respuestas', distinct=True),  
        )
        .order_by('username')
    )
    return render(request, 'hilos/lista_usuarios.html', {'usuarios': usuarios})

@login_required(login_url="login")
def eliminar_hilo(request, hilo_id):
    hilo = get_object_or_404(Hilo, id=hilo_id)
    if request.user != hilo.usuario and not request.user.is_staff:
        return HttpResponse("No tienes permiso para eliminar este hilo.", status=403)
    if request.method == 'POST':
        hilo.delete()
        messages.success(request, "Hilo eliminado correctamente.")
        if request.user.is_staff:
            return redirect('lista_hilos') 

    return render(request, 'hilos/confirm_delete.html', {'hilo': hilo})

@login_required
def mis_hilos(request):
    hilos = Hilo.objects.filter(usuario=request.user).select_related('categoria')
    return render(request, 'hilos/mis_hilos.html', {'hilos': hilos})

@login_required
def editar_hilo(request, hilo_id):
    hilo = get_object_or_404(Hilo, id=hilo_id, usuario=request.user)

    if request.method == 'POST':
        form = HiloForm(request.POST, request.FILES, instance=hilo) 
        if form.is_valid():
            form.save()
            messages.success(request, "Hilo actualizado correctamente.")
            return redirect('mis_hilos')
        else:
            messages.error(request, "Hubo un error al actualizar el hilo.")
    else:
        form = HiloForm(instance=hilo)
    
    return render(request, 'hilos/form.html', {
        'form': form,
        'titulo': 'Editar Hilo'
    })

@login_required(login_url="login")
def administrar_hilos(request):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso para acceder a esta página.", status=403)
    hilos = Hilo.objects.all().order_by('-fecha')
    return render(request, 'hilos/administrar_hilos.html', {'hilos': hilos})

@login_required(login_url="login")
def eliminar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id=respuesta_id)
    if request.user != respuesta.usuario and not request.user.is_staff:
        return HttpResponse("No tienes permiso para eliminar esta respuesta.", status=403)
    if request.method == 'POST':
        respuesta.delete()
        messages.success(request, "Respuesta eliminada correctamente.")  
        return redirect('detalle_hilo', hilo_id=respuesta.hilo.id)
    return render(request, 'hilos/confirm_delete.html', {'respuesta': respuesta})

@login_required
def editar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id=respuesta_id, usuario=request.user)
    if request.method == "POST":
        form = RespuestaForm(request.POST, instance=respuesta)
        if form.is_valid():
            form.save()
            messages.success(request, "Respuesta editada correctamente")
            return redirect("detalle_hilo", hilo_id=respuesta.hilo.id)
    else:
        form = RespuestaForm(instance=respuesta)

    return render(request, "hilos/form.html", {
        "form": form,
        "titulo": "Editar Respuesta"
    })
    
@login_required(login_url="login")
def lista_categorias(request):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso para acceder a esta página.", status=403)
    categorias = Categoria.objects.all()
    return render(request, 'hilos/lista_categorias.html', {'categorias': categorias})


@login_required(login_url="login")
def crear_categoria(request):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso.", status=403)
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect('lista_categorias')
        else:
            messages.error(request, "Error al crear categoría.")
    else:
        form = CategoriaForm()
    return render(request, 'hilos/form.html', {
        'form': form,
        'titulo': 'Crear Categoría'
    })

@login_required(login_url="login")
def editar_categoria(request, categoria_id):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso.", status=403)
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('lista_categorias')
        else:
            messages.error(request, "Error al actualizar categoría.")
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'hilos/form.html', {
        'form': form,
        'titulo': 'Editar Categoría'
    })

@login_required(login_url="login")
def eliminar_categoria(request, categoria_id):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso.", status=403)
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if categoria.hilos.exists():
        messages.error(request, "No se puede eliminar la categoría porque tiene hilos asociados.")
        return redirect('lista_categorias')
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect('lista_categorias')
    return render(request, 'hilos/confirm_delete_categoria.html', {'categoria': categoria})

def ver_perfil(request, username):
    user = get_object_or_404(User, username=username)
    perfil, created = Perfil.objects.get_or_create(user=user)
    return render(request, 'hilos/ver_perfil.html', {'perfil': perfil})

@login_required
def completar_perfil(request):
    perfil = request.user.perfil
    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('ver_perfil', username=request.user.username)
    else:
        form = PerfilForm(instance=perfil)
        return render(request, 'hilos/form.html', {
            'form': form,
            'titulo': 'Editar Perfil',
            'boton_texto': 'Guardar cambios',
            'volver_url': 'ver_perfil',
            'volver_args': [request.user.username], 
        })

def buscar(request):
    query = request.GET.get('query', '')
    resultados = []
    if query:
        resultados = Hilo.objects.filter(Q(titulo__icontains=query))
        for hilo in resultados:
            hilo.titulo_resaltado = re.sub(
                f'({re.escape(query)})',
                r'<mark>\1</mark>',
                hilo.titulo,
                flags=re.IGNORECASE
            )
    return render(request, 'hilos/buscar.html', {'resultados': resultados, 'query': query})

def filtrar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    hilos = categoria.hilos.all() 
    return render(request, 'hilos/lista_hilos.html', {
        'categoria': categoria,
        'hilos': hilos
    })

def faq(request):
    return render(request, 'hilos/faq.html')

def reglas(request):
    return render(request, 'hilos/reglas.html')

def acuerdo(request):
    return render(request, 'hilos/acuerdo.html')

def quienes_somos(request):
    return render(request, 'hilos/quienes_somos.html')

def guias(request):
    return render(request, 'hilos/guias.html')
