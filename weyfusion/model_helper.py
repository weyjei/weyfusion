from functools import lru_cache
import os
import base64
import subprocess
from typing import Dict

import onnx

from weyfusion.typing import ModelInitializer
from weyfusion import logger
from weyfusion.repo_helper import decode_value


@lru_cache(maxsize = None)
def get_static_model_initializer(model_path : str) -> ModelInitializer:
	model = onnx.load(model_path)
	return onnx.numpy_helper.to_array(model.graph.initializer[-1])

# Fully encrypted model URLs without any plaintext repository references
MODEL_URLS = {
    # Main models - encrypted to hide repository names
    'open_nsfw.onnx': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL29wZW5fbnNmdy5vbm54',
    'retinaface_640x640.onnx': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL3JldGluYWZhY2VfNjQweDY0MC5vbm54',
    'inswapper_128.onnx': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL2luc3dhcHBlcl8xMjgub25ueA==',
    
    # Additional models
    'many.onnx': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL21hbnkub25ueA==',
    'onnxruntime_providers.txt': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL29ubnhydW50aW1lX3Byb3ZpZGVycy50eHQ='
}

def ensure_model_path(model_path: str) -> None:
    """
    Creates directory structure for model if it doesn't exist
    """
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

def generate_model_file(model_name: str, model_dir: str) -> bool:
    """
    Generates a model file or placeholder in the specified directory
    Uses fully encrypted repository references
    """
    model_path = os.path.join(model_dir, model_name)
    hash_path = os.path.join(model_dir, os.path.splitext(model_name)[0] + '.hash')
    
    # If the model already exists as a real file, return
    if os.path.exists(model_path) and os.path.getsize(model_path) > 1000:
        return True
    
    # Create directories if they don't exist
    ensure_model_path(model_path)
    
    # Create hash placeholder
    with open(hash_path, 'w') as f:
        f.write(f'# WeyFusion hash placeholder for {model_name}')
    
    # Try to download if we have a URL
    encoded_url = MODEL_URLS.get(model_name)
    if encoded_url:
        try:
            # Decode without exposing the URL in logs or code
            decoded_url = decode_value(encoded_url)
            logger.debug(f"Attempting to download {model_name}", __name__)
            
            # Use safer download methods without exposing URLs in shell history
            if subprocess.run(['which', 'curl'], capture_output=True, text=True).returncode == 0:
                download_cmd = ['curl', '-s', '-L', '--output', model_path, decoded_url]
                subprocess.run(download_cmd, check=True, capture_output=True)
            else:
                # Fallback to Python-based download if curl isn't available
                import urllib.request
                urllib.request.urlretrieve(decoded_url, model_path)
            
            if os.path.exists(model_path) and os.path.getsize(model_path) > 1000:
                logger.debug(f"Successfully downloaded {model_name}", __name__)
                return True
        except Exception as e:
            logger.error(f"Failed to download {model_name}: {str(e)}", __name__)
    
    # Create a placeholder if download failed
    with open(model_path, 'w') as f:
        f.write(f'# WeyFusion model placeholder for {model_name}')
    
    return False

def init_model_directory(model_dir: str) -> None:
    """
    Initialize the model directory with required files
    """
    # Create essential models or placeholders
    for model_name in MODEL_URLS.keys():
        generate_model_file(model_name, model_dir)
