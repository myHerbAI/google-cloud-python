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
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.cloud.storageinsights_v1.types import storageinsights


class ListReportConfigsPager:
    """A pager for iterating through ``list_report_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storageinsights_v1.types.ListReportConfigsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``report_configs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListReportConfigs`` requests and continue to iterate
    through the ``report_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storageinsights_v1.types.ListReportConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., storageinsights.ListReportConfigsResponse],
        request: storageinsights.ListReportConfigsRequest,
        response: storageinsights.ListReportConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storageinsights_v1.types.ListReportConfigsRequest):
                The initial request object.
            response (google.cloud.storageinsights_v1.types.ListReportConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = storageinsights.ListReportConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[storageinsights.ListReportConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[storageinsights.ReportConfig]:
        for page in self.pages:
            yield from page.report_configs

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReportConfigsAsyncPager:
    """A pager for iterating through ``list_report_configs`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storageinsights_v1.types.ListReportConfigsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``report_configs`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListReportConfigs`` requests and continue to iterate
    through the ``report_configs`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storageinsights_v1.types.ListReportConfigsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[storageinsights.ListReportConfigsResponse]],
        request: storageinsights.ListReportConfigsRequest,
        response: storageinsights.ListReportConfigsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storageinsights_v1.types.ListReportConfigsRequest):
                The initial request object.
            response (google.cloud.storageinsights_v1.types.ListReportConfigsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = storageinsights.ListReportConfigsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[storageinsights.ListReportConfigsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[storageinsights.ReportConfig]:
        async def async_generator():
            async for page in self.pages:
                for response in page.report_configs:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReportDetailsPager:
    """A pager for iterating through ``list_report_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storageinsights_v1.types.ListReportDetailsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``report_details`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListReportDetails`` requests and continue to iterate
    through the ``report_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storageinsights_v1.types.ListReportDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., storageinsights.ListReportDetailsResponse],
        request: storageinsights.ListReportDetailsRequest,
        response: storageinsights.ListReportDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storageinsights_v1.types.ListReportDetailsRequest):
                The initial request object.
            response (google.cloud.storageinsights_v1.types.ListReportDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = storageinsights.ListReportDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[storageinsights.ListReportDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[storageinsights.ReportDetail]:
        for page in self.pages:
            yield from page.report_details

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListReportDetailsAsyncPager:
    """A pager for iterating through ``list_report_details`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.storageinsights_v1.types.ListReportDetailsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``report_details`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListReportDetails`` requests and continue to iterate
    through the ``report_details`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.storageinsights_v1.types.ListReportDetailsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[storageinsights.ListReportDetailsResponse]],
        request: storageinsights.ListReportDetailsRequest,
        response: storageinsights.ListReportDetailsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.storageinsights_v1.types.ListReportDetailsRequest):
                The initial request object.
            response (google.cloud.storageinsights_v1.types.ListReportDetailsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = storageinsights.ListReportDetailsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[storageinsights.ListReportDetailsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[storageinsights.ReportDetail]:
        async def async_generator():
            async for page in self.pages:
                for response in page.report_details:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
