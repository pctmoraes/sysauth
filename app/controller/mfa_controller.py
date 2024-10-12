from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.model.mfa_model import MfaModel
from app.database.schema import MfaSchema


class MfaController:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()
        self.db: Session = next(get_db())
    
    def start_scheduler(self) -> None:
        try:
            self.scheduler.add_job(self.update_mfa_code, 'interval', seconds=30)
            self.scheduler.start()
        except Exception as e:
            raise e
    
    def update_mfa_code(self) -> None:
        try:
            mfa_list = self.db.execute(select(MfaModel)).scalars().all()

            for mfa in mfa_list:
                mfa.code = self.get_random_code()
                mfa.been_used = False

            self.db.commit()
        except Exception as e:
            raise e

    def get_random_code(self) -> str:
        try:
            random_int = 0
            random_code = ''

            while len(random_code) < 6:
                random_int = randint(0, 9)
                random_code += str(random_int)
        except Exception as e:
            raise e
        finally:
            return random_code

    def stop_scheduler(self) -> None:
        try:
            self.scheduler.shutdown()
        except Exception as e:
            raise e

    def create(self, mfa: MfaSchema) -> str:
        try:
            if mfa_exists := self.db.execute(
                select(MfaModel)
                .filter(MfaModel.user_id == mfa.user_id)
                .filter(MfaModel.username == mfa.username)
                .filter(MfaModel.app == mfa.app)
            ).scalar():
                return "MFA already registered"

            new_mfa = MfaModel(
                user_id = mfa.user_id,
                app = mfa.app,
                username = mfa.username,
                code = self.get_random_code(),
                been_used = False
            )

            self.db.add(new_mfa)
            self.db.commit()

            return "MFA registered successfully"
        except Exception as e:
            raise e

    def get_code(self, id: int) -> str:
        try:
            return self.db.execute(
                select(MfaModel.code).filter(MfaModel.id == id)
            ).scalar()
        except Exception as e:
            raise e

    def authenticate(self, username: str, code: str) -> bool:
        try:
            if mfa := self.db.execute(
                select(MfaModel)
                .filter(MfaModel.username == username)
                .filter(MfaModel.code == code)
                .filter(MfaModel.been_used == False)
            ).scalar():
                mfa.been_used = True
                self.db.commit()
                return True
            return False
        except Exception as e:
            raise e
