from fastapi import Depends, APIRouter, HTTPException, status
from controllers.user_controller import UserController
from models.user import UserCreate, UserUpdate, UserOut
from database.mongodb import MongoDB


router = APIRouter(prefix="/users", tags=["users"])


def get_users_collection():
    """Dependency para obter a coleção de usuários."""
    return MongoDB.get_collection("users")


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, collection=Depends(get_users_collection)):
    user_controller = UserController(collection)
    user = user_controller.create_user(user_create)
    return UserOut(**user.model_dump())


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, collection=Depends(get_users_collection)):
    user_controller = UserController(collection)
    user = user_controller.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user.model_dump())


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_update: UserUpdate, collection=Depends(get_users_collection)):
    user_controller = UserController(collection)
    user = user_controller.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user.model_dump())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, collection=Depends(get_users_collection)):
    user_controller = UserController(collection)
    deleted = user_controller.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None
