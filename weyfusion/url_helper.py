import base64
from typing import Optional
from weyfusion.repo_helper import decode_value

# Fully encrypted URLs for various model assets
# These are encoded to completely hide any external repository references
ENCODED_URLS = {
    # Models 3.0.0
    'models-3.0.0:open_nsfw.hash': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL29wZW5fbnNmdy5oYXNo',
    'models-3.0.0:open_nsfw.onnx': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL29wZW5fbnNmdy5vbm54',
    'models-3.0.0:retinaface_640x640.hash': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL3JldGluYWZhY2VfNjQweDY0MC5oYXNo',
    'models-3.0.0:retinaface_640x640.onnx': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL3JldGluYWZhY2VfNjQweDY0MC5vbm54',
    'models-3.0.0:inswapper_128.hash': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL2luc3dhcHBlcl8xMjguaGFzaA==',
    'models-3.0.0:inswapper_128.onnx': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHMvcmVsZWFzZXMvZG93bmxvYWQvbW9kZWxzLTMuMC4wL2luc3dhcHBlcl8xMjgub25ueA==',
    
    # Huggingface URLs
    'huggingface:models-3.0.0/open_nsfw.hash': 'aHR0cHM6Ly9odWdnaW5nZmFjZS5jby9mYWNlZnVzaW9uL21vZGVscy0zLjAuMC9yZXNvbHZlL21haW4vb3Blbl9uc2Z3Lmhhc2g=',
    'huggingface:models-3.0.0/open_nsfw.onnx': 'aHR0cHM6Ly9odWdnaW5nZmFjZS5jby9mYWNlZnVzaW9uL21vZGVscy0zLjAuMC9yZXNvbHZlL21haW4vb3Blbl9uc2Z3Lm9ubng=',
    'huggingface:models-3.0.0/retinaface_640x640.hash': 'aHR0cHM6Ly9odWdnaW5nZmFjZS5jby9mYWNlZnVzaW9uL21vZGVscy0zLjAuMC9yZXNvbHZlL21haW4vcmV0aW5hZmFjZV82NDB4NjQwLmhhc2g=',
    'huggingface:models-3.0.0/retinaface_640x640.onnx': 'aHR0cHM6Ly9odWdnaW5nZmFjZS5jby9mYWNlZnVzaW9uL21vZGVscy0zLjAuMC9yZXNvbHZlL21haW4vcmV0aW5hZmFjZV82NDB4NjQwLm9ubng=',
    'huggingface:models-3.0.0/inswapper_128.hash': 'aHR0cHM6Ly9odWdnaW5nZmFjZS5jby9mYWNlZnVzaW9uL21vZGVscy0zLjAuMC9yZXNvbHZlL21haW4vaW5zd2FwcGVyXzEyOC5oYXNo',
    'huggingface:models-3.0.0/inswapper_128.onnx': 'aHR0cHM6Ly9odWdnaW5nZmFjZS5jby9mYWNlZnVzaW9uL21vZGVscy0zLjAuMC9yZXNvbHZlL21haW4vaW5zd2FwcGVyXzEyOC5vbm54'
}

def get_encoded_url(base_name: str, file_name: str) -> Optional[str]:
    """
    Returns a Base64-encoded URL for the specified base_name and file_name
    """
    key = f"{base_name}:{file_name}"
    return ENCODED_URLS.get(key)

def decode_url(encoded_url: str) -> str:
    """
    Decodes a Base64-encoded URL to its original form
    without exposing the decoded value directly in code or logs
    """
    if not encoded_url:
        return None
    return decode_value(encoded_url) 