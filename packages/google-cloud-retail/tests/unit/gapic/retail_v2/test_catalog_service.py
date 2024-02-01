# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.retail_v2.services.catalog_service import (
    CatalogServiceAsyncClient,
    CatalogServiceClient,
    pagers,
    transports,
)
from google.cloud.retail_v2.types import catalog
from google.cloud.retail_v2.types import catalog as gcr_catalog
from google.cloud.retail_v2.types import catalog_service, common, import_config


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


# Anonymous Credentials with universe domain property. If no universe domain is provided, then
# the default universe domain is "googleapis.com".
class _AnonymousCredentialsWithUniverseDomain(ga_credentials.AnonymousCredentials):
    def __init__(self, universe_domain="googleapis.com"):
        super(_AnonymousCredentialsWithUniverseDomain, self).__init__()
        self._universe_domain = universe_domain

    @property
    def universe_domain(self):
        return self._universe_domain


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CatalogServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


def test__read_environment_variables():
    assert CatalogServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert CatalogServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert CatalogServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            CatalogServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert CatalogServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert CatalogServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert CatalogServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            CatalogServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert CatalogServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert CatalogServiceClient._get_client_cert_source(None, False) is None
    assert (
        CatalogServiceClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        CatalogServiceClient._get_client_cert_source(mock_provided_cert_source, True)
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                CatalogServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                CatalogServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    CatalogServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceClient),
)
@mock.patch.object(
    CatalogServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = CatalogServiceClient._DEFAULT_UNIVERSE
    default_endpoint = CatalogServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = CatalogServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        CatalogServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        CatalogServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == CatalogServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CatalogServiceClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        CatalogServiceClient._get_api_endpoint(None, None, default_universe, "always")
        == CatalogServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CatalogServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == CatalogServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CatalogServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        CatalogServiceClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        CatalogServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        CatalogServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        CatalogServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        CatalogServiceClient._get_universe_domain(None, None)
        == CatalogServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        CatalogServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc"),
        (CatalogServiceClient, transports.CatalogServiceRestTransport, "rest"),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=_AnonymousCredentialsWithUniverseDomain())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # Test the case when there is a universe mismatch from the credentials.
    client = client_class(
        transport=transport_class(
            credentials=_AnonymousCredentialsWithUniverseDomain(
                universe_domain="foo.com"
            )
        )
    )
    with pytest.raises(ValueError) as excinfo:
        client._validate_universe_domain()
    assert (
        str(excinfo.value)
        == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
    )

    # Test the case when there is a universe mismatch from the client.
    #
    # TODO: Make this test unconditional once the minimum supported version of
    # google-api-core becomes 2.15.0 or higher.
    api_core_major, api_core_minor, _ = [
        int(part) for part in api_core_version.__version__.split(".")
    ]
    if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
        client = client_class(
            client_options={"universe_domain": "bar.com"},
            transport=transport_class(
                credentials=_AnonymousCredentialsWithUniverseDomain(),
            ),
        )
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CatalogServiceClient, "grpc"),
        (CatalogServiceAsyncClient, "grpc_asyncio"),
        (CatalogServiceClient, "rest"),
    ],
)
def test_catalog_service_client_from_service_account_info(client_class, transport_name):
    creds = _AnonymousCredentialsWithUniverseDomain()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "retail.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://retail.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CatalogServiceGrpcTransport, "grpc"),
        (transports.CatalogServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.CatalogServiceRestTransport, "rest"),
    ],
)
def test_catalog_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CatalogServiceClient, "grpc"),
        (CatalogServiceAsyncClient, "grpc_asyncio"),
        (CatalogServiceClient, "rest"),
    ],
)
def test_catalog_service_client_from_service_account_file(client_class, transport_name):
    creds = _AnonymousCredentialsWithUniverseDomain()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "retail.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://retail.googleapis.com"
        )


def test_catalog_service_client_get_transport_class():
    transport = CatalogServiceClient.get_transport_class()
    available_transports = [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceRestTransport,
    ]
    assert transport in available_transports

    transport = CatalogServiceClient.get_transport_class("grpc")
    assert transport == transports.CatalogServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CatalogServiceClient, transports.CatalogServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    CatalogServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceClient),
)
@mock.patch.object(
    CatalogServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceAsyncClient),
)
def test_catalog_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CatalogServiceClient, "get_transport_class") as gtc:
        transport = transport_class(
            credentials=_AnonymousCredentialsWithUniverseDomain()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CatalogServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc", "true"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc", "false"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (CatalogServiceClient, transports.CatalogServiceRestTransport, "rest", "true"),
        (CatalogServiceClient, transports.CatalogServiceRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    CatalogServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceClient),
)
@mock.patch.object(
    CatalogServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_catalog_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [CatalogServiceClient, CatalogServiceAsyncClient]
)
@mock.patch.object(
    CatalogServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CatalogServiceClient),
)
@mock.patch.object(
    CatalogServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CatalogServiceAsyncClient),
)
def test_catalog_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize(
    "client_class", [CatalogServiceClient, CatalogServiceAsyncClient]
)
@mock.patch.object(
    CatalogServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceClient),
)
@mock.patch.object(
    CatalogServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CatalogServiceAsyncClient),
)
def test_catalog_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = CatalogServiceClient._DEFAULT_UNIVERSE
    default_endpoint = CatalogServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = CatalogServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=_AnonymousCredentialsWithUniverseDomain(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=_AnonymousCredentialsWithUniverseDomain())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=_AnonymousCredentialsWithUniverseDomain())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )
    else:
        client = client_class(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CatalogServiceClient, transports.CatalogServiceRestTransport, "rest"),
    ],
)
def test_catalog_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            CatalogServiceClient,
            transports.CatalogServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (CatalogServiceClient, transports.CatalogServiceRestTransport, "rest", None),
    ],
)
def test_catalog_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_catalog_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.retail_v2.services.catalog_service.transports.CatalogServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CatalogServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            CatalogServiceClient,
            transports.CatalogServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_catalog_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = _AnonymousCredentialsWithUniverseDomain()
        file_creds = _AnonymousCredentialsWithUniverseDomain()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "retail.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="retail.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.ListCatalogsRequest,
        dict,
    ],
)
def test_list_catalogs(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.ListCatalogsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ListCatalogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_catalogs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        client.list_catalogs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ListCatalogsRequest()


@pytest.mark.asyncio
async def test_list_catalogs_async(
    transport: str = "grpc_asyncio", request_type=catalog_service.ListCatalogsRequest
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.ListCatalogsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ListCatalogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_catalogs_async_from_dict():
    await test_list_catalogs_async(request_type=dict)


def test_list_catalogs_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.ListCatalogsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        call.return_value = catalog_service.ListCatalogsResponse()
        client.list_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_catalogs_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.ListCatalogsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.ListCatalogsResponse()
        )
        await client.list_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_catalogs_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.ListCatalogsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_catalogs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_catalogs_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_catalogs(
            catalog_service.ListCatalogsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_catalogs_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.ListCatalogsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.ListCatalogsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_catalogs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_catalogs_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_catalogs(
            catalog_service.ListCatalogsRequest(),
            parent="parent_value",
        )


def test_list_catalogs_pager(transport_name: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_catalogs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, catalog.Catalog) for i in results)


def test_list_catalogs_pages(transport_name: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_catalogs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_catalogs_async_pager():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalogs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_catalogs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, catalog.Catalog) for i in responses)


