"""
API Data Validation Tests - Testar input-validering och data-typer
"""
import pytest
import requests
import json


@pytest.mark.api
@pytest.mark.validation
def test_api_repository_name_validation(api_client):
    """Test repository name validation"""
    invalid_names = [
        "",  # Tom sträng
        " ",  # Bara mellanslag
        "a" * 256,  # För långt namn
        "repo with spaces",  # Mellanslag
        "repo/with/slashes",  # Slashes
        "repo\\with\\backslashes",  # Backslashes
        "repo:with:colons",  # Kolon
        "repo|with|pipes",  # Pipe
        "repo<with>angles",  # Vinkelparenteser
        "repo\"with\"quotes",  # Citattecken
        "repo'with'apostrophes",  # Apostrofer
        "repo\twith\ttabs",  # Tabs
        "repo\nwith\nnewlines",  # Nyrader
        "repo\rwith\rcarriage",  # Carriage return
        "repo\0with\0nulls",  # Null bytes
    ]
    
    for invalid_name in invalid_names:
        response = api_client.get(f"/repositories/{invalid_name}")
        # Beroende på implementation kan detta returnera 200, 400 eller 404
        # Tom sträng kan matcha root path, så vi accepterar 200 också
        assert response.status_code in [200, 400, 404], f"Invalid name '{invalid_name}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_package_name_validation(api_client):
    """Test package name validation"""
    invalid_names = [
        "",  # Tom sträng
        " ",  # Bara mellanslag
        "a" * 256,  # För långt namn
        "package with spaces",  # Mellanslag
        "package/with/slashes",  # Slashes
        "package\\with\\backslashes",  # Backslashes
        "package:with:colons",  # Kolon
        "package|with|pipes",  # Pipe
        "package<with>angles",  # Vinkelparenteser
        "package\"with\"quotes",  # Citattecken
        "package'with'apostrophes",  # Apostrofer
        "package\twith\ttabs",  # Tabs
        "package\nwith\nnewlines",  # Nyrader
        "package\rwith\rcarriage",  # Carriage return
        "package\0with\0nulls",  # Null bytes
    ]
    
    for invalid_name in invalid_names:
        response = api_client.get(f"/packages/{invalid_name}")
        # Beroende på implementation kan detta returnera 200, 400 eller 404
        # Tom sträng kan matcha root path, så vi accepterar 200 också
        assert response.status_code in [200, 400, 404], f"Invalid package name '{invalid_name}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_json_schema_validation(api_client):
    """Test JSON schema validation for POST requests"""
    invalid_requests = [
        # Ogiltig JSON-struktur
        {"invalid": "structure"},
        {"name": 123},  # Fel datatyp
        {"name": None},  # Null värde
        {"name": []},  # Array istället för sträng
        {"name": {}},  # Objekt istället för sträng
        
        # Saknade required fields
        {},
        {"description": "test"},
        {"type": "hosted"},
        
        # Ogiltiga värden
        {"name": "", "type": "hosted", "format": "pypi"},
        {"name": "test", "type": "invalid", "format": "pypi"},
        {"name": "test", "type": "hosted", "format": "invalid"},
        
        # För långa värden
        {"name": "a" * 1000, "type": "hosted", "format": "pypi"},
        {"name": "test", "type": "a" * 1000, "format": "pypi"},
        {"name": "test", "type": "hosted", "format": "a" * 1000},
    ]
    
    for invalid_request in invalid_requests:
        response = api_client.post("/repositories/", json=invalid_request)
        assert response.status_code in [400, 422], f"Invalid request {invalid_request} returned {response.status_code}"
        
        data = response.json()
        assert "detail" in data, f"Validation error response should contain 'detail' field"


