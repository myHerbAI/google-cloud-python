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
    package="google.cloud.discoveryengine.v1alpha",
    manifest={
        "RankingRecord",
        "RankRequest",
        "RankResponse",
    },
)


class RankingRecord(proto.Message):
    r"""Record message for
    [RankService.Rank][google.cloud.discoveryengine.v1alpha.RankService.Rank]
    method.

    Attributes:
        id (str):
            The unique ID to represent the record.
        title (str):
            The title of the record. Empty by default. At least one of
            [title][google.cloud.discoveryengine.v1alpha.RankingRecord.title]
            or
            [content][google.cloud.discoveryengine.v1alpha.RankingRecord.content]
            should be set otherwise an INVALID_ARGUMENT error is thrown.
        content (str):
            The content of the record. Empty by default. At least one of
            [title][google.cloud.discoveryengine.v1alpha.RankingRecord.title]
            or
            [content][google.cloud.discoveryengine.v1alpha.RankingRecord.content]
            should be set otherwise an INVALID_ARGUMENT error is thrown.
        score (float):
            The score of this record based on the given
            query and selected model.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    title: str = proto.Field(
        proto.STRING,
        number=2,
    )
    content: str = proto.Field(
        proto.STRING,
        number=3,
    )
    score: float = proto.Field(
        proto.FLOAT,
        number=4,
    )


class RankRequest(proto.Message):
    r"""Request message for
    [RankService.Rank][google.cloud.discoveryengine.v1alpha.RankService.Rank]
    method.

    Attributes:
        ranking_config (str):
            Required. The resource name of the rank service config, such
            as
            ``projects/{project_num}/locations/{location_id}/rankingConfigs/default_ranking_config``.
        model (str):
            The identifier of the model to use. It is one of:

            -  ``semantic-ranker-512@latest``: Semantic ranking model
               with maxiumn input token size 512.

            It is set to ``semantic-ranker-512@latest`` by default if
            unspecified.
        top_n (int):
            The number of results to return. If this is
            unset or no bigger than zero, returns all
            results.
        query (str):
            The query to use.
        records (MutableSequence[google.cloud.discoveryengine_v1alpha.types.RankingRecord]):
            Required. A list of records to rank. At most
            200 records to rank.
        ignore_record_details_in_response (bool):
            If true, the response will contain only
            record ID and score. By default, it is false,
            the response will contain record details.
    """

    ranking_config: str = proto.Field(
        proto.STRING,
        number=1,
    )
    model: str = proto.Field(
        proto.STRING,
        number=2,
    )
    top_n: int = proto.Field(
        proto.INT32,
        number=3,
    )
    query: str = proto.Field(
        proto.STRING,
        number=4,
    )
    records: MutableSequence["RankingRecord"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="RankingRecord",
    )
    ignore_record_details_in_response: bool = proto.Field(
        proto.BOOL,
        number=6,
    )


class RankResponse(proto.Message):
    r"""Response message for
    [RankService.Rank][google.cloud.discoveryengine.v1alpha.RankService.Rank]
    method.

    Attributes:
        records (MutableSequence[google.cloud.discoveryengine_v1alpha.types.RankingRecord]):
            A list of records sorted by descending score.
    """

    records: MutableSequence["RankingRecord"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="RankingRecord",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