@pytest.mark.asyncio
async def test_list_catalogs_async_pages():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalogs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_catalogs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.UpdateCatalogRequest,
        dict,
    ],
)
def test_update_catalog(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_catalog.Catalog(
            name="name_value",
            display_name="display_name_value",
        )
        response = client.update_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_catalog.Catalog)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_update_catalog_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_catalog), "__call__") as call:
        client.update_catalog()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCatalogRequest()


@pytest.mark.asyncio
async def test_update_catalog_async(
    transport: str = "grpc_asyncio", request_type=catalog_service.UpdateCatalogRequest
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcr_catalog.Catalog(
                name="name_value",
                display_name="display_name_value",
            )
        )
        response = await client.update_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_catalog.Catalog)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_catalog_async_from_dict():
    await test_update_catalog_async(request_type=dict)


def test_update_catalog_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateCatalogRequest()

    request.catalog.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_catalog), "__call__") as call:
        call.return_value = gcr_catalog.Catalog()
        client.update_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "catalog.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_catalog_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateCatalogRequest()

    request.catalog.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_catalog), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_catalog.Catalog())
        await client.update_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "catalog.name=name_value",
    ) in kw["metadata"]


def test_update_catalog_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_catalog.Catalog()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_catalog(
            catalog=gcr_catalog.Catalog(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].catalog
        mock_val = gcr_catalog.Catalog(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_catalog_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_catalog(
            catalog_service.UpdateCatalogRequest(),
            catalog=gcr_catalog.Catalog(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_catalog_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_catalog.Catalog()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_catalog.Catalog())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_catalog(
            catalog=gcr_catalog.Catalog(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].catalog
        mock_val = gcr_catalog.Catalog(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_catalog_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_catalog(
            catalog_service.UpdateCatalogRequest(),
            catalog=gcr_catalog.Catalog(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.SetDefaultBranchRequest,
        dict,
    ],
)
def test_set_default_branch(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.set_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.SetDefaultBranchRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_set_default_branch_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_default_branch), "__call__"
    ) as call:
        client.set_default_branch()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.SetDefaultBranchRequest()


@pytest.mark.asyncio
async def test_set_default_branch_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.SetDefaultBranchRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.set_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.SetDefaultBranchRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_set_default_branch_async_from_dict():
    await test_set_default_branch_async(request_type=dict)


def test_set_default_branch_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.SetDefaultBranchRequest()

    request.catalog = "catalog_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_default_branch), "__call__"
    ) as call:
        call.return_value = None
        client.set_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "catalog=catalog_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_default_branch_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.SetDefaultBranchRequest()

    request.catalog = "catalog_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_default_branch), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.set_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "catalog=catalog_value",
    ) in kw["metadata"]


def test_set_default_branch_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_default_branch(
            catalog="catalog_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].catalog
        mock_val = "catalog_value"
        assert arg == mock_val


def test_set_default_branch_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_default_branch(
            catalog_service.SetDefaultBranchRequest(),
            catalog="catalog_value",
        )


@pytest.mark.asyncio
async def test_set_default_branch_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_default_branch(
            catalog="catalog_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].catalog
        mock_val = "catalog_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_default_branch_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_default_branch(
            catalog_service.SetDefaultBranchRequest(),
            catalog="catalog_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.GetDefaultBranchRequest,
        dict,
    ],
)
def test_get_default_branch(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.GetDefaultBranchResponse(
            branch="branch_value",
            note="note_value",
        )
        response = client.get_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetDefaultBranchRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog_service.GetDefaultBranchResponse)
    assert response.branch == "branch_value"
    assert response.note == "note_value"


def test_get_default_branch_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_default_branch), "__call__"
    ) as call:
        client.get_default_branch()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetDefaultBranchRequest()


@pytest.mark.asyncio
async def test_get_default_branch_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.GetDefaultBranchRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.GetDefaultBranchResponse(
                branch="branch_value",
                note="note_value",
            )
        )
        response = await client.get_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetDefaultBranchRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog_service.GetDefaultBranchResponse)
    assert response.branch == "branch_value"
    assert response.note == "note_value"


@pytest.mark.asyncio
async def test_get_default_branch_async_from_dict():
    await test_get_default_branch_async(request_type=dict)


def test_get_default_branch_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetDefaultBranchRequest()

    request.catalog = "catalog_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_default_branch), "__call__"
    ) as call:
        call.return_value = catalog_service.GetDefaultBranchResponse()
        client.get_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "catalog=catalog_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_default_branch_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetDefaultBranchRequest()

    request.catalog = "catalog_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_default_branch), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.GetDefaultBranchResponse()
        )
        await client.get_default_branch(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "catalog=catalog_value",
    ) in kw["metadata"]