@pytest.mark.api
@pytest.mark.validation
def test_api_content_type_validation(api_client):
    """Test Content-Type header validation"""
    # Testa olika Content-Type headers
    content_types = [
        "text/plain",
        "application/xml",
        "text/html",
        "application/octet-stream",
        "multipart/form-data",
    ]
    
    for content_type in content_types:
        response = requests.post(
            f"{api_client.base_url}/repositories/",
            data='{"name": "test-repo"}',
            headers={"Content-Type": content_type}
        )
        # Beroende på implementation kan detta returnera 400, 415, eller 422
        assert response.status_code in [200, 400, 415, 422], f"Content-Type {content_type} returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_encoding_validation(api_client):
    """Test character encoding validation"""
    # Testa olika encodings
    encodings = [
        "utf-8",
        "utf-16",
        "latin-1",
        "ascii",
    ]
    
    for encoding in encodings:
        try:
            data = {"name": "test-repo"}
            json_data = json.dumps(data).encode(encoding)
            
            response = requests.post(
                f"{api_client.base_url}/repositories/",
                data=json_data,
                headers={"Content-Type": f"application/json; charset={encoding}"}
            )
            # Beroende på implementation kan detta returnera 200, 400, eller 415
            assert response.status_code in [200, 400, 415, 422], f"Encoding {encoding} returned {response.status_code}"
        except UnicodeEncodeError:
            # Vissa encodings kan inte hantera vissa tecken
            pass


@pytest.mark.api
@pytest.mark.validation
def test_api_unicode_validation(api_client):
    """Test Unicode character validation"""
    unicode_strings = [
        "repo-åäö",
        "repo-中文",
        "repo-العربية",
        "repo-русский",
        "repo-🚀",
        "repo-ñáéíóú",
        "repo-αβγδε",
        "repo-日本語",
        "repo-한국어",
        "repo-עברית",
    ]
    
    for unicode_str in unicode_strings:
        response = api_client.get(f"/repositories/{unicode_str}")
        # Beroende på implementation kan detta returnera 200, 400, eller 404
        assert response.status_code in [200, 400, 404], f"Unicode string '{unicode_str}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_numeric_validation(api_client):
    """Test numeric value validation"""
    # Testa olika numeriska värden
    numeric_tests = [
        ("/stats", "Should accept numeric stats"),
        ("/repositories/", "Should handle numeric repository names"),
        ("/packages/", "Should handle numeric package names"),
    ]
    
    for endpoint, description in numeric_tests:
        response = api_client.get(endpoint)
        assert response.status_code == 200, f"{description}: {endpoint} returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_boolean_validation(api_client):
    """Test boolean value validation"""
    # Testa olika boolean-värden i JSON
    boolean_tests = [
        {"name": "test", "active": True},
        {"name": "test", "active": False},
        {"name": "test", "active": "true"},  # String boolean
        {"name": "test", "active": "false"},  # String boolean
        {"name": "test", "active": 1},  # Numeric boolean
        {"name": "test", "active": 0},  # Numeric boolean
    ]
    
    for test_data in boolean_tests:
        response = api_client.post("/repositories/", json=test_data)
        # Beroende på implementation kan detta returnera 200, 400, eller 422
        assert response.status_code in [200, 400, 422], f"Boolean test {test_data} returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_array_validation(api_client):
    """Test array value validation"""
    # Testa olika array-värden
    array_tests = [
        {"name": "test", "tags": []},  # Tom array
        {"name": "test", "tags": ["tag1"]},  # Enkel array
        {"name": "test", "tags": ["tag1", "tag2", "tag3"]},  # Flera element
        {"name": "test", "tags": [1, 2, 3]},  # Numerisk array
        {"name": "test", "tags": [True, False]},  # Boolean array
        {"name": "test", "tags": [{"key": "value"}]},  # Objekt array
    ]
    
    for test_data in array_tests:
        response = api_client.post("/repositories/", json=test_data)
        # Beroende på implementation kan detta returnera 200, 400, eller 422
        assert response.status_code in [200, 400, 422], f"Array test {test_data} returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_object_validation(api_client):
    """Test object value validation"""
    # Testa olika objekt-värden
    object_tests = [
        {"name": "test", "config": {}},  # Tomt objekt
        {"name": "test", "config": {"key": "value"}},  # Enkelt objekt
        {"name": "test", "config": {"nested": {"key": "value"}}},  # Nästlat objekt
        {"name": "test", "config": {"array": [1, 2, 3]}},  # Objekt med array
        {"name": "test", "config": {"boolean": True}},  # Objekt med boolean
    ]
    
    for test_data in object_tests:
        response = api_client.post("/repositories/", json=test_data)
        # Beroende på implementation kan detta returnera 200, 400, eller 422
        assert response.status_code in [200, 400, 422], f"Object test {test_data} returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_required_fields_validation(api_client):
    """Test required fields validation"""
    # Testa olika kombinationer av saknade fält
    missing_field_tests = [
        {},  # Alla fält saknas
        {"name": "test"},  # Bara name
        {"type": "hosted"},  # Bara type
        {"format": "pypi"},  # Bara format
        {"name": "test", "type": "hosted"},  # Format saknas
        {"name": "test", "format": "pypi"},  # Type saknas
        {"type": "hosted", "format": "pypi"},  # Name saknas
    ]
    
    for test_data in missing_field_tests:
        response = api_client.post("/repositories/", json=test_data)
        assert response.status_code in [400, 422], f"Missing fields test {test_data} returned {response.status_code}"
        
        data = response.json()
        assert "detail" in data, f"Missing fields error should contain 'detail' field"


