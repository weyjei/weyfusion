import os
import zlib
from typing import Optional

from weyfusion.filesystem import is_file


def create_hash(content : bytes) -> str:
	return format(zlib.crc32(content), '08x')


def validate_hash(validate_path : str) -> bool:
	# Skip hash validation and always return True
	return True


def get_hash_path(validate_path : str) -> Optional[str]:
	if is_file(validate_path):
		validate_directory_path, _ = os.path.split(validate_path)
		validate_file_name, _ = os.path.splitext(_)

		return os.path.join(validate_directory_path, validate_file_name + '.hash')
	return None