def test_get_default_branch_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.GetDefaultBranchResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_default_branch(
            catalog="catalog_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].catalog
        mock_val = "catalog_value"
        assert arg == mock_val


def test_get_default_branch_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_default_branch(
            catalog_service.GetDefaultBranchRequest(),
            catalog="catalog_value",
        )


@pytest.mark.asyncio
async def test_get_default_branch_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_default_branch), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.GetDefaultBranchResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.GetDefaultBranchResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_default_branch(
            catalog="catalog_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].catalog
        mock_val = "catalog_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_default_branch_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_default_branch(
            catalog_service.GetDefaultBranchRequest(),
            catalog="catalog_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.GetCompletionConfigRequest,
        dict,
    ],
)
def test_get_completion_config(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CompletionConfig(
            name="name_value",
            matching_order="matching_order_value",
            max_suggestions=1632,
            min_prefix_length=1810,
            auto_learning=True,
            last_suggestions_import_operation="last_suggestions_import_operation_value",
            last_denylist_import_operation="last_denylist_import_operation_value",
            last_allowlist_import_operation="last_allowlist_import_operation_value",
        )
        response = client.get_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetCompletionConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CompletionConfig)
    assert response.name == "name_value"
    assert response.matching_order == "matching_order_value"
    assert response.max_suggestions == 1632
    assert response.min_prefix_length == 1810
    assert response.auto_learning is True
    assert (
        response.last_suggestions_import_operation
        == "last_suggestions_import_operation_value"
    )
    assert (
        response.last_denylist_import_operation
        == "last_denylist_import_operation_value"
    )
    assert (
        response.last_allowlist_import_operation
        == "last_allowlist_import_operation_value"
    )


def test_get_completion_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_completion_config), "__call__"
    ) as call:
        client.get_completion_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetCompletionConfigRequest()


@pytest.mark.asyncio
async def test_get_completion_config_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.GetCompletionConfigRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CompletionConfig(
                name="name_value",
                matching_order="matching_order_value",
                max_suggestions=1632,
                min_prefix_length=1810,
                auto_learning=True,
                last_suggestions_import_operation="last_suggestions_import_operation_value",
                last_denylist_import_operation="last_denylist_import_operation_value",
                last_allowlist_import_operation="last_allowlist_import_operation_value",
            )
        )
        response = await client.get_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetCompletionConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CompletionConfig)
    assert response.name == "name_value"
    assert response.matching_order == "matching_order_value"
    assert response.max_suggestions == 1632
    assert response.min_prefix_length == 1810
    assert response.auto_learning is True
    assert (
        response.last_suggestions_import_operation
        == "last_suggestions_import_operation_value"
    )
    assert (
        response.last_denylist_import_operation
        == "last_denylist_import_operation_value"
    )
    assert (
        response.last_allowlist_import_operation
        == "last_allowlist_import_operation_value"
    )


@pytest.mark.asyncio
async def test_get_completion_config_async_from_dict():
    await test_get_completion_config_async(request_type=dict)


def test_get_completion_config_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetCompletionConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_completion_config), "__call__"
    ) as call:
        call.return_value = catalog.CompletionConfig()
        client.get_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_completion_config_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetCompletionConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_completion_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CompletionConfig()
        )
        await client.get_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_completion_config_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CompletionConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_completion_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_completion_config_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_completion_config(
            catalog_service.GetCompletionConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_completion_config_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CompletionConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CompletionConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_completion_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_completion_config_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_completion_config(
            catalog_service.GetCompletionConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.UpdateCompletionConfigRequest,
        dict,
    ],
)
def test_update_completion_config(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CompletionConfig(
            name="name_value",
            matching_order="matching_order_value",
            max_suggestions=1632,
            min_prefix_length=1810,
            auto_learning=True,
            last_suggestions_import_operation="last_suggestions_import_operation_value",
            last_denylist_import_operation="last_denylist_import_operation_value",
            last_allowlist_import_operation="last_allowlist_import_operation_value",
        )
        response = client.update_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCompletionConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CompletionConfig)
    assert response.name == "name_value"
    assert response.matching_order == "matching_order_value"
    assert response.max_suggestions == 1632
    assert response.min_prefix_length == 1810
    assert response.auto_learning is True
    assert (
        response.last_suggestions_import_operation
        == "last_suggestions_import_operation_value"
    )
    assert (
        response.last_denylist_import_operation
        == "last_denylist_import_operation_value"
    )
    assert (
        response.last_allowlist_import_operation
        == "last_allowlist_import_operation_value"
    )


def test_update_completion_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_completion_config), "__call__"
    ) as call:
        client.update_completion_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCompletionConfigRequest()


@pytest.mark.asyncio
async def test_update_completion_config_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.UpdateCompletionConfigRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CompletionConfig(
                name="name_value",
                matching_order="matching_order_value",
                max_suggestions=1632,
                min_prefix_length=1810,
                auto_learning=True,
                last_suggestions_import_operation="last_suggestions_import_operation_value",
                last_denylist_import_operation="last_denylist_import_operation_value",
                last_allowlist_import_operation="last_allowlist_import_operation_value",
            )
        )
        response = await client.update_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCompletionConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CompletionConfig)
    assert response.name == "name_value"
    assert response.matching_order == "matching_order_value"
    assert response.max_suggestions == 1632
    assert response.min_prefix_length == 1810
    assert response.auto_learning is True
    assert (
        response.last_suggestions_import_operation
        == "last_suggestions_import_operation_value"
    )
    assert (
        response.last_denylist_import_operation
        == "last_denylist_import_operation_value"
    )
    assert (
        response.last_allowlist_import_operation
        == "last_allowlist_import_operation_value"
    )


@pytest.mark.asyncio
async def test_update_completion_config_async_from_dict():
    await test_update_completion_config_async(request_type=dict)


def test_update_completion_config_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateCompletionConfigRequest()

    request.completion_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_completion_config), "__call__"
    ) as call:
        call.return_value = catalog.CompletionConfig()
        client.update_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "completion_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_completion_config_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateCompletionConfigRequest()

    request.completion_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_completion_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CompletionConfig()
        )
        await client.update_completion_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "completion_config.name=name_value",
    ) in kw["metadata"]


def test_update_completion_config_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CompletionConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_completion_config(
            completion_config=catalog.CompletionConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].completion_config
        mock_val = catalog.CompletionConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_completion_config_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_completion_config(
            catalog_service.UpdateCompletionConfigRequest(),
            completion_config=catalog.CompletionConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_completion_config_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_completion_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CompletionConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CompletionConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_completion_config(
            completion_config=catalog.CompletionConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].completion_config
        mock_val = catalog.CompletionConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_completion_config_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_completion_config(
            catalog_service.UpdateCompletionConfigRequest(),
            completion_config=catalog.CompletionConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.GetAttributesConfigRequest,
        dict,
    ],
)
def test_get_attributes_config(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )
        response = client.get_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetAttributesConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_get_attributes_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attributes_config), "__call__"
    ) as call:
        client.get_attributes_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetAttributesConfigRequest()


