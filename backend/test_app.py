from unittest.mock import MagicMock

import pytest

import app as backend

FAKE_DB_URL = "postgresql://teste:teste@localhost:5432/teste"


@pytest.fixture
def fake_db(monkeypatch):
    """Substitui o psycopg2.connect por um mock, para testar sem Postgres."""
    monkeypatch.setenv("DATABASE_URL", FAKE_DB_URL)

    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor

    connect = MagicMock(return_value=conn)
    monkeypatch.setattr(backend.psycopg2, "connect", connect)

    return {"connect": connect, "conn": conn, "cursor": cursor}


@pytest.fixture
def client():
    backend.app.config["TESTING"] = True
    with backend.app.test_client() as client:
        yield client


def test_usuarios_retorna_200_e_json(client, fake_db):
    fake_db["cursor"].fetchall.return_value = [
        (1, "Ana Silva", "ana.silva@email.com", "gatinho123"),
        (2, "Bruno Costa", "bruno.costa@email.com", "pizza4ever"),
    ]

    resposta = client.get("/usuarios")

    assert resposta.status_code == 200
    assert resposta.is_json
    assert resposta.get_json() == [
        [1, "Ana Silva", "ana.silva@email.com", "gatinho123"],
        [2, "Bruno Costa", "bruno.costa@email.com", "pizza4ever"],
    ]


def test_usuarios_tabela_vazia_retorna_lista_vazia(client, fake_db):
    fake_db["cursor"].fetchall.return_value = []

    resposta = client.get("/usuarios")

    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_usuarios_executa_select_na_tabela_usuarios(client, fake_db):
    fake_db["cursor"].fetchall.return_value = []

    client.get("/usuarios")

    fake_db["cursor"].execute.assert_called_once_with("SELECT * FROM usuarios")


def test_conexao_usa_variavel_database_url(client, fake_db):
    fake_db["cursor"].fetchall.return_value = []

    client.get("/usuarios")

    fake_db["connect"].assert_called_once_with(FAKE_DB_URL)


def test_conexao_e_fechada_apos_consulta(client, fake_db):
    fake_db["cursor"].fetchall.return_value = []

    client.get("/usuarios")

    fake_db["conn"].close.assert_called_once()


def test_cors_liberado_para_o_frontend(client, fake_db):
    fake_db["cursor"].fetchall.return_value = []

    resposta = client.get(
        "/usuarios",
        headers={"Origin": "https://devops-frontend-ys6u.onrender.com"},
    )

    assert "Access-Control-Allow-Origin" in resposta.headers


def test_rota_inexistente_retorna_404(client):
    resposta = client.get("/rota-que-nao-existe")

    assert resposta.status_code == 404
