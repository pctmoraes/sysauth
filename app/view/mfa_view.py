from fastapi import APIRouter, HTTPException
from app.controller.mfa_controller import MfaController
from app.database.schema import MfaSchema

mfa_controller = MfaController()
route = APIRouter(prefix='/sysauth/mfa')

@route.post('/create')
async def create(mfa: MfaSchema):
    try:
        return mfa_controller.create(mfa)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.get('/code/{id}')
async def get_code(id: int):
    try:
        return mfa_controller.get_code(id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.post('/authenticate')
async def authenticate(username: str, code: str):
    try:
        return mfa_controller.authenticate(username, code)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))
