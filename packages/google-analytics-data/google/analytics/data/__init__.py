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
from google.analytics.data import gapic_version as package_version

__version__ = package_version.__version__


from google.analytics.data_v1beta.services.beta_analytics_data.async_client import (
    BetaAnalyticsDataAsyncClient,
)
from google.analytics.data_v1beta.services.beta_analytics_data.client import (
    BetaAnalyticsDataClient,
)
from google.analytics.data_v1beta.types.analytics_data_api import (
    AudienceDimension,
    AudienceDimensionValue,
    AudienceExport,
    AudienceExportMetadata,
    AudienceRow,
    BatchRunPivotReportsRequest,
    BatchRunPivotReportsResponse,
    BatchRunReportsRequest,
    BatchRunReportsResponse,
    CheckCompatibilityRequest,
    CheckCompatibilityResponse,
    CreateAudienceExportRequest,
    GetAudienceExportRequest,
    GetMetadataRequest,
    ListAudienceExportsRequest,
    ListAudienceExportsResponse,
    Metadata,
    QueryAudienceExportRequest,
    QueryAudienceExportResponse,
    RunPivotReportRequest,
    RunPivotReportResponse,
    RunRealtimeReportRequest,
    RunRealtimeReportResponse,
    RunReportRequest,
    RunReportResponse,
)
from google.analytics.data_v1beta.types.data import (
    Cohort,
    CohortReportSettings,
    CohortSpec,
    CohortsRange,
    Compatibility,
    DateRange,
    Dimension,
    DimensionCompatibility,
    DimensionExpression,
    DimensionHeader,
    DimensionMetadata,
    DimensionValue,
    Filter,
    FilterExpression,
    FilterExpressionList,
    Metric,
    MetricAggregation,
    MetricCompatibility,
    MetricHeader,
    MetricMetadata,
    MetricType,
    MetricValue,
    MinuteRange,
    NumericValue,
    OrderBy,
    Pivot,
    PivotDimensionHeader,
    PivotHeader,
    PropertyQuota,
    QuotaStatus,
    ResponseMetaData,
    RestrictedMetricType,
    Row,
    SamplingMetadata,
)

__all__ = (
    "BetaAnalyticsDataClient",
    "BetaAnalyticsDataAsyncClient",
    "AudienceDimension",
    "AudienceDimensionValue",
    "AudienceExport",
    "AudienceExportMetadata",
    "AudienceRow",
    "BatchRunPivotReportsRequest",
    "BatchRunPivotReportsResponse",
    "BatchRunReportsRequest",
    "BatchRunReportsResponse",
    "CheckCompatibilityRequest",
    "CheckCompatibilityResponse",
    "CreateAudienceExportRequest",
    "GetAudienceExportRequest",
    "GetMetadataRequest",
    "ListAudienceExportsRequest",
    "ListAudienceExportsResponse",
    "Metadata",
    "QueryAudienceExportRequest",
    "QueryAudienceExportResponse",
    "RunPivotReportRequest",
    "RunPivotReportResponse",
    "RunRealtimeReportRequest",
    "RunRealtimeReportResponse",
    "RunReportRequest",
    "RunReportResponse",
    "Cohort",
    "CohortReportSettings",
    "CohortSpec",
    "CohortsRange",
    "DateRange",
    "Dimension",
    "DimensionCompatibility",
    "DimensionExpression",
    "DimensionHeader",
    "DimensionMetadata",
    "DimensionValue",
    "Filter",
    "FilterExpression",
    "FilterExpressionList",
    "Metric",
    "MetricCompatibility",
    "MetricHeader",
    "MetricMetadata",
    "MetricValue",
    "MinuteRange",
    "NumericValue",
    "OrderBy",
    "Pivot",
    "PivotDimensionHeader",
    "PivotHeader",
    "PropertyQuota",
    "QuotaStatus",
    "ResponseMetaData",
    "Row",
    "SamplingMetadata",
    "Compatibility",
    "MetricAggregation",
    "MetricType",
    "RestrictedMetricType",
)
