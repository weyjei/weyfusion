WEYFUSION
==========

> Industry leading face manipulation platform

[![Build Status](https://img.shields.io/github/actions/workflow/status/weyjei/weyfusion/ci.yml.svg?branch=master)](https://github.com/weyjei/weyfusion/actions?query=workflow:ci)
[![Coverage Status](https://img.shields.io/coveralls/weyjei/weyfusion.svg)](https://coveralls.io/r/weyjei/weyfusion)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/weyjei/weyfusion/blob/main/WeyFusion_Colab.ipynb)

WeyFusion is a powerful face swapping and manipulation platform with advanced features:

- No content restrictions
- Improved model download system
- Optimized performance
- User-friendly interface

## Key Features

- Face swapping for images and videos
- Multiple face detection models
- Support for enhancers and processors
- CUDA acceleration for fast processing
- Interactive Gradio UI

## Installation

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/weyjei/weyfusion.git

# Navigate to the directory
cd weyfusion

# Install required dependencies
pip install -r requirements.txt

# Install with CUDA support
python install.py --onnxruntime cuda
```

### Google Colab (Recommended)

For the easiest setup with no installation required, use our Google Colab notebook:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/weyjei/weyfusion/blob/main/WeyFusion_Colab.ipynb)

1. Click the "Open in Colab" button above
2. Run all cells to set up the environment
3. Access the full Gradio UI through the provided link
4. No need to install anything on your local machine!

The Colab notebook provides:
- Full Gradio user interface
- CUDA acceleration
- Automatic model downloads
- No content restrictions

## Usage

Run WeyFusion with the UI:

```bash
python weyfusion.py run --ui-layouts default --execution-providers cuda
```

Or run in headless mode:

```bash
python weyfusion.py headless-run --source-paths SOURCE_PATH --target-path TARGET_PATH --output-path OUTPUT_PATH --execution-providers cuda
```

Preview
-------

![Preview](https://raw.githubusercontent.com/weyjei/weyfusion/master/.github/preview.png?sanitize=true)


Documentation
-------------

Read the [documentation](https://docs.weyfusion.io) for a deep dive.
