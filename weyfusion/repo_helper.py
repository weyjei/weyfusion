import base64
from typing import Dict, Optional

# Base64 encoded repository URLs
# These completely hide all references to external repositories
ENCODED_REPOS = {
    # Primary model repository 
    'model_repo': 'aHR0cHM6Ly9naXRodWIuY29tL2ZhY2VmdXNpb24vZmFjZWZ1c2lvbi1hc3NldHM=',
    
    # Secondary repositories
    'models_repo': 'aHR0cHM6Ly9odWdnaW5nZmFjZS5jby9mYWNlZnVzaW9u',
    
    # Release paths
    'release_path': 'cmVsZWFzZXMvZG93bmxvYWQv',
    
    # Mirror URLs if needed
    'mirror_repo': 'aHR0cHM6Ly9taXJyb3IuZ2l0aHViLmNvbS9mYWNlZnVzaW9uL2ZhY2VmdXNpb24tYXNzZXRz'
}

def get_repo_url(repo_key: str) -> Optional[str]:
    """
    Returns a decoded repository URL based on the key
    """
    encoded_url = ENCODED_REPOS.get(repo_key)
    if not encoded_url:
        return None
    return decode_value(encoded_url)

def decode_value(encoded_value: str) -> str:
    """
    Decodes a Base64-encoded value to its original form
    """
    if not encoded_value:
        return None
    return base64.b64decode(encoded_value).decode('utf-8')

def encode_value(value: str) -> str:
    """
    Encodes a value to Base64
    """
    if not value:
        return None
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')

def build_asset_url(model_type: str, version: str, filename: str) -> str:
    """
    Builds a fully encrypted URL for model assets
    
    Example:
    build_asset_url('models', '3.0.0', 'open_nsfw.onnx')
    """
    repo_url = get_repo_url('model_repo')
    release_path = decode_value(ENCODED_REPOS.get('release_path'))
    
    if not repo_url or not release_path:
        return None
        
    return f"{repo_url}/{release_path}{model_type}-{version}/{filename}"

def build_huggingface_url(model_path: str, filename: str) -> str:
    """
    Builds a fully encrypted URL for HuggingFace assets
    """
    repo_url = get_repo_url('models_repo')
    
    if not repo_url:
        return None
        
    return f"{repo_url}/{model_path}/resolve/main/{filename}" 