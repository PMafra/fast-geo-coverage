from typing import Annotated

from fastapi import Depends
from sqlmodel import (
	Session,
	create_engine,
)

from app.configs.settings import (
	get_settings,
)

settings = get_settings()
mysql_url = settings.db_dsn_sync

engine = create_engine(mysql_url, echo=True)


def get_db_session():
	with Session(engine) as session:
		yield session


DbSessionDep = Annotated[Session, Depends(get_db_session)]
