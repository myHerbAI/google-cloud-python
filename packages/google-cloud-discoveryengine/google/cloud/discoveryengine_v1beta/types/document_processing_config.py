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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1beta",
    manifest={
        "DocumentProcessingConfig",
    },
)


class DocumentProcessingConfig(proto.Message):
    r"""A singleton resource of
    [DataStore][google.cloud.discoveryengine.v1beta.DataStore]. It's
    empty when
    [DataStore][google.cloud.discoveryengine.v1beta.DataStore] is
    created, which defaults to digital parser. The first call to
    [DataStoreService.UpdateDocumentProcessingConfig][] method will
    initialize the config.

    Attributes:
        name (str):
            The full resource name of the Document Processing Config.
            Format:
            ``projects/*/locations/*/collections/*/dataStores/*/documentProcessingConfig``.
        default_parsing_config (google.cloud.discoveryengine_v1beta.types.DocumentProcessingConfig.ParsingConfig):
            Configurations for default Document parser.
            If not specified, we will configure it as
            default DigitalParsingConfig, and the default
            parsing config will be applied to all file types
            for Document parsing.
        parsing_config_overrides (MutableMapping[str, google.cloud.discoveryengine_v1beta.types.DocumentProcessingConfig.ParsingConfig]):
            Map from file type to override the default parsing
            configuration based on the file type. Supported keys:

            -  ``pdf``: Override parsing config for PDF files, either
               digital parsing, ocr parsing or layout parsing is
               supported.
            -  ``html``: Override parsing config for HTML files, only
               digital parsing and or layout parsing are supported.
            -  ``docx``: Override parsing config for DOCX files, only
               digital parsing and or layout parsing are supported.
    """

    class ParsingConfig(proto.Message):
        r"""Related configurations applied to a specific type of document
        parser.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            digital_parsing_config (google.cloud.discoveryengine_v1beta.types.DocumentProcessingConfig.ParsingConfig.DigitalParsingConfig):
                Configurations applied to digital parser.

                This field is a member of `oneof`_ ``type_dedicated_config``.
            ocr_parsing_config (google.cloud.discoveryengine_v1beta.types.DocumentProcessingConfig.ParsingConfig.OcrParsingConfig):
                Configurations applied to OCR parser.
                Currently it only applies to PDFs.

                This field is a member of `oneof`_ ``type_dedicated_config``.
        """

        class DigitalParsingConfig(proto.Message):
            r"""The digital parsing configurations for documents."""

        class OcrParsingConfig(proto.Message):
            r"""The OCR parsing configurations for documents.

            Attributes:
                enhanced_document_elements (MutableSequence[str]):
                    [DEPRECATED] This field is deprecated. To use the additional
                    enhanced document elements processing, please switch to
                    ``layout_parsing_config``.
                use_native_text (bool):
                    If true, will use native text instead of OCR
                    text on pages containing native text.
            """

            enhanced_document_elements: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=1,
            )
            use_native_text: bool = proto.Field(
                proto.BOOL,
                number=2,
            )

        digital_parsing_config: "DocumentProcessingConfig.ParsingConfig.DigitalParsingConfig" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="type_dedicated_config",
            message="DocumentProcessingConfig.ParsingConfig.DigitalParsingConfig",
        )
        ocr_parsing_config: "DocumentProcessingConfig.ParsingConfig.OcrParsingConfig" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="type_dedicated_config",
            message="DocumentProcessingConfig.ParsingConfig.OcrParsingConfig",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    default_parsing_config: ParsingConfig = proto.Field(
        proto.MESSAGE,
        number=4,
        message=ParsingConfig,
    )
    parsing_config_overrides: MutableMapping[str, ParsingConfig] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=5,
        message=ParsingConfig,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
