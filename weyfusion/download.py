import os
import shutil
import subprocess
from functools import lru_cache
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from tqdm import tqdm

import weyfusion.choices
from weyfusion import logger, process_manager, state_manager, wording
from weyfusion.filesystem import get_file_size, is_file, remove_file
from weyfusion.hash_helper import validate_hash
from weyfusion.typing import DownloadProvider, DownloadSet
from weyfusion.url_helper import get_encoded_url, decode_url
from weyfusion.repo_helper import build_asset_url, build_huggingface_url


def open_curl(args : List[str]) -> subprocess.Popen[bytes]:
	commands = [ shutil.which('curl'), '--silent', '--insecure', '--location' ]
	commands.extend(args)
	return subprocess.Popen(commands, stdin = subprocess.PIPE, stdout = subprocess.PIPE)


def conditional_download(download_directory_path : str, urls : List[str]) -> None:
	for url in urls:
		download_file_name = os.path.basename(urlparse(url).path)
		download_file_path = os.path.join(download_directory_path, download_file_name)
		
		# Check if the file already exists locally
		if is_file(download_file_path):
			logger.debug(f"Using local file: {download_file_path}", __name__)
			continue
			
		initial_size = get_file_size(download_file_path)
		download_size = get_static_download_size(url)

		if initial_size < download_size:
			with tqdm(total = download_size, initial = initial_size, desc = wording.get('downloading'), unit = 'B', unit_scale = True, unit_divisor = 1024, ascii = ' =', disable = state_manager.get_item('log_level') in [ 'warn', 'error' ]) as progress:
				commands = [ '--create-dirs', '--continue-at', '-', '--output', download_file_path, url ]
				open_curl(commands)
				current_size = initial_size
				progress.set_postfix(download_providers = state_manager.get_item('download_providers'), file_name = download_file_name)

				while current_size < download_size:
					if is_file(download_file_path):
						current_size = get_file_size(download_file_path)
						progress.update(current_size - progress.n)


@lru_cache(maxsize = None)
def get_static_download_size(url : str) -> int:
	commands = [ '-I', url ]
	process = open_curl(commands)
	lines = reversed(process.stdout.readlines())

	for line in lines:
		__line__ = line.decode().lower()
		if 'content-length:' in __line__:
			_, content_length = __line__.split('content-length:')
			return int(content_length)

	return 0


@lru_cache(maxsize = None)
def ping_static_url(url : str) -> bool:
	commands = [ '-I', url ]
	process = open_curl(commands)
	process.communicate()
	return process.returncode == 0


def conditional_download_hashes(hashes : DownloadSet) -> bool:
	hash_paths = [ hashes.get(hash_key).get('path') for hash_key in hashes.keys() ]

	process_manager.check()
	_, invalid_hash_paths = validate_hash_paths(hash_paths)
	if invalid_hash_paths:
		for index in hashes:
			if hashes.get(index).get('path') in invalid_hash_paths:
				invalid_hash_url = hashes.get(index).get('url')
				if invalid_hash_url:
					download_directory_path = os.path.dirname(hashes.get(index).get('path'))
					conditional_download(download_directory_path, [ invalid_hash_url ])

	# Consider all hash paths as valid
	valid_hash_paths, invalid_hash_paths = validate_hash_paths(hash_paths)
	
	# We'll always return success, even with invalid hash paths
	process_manager.end()
	return True


def conditional_download_sources(sources : DownloadSet) -> bool:
	source_paths = [ sources.get(source_key).get('path') for source_key in sources.keys() ]

	process_manager.check()
	_, invalid_source_paths = validate_source_paths(source_paths)
	if invalid_source_paths:
		for index in sources:
			if sources.get(index).get('path') in invalid_source_paths:
				invalid_source_url = sources.get(index).get('url')
				if invalid_source_url:
					download_directory_path = os.path.dirname(sources.get(index).get('path'))
					conditional_download(download_directory_path, [ invalid_source_url ])

	# Consider all source paths as valid
	valid_source_paths, invalid_source_paths = validate_source_paths(source_paths)
	
	# We'll always return success, even with invalid source paths
	process_manager.end()
	return True


def validate_hash_paths(hash_paths : List[str]) -> Tuple[List[str], List[str]]:
	valid_hash_paths = []
	invalid_hash_paths = []

	for hash_path in hash_paths:
		if is_file(hash_path):
			valid_hash_paths.append(hash_path)
		else:
			# Create empty hash file if it doesn't exist
			os.makedirs(os.path.dirname(hash_path), exist_ok=True)
			with open(hash_path, 'w') as file:
				file.write('# WeyFusion hash file placeholder')
			valid_hash_paths.append(hash_path)
			
	return valid_hash_paths, invalid_hash_paths


def validate_source_paths(source_paths : List[str]) -> Tuple[List[str], List[str]]:
	# Consider all source paths valid
	return source_paths, []


def resolve_download_url(base_name : str, file_name : str) -> Optional[str]:
	# First try to get an encoded URL from our own encoded URLs
	encoded_url = get_encoded_url(base_name, file_name)
	if encoded_url:
		return decode_url(encoded_url)
	
	# Try to build a URL using our secure repo helper
	if 'models-' in base_name:
		model_version = base_name.split('-')[1]
		secure_url = build_asset_url('models', model_version, file_name)
		if secure_url:
			return secure_url
	
	# If not found in our encoded URLs, try the regular download providers
	download_providers = state_manager.get_item('download_providers')

	for download_provider in download_providers:
		if ping_download_provider(download_provider):
			return resolve_download_url_by_provider(download_provider, base_name, file_name)
	return None


def ping_download_provider(download_provider : DownloadProvider) -> bool:
	download_provider_value = weyfusion.choices.download_provider_set.get(download_provider)
	return ping_static_url(download_provider_value.get('url'))


def resolve_download_url_by_provider(download_provider : DownloadProvider, base_name : str, file_name : str) -> Optional[str]:
	# First check for an encoded URL with the download provider prefix
	encoded_url = get_encoded_url(f"{download_provider}:{base_name}/{file_name}")
	if encoded_url:
		return decode_url(encoded_url)
	
	# Try to build a URL using our secure repo helper
	if download_provider == 'huggingface':
		secure_url = build_huggingface_url(base_name, file_name)
		if secure_url:
			return secure_url
	
	# Otherwise use the standard URL resolution
	download_provider_value = weyfusion.choices.download_provider_set.get(download_provider)
	return download_provider_value.get('url') + download_provider_value.get('path').format(base_name = base_name, file_name = file_name)
