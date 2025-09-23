"""
Smart tester för att extrahera och testa alla Request URLs från Swagger UI
"""
import pytest
import requests
import json
import re
from playwright.sync_api import sync_playwright, Page, Browser


class SwaggerEndpointExtractor:
    """Smart klass för att extrahera endpoints från Swagger UI"""
    
    def __init__(self, page: Page):
        self.page = page
        
    def extract_all_endpoints(self):
        """Extraherar alla endpoints från Swagger UI med Request URLs"""
        endpoints = []
        
        # Hitta alla operation-grupper
        operations = self.page.locator(".opblock-tag")
        operation_count = operations.count()
        
        print(f"🔍 Found {operation_count} operation groups")
        
        for i in range(operation_count):
            operation_group = operations.nth(i)
            group_name = operation_group.text_content().strip()
            
            # Expandera gruppen
            operation_group.click()
            self.page.wait_for_timeout(300)
            
            # Hitta alla endpoints i gruppen
            endpoint_blocks = operation_group.locator("..").locator(".opblock")
            endpoint_count = endpoint_blocks.count()
            
            print(f"  📁 Group '{group_name}': {endpoint_count} endpoints")
            
            for j in range(endpoint_count):
                endpoint_block = endpoint_blocks.nth(j)
                
                # Hämta HTTP verb och path
                verb_element = endpoint_block.locator(".opblock-summary-method")
                path_element = endpoint_block.locator(".opblock-summary-path")
                
                if verb_element.count() > 0 and path_element.count() > 0:
                    verb = verb_element.text_content().strip()
                    path = path_element.text_content().strip()
                    
                    # Bygg fullständig URL
                    full_url = f"http://localhost:8000{path}"
                    
                    endpoint_info = {
                        "method": verb,
                        "path": path,
                        "full_url": full_url,
                        "group": group_name,
                        "endpoint_block": endpoint_block
                    }
                    
                    endpoints.append(endpoint_info)
                    print(f"    ✅ {verb} {path}")
        
        return endpoints
    
    def get_request_url_from_swagger(self, endpoint_block):
        """Extraherar Request URL från Swagger UI för en specifik endpoint"""
        try:
            # Klicka på endpoint för att expandera
            endpoint_block.click()
            self.page.wait_for_timeout(300)
            
            # Klicka på "Try it out"
            try_it_out = endpoint_block.locator("button:has-text('Try it out')")
            if try_it_out.count() > 0:
                try_it_out.click()
                self.page.wait_for_timeout(300)
                
                # Hitta Request URL i response-sektionen
                request_url_element = endpoint_block.locator(".request-url")
                if request_url_element.count() > 0:
                    request_url = request_url_element.text_content().strip()
                    return request_url
                    
        except Exception as e:
            print(f"      ⚠️ Could not extract Request URL: {e}")
            
        return None


