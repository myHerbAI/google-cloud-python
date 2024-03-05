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

from google.protobuf import wrappers_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.apps.script.type",
    manifest={
        "MenuItemExtensionPoint",
        "HomepageExtensionPoint",
        "UniversalActionExtensionPoint",
    },
)


class MenuItemExtensionPoint(proto.Message):
    r"""Common format for declaring a  menu item, or button, that
    appears within a host app.

    Attributes:
        run_function (str):
            Required. The endpoint to execute when this
            extension point is activated.
        label (str):
            Required. User-visible text describing the
            action taken by activating this extension point.
            For example, "Insert invoice".
        logo_url (str):
            The URL for the logo image shown in the
            add-on toolbar.
            If not set, defaults to the add-on's primary
            logo URL.
    """

    run_function: str = proto.Field(
        proto.STRING,
        number=1,
    )
    label: str = proto.Field(
        proto.STRING,
        number=2,
    )
    logo_url: str = proto.Field(
        proto.STRING,
        number=3,
    )


class HomepageExtensionPoint(proto.Message):
    r"""Common format for declaring an add-on's home-page view.

    Attributes:
        run_function (str):
            Required. The endpoint to execute when this
            extension point is activated.
        enabled (google.protobuf.wrappers_pb2.BoolValue):
            Optional. If set to ``false``, disable the home-page view in
            this context.

            Defaults to ``true`` if unset.

            If an add-ons custom home-page view is disabled, an
            autogenerated overview card will be provided for users
            instead.
    """

    run_function: str = proto.Field(
        proto.STRING,
        number=1,
    )
    enabled: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.BoolValue,
    )


class UniversalActionExtensionPoint(proto.Message):
    r"""Format for declaring a universal action menu item extension
    point.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        label (str):
            Required. User-visible text describing the
            action taken by activating this extension point,
            for example, "Add a new contact".
        open_link (str):
            URL to be opened by the UniversalAction.

            This field is a member of `oneof`_ ``action_type``.
        run_function (str):
            Endpoint to be run by the UniversalAction.

            This field is a member of `oneof`_ ``action_type``.
    """

    label: str = proto.Field(
        proto.STRING,
        number=1,
    )
    open_link: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="action_type",
    )
    run_function: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="action_type",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
