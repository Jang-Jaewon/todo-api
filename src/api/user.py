from fastapi import APIRouter


router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def sign_up_user():
    return True
