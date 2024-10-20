import urllib.parse
from functools import (
	lru_cache,
)
from typing import Literal

from pydantic_settings import (
	BaseSettings,
	SettingsConfigDict,
)
from sqlmodel import Field


class Settings(BaseSettings):
	db_user: str = ''
	db_password: str = ''
	db_name: str = ''
	db_host: str = 'localhost'
	db_port: int = 3306
	log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = (
		Field('INFO', description='Logging level for the application')
	)

	model_config = SettingsConfigDict(env_prefix='APP_', env_file='.env')

	@property
	def _db_password_escaped_for_alembic(self) -> str:
		"""Return the password escaping the special characters
		as required for Alembic.
		Follows recomendation on https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls.
		"""
		return urllib.parse.quote_plus(self.db_password).replace('%', '%%')

	@property
	def db_dsn_sync(self) -> str:
		return f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}sadffffffffff'


@lru_cache
def get_settings():
	return Settings()