@pytest.mark.asyncio
async def test_get_attributes_config_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.GetAttributesConfigRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig(
                name="name_value",
                attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
            )
        )
        response = await client.get_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetAttributesConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


@pytest.mark.asyncio
async def test_get_attributes_config_async_from_dict():
    await test_get_attributes_config_async(request_type=dict)


def test_get_attributes_config_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetAttributesConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attributes_config), "__call__"
    ) as call:
        call.return_value = catalog.AttributesConfig()
        client.get_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_attributes_config_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetAttributesConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attributes_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig()
        )
        await client.get_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_attributes_config_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_attributes_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_attributes_config_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attributes_config(
            catalog_service.GetAttributesConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_attributes_config_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_attributes_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_attributes_config_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_attributes_config(
            catalog_service.GetAttributesConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.UpdateAttributesConfigRequest,
        dict,
    ],
)
def test_update_attributes_config(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )
        response = client.update_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateAttributesConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_update_attributes_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attributes_config), "__call__"
    ) as call:
        client.update_attributes_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateAttributesConfigRequest()


@pytest.mark.asyncio
async def test_update_attributes_config_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.UpdateAttributesConfigRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig(
                name="name_value",
                attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
            )
        )
        response = await client.update_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateAttributesConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


@pytest.mark.asyncio
async def test_update_attributes_config_async_from_dict():
    await test_update_attributes_config_async(request_type=dict)


def test_update_attributes_config_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateAttributesConfigRequest()

    request.attributes_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attributes_config), "__call__"
    ) as call:
        call.return_value = catalog.AttributesConfig()
        client.update_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_attributes_config_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateAttributesConfigRequest()

    request.attributes_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attributes_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig()
        )
        await client.update_attributes_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config.name=name_value",
    ) in kw["metadata"]


def test_update_attributes_config_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_attributes_config(
            attributes_config=catalog.AttributesConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].attributes_config
        mock_val = catalog.AttributesConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_attributes_config_flattened_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_attributes_config(
            catalog_service.UpdateAttributesConfigRequest(),
            attributes_config=catalog.AttributesConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_attributes_config_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attributes_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_attributes_config(
            attributes_config=catalog.AttributesConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].attributes_config
        mock_val = catalog.AttributesConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_attributes_config_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_attributes_config(
            catalog_service.UpdateAttributesConfigRequest(),
            attributes_config=catalog.AttributesConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.AddCatalogAttributeRequest,
        dict,
    ],
)
def test_add_catalog_attribute(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_catalog_attribute), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )
        response = client.add_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.AddCatalogAttributeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_add_catalog_attribute_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_catalog_attribute), "__call__"
    ) as call:
        client.add_catalog_attribute()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.AddCatalogAttributeRequest()


@pytest.mark.asyncio
async def test_add_catalog_attribute_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.AddCatalogAttributeRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_catalog_attribute), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig(
                name="name_value",
                attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
            )
        )
        response = await client.add_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.AddCatalogAttributeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


@pytest.mark.asyncio
async def test_add_catalog_attribute_async_from_dict():
    await test_add_catalog_attribute_async(request_type=dict)


def test_add_catalog_attribute_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.AddCatalogAttributeRequest()

    request.attributes_config = "attributes_config_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_catalog_attribute), "__call__"
    ) as call:
        call.return_value = catalog.AttributesConfig()
        client.add_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config=attributes_config_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_add_catalog_attribute_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.AddCatalogAttributeRequest()

    request.attributes_config = "attributes_config_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_catalog_attribute), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig()
        )
        await client.add_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config=attributes_config_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.RemoveCatalogAttributeRequest,
        dict,
    ],
)
def test_remove_catalog_attribute(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_catalog_attribute), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )
        response = client.remove_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.RemoveCatalogAttributeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_remove_catalog_attribute_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_catalog_attribute), "__call__"
    ) as call:
        client.remove_catalog_attribute()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.RemoveCatalogAttributeRequest()


@pytest.mark.asyncio
async def test_remove_catalog_attribute_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.RemoveCatalogAttributeRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_catalog_attribute), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig(
                name="name_value",
                attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
            )
        )
        response = await client.remove_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.RemoveCatalogAttributeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


@pytest.mark.asyncio
async def test_remove_catalog_attribute_async_from_dict():
    await test_remove_catalog_attribute_async(request_type=dict)


def test_remove_catalog_attribute_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.RemoveCatalogAttributeRequest()

    request.attributes_config = "attributes_config_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_catalog_attribute), "__call__"
    ) as call:
        call.return_value = catalog.AttributesConfig()
        client.remove_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config=attributes_config_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_remove_catalog_attribute_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.RemoveCatalogAttributeRequest()

    request.attributes_config = "attributes_config_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_catalog_attribute), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig()
        )
        await client.remove_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config=attributes_config_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.ReplaceCatalogAttributeRequest,
        dict,
    ],
)
def test_replace_catalog_attribute(request_type, transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_catalog_attribute), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )
        response = client.replace_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ReplaceCatalogAttributeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_replace_catalog_attribute_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_catalog_attribute), "__call__"
    ) as call:
        client.replace_catalog_attribute()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ReplaceCatalogAttributeRequest()


@pytest.mark.asyncio
async def test_replace_catalog_attribute_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.ReplaceCatalogAttributeRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_catalog_attribute), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig(
                name="name_value",
                attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
            )
        )
        response = await client.replace_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ReplaceCatalogAttributeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


@pytest.mark.asyncio
async def test_replace_catalog_attribute_async_from_dict():
    await test_replace_catalog_attribute_async(request_type=dict)


