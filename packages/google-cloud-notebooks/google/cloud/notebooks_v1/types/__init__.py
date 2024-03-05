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
from .diagnostic_config import DiagnosticConfig
from .environment import ContainerImage, Environment, VmImage
from .event import Event
from .execution import Execution, ExecutionTemplate
from .instance import Instance, ReservationAffinity
from .instance_config import InstanceConfig
from .managed_service import (
    CreateRuntimeRequest,
    DeleteRuntimeRequest,
    DiagnoseRuntimeRequest,
    GetRuntimeRequest,
    ListRuntimesRequest,
    ListRuntimesResponse,
    RefreshRuntimeTokenInternalRequest,
    RefreshRuntimeTokenInternalResponse,
    ReportRuntimeEventRequest,
    ResetRuntimeRequest,
    StartRuntimeRequest,
    StopRuntimeRequest,
    SwitchRuntimeRequest,
    UpdateRuntimeRequest,
    UpgradeRuntimeRequest,
)
from .runtime import (
    EncryptionConfig,
    LocalDisk,
    LocalDiskInitializeParams,
    Runtime,
    RuntimeAcceleratorConfig,
    RuntimeAccessConfig,
    RuntimeMetrics,
    RuntimeShieldedInstanceConfig,
    RuntimeSoftwareConfig,
    VirtualMachine,
    VirtualMachineConfig,
)
from .schedule import Schedule
from .service import (
    CreateEnvironmentRequest,
    CreateExecutionRequest,
    CreateInstanceRequest,
    CreateScheduleRequest,
    DeleteEnvironmentRequest,
    DeleteExecutionRequest,
    DeleteInstanceRequest,
    DeleteScheduleRequest,
    DiagnoseInstanceRequest,
    GetEnvironmentRequest,
    GetExecutionRequest,
    GetInstanceHealthRequest,
    GetInstanceHealthResponse,
    GetInstanceRequest,
    GetScheduleRequest,
    IsInstanceUpgradeableRequest,
    IsInstanceUpgradeableResponse,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    ListExecutionsRequest,
    ListExecutionsResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    ListSchedulesRequest,
    ListSchedulesResponse,
    OperationMetadata,
    RegisterInstanceRequest,
    ReportInstanceInfoRequest,
    ResetInstanceRequest,
    RollbackInstanceRequest,
    SetInstanceAcceleratorRequest,
    SetInstanceLabelsRequest,
    SetInstanceMachineTypeRequest,
    StartInstanceRequest,
    StopInstanceRequest,
    TriggerScheduleRequest,
    UpdateInstanceConfigRequest,
    UpdateInstanceMetadataItemsRequest,
    UpdateInstanceMetadataItemsResponse,
    UpdateShieldedInstanceConfigRequest,
    UpgradeInstanceInternalRequest,
    UpgradeInstanceRequest,
    UpgradeType,
)

__all__ = (
    "DiagnosticConfig",
    "ContainerImage",
    "Environment",
    "VmImage",
    "Event",
    "Execution",
    "ExecutionTemplate",
    "Instance",
    "ReservationAffinity",
    "InstanceConfig",
    "CreateRuntimeRequest",
    "DeleteRuntimeRequest",
    "DiagnoseRuntimeRequest",
    "GetRuntimeRequest",
    "ListRuntimesRequest",
    "ListRuntimesResponse",
    "RefreshRuntimeTokenInternalRequest",
    "RefreshRuntimeTokenInternalResponse",
    "ReportRuntimeEventRequest",
    "ResetRuntimeRequest",
    "StartRuntimeRequest",
    "StopRuntimeRequest",
    "SwitchRuntimeRequest",
    "UpdateRuntimeRequest",
    "UpgradeRuntimeRequest",
    "EncryptionConfig",
    "LocalDisk",
    "LocalDiskInitializeParams",
    "Runtime",
    "RuntimeAcceleratorConfig",
    "RuntimeAccessConfig",
    "RuntimeMetrics",
    "RuntimeShieldedInstanceConfig",
    "RuntimeSoftwareConfig",
    "VirtualMachine",
    "VirtualMachineConfig",
    "Schedule",
    "CreateEnvironmentRequest",
    "CreateExecutionRequest",
    "CreateInstanceRequest",
    "CreateScheduleRequest",
    "DeleteEnvironmentRequest",
    "DeleteExecutionRequest",
    "DeleteInstanceRequest",
    "DeleteScheduleRequest",
    "DiagnoseInstanceRequest",
    "GetEnvironmentRequest",
    "GetExecutionRequest",
    "GetInstanceHealthRequest",
    "GetInstanceHealthResponse",
    "GetInstanceRequest",
    "GetScheduleRequest",
    "IsInstanceUpgradeableRequest",
    "IsInstanceUpgradeableResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListExecutionsRequest",
    "ListExecutionsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListSchedulesRequest",
    "ListSchedulesResponse",
    "OperationMetadata",
    "RegisterInstanceRequest",
    "ReportInstanceInfoRequest",
    "ResetInstanceRequest",
    "RollbackInstanceRequest",
    "SetInstanceAcceleratorRequest",
    "SetInstanceLabelsRequest",
    "SetInstanceMachineTypeRequest",
    "StartInstanceRequest",
    "StopInstanceRequest",
    "TriggerScheduleRequest",
    "UpdateInstanceConfigRequest",
    "UpdateInstanceMetadataItemsRequest",
    "UpdateInstanceMetadataItemsResponse",
    "UpdateShieldedInstanceConfigRequest",
    "UpgradeInstanceInternalRequest",
    "UpgradeInstanceRequest",
    "UpgradeType",
)
