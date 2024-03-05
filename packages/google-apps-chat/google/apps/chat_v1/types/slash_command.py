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
    package="google.chat.v1",
    manifest={
        "SlashCommand",
    },
)


class SlashCommand(proto.Message):
    r"""A `slash
    command <https://developers.google.com/chat/how-tos/slash-commands>`__
    in Google Chat.

    Attributes:
        command_id (int):
            The ID of the slash command invoked.
    """

    command_id: int = proto.Field(
        proto.INT64,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
