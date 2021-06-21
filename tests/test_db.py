import pytest
import sys

from models.usuario import *
from models.receitas import *


@pytest.fixture
def usuario_teste():
    yield Usuario.query.filter(Usuario.email == 'test@test.com').one_or_none()

@pytest.fixture
def receita():
    yield Receita.query.filter(Receita.nome == 'Arroz Doce').one_or_none()


def test_create_user():
    usuario_teste = Usuario(
        nome='Test Testing',
        email='test@test.com',
        senha='1234567890'
    )
    usuario_teste.save(commit=True)


def test_create_receita(usuario_teste):
    receita = Receita(
        nome='Arroz Doce',
        descricao='Uma delícia, esse é o verdadeiro arroz doce.',
        modo_preparo='Arroz Doce',
        criador=usuario_teste,
        ingredientes = [Ingrediente(
            nome = 'Leite Condensado',
            quantidade = 1,
            unidade_medida = UnidadeMedida(
                id='LATA', nome='Lata', descricao='DESCRICAO'),
        )],
        categorias = [Categoria(
            nome='Doces e Sobremesas', descricao='Pudins, mousses etc')]
    )
    receita.save(commit=True)


def test_get_delete_fixtures_not_none(receita, usuario_teste):
    assert receita is not None and usuario_teste is not None, \
           'Execute os testes create antes'


def test_get_receita(receita, usuario_teste):
    assert receita.nome == 'Arroz Doce'
    assert receita.criador == usuario_teste
    assert len(receita.ingredientes) == 1
    assert len(receita.categorias) == 1
    assert receita.id == receita.ingredientes[0].receita.id
    assert receita.id == receita.categorias[0].receitas[0].id


def test_get_user(usuario_teste):
    assert usuario_teste.nome == 'Test Testing'
    assert usuario_teste.senha == '1234567890'


def test_delete_user(usuario_teste):
    usuario_teste.delete(commit=True)


def test_criador_receita_none(receita):
    assert receita.criador is None


def test_delete_receita(receita):
    receita.delete(commit=True)