def test_replace_catalog_attribute_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.ReplaceCatalogAttributeRequest()

    request.attributes_config = "attributes_config_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_catalog_attribute), "__call__"
    ) as call:
        call.return_value = catalog.AttributesConfig()
        client.replace_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config=attributes_config_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_replace_catalog_attribute_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.ReplaceCatalogAttributeRequest()

    request.attributes_config = "attributes_config_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_catalog_attribute), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.AttributesConfig()
        )
        await client.replace_catalog_attribute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attributes_config=attributes_config_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.ListCatalogsRequest,
        dict,
    ],
)
def test_list_catalogs_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog_service.ListCatalogsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog_service.ListCatalogsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_catalogs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_catalogs_rest_required_fields(
    request_type=catalog_service.ListCatalogsRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).list_catalogs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).list_catalogs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog_service.ListCatalogsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog_service.ListCatalogsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_catalogs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_catalogs_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.list_catalogs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_catalogs_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_list_catalogs"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_list_catalogs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.ListCatalogsRequest.pb(
            catalog_service.ListCatalogsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog_service.ListCatalogsResponse.to_json(
            catalog_service.ListCatalogsResponse()
        )

        request = catalog_service.ListCatalogsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog_service.ListCatalogsResponse()

        client.list_catalogs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_catalogs_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.ListCatalogsRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_catalogs(request)


def test_list_catalogs_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog_service.ListCatalogsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog_service.ListCatalogsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_catalogs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/catalogs" % client.transport._host,
            args[1],
        )


def test_list_catalogs_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_catalogs(
            catalog_service.ListCatalogsRequest(),
            parent="parent_value",
        )


