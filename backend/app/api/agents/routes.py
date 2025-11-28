from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_agents():
    return {"msg": "agents router works"}
