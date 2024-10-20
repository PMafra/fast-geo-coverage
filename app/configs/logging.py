import logging
import logging.config
from typing import Any

from app.configs.settings import (
	get_settings,
)


def get_logging_config() -> dict[str, Any]:
	"""
	Returns the logging configuration dictionary.
	"""
	settings = get_settings()
	log_level = settings.log_level.upper()

	return {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'standard': {
				'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
				'datefmt': '%Y-%m-%d %H:%M:%S',
			},
			'detailed': {
				'format': (
					'%(asctime)s [%(levelname)s] %(name)s '
					'%(filename)s:%(lineno)d: %(message)s'
				),
				'datefmt': '%Y-%m-%d %H:%M:%S',
			},
		},
		'handlers': {
			'console': {
				'level': log_level,
				'class': 'logging.StreamHandler',
				'formatter': 'standard',
			},
		},
		'loggers': {
			'': {  # Root logger
				'handlers': ['console'],
				'level': 'DEBUG',
				'propagate': True,
			},
			'uvicorn.error': {
				'level': 'INFO',
				'handlers': ['console'],
				'propagate': False,
			},
			'uvicorn.access': {
				'level': 'INFO',
				'handlers': ['console'],
				'propagate': False,
			},
		},
	}


def setup_logging():
	"""
	Configures the logging system using the configuration dictionary.
	"""
	logging_config = get_logging_config()
	logging.config.dictConfig(logging_config)
