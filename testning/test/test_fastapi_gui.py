"""
FastAPI GUI-tester med Playwright
"""
import pytest
import time
from support.playwright_client import PlaywrightClient
from support.fastapi_gui_support import (
    navigate_to_docs, click_endpoint, try_it_out, execute_request, 
    get_response_status, get_response_body, check_endpoint_visible,
    set_viewport_size, scroll_to_bottom
)

# Inaktivera asyncio för Playwright-tester
pytestmark = pytest.mark.asyncio(mode="off")


@pytest.mark.gui
@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
def test_docs_page_loads(api_base_url, browser_type):
    """Testa att API-dokumentationssidan laddas i olika browsers"""
    with PlaywrightClient(browser_type=browser_type, headless=True) as client:
        navigate_to_docs(client, api_base_url)
        assert client.is_element_visible(".swagger-ui")
        assert "Nexus Repository Manager API" in client.get_title()


@pytest.mark.gui
def test_root_page_loads(api_base_url):
    """Testa att root-sidan laddas korrekt"""
    with PlaywrightClient(headless=True) as client:
        client.navigate_to(f"{api_base_url}/")
        client.wait_for_load_state()
        assert "Nexus Repository Manager API" in client.get_page_source()


@pytest.mark.gui
def test_redoc_page_loads(api_base_url):
    """Testa att ReDoc-dokumentationssidan laddas"""
    with PlaywrightClient(headless=True) as client:
        client.navigate_to(f"{api_base_url}/redoc")
        client.wait_for_load_state()
        client.wait_for_selector("[data-cy='api-info']", timeout=10000)
        assert "Nexus Repository Manager API" in client.get_title()


@pytest.mark.gui
def test_health_endpoint_via_swagger(api_base_url):
    """Testa att köra health endpoint via Swagger UI"""
    with PlaywrightClient(headless=True) as client:
        navigate_to_docs(client, api_base_url)
        click_endpoint(client, "/health")
        try_it_out(client)
        execute_request(client)
        
        status_text = get_response_status(client)
        assert "200" in status_text
        
        # Validera JSON-responsstruktur
        response_body = get_response_body(client)
        expected_keys = ["status", "timestamp", "version", "environment"]
        for key in expected_keys:
            assert f'"{key}"' in response_body, f"Nyckel '{key}' saknas i JSON-response"


@pytest.mark.gui
def test_repositories_endpoint_via_swagger(api_base_url):
    """Testa repositories endpoint via Swagger UI"""
    with PlaywrightClient(headless=True) as client:
        navigate_to_docs(client, api_base_url)
        click_endpoint(client, "/repositories")
        try_it_out(client)
        execute_request(client)
        
        status_text = get_response_status(client)
        assert "200" in status_text


@pytest.mark.gui
def test_api_endpoints_visible(api_base_url):
    """Testa att alla viktiga endpoints syns i dokumentationen"""
    with PlaywrightClient(headless=True) as client:
        navigate_to_docs(client, api_base_url)
        
        expected_endpoints = ["/health", "/repositories", "/packages", "/stats", "/formats", "/config"]
        
        for endpoint in expected_endpoints:
            assert check_endpoint_visible(client, endpoint), f"Endpoint {endpoint} inte synlig"


@pytest.mark.gui
@pytest.mark.parametrize("viewport_size", [
    {"width": 1920, "height": 1080},  # Desktop
    {"width": 768, "height": 1024},   # Tablet
    {"width": 375, "height": 667}     # Mobile
])
def test_responsive_design(api_base_url, viewport_size):
    """Testa responsiv design av dokumentationen"""
    with PlaywrightClient(headless=True) as client:
        set_viewport_size(client, viewport_size["width"], viewport_size["height"])
        navigate_to_docs(client, api_base_url)
        assert client.is_element_visible(".swagger-ui")


@pytest.mark.gui
def test_error_page_handling(api_base_url):
    """Testa felhantering för icke-existerande sidor"""
    with PlaywrightClient(headless=True) as client:
        client.navigate_to(f"{api_base_url}/nonexistent")
        client.wait_for_load_state()
        
        page_content = client.get_page_source()
        assert "404" in page_content or "Not Found" in page_content or "detail" in page_content


@pytest.mark.gui
def test_swagger_ui_performance(api_base_url):
    """Testa prestanda för Swagger UI-laddning"""
    with PlaywrightClient(headless=True) as client:
        start_time = time.time()
        navigate_to_docs(client, api_base_url)
        load_time = time.time() - start_time
        
        assert load_time < 10, f"Swagger UI tog {load_time:.2f}s att ladda (för långsamt)"
        assert client.is_element_visible(".swagger-ui")


@pytest.mark.gui
def test_multiple_endpoints_workflow(api_base_url):
    """Testa att köra flera endpoints i sekvens"""
    with PlaywrightClient(headless=True) as client:
        navigate_to_docs(client, api_base_url)
        
        endpoints_to_test = ["/health", "/repositories", "/stats", "/formats"]
        
        for endpoint in endpoints_to_test:
            click_endpoint(client, endpoint)
            try_it_out(client)
            execute_request(client)
            status_text = get_response_status(client)
            assert "200" in status_text, f"Endpoint {endpoint} returnerade inte 200"


@pytest.mark.gui
def test_browser_compatibility(api_base_url):
    """Testa kompatibilitet med olika browsers"""
    browsers = ["chromium", "firefox"]
    
    for browser_type in browsers:
        with PlaywrightClient(browser_type=browser_type, headless=True) as client:
            navigate_to_docs(client, api_base_url)
            assert client.is_element_visible(".swagger-ui"), f"Swagger UI fungerar inte i {browser_type}"
            
            # Testa interaktion
            click_endpoint(client, "/health")
            assert client.is_element_visible(".btn.try-out__btn"), f"Try it out knappen fungerar inte i {browser_type}"


@pytest.mark.gui
def test_swagger_ui_navigation(api_base_url):
    """Testa navigation inom Swagger UI"""
    with PlaywrightClient(headless=True) as client:
        navigate_to_docs(client, api_base_url)
        
        # Scrolla ned för att se alla endpoints
        scroll_to_bottom(client)
        
        # Kontrollera att vi kan se endpoints längre ned på sidan
        assert check_endpoint_visible(client, "/config"), "Config endpoint inte synlig efter scrollning"


@pytest.mark.gui
@pytest.mark.slow
def test_full_workflow(api_base_url):
    """Testa komplett GUI-workflow"""
    with PlaywrightClient(headless=True) as client:
        # 1. Ladda docs
        navigate_to_docs(client, api_base_url)
        
        # 2. Kontrollera endpoints finns
        assert check_endpoint_visible(client, "/health")
        assert check_endpoint_visible(client, "/repositories")
        
        # 3. Testa health endpoint
        click_endpoint(client, "/health")
        try_it_out(client)
        execute_request(client)
        assert "200" in get_response_status(client)
        
        # 4. Testa repositories endpoint
        click_endpoint(client, "/repositories")
        try_it_out(client)
        execute_request(client)
        assert "200" in get_response_status(client)
        
        # 5. Testa ReDoc
        client.navigate_to(f"{api_base_url}/redoc")
        client.wait_for_load_state()
        assert "Nexus Repository Manager API" in client.get_title()
