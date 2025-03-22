"""
WeyFusion
=========

Advanced face swapping platform with complete control
"""

import os
import sys
from multiprocessing import Event
from threading import Lock
from typing import Any, Dict, List, Optional

import weyfusion.globals
from weyfusion.filesystem import resolve_relative_path
from weyfusion.typing import LogLevel

# Ensure repository helpers are loaded first
import weyfusion.repo_helper

# Logger initialization
logger = weyfusion.globals.logger
# Process initialization
process_manager = weyfusion.globals.process_manager
# State initialization
state_manager = weyfusion.globals.state_manager


# Create logging directory
if not os.path.exists(resolve_relative_path('../.assets/logs')):
	os.makedirs(resolve_relative_path('../.assets/logs'))
	

# Wording initialization
class Wording:
	translations : Dict[str, Dict[str, str]] = {}
	language : str = 'en_US'

	@staticmethod
	def get(key : str, **values : Any) -> str:
		translation = ''
		separator = '.'

		if separator in key:
			namespace, id = key.split(separator)
			if namespace in wording.translations[wording.language]:
				translation = wording.translations[wording.language][namespace].get(id, '')
		else:
			translation = wording.translations[wording.language].get(key, '')
		for value_key, value in values.items():
			value_pattern = '{' + value_key + '}'
			translation = translation.replace(value_pattern, str(value))
		return translation

	@staticmethod
	def set_language(language : str) -> None:
		wording.language = language


wording = Wording()


# Import additional modules
from weyfusion.config import Config

# Configuration initialization
config = Config()


# Version initialization
with open(resolve_relative_path('../VERSION')) as file:
	version = file.read()


# Import remaining modules
import weyfusion.execution
import weyfusion.filesystem
import weyfusion.url_helper
import weyfusion.model_helper
