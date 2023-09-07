"""
Para usar WTForms-Alchemy e Flask-WTF juntos:
https://wtforms-alchemy.readthedocs.io/en/latest/advanced.html#using-wtforms-alchemy-with-flask-wtf
"""
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

import exts


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return exts.db.session
