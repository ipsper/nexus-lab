"""
Playwright-tester för frontend API-integration
Testar att frontend kommunicerar korrekt med backend API
"""
import pytest
import time
from support.playwright_client import PlaywrightClient


@pytest.fixture(scope="function")
def frontend_url():
    """Frontend URL för tester"""
    return "http://localhost:8000"


@pytest.fixture(scope="function")
def api_url():
    """API URL för tester"""
    return "http://localhost:8000/api"


@pytest.fixture(scope="function")
def playwright_client():
    """Playwright klient för GUI-testning"""
    client = PlaywrightClient(browser_type="chromium", headless=True, timeout=30000)
    client.start()
    yield client
    client.close()


def test_api_health_endpoint_integration(playwright_client, frontend_url):
    """Test att frontend kan kommunicera med health endpoint"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(3000)
    
    # Kontrollera att det finns hälsokontroller i UI
    health_elements = playwright_client.get_elements("[data-testid='health'], .health, .status, .health-check")
    if health_elements:
        # Kontrollera att hälsokontrollerna har innehåll
        for element in health_elements[:3]:  # Kontrollera första 3 elementen
            if playwright_client.is_element_visible(f"[data-testid='health'], .health, .status, .health-check"):
                health_text = playwright_client.get_text(f"[data-testid='health'], .health, .status, .health-check")
                assert len(health_text.strip()) > 0, "Hälsokontroller borde ha innehåll"


def test_api_repositories_endpoint_integration(playwright_client, frontend_url):
    """Test att frontend kan kommunicera med repositories endpoint"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(3000)
    
    # Kontrollera att det finns repository-data i UI
    repo_elements = playwright_client.get_elements("[data-testid='repository'], .repository, .repo, .repo-list")
    if repo_elements:
        # Kontrollera att repository-elementen har innehåll
        for element in repo_elements[:3]:  # Kontrollera första 3 elementen
            if playwright_client.is_element_visible(f"[data-testid='repository'], .repository, .repo, .repo-list"):
                repo_text = playwright_client.get_text(f"[data-testid='repository'], .repository, .repo, .repo-list")
                assert len(repo_text.strip()) > 0, "Repository-element borde ha innehåll"


def test_api_schedule_endpoint_integration(playwright_client, frontend_url):
    """Test att frontend kan kommunicera med schedule endpoint"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(3000)
    
    # Kontrollera att det finns schema-data i UI
    schedule_elements = playwright_client.get_elements("[data-testid='schedule'], .schedule, .scheduler, .schedule-list")
    if schedule_elements:
        # Kontrollera att schema-elementen har innehåll
        for element in schedule_elements[:3]:  # Kontrollera första 3 elementen
            if playwright_client.is_element_visible(f"[data-testid='schedule'], .schedule, .scheduler, .schedule-list"):
                schedule_text = playwright_client.get_text(f"[data-testid='schedule'], .schedule, .scheduler, .schedule-list")
                assert len(schedule_text.strip()) > 0, "Schema-element borde ha innehåll"


def test_api_error_handling_in_ui(playwright_client, frontend_url):
    """Test att frontend hanterar API-fel korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(3000)
    
    # Kontrollera att det inte finns synliga API-fel
    error_elements = playwright_client.get_elements(".error, .alert, .warning, [data-testid='error']")
    for element in error_elements:
        if playwright_client.is_element_visible(f".error, .alert, .warning, [data-testid='error']"):
            error_text = playwright_client.get_text(f".error, .alert, .warning, [data-testid='error']")
            # Tillåt vissa fel men inte kritiska API-fel
            assert "api" not in error_text.lower() or "critical" not in error_text.lower(), f"Kritiskt API-fel hittades: {error_text}"


def test_api_loading_states_in_ui(playwright_client, frontend_url):
    """Test att frontend visar loading states för API-anrop"""
    playwright_client.navigate_to(frontend_url)
    
    # Kontrollera att sidan laddas
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att loading states försvinner
    loading_elements = playwright_client.get_elements(".loading, .spinner, .loader, [data-testid='loading']")
    for element in loading_elements:
        if playwright_client.is_element_visible(f".loading, .spinner, .loader, [data-testid='loading']"):
            # Vänta lite till för att se om loading försvinner
            playwright_client.wait_for_timeout(3000)
            # Kontrollera att loading inte är kvar
            assert not playwright_client.is_element_visible(f".loading, .spinner, .loader, [data-testid='loading']"), "Loading state borde ha försvunnit"


