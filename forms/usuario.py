
from .base import ModelForm
import models.usuario as usuario


class UsuarioForm(ModelForm):
    class Meta:
        model = usuario.Usuario
