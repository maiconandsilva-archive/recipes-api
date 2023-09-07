from uuid import uuid4
import pytest


from models.usuario import *
from models.receitas import *


@pytest.fixture
def usuario_teste():
    yield Usuario.query.filter(Usuario.email.like('test%@test.com')).first()


@pytest.fixture
def receita():
    yield Receita.query.filter(Receita.nome == 'Arroz Doce').one_or_none()


def test_create_user():
    usuario_teste = Usuario(
        nome='Test Testing',
        email=f'{uuid4()!s}@test.com',
        senha='1234567890'
    )
    usuario_teste.save(commit=True)


def test_create_receita(usuario_teste):
    receita = Receita(
        nome='Doce',
        descricao='Uma delícia, esse é o verdadeiro arroz doce.',
        modo_preparo=[
            'Cozinhe o arroz no leite, juntamente com a canela (utilize uma '
                'panela grande para que o leite ferva e não derrame).',
            'Após 20 minutos, mexa de tempos em tempos.',
            'Acrescente o açúcar e deixe por 20 minutos.',
            'Logo em seguida, acrescente o leite condensado e deixe por mais '
                '20 minutos.',
            'Coloque em uma linda travessa.',
        ],
        tempo_preparo=45,
        criador=usuario_teste,
        rendimento_porcoes=5,
        ingredientes = [Ingrediente(
            nome = 'Leite Condensado',
            quantidade = 1,
            unidade_medida = UnidadeMedida(
                id=f'{uuid4()!s}LATA', nome='Lata', descricao='DESCRICAO'),
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
    assert len(receita.bp_ingredientes) == 1
    assert len(receita.bp_categorias) == 1
    assert receita.id == receita.bp_ingredientes[0].receita.id
    assert receita.id == receita.bp_categorias[0].bp_receitas[0].id


def test_get_user(usuario_teste):
    assert usuario_teste.nome == 'Test Testing'
    assert usuario_teste.senha == '1234567890'


def test_delete_user(usuario_teste):
    usuario_teste.delete(commit=True)


def test_criador_receita_none(receita):
    assert receita.criador is None


def test_delete_receita(receita):
    receita.delete(commit=True)

