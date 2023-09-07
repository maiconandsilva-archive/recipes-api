
from typing import Union
from wtforms.fields.core import Field

from .base import ModelForm
from models.receitas.receita import Receita


class ReceitaForm(ModelForm):
    class Meta:
        model = Receita