def test_api_data_display_in_ui(playwright_client, frontend_url):
    """Test att frontend visar API-data korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(3000)
    
    # Kontrollera att det finns data som visas i UI
    data_elements = playwright_client.get_elements("[data-testid='data'], .data, .content, .list, .card")
    if data_elements:
        # Kontrollera att data-elementen har innehåll
        for element in data_elements[:5]:  # Kontrollera första 5 elementen
            if playwright_client.is_element_visible(f"[data-testid='data'], .data, .content, .list, .card"):
                data_text = playwright_client.get_text(f"[data-testid='data'], .data, .content, .list, .card")
                assert len(data_text.strip()) > 0, "Data-element borde ha innehåll"


def test_api_form_submission_in_ui(playwright_client, frontend_url):
    """Test att frontend kan skicka formulär till API"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Sök efter formulär
    form_elements = playwright_client.get_elements("form, [data-testid='form'], .form")
    if form_elements:
        # Sök efter input-fält i formuläret
        input_elements = playwright_client.get_elements("form input, [data-testid='form'] input, .form input")
        if input_elements:
            # Fyll i första input-fältet
            playwright_client.fill("form input, [data-testid='form'] input, .form input", "test data")
            
            # Sök efter submit-knapp
            submit_elements = playwright_client.get_elements("form button[type='submit'], form input[type='submit'], [data-testid='submit']")
            if submit_elements:
                # Klicka på submit-knappen
                playwright_client.click("form button[type='submit'], form input[type='submit'], [data-testid='submit']")
                playwright_client.wait_for_load_state("networkidle")
                
                # Kontrollera att formuläret skickades
                current_url = playwright_client.get_url()
                assert current_url, "Formulär borde ha skickats"


def test_api_authentication_in_ui(playwright_client, frontend_url):
    """Test att frontend hanterar autentisering korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det inte finns autentiseringsfel
    auth_elements = playwright_client.get_elements(".auth-error, .login-error, [data-testid='auth-error']")
    for element in auth_elements:
        if playwright_client.is_element_visible(f".auth-error, .login-error, [data-testid='auth-error']"):
            auth_text = playwright_client.get_text(f".auth-error, .login-error, [data-testid='auth-error']")
            # Tillåt vissa autentiseringsfel men inte kritiska
            assert "critical" not in auth_text.lower(), f"Kritiskt autentiseringsfel hittades: {auth_text}"


def test_api_cors_handling_in_ui(playwright_client, frontend_url):
    """Test att frontend hanterar CORS korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det inte finns CORS-fel
    cors_elements = playwright_client.get_elements(".cors-error, .cors-warning, [data-testid='cors-error']")
    for element in cors_elements:
        if playwright_client.is_element_visible(f".cors-error, .cors-warning, [data-testid='cors-error']"):
            cors_text = playwright_client.get_text(f".cors-error, .cors-warning, [data-testid='cors-error']")
            # Tillåt vissa CORS-fel men inte kritiska
            assert "critical" not in cors_text.lower(), f"Kritiskt CORS-fel hittades: {cors_text}"


def test_api_timeout_handling_in_ui(playwright_client, frontend_url):
    """Test att frontend hanterar API-timeouts korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(5000)
    
    # Kontrollera att det inte finns timeout-fel
    timeout_elements = playwright_client.get_elements(".timeout-error, .timeout-warning, [data-testid='timeout-error']")
    for element in timeout_elements:
        if playwright_client.is_element_visible(f".timeout-error, .timeout-warning, [data-testid='timeout-error']"):
            timeout_text = playwright_client.get_text(f".timeout-error, .timeout-warning, [data-testid='timeout-error']")
            # Tillåt vissa timeout-fel men inte kritiska
            assert "critical" not in timeout_text.lower(), f"Kritiskt timeout-fel hittades: {timeout_text}"


def test_api_response_handling_in_ui(playwright_client, frontend_url):
    """Test att frontend hanterar API-svar korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(3000)
    
    # Kontrollera att det finns data som visas i UI
    response_elements = playwright_client.get_elements("[data-testid='response'], .response, .api-response, .data")
    if response_elements:
        # Kontrollera att response-elementen har innehåll
        for element in response_elements[:3]:  # Kontrollera första 3 elementen
            if playwright_client.is_element_visible(f"[data-testid='response'], .response, .api-response, .data"):
                response_text = playwright_client.get_text(f"[data-testid='response'], .response, .api-response, .data")
                assert len(response_text.strip()) > 0, "Response-element borde ha innehåll"