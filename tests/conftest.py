"""Configuração compartilhada para todos os testes."""
import pytest
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Define ambiente de teste antes de importar
os.environ["TESTING"] = "true"

from fastapi.testclient import TestClient
from mongomock import MongoClient as MockMongoClient

# Cliente de teste MongoDB em memória usando mongomock
test_client_mongo = MockMongoClient()
test_db = test_client_mongo["test_db"]


def override_get_collection(collection_name: str):
    """Override da dependency para usar banco de testes."""
    return test_db[collection_name]


# Importa e configura após definir o override
from database.mongodb import MongoDB
MongoDB.get_collection = staticmethod(override_get_collection)

from main import app
# Cria o cliente de teste FastAPI
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Limpa o banco de dados antes de cada teste."""
    # Limpa todas as coleções
    for collection_name in test_db.list_collection_names():
        test_db[collection_name].delete_many({})
    yield
    # Limpa novamente após o teste
    for collection_name in test_db.list_collection_names():
        test_db[collection_name].delete_many({})


@pytest.fixture
def test_user():
    """Fixture para criar um usuário de teste."""
    response = client.post(
        "/users/",
        json={
            "display_name": "John Doe",
            "public_key": "test_public_key_123",
            "phone_number": "+5511999999999",
            "phone_verified": True
        }
    )
    return response.json()


@pytest.fixture
def test_user_data():
    """Fixture com dados de usuário para criar."""
    return {
        "display_name": "Jane Smith",
        "public_key": "test_public_key_456",
        "phone_number": "+5511888888888",
        "phone_verified": True
    }
