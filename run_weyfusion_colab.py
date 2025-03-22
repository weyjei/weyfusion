#!/usr/bin/env python3

"""
Quick launcher for WeyFusion in Google Colab
This script opens the WeyFusion Colab notebook in your browser
"""

import os
import webbrowser
import argparse

def open_colab_notebook(github_username="weyjei", repository="weyfusion", notebook_name="WeyFusion_Colab.ipynb"):
    """Open the WeyFusion Colab notebook in a web browser"""
    colab_url = f"https://colab.research.google.com/github/{github_username}/{repository}/blob/main/{notebook_name}"
    
    print(f"🚀 Opening WeyFusion Colab notebook: {colab_url}")
    webbrowser.open(colab_url)
    
    print("""
✅ Successfully launched WeyFusion in Google Colab!

📋 Instructions:
1. In the Colab interface, click "Runtime" > "Run all" to execute all cells
2. Wait for the environment setup to complete
3. When the UI is ready, click the "Open WeyFusion UI" button
4. Enjoy using WeyFusion with the complete Gradio interface!

⭐ If you like WeyFusion, please star the repository on GitHub
""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch WeyFusion in Google Colab")
    parser.add_argument("--username", default="weyjei", help="GitHub username where WeyFusion is hosted")
    parser.add_argument("--repository", default="weyfusion", help="Repository name")
    parser.add_argument("--notebook", default="WeyFusion_Colab.ipynb", help="Notebook filename")
    args = parser.parse_args()
    
    open_colab_notebook(args.username, args.repository, args.notebook) 