@pytest.mark.gui
def test_extract_and_verify_all_endpoints():
    """Smart test som extraherar alla endpoints och verifierar dem"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # Gå till Swagger docs
            print("🌐 Loading Swagger UI...")
            page.goto("http://localhost:8000/api/docs")
            page.wait_for_load_state("networkidle")
            
            # Extrahera alla endpoints
            extractor = SwaggerEndpointExtractor(page)
            endpoints = extractor.extract_all_endpoints()
            
            print(f"\n📊 Found {len(endpoints)} total endpoints")
            
            # Testa varje endpoint
            successful_tests = 0
            failed_tests = 0
            
            for endpoint in endpoints:
                method = endpoint["method"]
                path = endpoint["path"]
                full_url = endpoint["full_url"]
                
                print(f"\n🧪 Testing {method} {path}")
                
                # Test 1: Verifiera att path börjar med /api
                if not path.startswith("/api"):
                    print(f"  ❌ Path missing /api prefix: {path}")
                    failed_tests += 1
                    continue
                
                # Test 2: Testa endpoint direkt med requests
                try:
                    if method == "GET":
                        response = requests.get(full_url, timeout=5)
                    elif method == "POST":
                        # För POST endpoints, skicka tom data
                        response = requests.post(full_url, json={}, timeout=5)
                    else:
                        response = requests.request(method, full_url, timeout=5)
                    
                    if response.status_code in [200, 201, 422]:  # 422 = validation error (OK för test)
                        print(f"  ✅ HTTP {response.status_code} - Endpoint works")
                        successful_tests += 1
                    else:
                        print(f"  ⚠️ HTTP {response.status_code} - Unexpected status")
                        failed_tests += 1
                        
                except requests.exceptions.RequestException as e:
                    print(f"  ❌ Request failed: {e}")
                    failed_tests += 1
                
                # Test 3: Extrahera Request URL från Swagger (för GET endpoints)
                if method == "GET":
                    request_url = extractor.get_request_url_from_swagger(endpoint["endpoint_block"])
                    if request_url:
                        print(f"  📋 Swagger Request URL: {request_url}")
                        if not request_url.startswith("http://localhost:8000/api"):
                            print(f"  ❌ Swagger Request URL missing /api prefix")
                            failed_tests += 1
                        else:
                            successful_tests += 1
                    else:
                        print(f"  ⚠️ Could not extract Request URL from Swagger")
            
            # Sammanfattning
            print(f"\n📈 Test Results:")
            print(f"  ✅ Successful: {successful_tests}")
            print(f"  ❌ Failed: {failed_tests}")
            print(f"  📊 Total: {len(endpoints)}")
            
            # Assertions
            assert failed_tests == 0, f"{failed_tests} endpoints failed validation"
            assert successful_tests > 0, "No endpoints passed validation"
            
            print(f"\n🎉 All {len(endpoints)} endpoints validated successfully!")
            
        finally:
            browser.close()


@pytest.mark.gui
def test_openapi_spec_consistency():
    """Testar att OpenAPI spec är konsistent med Swagger UI"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # Hämta OpenAPI spec direkt
            print("📥 Fetching OpenAPI specification...")
            response = requests.get("http://localhost:8000/api/openapi.json")
            assert response.status_code == 200, "Could not fetch OpenAPI spec"
            
            openapi_spec = response.json()
            
            # Extrahera paths från OpenAPI spec
            api_paths = list(openapi_spec.get("paths", {}).keys())
            
            print(f"📋 Found {len(api_paths)} paths in OpenAPI spec:")
            for path in api_paths:
                print(f"  - {path}")
            
            # Verifiera att alla paths börjar med /api
            non_api_paths = [path for path in api_paths if not path.startswith("/api")]
            
            if non_api_paths:
                print(f"\n❌ Found paths without /api prefix:")
                for path in non_api_paths:
                    print(f"  - {path}")
                assert False, f"OpenAPI spec contains {len(non_api_paths)} paths without /api prefix"
            
            print(f"\n✅ All {len(api_paths)} paths in OpenAPI spec have /api prefix")
            
            # Testa några viktiga endpoints
            important_endpoints = [
                "/api/",
                "/api/health",
                "/api/pip-package",
                "/api/repositories/",
                "/api/packages/"
            ]
            
            missing_endpoints = []
            for endpoint in important_endpoints:
                if endpoint not in api_paths:
                    missing_endpoints.append(endpoint)
            
            if missing_endpoints:
                print(f"\n❌ Missing important endpoints:")
                for endpoint in missing_endpoints:
                    print(f"  - {endpoint}")
                assert False, f"Missing {len(missing_endpoints)} important endpoints"
            
            print(f"\n✅ All important endpoints present in OpenAPI spec")
            
        finally:
            browser.close()


