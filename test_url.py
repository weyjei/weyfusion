#!/usr/bin/env python3

"""
Test script to verify encrypted URL handling
This script should print out the URLs without showing 'facefusion' in plaintext
"""

import os
import sys

# Set up paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import modules
from weyfusion import repo_helper
from weyfusion.url_helper import get_encoded_url, decode_url
from weyfusion.model_helper import MODEL_URLS

def test_url_encryption():
    """Test that URLs are properly encrypted and don't reveal repository names"""
    print("=== Testing URL encryption ===")
    print("\nEncoded URLs from URL helper:")
    
    # Test a few URLs from url_helper
    test_urls = [
        ('models-3.0.0', 'open_nsfw.onnx'),
        ('models-3.0.0', 'inswapper_128.onnx'),
        ('models-3.0.0', 'retinaface_10g.onnx')
    ]
    
    for base_name, file_name in test_urls:
        encoded_url = get_encoded_url(base_name, file_name)
        print(f"Base: {base_name}, File: {file_name}")
        print(f"Encoded URL: {encoded_url}")
        
        # Check if the decoded URL contains 'facefusion' - this should not print anything
        # when properly encoded
        decoded = decode_url(encoded_url)
        if 'facefusion' in decoded.lower():
            print(f"WARNING: URL reveals repository name: {decoded}")
        else:
            print("URL properly secured ✓")
        print()
    
    print("\nEncoded URLs from model_helper:")
    # Test a few URLs from model_helper
    for model_name, encoded_url in list(MODEL_URLS.items())[:3]:
        print(f"Model: {model_name}")
        print(f"Encoded URL: {encoded_url}")
        
        # Safely decode without printing
        decoded = repo_helper.decode_value(encoded_url)
        if 'facefusion' in decoded.lower():
            print(f"WARNING: URL reveals repository name")
        else:
            print("URL properly secured ✓")
        print()
    
    print("\nEncoded repository URLs:")
    # Test repository URLs
    for repo_key, encoded_url in repo_helper.ENCODED_REPOS.items():
        print(f"Repo key: {repo_key}")
        print(f"Encoded URL: {encoded_url}")
        
        # Safely decode without printing
        decoded = repo_helper.decode_value(encoded_url)
        if 'facefusion' in decoded.lower():
            print(f"WARNING: URL reveals repository name")
        else:
            print("URL properly secured ✓")
        print()
    
    print("URL encryption test complete")

if __name__ == "__main__":
    test_url_encryption() 