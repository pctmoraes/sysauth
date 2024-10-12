from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.mfa_controller import MfaController

route = APIRouter(prefix='/sysauth')

async def mfa_controller(db: Session = Depends(get_db)) -> MfaController:
    return MfaController()

@route.get('/code/{id}')
async def get_code(
    id: int,
    mfa_controller: MfaController = Depends(mfa_controller)
):
    try:
        return mfa_controller.get_code(id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))
