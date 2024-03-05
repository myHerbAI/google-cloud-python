# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.cloud.videointelligence_v1p1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.video_intelligence_service import (
    VideoIntelligenceServiceAsyncClient,
    VideoIntelligenceServiceClient,
)
from .types.video_intelligence import (
    AnnotateVideoProgress,
    AnnotateVideoRequest,
    AnnotateVideoResponse,
    Entity,
    ExplicitContentAnnotation,
    ExplicitContentDetectionConfig,
    ExplicitContentFrame,
    Feature,
    LabelAnnotation,
    LabelDetectionConfig,
    LabelDetectionMode,
    LabelFrame,
    LabelSegment,
    Likelihood,
    ShotChangeDetectionConfig,
    SpeechContext,
    SpeechRecognitionAlternative,
    SpeechTranscription,
    SpeechTranscriptionConfig,
    VideoAnnotationProgress,
    VideoAnnotationResults,
    VideoContext,
    VideoSegment,
    WordInfo,
)

__all__ = (
    "VideoIntelligenceServiceAsyncClient",
    "AnnotateVideoProgress",
    "AnnotateVideoRequest",
    "AnnotateVideoResponse",
    "Entity",
    "ExplicitContentAnnotation",
    "ExplicitContentDetectionConfig",
    "ExplicitContentFrame",
    "Feature",
    "LabelAnnotation",
    "LabelDetectionConfig",
    "LabelDetectionMode",
    "LabelFrame",
    "LabelSegment",
    "Likelihood",
    "ShotChangeDetectionConfig",
    "SpeechContext",
    "SpeechRecognitionAlternative",
    "SpeechTranscription",
    "SpeechTranscriptionConfig",
    "VideoAnnotationProgress",
    "VideoAnnotationResults",
    "VideoContext",
    "VideoIntelligenceServiceClient",
    "VideoSegment",
    "WordInfo",
)
