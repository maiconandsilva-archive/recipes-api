import pytest

from models.usuario import Usuario


def test_create_user(client):
    usuario = Usuario(email='test@test.com', senha='OK')
    usuario.save(commit=True)


def test_get_user_and_delete(client):
    usuario = Usuario.query.filter(
        Usuario.email == 'test@test.com').one_or_none()
    assert usuario is not None, 'Usuario nao foi inserido!'
    usuario.delete(commit=True)
