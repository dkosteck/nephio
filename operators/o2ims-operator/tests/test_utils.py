import responses
import sys
import os
import pytest
import random
import string

from controllers.utils import *

NAME = "test_name"
NAMESPACE = "test_ns"
TEST_JSON = {"status": {"conditions": [{"message": "test"}]}}
PACKAGE_VARIANTS_URI = f"{KUBERNETES_BASE_URL}/apis/config.porch.kpt.dev/v1alpha1/namespaces/{NAMESPACE}/packagevariants/{NAME}"
PACKAGE_REVISIONS_URI = f"{KUBERNETES_BASE_URL}/apis/porch.kpt.dev/v1alpha1/namespaces/{NAMESPACE}/packagerevisions/{NAME}"
PROVISIONING_REQUEST_URI = f"{KUBERNETES_BASE_URL}/apis/o2ims.provisioning.oran.org/v1alpha1/provisioningrequests"
CAPI_URI = f"{KUBERNETES_BASE_URL}/apis/cluster.x-k8s.io/v1beta1/namespaces/{NAMESPACE}/clusters/{NAME}"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Create a test token in /tmp
    test_utils_token_path = "/tmp/test_utils_token"
    test_utils_token_path += "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )
    os.environ["TOKEN"] = test_utils_token_path
    with open(test_utils_token_path, "w") as fp:
        pass
    # Wait for tests to finish
    yield NAME, NAMESPACE
    # Cleanup token
    if os.path.exists(test_utils_token_path):
        os.remove(test_utils_token_path)


@responses.activate
def test_create_package_variant():
    pass


@responses.activate
@pytest.mark.parametrize(
    "http_codes, status, response_2, response_2_value, exception",
    [
        (200, True, "name", NAME, False),
        (202, True, "name", NAME, False),
        (204, True, "name", NAME, False),
        (401, False, "reason", "unauthorized", False),
        (403, False, "reason", "unauthorized", False),
        (404, False, "reason", "notFound", False),
        (1234, False, "reason", TEST_JSON, False),
        (None, False, "reason", "NotAbleToCommunicateWithTheCluster ", True),
    ],
)
def test_delete_package_variant(
    http_codes, status, response_2, response_2_value, exception
):
    if not exception:
        responses.delete(
            PACKAGE_VARIANTS_URI,
            json=TEST_JSON,
            status=http_codes,
        )
    else:
        responses.delete(
            PACKAGE_VARIANTS_URI,
            body=Exception(""),
        )
    response = delete_package_variant(NAME, NAMESPACE)
    assert response["status"] == status and response[response_2] == response_2_value


@responses.activate
@pytest.mark.parametrize(
    "http_codes, status, response_2, response_2_value, response_3, response_3_value, exception",
    [
        (200, True, "name", NAME, "body", TEST_JSON, False),
        (401, False, "reason", "unauthorized", None, None, False),
        (403, False, "reason", "unauthorized", None, None, False),
        (404, False, "reason", "notFound", None, None, False),
        (1234, False, "reason", TEST_JSON, None, None, False),
        (
            None,
            False,
            "reason",
            "NotAbleToCommunicateWithTheCluster ",
            None,
            None,
            True,
        ),
    ],
)
def test_get_package_variant(
    http_codes,
    status,
    response_2,
    response_2_value,
    response_3,
    response_3_value,
    exception,
):
    if not exception:
        responses.get(
            PACKAGE_VARIANTS_URI,
            json=TEST_JSON,
            status=http_codes,
        )
    else:
        responses.get(
            PACKAGE_VARIANTS_URI,
            body=Exception(""),
        )
    response = get_package_variant(NAME, NAMESPACE)
    assert response["status"] == status and response[response_2] == response_2_value
    if response_3:
        assert response[response_3] == response_3_value


@responses.activate
def test_get_package_revisions_for_package_variant():
    pass


@responses.activate
@pytest.mark.parametrize(
    "http_codes, status, response_2, response_2_value, exception",
    [
        (200, True, "name", NAME, False),
        (202, True, "name", NAME, False),
        (204, True, "name", NAME, False),
        (401, False, "reason", "unauthorized", False),
        (403, False, "reason", "unauthorized", False),
        (404, False, "reason", "notFound", False),
        (1234, False, "reason", TEST_JSON, False),
        (None, False, "reason", "NotAbleToCommunicateWithTheCluster ", True),
    ],
)
def test_delete_package_revision(
    http_codes, status, response_2, response_2_value, exception
):
    if not exception:
        responses.delete(
            PACKAGE_REVISIONS_URI,
            json=TEST_JSON,
            status=http_codes,
        )
    else:
        responses.delete(
            PACKAGE_REVISIONS_URI,
            body=Exception(""),
        )
    response = delete_package_revision(NAME, NAMESPACE)
    assert response["status"] == status and response[response_2] == response_2_value


@responses.activate
def test_check_o2ims_provisioning_request():
    pass


@responses.activate
@pytest.mark.parametrize(
    "http_codes, status, response_2, response_2_value, exception",
    [
        (200, True, "body", TEST_JSON, False),
        (401, False, "reason", "unauthorized", False),
        (403, False, "reason", "unauthorized", False),
        (404, False, "reason", "notFound", False),
        (1234, False, "reason", TEST_JSON["status"]["conditions"][0]["message"], False),
        (None, False, "reason", "NotAbleToCommunicateWithTheCluster ", True),
    ],
)
def test_get_capi_cluster(http_codes, status, response_2, response_2_value, exception):
    if not exception:
        responses.get(
            CAPI_URI,
            json=TEST_JSON,
            status=http_codes,
        )
    else:
        responses.get(
            CAPI_URI,
            body=Exception(""),
        )
    response = get_capi_cluster(NAME, NAMESPACE)
    assert response["status"] == status and response[response_2] == response_2_value
