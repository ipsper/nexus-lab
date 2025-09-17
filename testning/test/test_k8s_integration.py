"""
Kubernetes integration tests
"""
import pytest
from support.k8s_support import (
    test_cluster_running,
    test_nexus_pod_running,
    test_api_pod_running,
    test_kong_pod_running,
    test_services_available,
    test_pod_health
)


@pytest.mark.k8s
@pytest.mark.integration
def test_k8s_cluster_running(k8s_helper):
    """Test that Kubernetes cluster is running"""
    test_cluster_running(k8s_helper)


@pytest.mark.k8s
@pytest.mark.integration
def test_k8s_nexus_pod_running(k8s_helper):
    """Test that Nexus pod is running"""
    test_nexus_pod_running(k8s_helper)


@pytest.mark.k8s
@pytest.mark.integration
def test_k8s_api_pod_running(k8s_helper):
    """Test that FastAPI pod is running"""
    test_api_pod_running(k8s_helper)


@pytest.mark.k8s
@pytest.mark.integration
def test_k8s_kong_pod_running(k8s_helper):
    """Test that Kong pod is running"""
    test_kong_pod_running(k8s_helper)


@pytest.mark.k8s
@pytest.mark.integration
def test_k8s_services_available(k8s_helper):
    """Test that all required services are available"""
    test_services_available(k8s_helper)


@pytest.mark.k8s
@pytest.mark.integration
def test_k8s_pod_health(k8s_helper):
    """Test that pods are healthy"""
    test_pod_health(k8s_helper)