@pytest.mark.gui
def test_all_endpoint_urls_correct():
    """Testar att alla endpoints i Swagger har korrekta Request URLs med /api prefix"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # Gå till Swagger docs
            page.goto("http://localhost:8000/api/docs")
            page.wait_for_load_state("networkidle")
            
            # Samla alla endpoint URLs från Swagger UI
            endpoint_urls = []
            
            # Hitta alla operation-element
            operations = page.locator("[data-testid='operations'] > div")
            operation_count = operations.count()
            
            print(f"Found {operation_count} operations in Swagger UI")
            
            for i in range(operation_count):
                operation = operations.nth(i)
                
                # Klicka för att expandera operation
                operation.click()
                page.wait_for_timeout(500)
                
                # Hitta alla endpoints inom denna operation
                endpoint_elements = operation.locator("[data-testid='http-verb']")
                endpoint_count = endpoint_elements.count()
                
                for j in range(endpoint_count):
                    endpoint_element = endpoint_elements.nth(j)
                    
                    # Hämta HTTP verb och path
                    verb = endpoint_element.text_content().strip()
                    path_element = endpoint_element.locator("..").locator("[data-testid='endpoint-path']")
                    path = path_element.text_content().strip()
                    
                    full_url = f"{verb} {path}"
                    endpoint_urls.append(full_url)
                    
                    print(f"Found endpoint: {full_url}")
            
            # Förväntade endpoints (med /api prefix)
            expected_endpoints = [
                "GET /api/",
                "GET /api/health", 
                "GET /api/stats",
                "GET /api/formats",
                "GET /api/config",
                "GET /api/pip-package",
                "GET /api/repositories/",
                "GET /api/repositories/{repository_name}",
                "POST /api/repositories/",
                "GET /api/packages/",
                "POST /api/packages/",
                "GET /api/packages/{package_name}",
                "GET /api/repositories/{repository_name}/packages"
            ]
            
            print(f"\nFound {len(endpoint_urls)} endpoints:")
            for url in endpoint_urls:
                print(f"  - {url}")
            
            print(f"\nExpected {len(expected_endpoints)} endpoints:")
            for url in expected_endpoints:
                print(f"  - {url}")
            
            # Verifiera att alla förväntade endpoints finns
            missing_endpoints = []
            for expected in expected_endpoints:
                if expected not in endpoint_urls:
                    missing_endpoints.append(expected)
            
            # Verifiera att alla endpoints börjar med /api
            non_api_endpoints = []
            for url in endpoint_urls:
                if not url.split()[1].startswith("/api"):
                    non_api_endpoints.append(url)
            
            # Assertions
            assert len(missing_endpoints) == 0, f"Missing endpoints: {missing_endpoints}"
            assert len(non_api_endpoints) == 0, f"Endpoints without /api prefix: {non_api_endpoints}"
            
            print(f"\n✅ All {len(endpoint_urls)} endpoints have correct /api prefix")
            print(f"✅ All {len(expected_endpoints)} expected endpoints found")
            
        finally:
            browser.close()


@pytest.mark.gui 
def test_specific_endpoint_urls():
    """Testar specifika endpoints för att verifiera att de fungerar med korrekta URLs"""
    
    endpoints_to_test = [
        ("GET", "/api/"),
        ("GET", "/api/health"),
        ("GET", "/api/pip-package"),
        ("GET", "/api/repositories/"),
        ("GET", "/api/packages/"),
        ("GET", "/api/stats"),
        ("GET", "/api/formats"),
        ("GET", "/api/config")
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            for method, endpoint in endpoints_to_test:
                print(f"Testing {method} {endpoint}")
                
                # Gå till Swagger docs
                page.goto("http://localhost:8000/api/docs")
                page.wait_for_load_state("networkidle")
                
                # Hitta och klicka på endpoint
                endpoint_element = page.locator(f"text={method} {endpoint}")
                if endpoint_element.count() > 0:
                    endpoint_element.click()
                    page.wait_for_timeout(500)
                    
                    # Klicka på "Try it out"
                    try_it_out = page.locator("button:has-text('Try it out')")
                    if try_it_out.count() > 0:
                        try_it_out.click()
                        page.wait_for_timeout(500)
                        
                        # Klicka på "Execute"
                        execute_button = page.locator("button:has-text('Execute')")
                        if execute_button.count() > 0:
                            execute_button.click()
                            page.wait_for_timeout(1000)
                            
                            # Verifiera att request URL visas korrekt
                            response_section = page.locator("[data-testid='response']")
                            if response_section.count() > 0:
                                request_url = response_section.locator("text=/api/").first.text_content()
                                assert endpoint in request_url, f"Expected {endpoint} in request URL, got {request_url}"
                                print(f"  ✅ Request URL correct: {request_url}")
                            else:
                                print(f"  ⚠️ No response section found")
                        else:
                            print(f"  ⚠️ Execute button not found")
                    else:
                        print(f"  ⚠️ Try it out button not found")
                else:
                    print(f"  ❌ Endpoint {method} {endpoint} not found in Swagger UI")
                    
        finally:
            browser.close()
