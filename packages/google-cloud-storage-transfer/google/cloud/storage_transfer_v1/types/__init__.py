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
from .transfer import (
    CreateAgentPoolRequest,
    CreateTransferJobRequest,
    DeleteAgentPoolRequest,
    DeleteTransferJobRequest,
    GetAgentPoolRequest,
    GetGoogleServiceAccountRequest,
    GetTransferJobRequest,
    ListAgentPoolsRequest,
    ListAgentPoolsResponse,
    ListTransferJobsRequest,
    ListTransferJobsResponse,
    PauseTransferOperationRequest,
    ResumeTransferOperationRequest,
    RunTransferJobRequest,
    UpdateAgentPoolRequest,
    UpdateTransferJobRequest,
)
from .transfer_types import (
    AgentPool,
    AwsAccessKey,
    AwsS3CompatibleData,
    AwsS3Data,
    AzureBlobStorageData,
    AzureCredentials,
    ErrorLogEntry,
    ErrorSummary,
    EventStream,
    GcsData,
    GoogleServiceAccount,
    HttpData,
    LoggingConfig,
    MetadataOptions,
    NotificationConfig,
    ObjectConditions,
    PosixFilesystem,
    S3CompatibleMetadata,
    Schedule,
    TransferCounters,
    TransferJob,
    TransferManifest,
    TransferOperation,
    TransferOptions,
    TransferSpec,
)

__all__ = (
    "CreateAgentPoolRequest",
    "CreateTransferJobRequest",
    "DeleteAgentPoolRequest",
    "DeleteTransferJobRequest",
    "GetAgentPoolRequest",
    "GetGoogleServiceAccountRequest",
    "GetTransferJobRequest",
    "ListAgentPoolsRequest",
    "ListAgentPoolsResponse",
    "ListTransferJobsRequest",
    "ListTransferJobsResponse",
    "PauseTransferOperationRequest",
    "ResumeTransferOperationRequest",
    "RunTransferJobRequest",
    "UpdateAgentPoolRequest",
    "UpdateTransferJobRequest",
    "AgentPool",
    "AwsAccessKey",
    "AwsS3CompatibleData",
    "AwsS3Data",
    "AzureBlobStorageData",
    "AzureCredentials",
    "ErrorLogEntry",
    "ErrorSummary",
    "EventStream",
    "GcsData",
    "GoogleServiceAccount",
    "HttpData",
    "LoggingConfig",
    "MetadataOptions",
    "NotificationConfig",
    "ObjectConditions",
    "PosixFilesystem",
    "S3CompatibleMetadata",
    "Schedule",
    "TransferCounters",
    "TransferJob",
    "TransferManifest",
    "TransferOperation",
    "TransferOptions",
    "TransferSpec",
)
