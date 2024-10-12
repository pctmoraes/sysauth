from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.model.mfa_model import MfaModel


class MfaController:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()
        self.db: Session = next(get_db())
    
    def start_scheduler(self):
        try:
            self.scheduler.add_job(self.update_mfa_code, 'interval', seconds=30)
            self.scheduler.start()
        except Exception as e:
            raise e
    
    def update_mfa_code(self):
        try:
            mfa_list = self.db.execute(select(MfaModel)).scalars().all()

            for mfa in mfa_list:
                mfa.code = self.get_random_code()

            self.db.commit()
        except Exception as e:
            raise e

    def get_random_code(self):
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

    def stop_scheduler(self):
        try:
            self.scheduler.shutdown()
        except Exception as e:
            raise e