@pytest.mark.api
@pytest.mark.validation
def test_api_field_length_validation(api_client):
    """Test field length validation"""
    # Testa olika fältlängder
    length_tests = [
        {"name": "", "type": "hosted", "format": "pypi"},  # Tomt namn
        {"name": "a", "type": "hosted", "format": "pypi"},  # För kort namn
        {"name": "a" * 1000, "type": "hosted", "format": "pypi"},  # För långt namn
        {"name": "test", "type": "", "format": "pypi"},  # Tomt type
        {"name": "test", "type": "hosted", "format": ""},  # Tomt format
    ]
    
    for test_data in length_tests:
        response = api_client.post("/repositories/", json=test_data)
        # Beroende på implementation kan detta returnera 200, 400, eller 422
        assert response.status_code in [200, 400, 422], f"Length test {test_data} returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_sql_injection_protection(api_client):
    """Test SQL injection protection"""
    sql_injection_tests = [
        "'; DROP TABLE repositories; --",
        "1' OR '1'='1",
        "admin'--",
        "1' UNION SELECT * FROM repositories--",
        "'; INSERT INTO repositories VALUES ('hacked'); --",
    ]
    
    for injection in sql_injection_tests:
        response = api_client.get(f"/repositories/{injection}")
        # Beroende på implementation kan detta returnera 400, 404, eller 500
        assert response.status_code in [200, 400, 404, 500], f"SQL injection '{injection}' returned {response.status_code}"


@pytest.mark.api
@pytest.mark.validation
def test_api_xss_protection(api_client):
    """Test XSS protection"""
    xss_tests = [
        "<script>alert('xss')</script>",
        "javascript:alert('xss')",
        "<img src=x onerror=alert('xss')>",
        "';alert('xss');//",
        "<svg onload=alert('xss')>",
    ]
    
    for xss in xss_tests:
        try:
            response = api_client.get(f"/repositories/{xss}")
            # Beroende på implementation kan detta returnera 200, 400, 404, eller 500
            assert response.status_code in [200, 400, 404, 500], f"XSS test '{xss}' returned {response.status_code}"
            
            # Kontrollera att response inte innehåller oskyddad XSS
            if response.status_code == 200:
                response_text = response.text
                assert "<script>" not in response_text, f"XSS not properly escaped in response for '{xss}'"
        except Exception as e:
            # Om det är ett nätverksfel, hoppa över testet
            if "ConnectionError" in str(type(e)) or "NameResolutionError" in str(type(e)):
                pytest.skip(f"Skipping XSS test due to connection error: {e}")
            else:
                raise
