"""Testes para rotas de usuários."""
from tests.conftest import client


class TestUserCreation:
    """Testes para criação de usuários."""

    def test_create_user_success(self):
        """Testa criação de usuário com sucesso."""
        response = client.post(
            "/users/",
            json={
                "display_name": "John Doe",
                "public_key": "test_public_key_123",
                "phone_number": "+5511999999999",
                "phone_verified": True
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["display_name"] == "John Doe"
        assert data["public_key"] == "test_public_key_123"
        assert "id" in data
        assert "created_at" in data
        assert "phone_number" not in data  # Não deve retornar no UserOut

    def test_create_user_missing_fields(self):
        """Testa erro quando faltam campos obrigatórios."""
        response = client.post(
            "/users/",
            json={
                "display_name": "John Doe"
                # faltam public_key e phone_number
            }
        )
        assert response.status_code == 422

    def test_create_user_invalid_url(self):
        """Testa validação de URL do avatar."""
        response = client.post(
            "/users/",
            json={
                "display_name": "John Doe",
                "public_key": "test_public_key_123",
                "phone_number": "+5511999999999",
                "avatar_url": "invalid-url"
            }
        )
        assert response.status_code == 422


class TestUserRetrieval:
    """Testes para busca de usuários."""

    def test_get_user_success(self, test_user):
        """Testa busca de usuário com sucesso."""
        user_id = test_user["id"]
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["display_name"] == "John Doe"
        assert data["public_key"] == "test_public_key_123"

    def test_get_nonexistent_user(self):
        """Testa erro ao buscar usuário inexistente."""
        # ID válido do MongoDB mas que não existe
        fake_id = "507f1f77bcf86cd799439011"
        response = client.get(f"/users/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_get_user_invalid_id(self):
        """Testa erro com ID inválido."""
        response = client.get("/users/invalid_id")
        assert response.status_code == 404


class TestUserUpdate:
    """Testes para atualização de usuários."""

    def test_update_user_success(self, test_user):
        """Testa atualização de usuário com sucesso."""
        user_id = test_user["id"]
        
        response = client.put(
            f"/users/{user_id}",
            json={
                "display_name": "Jane Smith",
                "avatar_url": "https://example.com/avatar.jpg"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["display_name"] == "Jane Smith"
        assert data["public_key"] == "test_public_key_123"  # Não mudou

    def test_update_user_partial(self, test_user):
        """Testa atualização parcial de usuário."""
        user_id = test_user["id"]
        
        response = client.put(
            f"/users/{user_id}",
            json={
                "display_name": "New Name"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["display_name"] == "New Name"

    def test_update_nonexistent_user(self):
        """Testa erro ao atualizar usuário inexistente."""
        fake_id = "507f1f77bcf86cd799439011"
        response = client.put(
            f"/users/{fake_id}",
            json={
                "display_name": "New Name"
            }
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_update_user_invalid_id(self):
        """Testa erro ao atualizar com ID inválido."""
        response = client.put(
            "/users/invalid_id",
            json={
                "display_name": "New Name"
            }
        )
        assert response.status_code == 404


class TestUserDeletion:
    """Testes para deleção de usuários."""

    def test_delete_user_success(self, test_user):
        """Testa deleção de usuário com sucesso."""
        user_id = test_user["id"]
        
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Verifica que o usuário foi deletado
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_user(self):
        """Testa erro ao deletar usuário inexistente."""
        fake_id = "507f1f77bcf86cd799439011"
        response = client.delete(f"/users/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user_twice(self, test_user):
        """Testa erro ao deletar usuário já deletado."""
        user_id = test_user["id"]
        
        # Primeira deleção
        response1 = client.delete(f"/users/{user_id}")
        assert response1.status_code == 204
        
        # Segunda deleção
        response2 = client.delete(f"/users/{user_id}")
        assert response2.status_code == 404

    def test_delete_user_invalid_id(self):
        """Testa erro ao deletar com ID inválido."""
        response = client.delete("/users/invalid_id")
        assert response.status_code == 404


class TestHealthEndpoints:
    """Testes para endpoints de saúde da API."""

    def test_root_endpoint(self):
        """Testa endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "TalkHub API"
        assert data["status"] == "running"

    def test_health_endpoint(self):
        """Testa endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
