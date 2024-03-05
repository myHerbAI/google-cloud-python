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
from google.cloud.telcoautomation_v1alpha1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.telco_automation import TelcoAutomationAsyncClient, TelcoAutomationClient
from .types.telcoautomation import (
    ApplyDeploymentRequest,
    ApplyHydratedDeploymentRequest,
    ApproveBlueprintRequest,
    Blueprint,
    BlueprintView,
    ComputeDeploymentStatusRequest,
    ComputeDeploymentStatusResponse,
    CreateBlueprintRequest,
    CreateDeploymentRequest,
    CreateEdgeSlmRequest,
    CreateOrchestrationClusterRequest,
    DeleteBlueprintRequest,
    DeleteEdgeSlmRequest,
    DeleteOrchestrationClusterRequest,
    Deployment,
    DeploymentLevel,
    DeploymentView,
    DiscardBlueprintChangesRequest,
    DiscardBlueprintChangesResponse,
    DiscardDeploymentChangesRequest,
    DiscardDeploymentChangesResponse,
    EdgeSlm,
    File,
    FullManagementConfig,
    GetBlueprintRequest,
    GetDeploymentRequest,
    GetEdgeSlmRequest,
    GetHydratedDeploymentRequest,
    GetOrchestrationClusterRequest,
    GetPublicBlueprintRequest,
    HydratedDeployment,
    HydrationStatus,
    ListBlueprintRevisionsRequest,
    ListBlueprintRevisionsResponse,
    ListBlueprintsRequest,
    ListBlueprintsResponse,
    ListDeploymentRevisionsRequest,
    ListDeploymentRevisionsResponse,
    ListDeploymentsRequest,
    ListDeploymentsResponse,
    ListEdgeSlmsRequest,
    ListEdgeSlmsResponse,
    ListHydratedDeploymentsRequest,
    ListHydratedDeploymentsResponse,
    ListOrchestrationClustersRequest,
    ListOrchestrationClustersResponse,
    ListPublicBlueprintsRequest,
    ListPublicBlueprintsResponse,
    ManagementConfig,
    MasterAuthorizedNetworksConfig,
    NFDeploySiteStatus,
    NFDeployStatus,
    OperationMetadata,
    OrchestrationCluster,
    ProposeBlueprintRequest,
    PublicBlueprint,
    RejectBlueprintRequest,
    RemoveDeploymentRequest,
    ResourceStatus,
    ResourceType,
    RollbackDeploymentRequest,
    SearchBlueprintRevisionsRequest,
    SearchBlueprintRevisionsResponse,
    SearchDeploymentRevisionsRequest,
    SearchDeploymentRevisionsResponse,
    SiteVersion,
    StandardManagementConfig,
    Status,
    UpdateBlueprintRequest,
    UpdateDeploymentRequest,
    UpdateHydratedDeploymentRequest,
    WorkloadStatus,
)

__all__ = (
    "TelcoAutomationAsyncClient",
    "ApplyDeploymentRequest",
    "ApplyHydratedDeploymentRequest",
    "ApproveBlueprintRequest",
    "Blueprint",
    "BlueprintView",
    "ComputeDeploymentStatusRequest",
    "ComputeDeploymentStatusResponse",
    "CreateBlueprintRequest",
    "CreateDeploymentRequest",
    "CreateEdgeSlmRequest",
    "CreateOrchestrationClusterRequest",
    "DeleteBlueprintRequest",
    "DeleteEdgeSlmRequest",
    "DeleteOrchestrationClusterRequest",
    "Deployment",
    "DeploymentLevel",
    "DeploymentView",
    "DiscardBlueprintChangesRequest",
    "DiscardBlueprintChangesResponse",
    "DiscardDeploymentChangesRequest",
    "DiscardDeploymentChangesResponse",
    "EdgeSlm",
    "File",
    "FullManagementConfig",
    "GetBlueprintRequest",
    "GetDeploymentRequest",
    "GetEdgeSlmRequest",
    "GetHydratedDeploymentRequest",
    "GetOrchestrationClusterRequest",
    "GetPublicBlueprintRequest",
    "HydratedDeployment",
    "HydrationStatus",
    "ListBlueprintRevisionsRequest",
    "ListBlueprintRevisionsResponse",
    "ListBlueprintsRequest",
    "ListBlueprintsResponse",
    "ListDeploymentRevisionsRequest",
    "ListDeploymentRevisionsResponse",
    "ListDeploymentsRequest",
    "ListDeploymentsResponse",
    "ListEdgeSlmsRequest",
    "ListEdgeSlmsResponse",
    "ListHydratedDeploymentsRequest",
    "ListHydratedDeploymentsResponse",
    "ListOrchestrationClustersRequest",
    "ListOrchestrationClustersResponse",
    "ListPublicBlueprintsRequest",
    "ListPublicBlueprintsResponse",
    "ManagementConfig",
    "MasterAuthorizedNetworksConfig",
    "NFDeploySiteStatus",
    "NFDeployStatus",
    "OperationMetadata",
    "OrchestrationCluster",
    "ProposeBlueprintRequest",
    "PublicBlueprint",
    "RejectBlueprintRequest",
    "RemoveDeploymentRequest",
    "ResourceStatus",
    "ResourceType",
    "RollbackDeploymentRequest",
    "SearchBlueprintRevisionsRequest",
    "SearchBlueprintRevisionsResponse",
    "SearchDeploymentRevisionsRequest",
    "SearchDeploymentRevisionsResponse",
    "SiteVersion",
    "StandardManagementConfig",
    "Status",
    "TelcoAutomationClient",
    "UpdateBlueprintRequest",
    "UpdateDeploymentRequest",
    "UpdateHydratedDeploymentRequest",
    "WorkloadStatus",
)
