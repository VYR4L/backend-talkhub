"""Testes para rotas de chats."""
from tests.conftest import client


class TestChatCreation:
    """Testes para criação de chats."""

    def test_create_chat_success(self):
        """Testa criação de chat com sucesso."""
        response = client.post(
            "/chats/",
            json={
                "type": "private",
                "participant_ids": ["user1", "user2"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "private"
        assert data["participant_ids"] == ["user1", "user2"]
        assert "id" in data
        assert "created_at" in data

    def test_create_group_chat_success(self):
        """Testa criação de chat em grupo com sucesso."""
        response = client.post(
            "/chats/",
            json={
                "type": "group",
                "participant_ids": ["user1", "user2", "user3"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "group"
        assert len(data["participant_ids"]) == 3

    def test_create_chat_missing_fields(self):
        """Testa erro quando faltam campos obrigatórios."""
        response = client.post(
            "/chats/",
            json={
                "type": "private"
                # falta participant_ids
            }
        )
        assert response.status_code == 422


class TestChatRetrieval:
    """Testes para busca de chats."""

    def test_get_chat_success(self):
        """Testa busca de chat com sucesso."""
        # Criar um chat primeiro
        create_response = client.post(
            "/chats/",
            json={
                "type": "private",
                "participant_ids": ["user1", "user2"]
            }
        )
        chat_id = create_response.json()["id"]
        
        # Buscar o chat
        response = client.get(f"/chats/{chat_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == chat_id
        assert data["type"] == "private"
        assert data["participant_ids"] == ["user1", "user2"]

    def test_get_nonexistent_chat(self):
        """Testa erro ao buscar chat inexistente."""
        fake_id = "507f1f77bcf86cd799439011"
        response = client.get(f"/chats/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Chat not found"

    def test_get_chat_invalid_id(self):
        """Testa erro com ID inválido."""
        response = client.get("/chats/invalid_id")
        assert response.status_code == 404


class TestChatUpdate:
    """Testes para atualização de chats."""

    def test_update_chat_success(self):
        """Testa atualização de chat com sucesso."""
        # Criar um chat
        create_response = client.post(
            "/chats/",
            json={
                "type": "private",
                "participant_ids": ["user1", "user2"]
            }
        )
        chat_id = create_response.json()["id"]
        
        # Atualizar o chat
        response = client.put(
            f"/chats/{chat_id}",
            json={
                "type": "group",
                "participant_ids": ["user1", "user2", "user3"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "group"
        assert len(data["participant_ids"]) == 3

    def test_update_chat_partial(self):
        """Testa atualização parcial de chat."""
        # Criar um chat
        create_response = client.post(
            "/chats/",
            json={
                "type": "private",
                "participant_ids": ["user1", "user2"]
            }
        )
        chat_id = create_response.json()["id"]
        
        # Atualizar apenas o tipo
        response = client.put(
            f"/chats/{chat_id}",
            json={
                "type": "group"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "group"
        assert data["participant_ids"] == ["user1", "user2"]  # Não mudou

    def test_update_nonexistent_chat(self):
        """Testa erro ao atualizar chat inexistente."""
        fake_id = "507f1f77bcf86cd799439011"
        response = client.put(
            f"/chats/{fake_id}",
            json={
                "type": "group"
            }
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Chat not found"

    def test_update_chat_invalid_id(self):
        """Testa erro ao atualizar com ID inválido."""
        response = client.put(
            "/chats/invalid_id",
            json={
                "type": "group"
            }
        )
        assert response.status_code == 404


class TestChatDeletion:
    """Testes para deleção de chats."""

    def test_delete_chat_success(self):
        """Testa deleção de chat com sucesso."""
        # Criar um chat
        create_response = client.post(
            "/chats/",
            json={
                "type": "private",
                "participant_ids": ["user1", "user2"]
            }
        )
        chat_id = create_response.json()["id"]
        
        # Deletar o chat
        response = client.delete(f"/chats/{chat_id}")
        assert response.status_code == 204

        # Verificar que foi deletado
        get_response = client.get(f"/chats/{chat_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_chat(self):
        """Testa erro ao deletar chat inexistente."""
        fake_id = "507f1f77bcf86cd799439011"
        response = client.delete(f"/chats/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Chat not found"

    def test_delete_chat_twice(self):
        """Testa erro ao deletar chat já deletado."""
        # Criar um chat
        create_response = client.post(
            "/chats/",
            json={
                "type": "private",
                "participant_ids": ["user1", "user2"]
            }
        )
        chat_id = create_response.json()["id"]
        
        # Primeira deleção
        response1 = client.delete(f"/chats/{chat_id}")
        assert response1.status_code == 204
        
        # Segunda deleção
        response2 = client.delete(f"/chats/{chat_id}")
        assert response2.status_code == 404

    def test_delete_chat_invalid_id(self):
        """Testa erro ao deletar com ID inválido."""
        response = client.delete("/chats/invalid_id")
        assert response.status_code == 404


class TestChatList:
    """Testes para listagem de chats."""

    def test_list_chats_empty(self):
        """Testa listagem de chats quando não há nenhum."""
        response = client.get("/chats/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_chats_with_data(self):
        """Testa listagem de chats com dados."""
        # Criar alguns chats
        client.post(
            "/chats/",
            json={
                "type": "private",
                "participant_ids": ["user1", "user2"]
            }
        )
        client.post(
            "/chats/",
            json={
                "type": "group",
                "participant_ids": ["user1", "user2", "user3"]
            }
        )
        
        # Listar chats
        response = client.get("/chats/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["type"] in ["private", "group"]
        assert data[1]["type"] in ["private", "group"]
