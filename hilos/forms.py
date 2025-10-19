from django import forms
from .models import Hilo, Respuesta ,Categoria , Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username'] 

class HiloForm(forms.ModelForm):
    class Meta:
        model = Hilo
        fields = ['titulo', 'categoria', 'contenido', 'imagen']

    def clean_titulo(self):
        titulo = self.cleaned_data.get("titulo")
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo

    def clean_contenido(self):
        contenido = self.cleaned_data.get("contenido")
        if len(contenido.strip()) == 0:
            raise forms.ValidationError("El contenido no puede estar vacío.")
        return contenido

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ["contenido"]

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre").strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

class CustomClearableFileInput(forms.ClearableFileInput):
    initial_text = ""           
    input_text = ""            
    clear_checkbox_label = ""  

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['avatar', 'apodo', 'bio', 'ubicacion', 'email']
        widgets = {
            'avatar': CustomClearableFileInput(),
        }