def test_list_catalogs_rest_pager(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            catalog_service.ListCatalogsResponse(
                catalogs=[
                    catalog.Catalog(),
                    catalog.Catalog(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            catalog_service.ListCatalogsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_catalogs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, catalog.Catalog) for i in results)

        pages = list(client.list_catalogs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.UpdateCatalogRequest,
        dict,
    ],
)
def test_update_catalog_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "catalog": {"name": "projects/sample1/locations/sample2/catalogs/sample3"}
    }
    request_init["catalog"] = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3",
        "display_name": "display_name_value",
        "product_level_config": {
            "ingestion_product_type": "ingestion_product_type_value",
            "merchant_center_product_id_field": "merchant_center_product_id_field_value",
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = catalog_service.UpdateCatalogRequest.meta.fields["catalog"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["catalog"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["catalog"][field])):
                    del request_init["catalog"][field][i][subfield]
            else:
                del request_init["catalog"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcr_catalog.Catalog(
            name="name_value",
            display_name="display_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcr_catalog.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_catalog(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_catalog.Catalog)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_update_catalog_rest_required_fields(
    request_type=catalog_service.UpdateCatalogRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).update_catalog._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).update_catalog._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcr_catalog.Catalog()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gcr_catalog.Catalog.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_catalog(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_catalog_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.update_catalog._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("catalog",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_catalog_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_update_catalog"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_update_catalog"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.UpdateCatalogRequest.pb(
            catalog_service.UpdateCatalogRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gcr_catalog.Catalog.to_json(gcr_catalog.Catalog())

        request = catalog_service.UpdateCatalogRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcr_catalog.Catalog()

        client.update_catalog(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_catalog_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.UpdateCatalogRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "catalog": {"name": "projects/sample1/locations/sample2/catalogs/sample3"}
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_catalog(request)


def test_update_catalog_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcr_catalog.Catalog()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "catalog": {"name": "projects/sample1/locations/sample2/catalogs/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            catalog=gcr_catalog.Catalog(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gcr_catalog.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_catalog(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{catalog.name=projects/*/locations/*/catalogs/*}"
            % client.transport._host,
            args[1],
        )


def test_update_catalog_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_catalog(
            catalog_service.UpdateCatalogRequest(),
            catalog=gcr_catalog.Catalog(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_catalog_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.SetDefaultBranchRequest,
        dict,
    ],
)
def test_set_default_branch_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"catalog": "projects/sample1/locations/sample2/catalogs/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_default_branch(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_default_branch_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_set_default_branch"
    ) as pre:
        pre.assert_not_called()
        pb_message = catalog_service.SetDefaultBranchRequest.pb(
            catalog_service.SetDefaultBranchRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = catalog_service.SetDefaultBranchRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.set_default_branch(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_set_default_branch_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.SetDefaultBranchRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"catalog": "projects/sample1/locations/sample2/catalogs/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_default_branch(request)


def test_set_default_branch_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "catalog": "projects/sample1/locations/sample2/catalogs/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            catalog="catalog_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.set_default_branch(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{catalog=projects/*/locations/*/catalogs/*}:setDefaultBranch"
            % client.transport._host,
            args[1],
        )


def test_set_default_branch_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_default_branch(
            catalog_service.SetDefaultBranchRequest(),
            catalog="catalog_value",
        )


def test_set_default_branch_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.GetDefaultBranchRequest,
        dict,
    ],
)
def test_get_default_branch_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"catalog": "projects/sample1/locations/sample2/catalogs/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog_service.GetDefaultBranchResponse(
            branch="branch_value",
            note="note_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog_service.GetDefaultBranchResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_default_branch(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog_service.GetDefaultBranchResponse)
    assert response.branch == "branch_value"
    assert response.note == "note_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_default_branch_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_get_default_branch"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_get_default_branch"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.GetDefaultBranchRequest.pb(
            catalog_service.GetDefaultBranchRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog_service.GetDefaultBranchResponse.to_json(
            catalog_service.GetDefaultBranchResponse()
        )

        request = catalog_service.GetDefaultBranchRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog_service.GetDefaultBranchResponse()

        client.get_default_branch(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_default_branch_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.GetDefaultBranchRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"catalog": "projects/sample1/locations/sample2/catalogs/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_default_branch(request)


def test_get_default_branch_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog_service.GetDefaultBranchResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "catalog": "projects/sample1/locations/sample2/catalogs/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            catalog="catalog_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog_service.GetDefaultBranchResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_default_branch(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{catalog=projects/*/locations/*/catalogs/*}:getDefaultBranch"
            % client.transport._host,
            args[1],
        )


def test_get_default_branch_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_default_branch(
            catalog_service.GetDefaultBranchRequest(),
            catalog="catalog_value",
        )


def test_get_default_branch_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.GetCompletionConfigRequest,
        dict,
    ],
)
def test_get_completion_config_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/completionConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.CompletionConfig(
            name="name_value",
            matching_order="matching_order_value",
            max_suggestions=1632,
            min_prefix_length=1810,
            auto_learning=True,
            last_suggestions_import_operation="last_suggestions_import_operation_value",
            last_denylist_import_operation="last_denylist_import_operation_value",
            last_allowlist_import_operation="last_allowlist_import_operation_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.CompletionConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_completion_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CompletionConfig)
    assert response.name == "name_value"
    assert response.matching_order == "matching_order_value"
    assert response.max_suggestions == 1632
    assert response.min_prefix_length == 1810
    assert response.auto_learning is True
    assert (
        response.last_suggestions_import_operation
        == "last_suggestions_import_operation_value"
    )
    assert (
        response.last_denylist_import_operation
        == "last_denylist_import_operation_value"
    )
    assert (
        response.last_allowlist_import_operation
        == "last_allowlist_import_operation_value"
    )


def test_get_completion_config_rest_required_fields(
    request_type=catalog_service.GetCompletionConfigRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get_completion_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get_completion_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog.CompletionConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog.CompletionConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_completion_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_completion_config_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.get_completion_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_completion_config_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_get_completion_config"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_get_completion_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.GetCompletionConfigRequest.pb(
            catalog_service.GetCompletionConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog.CompletionConfig.to_json(
            catalog.CompletionConfig()
        )

        request = catalog_service.GetCompletionConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog.CompletionConfig()

        client.get_completion_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_completion_config_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.GetCompletionConfigRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/completionConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_completion_config(request)


def test_get_completion_config_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.CompletionConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/completionConfig"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.CompletionConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_completion_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/catalogs/*/completionConfig}"
            % client.transport._host,
            args[1],
        )


def test_get_completion_config_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_completion_config(
            catalog_service.GetCompletionConfigRequest(),
            name="name_value",
        )


def test_get_completion_config_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.UpdateCompletionConfigRequest,
        dict,
    ],
)
def test_update_completion_config_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "completion_config": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/completionConfig"
        }
    }
    request_init["completion_config"] = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/completionConfig",
        "matching_order": "matching_order_value",
        "max_suggestions": 1632,
        "min_prefix_length": 1810,
        "auto_learning": True,
        "suggestions_input_config": {
            "big_query_source": {
                "partition_date": {"year": 433, "month": 550, "day": 318},
                "project_id": "project_id_value",
                "dataset_id": "dataset_id_value",
                "table_id": "table_id_value",
                "gcs_staging_dir": "gcs_staging_dir_value",
                "data_schema": "data_schema_value",
            }
        },
        "last_suggestions_import_operation": "last_suggestions_import_operation_value",
        "denylist_input_config": {},
        "last_denylist_import_operation": "last_denylist_import_operation_value",
        "allowlist_input_config": {},
        "last_allowlist_import_operation": "last_allowlist_import_operation_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = catalog_service.UpdateCompletionConfigRequest.meta.fields[
        "completion_config"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["completion_config"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["completion_config"][field])):
                    del request_init["completion_config"][field][i][subfield]
            else:
                del request_init["completion_config"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.CompletionConfig(
            name="name_value",
            matching_order="matching_order_value",
            max_suggestions=1632,
            min_prefix_length=1810,
            auto_learning=True,
            last_suggestions_import_operation="last_suggestions_import_operation_value",
            last_denylist_import_operation="last_denylist_import_operation_value",
            last_allowlist_import_operation="last_allowlist_import_operation_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.CompletionConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_completion_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CompletionConfig)
    assert response.name == "name_value"
    assert response.matching_order == "matching_order_value"
    assert response.max_suggestions == 1632
    assert response.min_prefix_length == 1810
    assert response.auto_learning is True
    assert (
        response.last_suggestions_import_operation
        == "last_suggestions_import_operation_value"
    )
    assert (
        response.last_denylist_import_operation
        == "last_denylist_import_operation_value"
    )
    assert (
        response.last_allowlist_import_operation
        == "last_allowlist_import_operation_value"
    )


def test_update_completion_config_rest_required_fields(
    request_type=catalog_service.UpdateCompletionConfigRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).update_completion_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).update_completion_config._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog.CompletionConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog.CompletionConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_completion_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_completion_config_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.update_completion_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("completionConfig",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_completion_config_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_update_completion_config"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_update_completion_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.UpdateCompletionConfigRequest.pb(
            catalog_service.UpdateCompletionConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog.CompletionConfig.to_json(
            catalog.CompletionConfig()
        )

        request = catalog_service.UpdateCompletionConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog.CompletionConfig()

        client.update_completion_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_completion_config_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.UpdateCompletionConfigRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "completion_config": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/completionConfig"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_completion_config(request)


def test_update_completion_config_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.CompletionConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "completion_config": {
                "name": "projects/sample1/locations/sample2/catalogs/sample3/completionConfig"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            completion_config=catalog.CompletionConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.CompletionConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_completion_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{completion_config.name=projects/*/locations/*/catalogs/*/completionConfig}"
            % client.transport._host,
            args[1],
        )


def test_update_completion_config_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_completion_config(
            catalog_service.UpdateCompletionConfigRequest(),
            completion_config=catalog.CompletionConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_completion_config_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.GetAttributesConfigRequest,
        dict,
    ],
)
def test_get_attributes_config_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.AttributesConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_attributes_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_get_attributes_config_rest_required_fields(
    request_type=catalog_service.GetAttributesConfigRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get_attributes_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).get_attributes_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog.AttributesConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog.AttributesConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_attributes_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_attributes_config_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.get_attributes_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_attributes_config_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_get_attributes_config"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_get_attributes_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.GetAttributesConfigRequest.pb(
            catalog_service.GetAttributesConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog.AttributesConfig.to_json(
            catalog.AttributesConfig()
        )

        request = catalog_service.GetAttributesConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog.AttributesConfig()

        client.get_attributes_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_attributes_config_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.GetAttributesConfigRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_attributes_config(request)


def test_get_attributes_config_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.AttributesConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.AttributesConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_attributes_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/catalogs/*/attributesConfig}"
            % client.transport._host,
            args[1],
        )


def test_get_attributes_config_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attributes_config(
            catalog_service.GetAttributesConfigRequest(),
            name="name_value",
        )


def test_get_attributes_config_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.UpdateAttributesConfigRequest,
        dict,
    ],
)
def test_update_attributes_config_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
        }
    }
    request_init["attributes_config"] = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig",
        "catalog_attributes": {},
        "attribute_config_level": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = catalog_service.UpdateAttributesConfigRequest.meta.fields[
        "attributes_config"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["attributes_config"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["attributes_config"][field])):
                    del request_init["attributes_config"][field][i][subfield]
            else:
                del request_init["attributes_config"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.AttributesConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_attributes_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_update_attributes_config_rest_required_fields(
    request_type=catalog_service.UpdateAttributesConfigRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).update_attributes_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).update_attributes_config._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog.AttributesConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog.AttributesConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_attributes_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_attributes_config_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.update_attributes_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("attributesConfig",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_attributes_config_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_update_attributes_config"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_update_attributes_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.UpdateAttributesConfigRequest.pb(
            catalog_service.UpdateAttributesConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog.AttributesConfig.to_json(
            catalog.AttributesConfig()
        )

        request = catalog_service.UpdateAttributesConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog.AttributesConfig()

        client.update_attributes_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_attributes_config_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.UpdateAttributesConfigRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_attributes_config(request)


def test_update_attributes_config_rest_flattened():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.AttributesConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "attributes_config": {
                "name": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            attributes_config=catalog.AttributesConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.AttributesConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_attributes_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{attributes_config.name=projects/*/locations/*/catalogs/*/attributesConfig}"
            % client.transport._host,
            args[1],
        )


def test_update_attributes_config_rest_flattened_error(transport: str = "rest"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_attributes_config(
            catalog_service.UpdateAttributesConfigRequest(),
            attributes_config=catalog.AttributesConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_attributes_config_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.AddCatalogAttributeRequest,
        dict,
    ],
)
def test_add_catalog_attribute_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.AttributesConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_catalog_attribute(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_add_catalog_attribute_rest_required_fields(
    request_type=catalog_service.AddCatalogAttributeRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request_init["attributes_config"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).add_catalog_attribute._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["attributesConfig"] = "attributes_config_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).add_catalog_attribute._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "attributesConfig" in jsonified_request
    assert jsonified_request["attributesConfig"] == "attributes_config_value"

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog.AttributesConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog.AttributesConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.add_catalog_attribute(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_add_catalog_attribute_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.add_catalog_attribute._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "attributesConfig",
                "catalogAttribute",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_add_catalog_attribute_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_add_catalog_attribute"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_add_catalog_attribute"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.AddCatalogAttributeRequest.pb(
            catalog_service.AddCatalogAttributeRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog.AttributesConfig.to_json(
            catalog.AttributesConfig()
        )

        request = catalog_service.AddCatalogAttributeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog.AttributesConfig()

        client.add_catalog_attribute(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_add_catalog_attribute_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.AddCatalogAttributeRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_catalog_attribute(request)


def test_add_catalog_attribute_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.RemoveCatalogAttributeRequest,
        dict,
    ],
)
def test_remove_catalog_attribute_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.AttributesConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_catalog_attribute(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_remove_catalog_attribute_rest_required_fields(
    request_type=catalog_service.RemoveCatalogAttributeRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request_init["attributes_config"] = ""
    request_init["key"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).remove_catalog_attribute._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["attributesConfig"] = "attributes_config_value"
    jsonified_request["key"] = "key_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).remove_catalog_attribute._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "attributesConfig" in jsonified_request
    assert jsonified_request["attributesConfig"] == "attributes_config_value"
    assert "key" in jsonified_request
    assert jsonified_request["key"] == "key_value"

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog.AttributesConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog.AttributesConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.remove_catalog_attribute(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_remove_catalog_attribute_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.remove_catalog_attribute._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "attributesConfig",
                "key",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_catalog_attribute_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_remove_catalog_attribute"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_remove_catalog_attribute"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.RemoveCatalogAttributeRequest.pb(
            catalog_service.RemoveCatalogAttributeRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog.AttributesConfig.to_json(
            catalog.AttributesConfig()
        )

        request = catalog_service.RemoveCatalogAttributeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog.AttributesConfig()

        client.remove_catalog_attribute(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_remove_catalog_attribute_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.RemoveCatalogAttributeRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.remove_catalog_attribute(request)


def test_remove_catalog_attribute_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        catalog_service.ReplaceCatalogAttributeRequest,
        dict,
    ],
)
def test_replace_catalog_attribute_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = catalog.AttributesConfig(
            name="name_value",
            attribute_config_level=common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = catalog.AttributesConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.replace_catalog_attribute(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.AttributesConfig)
    assert response.name == "name_value"
    assert (
        response.attribute_config_level
        == common.AttributeConfigLevel.PRODUCT_LEVEL_ATTRIBUTE_CONFIG
    )


def test_replace_catalog_attribute_rest_required_fields(
    request_type=catalog_service.ReplaceCatalogAttributeRequest,
):
    transport_class = transports.CatalogServiceRestTransport

    request_init = {}
    request_init["attributes_config"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).replace_catalog_attribute._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["attributesConfig"] = "attributes_config_value"

    unset_fields = transport_class(
        credentials=_AnonymousCredentialsWithUniverseDomain()
    ).replace_catalog_attribute._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "attributesConfig" in jsonified_request
    assert jsonified_request["attributesConfig"] == "attributes_config_value"

    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = catalog.AttributesConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = catalog.AttributesConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.replace_catalog_attribute(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_replace_catalog_attribute_rest_unset_required_fields():
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain
    )

    unset_fields = transport.replace_catalog_attribute._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "attributesConfig",
                "catalogAttribute",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_replace_catalog_attribute_rest_interceptors(null_interceptor):
    transport = transports.CatalogServiceRestTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        interceptor=None
        if null_interceptor
        else transports.CatalogServiceRestInterceptor(),
    )
    client = CatalogServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "post_replace_catalog_attribute"
    ) as post, mock.patch.object(
        transports.CatalogServiceRestInterceptor, "pre_replace_catalog_attribute"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = catalog_service.ReplaceCatalogAttributeRequest.pb(
            catalog_service.ReplaceCatalogAttributeRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = catalog.AttributesConfig.to_json(
            catalog.AttributesConfig()
        )

        request = catalog_service.ReplaceCatalogAttributeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = catalog.AttributesConfig()

        client.replace_catalog_attribute(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_replace_catalog_attribute_rest_bad_request(
    transport: str = "rest", request_type=catalog_service.ReplaceCatalogAttributeRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attributes_config": "projects/sample1/locations/sample2/catalogs/sample3/attributesConfig"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.replace_catalog_attribute(request)


def test_replace_catalog_attribute_rest_error():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            client_options=options,
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    client = CatalogServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CatalogServiceGrpcAsyncIOTransport(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
        transports.CatalogServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = CatalogServiceClient.get_transport_class(transport_name)(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    assert isinstance(
        client.transport,
        transports.CatalogServiceGrpcTransport,
    )


def test_catalog_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CatalogServiceTransport(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            credentials_file="credentials.json",
        )


def test_catalog_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.retail_v2.services.catalog_service.transports.CatalogServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CatalogServiceTransport(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_catalogs",
        "update_catalog",
        "set_default_branch",
        "get_default_branch",
        "get_completion_config",
        "update_completion_config",
        "get_attributes_config",
        "update_attributes_config",
        "add_catalog_attribute",
        "remove_catalog_attribute",
        "replace_catalog_attribute",
        "get_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_catalog_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.retail_v2.services.catalog_service.transports.CatalogServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        transport = transports.CatalogServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_catalog_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.retail_v2.services.catalog_service.transports.CatalogServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        transport = transports.CatalogServiceTransport()
        adc.assert_called_once()


def test_catalog_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        CatalogServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
def test_catalog_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (_AnonymousCredentialsWithUniverseDomain(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
        transports.CatalogServiceRestTransport,
    ],
)
def test_catalog_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.CatalogServiceGrpcTransport, grpc_helpers),
        (transports.CatalogServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_catalog_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = _AnonymousCredentialsWithUniverseDomain()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "retail.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="retail.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
def test_catalog_service_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = _AnonymousCredentialsWithUniverseDomain()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_catalog_service_http_transport_client_cert_source_for_mtls():
    cred = _AnonymousCredentialsWithUniverseDomain()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.CatalogServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_catalog_service_host_no_port(transport_name):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        client_options=client_options.ClientOptions(
            api_endpoint="retail.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "retail.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://retail.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_catalog_service_host_with_port(transport_name):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        client_options=client_options.ClientOptions(
            api_endpoint="retail.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "retail.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://retail.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_catalog_service_client_transport_session_collision(transport_name):
    creds1 = _AnonymousCredentialsWithUniverseDomain()
    creds2 = _AnonymousCredentialsWithUniverseDomain()
    client1 = CatalogServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = CatalogServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_catalogs._session
    session2 = client2.transport.list_catalogs._session
    assert session1 != session2
    session1 = client1.transport.update_catalog._session
    session2 = client2.transport.update_catalog._session
    assert session1 != session2
    session1 = client1.transport.set_default_branch._session
    session2 = client2.transport.set_default_branch._session
    assert session1 != session2
    session1 = client1.transport.get_default_branch._session
    session2 = client2.transport.get_default_branch._session
    assert session1 != session2
    session1 = client1.transport.get_completion_config._session
    session2 = client2.transport.get_completion_config._session
    assert session1 != session2
    session1 = client1.transport.update_completion_config._session
    session2 = client2.transport.update_completion_config._session
    assert session1 != session2
    session1 = client1.transport.get_attributes_config._session
    session2 = client2.transport.get_attributes_config._session
    assert session1 != session2
    session1 = client1.transport.update_attributes_config._session
    session2 = client2.transport.update_attributes_config._session
    assert session1 != session2
    session1 = client1.transport.add_catalog_attribute._session
    session2 = client2.transport.add_catalog_attribute._session
    assert session1 != session2
    session1 = client1.transport.remove_catalog_attribute._session
    session2 = client2.transport.remove_catalog_attribute._session
    assert session1 != session2
    session1 = client1.transport.replace_catalog_attribute._session
    session2 = client2.transport.replace_catalog_attribute._session
    assert session1 != session2


def test_catalog_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CatalogServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_catalog_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CatalogServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
def test_catalog_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = _AnonymousCredentialsWithUniverseDomain()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
def test_catalog_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_attributes_config_path():
    project = "squid"
    location = "clam"
    catalog = "whelk"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/attributesConfig".format(
        project=project,
        location=location,
        catalog=catalog,
    )
    actual = CatalogServiceClient.attributes_config_path(project, location, catalog)
    assert expected == actual


def test_parse_attributes_config_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "catalog": "nudibranch",
    }
    path = CatalogServiceClient.attributes_config_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_attributes_config_path(path)
    assert expected == actual


def test_branch_path():
    project = "cuttlefish"
    location = "mussel"
    catalog = "winkle"
    branch = "nautilus"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/branches/{branch}".format(
        project=project,
        location=location,
        catalog=catalog,
        branch=branch,
    )
    actual = CatalogServiceClient.branch_path(project, location, catalog, branch)
    assert expected == actual


def test_parse_branch_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "catalog": "squid",
        "branch": "clam",
    }
    path = CatalogServiceClient.branch_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_branch_path(path)
    assert expected == actual


def test_catalog_path():
    project = "whelk"
    location = "octopus"
    catalog = "oyster"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}".format(
        project=project,
        location=location,
        catalog=catalog,
    )
    actual = CatalogServiceClient.catalog_path(project, location, catalog)
    assert expected == actual


def test_parse_catalog_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "catalog": "mussel",
    }
    path = CatalogServiceClient.catalog_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_catalog_path(path)
    assert expected == actual


def test_completion_config_path():
    project = "winkle"
    location = "nautilus"
    catalog = "scallop"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/completionConfig".format(
        project=project,
        location=location,
        catalog=catalog,
    )
    actual = CatalogServiceClient.completion_config_path(project, location, catalog)
    assert expected == actual


def test_parse_completion_config_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "catalog": "clam",
    }
    path = CatalogServiceClient.completion_config_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_completion_config_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CatalogServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = CatalogServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CatalogServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = CatalogServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CatalogServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = CatalogServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CatalogServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = CatalogServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CatalogServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = CatalogServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CatalogServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CatalogServiceClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CatalogServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CatalogServiceClient.get_transport_class()
        transport = transport_class(
            credentials=_AnonymousCredentialsWithUniverseDomain(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_get_operation(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = CatalogServiceClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = CatalogServiceAsyncClient(
        credentials=_AnonymousCredentialsWithUniverseDomain(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = CatalogServiceClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = CatalogServiceClient(
            credentials=_AnonymousCredentialsWithUniverseDomain(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport),
        (CatalogServiceAsyncClient, transports.CatalogServiceGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
