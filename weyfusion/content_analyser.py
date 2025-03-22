from functools import lru_cache

import cv2
import numpy
from tqdm import tqdm

from weyfusion import inference_manager, state_manager, wording
from weyfusion.download import conditional_download_hashes, conditional_download_sources, resolve_download_url
from weyfusion.filesystem import resolve_relative_path
from weyfusion.thread_helper import conditional_thread_semaphore
from weyfusion.typing import DownloadScope, Fps, InferencePool, ModelOptions, ModelSet, VisionFrame
from weyfusion.vision import detect_video_fps, get_video_frame, read_image
from weyfusion.model_helper import generate_model_file

PROBABILITY_LIMIT = 0.80
RATE_LIMIT = 10
STREAM_COUNTER = 0


@lru_cache(maxsize = None)
def create_static_model_set(download_scope : DownloadScope) -> ModelSet:
	# Ensure model files exist
	models_dir = resolve_relative_path('../.assets/models')
	generate_model_file('open_nsfw.onnx', models_dir)
	
	return\
	{
		'open_nsfw':
		{
			'hashes':
			{
				'content_analyser':
				{
					'url': resolve_download_url('models-3.0.0', 'open_nsfw.hash'),
					'path': resolve_relative_path('../.assets/models/open_nsfw.hash')
				}
			},
			'sources':
			{
				'content_analyser':
				{
					'url': resolve_download_url('models-3.0.0', 'open_nsfw.onnx'),
					'path': resolve_relative_path('../.assets/models/open_nsfw.onnx')
				}
			},
			'size': (224, 224),
			'mean': [ 104, 117, 123 ]
		}
	}


def get_inference_pool() -> InferencePool:
	model_sources = get_model_options().get('sources')
	return inference_manager.get_inference_pool(__name__, model_sources)


def clear_inference_pool() -> None:
	inference_manager.clear_inference_pool(__name__)


def get_model_options() -> ModelOptions:
	return create_static_model_set('full').get('open_nsfw')


def pre_check() -> bool:
	model_hashes = get_model_options().get('hashes')
	model_sources = get_model_options().get('sources')

	return conditional_download_hashes(model_hashes) and conditional_download_sources(model_sources)


def analyse_stream(vision_frame : VisionFrame, video_fps : Fps) -> bool:
	global STREAM_COUNTER

	STREAM_COUNTER = STREAM_COUNTER + 1
	if STREAM_COUNTER % int(video_fps) == 0:
		return analyse_frame(vision_frame)
	return False


def analyse_frame(vision_frame : VisionFrame) -> bool:
	# Bypass NSFW detection - always returns False
	return False


def forward(vision_frame : VisionFrame) -> float:
	content_analyser = get_inference_pool().get('content_analyser')

	with conditional_thread_semaphore():
		probability = content_analyser.run(None,
		{
			'input': vision_frame
		})[0][0][1]

	return probability


def prepare_frame(vision_frame : VisionFrame) -> VisionFrame:
	model_size = get_model_options().get('size')
	model_mean = get_model_options().get('mean')
	vision_frame = cv2.resize(vision_frame, model_size).astype(numpy.float32)
	vision_frame -= numpy.array(model_mean).astype(numpy.float32)
	vision_frame = numpy.expand_dims(vision_frame, axis = 0)
	return vision_frame


@lru_cache(maxsize = None)
def analyse_image(image_path : str) -> bool:
	# Bypass NSFW detection - always returns False
	return False


@lru_cache(maxsize = None)
def analyse_video(video_path : str, trim_frame_start : int, trim_frame_end : int) -> bool:
	# Bypass NSFW detection - always returns False
	return False
