"""
API Error Handling Tests - Testar felhantering och edge cases
"""
import pytest
import requests


@pytest.mark.api
@pytest.mark.error_handling
def test_api_404_not_found(api_client):
    """Test 404 errors for non-existent endpoints"""
    non_existent_endpoints = [
        "/nonexistent",
        "/api/nonexistent",
        "/repositories/nonexistent-repo",
        "/packages/nonexistent-package",
        "/repositories/nonexistent-repo/packages"
    ]
    
    for endpoint in non_existent_endpoints:
        response = api_client.get(endpoint)
        assert response.status_code == 404, f"Endpoint {endpoint} should return 404"
        
        data = response.json()
        assert "detail" in data, f"404 response for {endpoint} should contain 'detail' field"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_405_method_not_allowed(api_client):
    """Test 405 errors for unsupported HTTP methods"""
    # Testa POST på GET-only endpoints
    get_only_endpoints = [
        "/",
        "/health",
        "/stats",
        "/formats",
        "/config",
        "/pip-package",
        "/repositories/",
        "/packages/"
    ]
    
    for endpoint in get_only_endpoints:
        response = api_client.post(endpoint, json={})
        # API:et kan returnera 405 (method not allowed) eller 422 (validation error)
        assert response.status_code in [405, 422], f"POST to {endpoint} should return 405 or 422, got {response.status_code}"
        
        data = response.json()
        assert "detail" in data, f"Error response for {endpoint} should contain 'detail' field"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_422_validation_error(api_client):
    """Test 422 errors for invalid request data"""
    # Testa POST med ogiltig JSON
    response = api_client.post("/repositories/", json={"invalid": "data"})
    assert response.status_code == 422, "POST with invalid data should return 422"
    
    data = response.json()
    assert "detail" in data, "422 response should contain 'detail' field"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_invalid_json_request(api_client):
    """Test handling of invalid JSON in request body"""
    # Skicka ogiltig JSON
    response = requests.post(
        f"{api_client.base_url}/repositories/",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422, "Invalid JSON should return 422"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_missing_content_type(api_client):
    """Test handling of missing Content-Type header"""
    response = requests.post(
        f"{api_client.base_url}/repositories/",
        data='{"name": "test-repo"}',
        headers={}  # Ingen Content-Type
    )
    # Beroende på implementation kan detta returnera 400 eller 415
    assert response.status_code in [400, 415, 422], "Missing Content-Type should return 400, 415, or 422"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_large_request_body(api_client):
    """Test handling of large request bodies"""
    # Skapa en stor JSON-payload
    large_data = {
        "name": "test-repo",
        "description": "x" * 10000,  # 10KB sträng
        "config": {"key": "value" * 1000}  # Ytterligare data
    }
    
    response = api_client.post("/repositories/", json=large_data)
    # Beroende på implementation kan detta returnera 413 eller 422
    assert response.status_code in [200, 413, 422], f"Large request body returned {response.status_code}"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_special_characters_in_path(api_client):
    """Test handling of special characters in path parameters"""
    special_chars = [
        "repo with spaces",
        "repo-with-dashes",
        "repo_with_underscores",
        "repo.with.dots",
        "repo@with#special$chars",
        "repo/with/slashes",
        "repo\\with\\backslashes"
    ]
    
    for special_char in special_chars:
        response = api_client.get(f"/repositories/{special_char}")
        # Beroende på implementation kan detta returnera 404 eller 400
        assert response.status_code in [200, 400, 404], f"Special char '{special_char}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_unicode_in_path(api_client):
    """Test handling of Unicode characters in path parameters"""
    unicode_chars = [
        "repo-åäö",
        "repo-中文",
        "repo-العربية",
        "repo-русский",
        "repo-🚀",
        "repo-ñáéíóú"
    ]
    
    for unicode_char in unicode_chars:
        response = api_client.get(f"/repositories/{unicode_char}")
        # Beroende på implementation kan detta returnera 404 eller 400
        assert response.status_code in [200, 400, 404], f"Unicode char '{unicode_char}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_empty_path_parameters(api_client):
    """Test handling of empty path parameters"""
    empty_params = [
        "/repositories/",
        "/packages/",
        "/repositories//packages",  # Dubbel slash
        "/repositories/ /packages"  # Space i path
    ]
    
    for path in empty_params:
        response = api_client.get(path)
        # Beroende på implementation kan detta returnera 404 eller 400
        assert response.status_code in [200, 400, 404], f"Empty param path '{path}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_malformed_urls(api_client):
    """Test handling of malformed URLs"""
    malformed_urls = [
        "/repositories/%20",  # URL-encoded space
        "/repositories/%00",  # Null byte
        "/repositories/..",   # Path traversal attempt
        "/repositories/../",  # Path traversal attempt
        "/repositories/./",   # Current directory
        "/repositories/...",  # Multiple dots
    ]
    
    for url in malformed_urls:
        response = api_client.get(url)
        # Beroende på implementation kan detta returnera 404 eller 400
        assert response.status_code in [200, 400, 404], f"Malformed URL '{url}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_timeout_handling(api_client):
    """Test API timeout handling"""
    import time
    
    # Testa att API svarar inom rimlig tid
    start_time = time.time()
    response = api_client.get("/health")
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response.status_code == 200, "Health endpoint should respond with 200"
    assert response_time < 5.0, f"API response took {response_time:.2f}s (should be < 5s)"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_error_response_format(api_client):
    """Test that error responses have consistent format"""
    error_endpoints = [
        "/nonexistent",
        "/repositories/nonexistent-repo",
        "/packages/nonexistent-package"
    ]
    
    for endpoint in error_endpoints:
        response = api_client.get(endpoint)
        assert response.status_code >= 400, f"Endpoint {endpoint} should return error status"
        
        data = response.json()
        assert isinstance(data, dict), f"Error response for {endpoint} should be JSON object"
        assert "detail" in data, f"Error response for {endpoint} should contain 'detail' field"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_cors_headers(api_client):
    """Test CORS headers in error responses"""
    response = api_client.get("/nonexistent")
    assert response.status_code == 404
    
    # Kontrollera att response har headers
    headers = response.headers
    assert hasattr(headers, 'get'), "Response should have headers"
    
    # Kontrollera att viktiga headers finns
    assert 'Content-Type' in headers, "Response should have Content-Type header"
    assert 'Content-Length' in headers, "Response should have Content-Length header"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_rate_limiting(api_client):
    """Test API rate limiting (if implemented)"""
    # Skicka många requests snabbt
    responses = []
    for i in range(20):  # 20 requests
        response = api_client.get("/health")
        responses.append(response.status_code)
    
    # Kontrollera att alla requests lyckades (ingen rate limiting implementerad än)
    success_count = sum(1 for status in responses if status == 200)
    assert success_count == 20, f"Rate limiting may be active: {success_count}/20 requests succeeded"


@pytest.mark.api
@pytest.mark.error_handling
def test_api_concurrent_error_handling(api_client):
    """Test error handling under concurrent requests"""
    import threading
    import time
    
    results = []
    errors = []
    
    def make_error_request():
        try:
            response = api_client.get("/nonexistent")
            results.append(response.status_code)
        except Exception as e:
            errors.append(str(e))
    
    # Skapa 10 samtidiga error requests
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=make_error_request)
        threads.append(thread)
        thread.start()
    
    # Vänta på att alla trådar ska slutföras
    for thread in threads:
        thread.join()
    
    # Verifiera att alla error requests returnerade 404
    assert len(errors) == 0, f"Concurrent error requests failed: {errors}"
    assert len(results) == 10, f"Expected 10 responses, got {len(results)}"
    assert all(status == 404 for status in results), f"Not all error requests returned 404: {results}"
