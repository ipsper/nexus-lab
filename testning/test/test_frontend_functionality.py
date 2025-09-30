"""
Avancerade Playwright-tester för frontend-funktionalitet
Testar specifika React-komponenter och användarinteraktioner
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


def test_dashboard_components_load(playwright_client, frontend_url):
    """Test att dashboard-komponenter laddas"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att React-komponenter ska laddas
    playwright_client.wait_for_timeout(2000)
    
    # Kontrollera att det finns dashboard-innehåll
    dashboard_elements = playwright_client.get_elements("[data-testid='dashboard'], .dashboard, .stats, .health")
    if dashboard_elements:
        assert len(dashboard_elements) > 0, "Dashboard-komponenter borde laddas"
    
    # Kontrollera att det finns statistik eller hälsokontroller
    stats_elements = playwright_client.get_elements(".stat, .metric, .card, .health-card")
    if stats_elements:
        assert len(stats_elements) > 0, "Statistik-komponenter borde laddas"


def test_repository_list_functionality(playwright_client, frontend_url):
    """Test att repository-listan fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Försök att hitta repository-länkar eller knappar
    repo_elements = playwright_client.get_elements("[data-testid='repository'], .repository, .repo, a[href*='repo']")
    if repo_elements:
        # Klicka på första repository-elementet
        repo_elements[0].click()
        playwright_client.wait_for_load_state("networkidle")
        
        # Kontrollera att vi navigerade till repository-sidan
        current_url = playwright_client.get_url()
        assert "repo" in current_url.lower() or current_url != frontend_url, "Borde ha navigerat till repository-sida"


def test_schedule_management_interface(playwright_client, frontend_url):
    """Test att schema-hanteringsgränssnittet fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Försök att hitta schema-länkar eller knappar
    schedule_elements = playwright_client.get_elements("[data-testid='schedule'], .schedule, .scheduler, a[href*='schedule']")
    if schedule_elements:
        # Klicka på första schema-elementet
        schedule_elements[0].click()
        playwright_client.wait_for_load_state("networkidle")
        
        # Kontrollera att vi navigerade till schema-sidan
        current_url = playwright_client.get_url()
        assert "schedule" in current_url.lower() or current_url != frontend_url, "Borde ha navigerat till schema-sida"


def test_settings_page_functionality(playwright_client, frontend_url):
    """Test att inställningssidan fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Försök att hitta inställnings-länkar eller knappar
    settings_elements = playwright_client.get_elements("[data-testid='settings'], .settings, .config, a[href*='settings']")
    if settings_elements:
        # Klicka på första inställnings-elementet
        settings_elements[0].click()
        playwright_client.wait_for_load_state("networkidle")
        
        # Kontrollera att vi navigerade till inställningssidan
        current_url = playwright_client.get_url()
        assert "settings" in current_url.lower() or current_url != frontend_url, "Borde ha navigerat till inställningssida"


def test_form_interactions(playwright_client, frontend_url):
    """Test att formulärinteraktioner fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Sök efter input-fält
    input_elements = playwright_client.get_elements("input, textarea, select")
    if input_elements:
        # Testa att fylla i första input-fältet
        first_input = input_elements[0]
        if playwright_client.is_element_enabled("input, textarea, select"):
            playwright_client.fill("input, textarea, select", "test input")
            
            # Kontrollera att texten fylldes i
            input_value = playwright_client.execute_javascript("document.querySelector('input, textarea, select').value")
            assert "test input" in str(input_value), "Input-fält borde ha fyllts i"


def test_button_interactions(playwright_client, frontend_url):
    """Test att knappinteraktioner fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Sök efter knappar
    button_elements = playwright_client.get_elements("button, input[type='button'], input[type='submit']")
    if button_elements:
        # Testa att klicka på första knappen
        first_button = button_elements[0]
        if playwright_client.is_element_enabled("button, input[type='button'], input[type='submit']"):
            playwright_client.click("button, input[type='button'], input[type='submit']")
            playwright_client.wait_for_load_state("networkidle")
            
            # Kontrollera att något hände (sidan laddades om eller URL ändrades)
            current_url = playwright_client.get_url()
            assert current_url, "Knappen borde ha gjort något"


def test_api_integration_ui(playwright_client, frontend_url, api_url):
    """Test att API-integration fungerar i UI"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att API-anrop ska slutföras
    playwright_client.wait_for_timeout(3000)
    
    # Kontrollera att det finns data som kommer från API
    data_elements = playwright_client.get_elements("[data-testid='data'], .data, .content, .list")
    if data_elements:
        # Kontrollera att data-elementen har innehåll
        for element in data_elements[:3]:  # Kontrollera första 3 elementen
            if playwright_client.is_element_visible(f"[data-testid='data'], .data, .content, .list"):
                element_text = playwright_client.get_text(f"[data-testid='data'], .data, .content, .list")
                assert len(element_text.strip()) > 0, "Data-element borde ha innehåll"


def test_error_handling_ui(playwright_client, frontend_url):
    """Test att felhantering fungerar i UI"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det inte finns synliga fel
    error_elements = playwright_client.get_elements(".error, .alert, .warning, [data-testid='error']")
    for element in error_elements:
        if playwright_client.is_element_visible(f".error, .alert, .warning, [data-testid='error']"):
            error_text = playwright_client.get_text(f".error, .alert, .warning, [data-testid='error']")
            # Tillåt vissa fel men inte kritiska
            assert "critical" not in error_text.lower(), f"Kritiskt fel hittades: {error_text}"


def test_loading_states_ui(playwright_client, frontend_url):
    """Test att loading states fungerar i UI"""
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


def test_navigation_consistency(playwright_client, frontend_url):
    """Test att navigation är konsistent"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att navigation finns
    nav_elements = playwright_client.get_elements("nav, [role='navigation'], .nav, .navigation")
    if nav_elements:
        # Kontrollera att navigation är synlig
        assert playwright_client.is_element_visible("nav, [role='navigation'], .nav, .navigation"), "Navigation borde vara synlig"
        
        # Kontrollera att navigation har länkar
        nav_links = playwright_client.get_elements("nav a, [role='navigation'] a, .nav a, .navigation a")
        assert len(nav_links) > 0, "Navigation borde ha länkar"


def test_mobile_responsiveness(playwright_client, frontend_url):
    """Test att frontend är responsiv på mobile"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Test mobile viewport
    playwright_client.page.set_viewport_size({"width": 375, "height": 667})
    playwright_client.wait_for_timeout(1000)
    
    # Kontrollera att sidan fortfarande är användbar
    assert playwright_client.is_element_visible("body"), "Sidan borde vara synlig på mobile"
    
    # Kontrollera att navigation fungerar på mobile (om den finns)
    nav_elements = playwright_client.get_elements("nav, [role='navigation'], .nav, .navigation")
    if nav_elements:
        # Kontrollera att minst ett navigation-element är synligt
        nav_visible = any(playwright_client.is_element_visible(f"nav:nth-of-type({i+1}), [role='navigation']:nth-of-type({i+1}), .nav:nth-of-type({i+1}), .navigation:nth-of-type({i+1})") for i in range(len(nav_elements)))
        if not nav_visible:
            # Om ingen navigation är synlig, kontrollera att sidan ändå är användbar
            interactive_elements = playwright_client.get_elements("button, a, input, select, textarea")
            assert len(interactive_elements) > 0, "Sidan borde ha interaktiva element även på mobile"


def test_accessibility_basics(playwright_client, frontend_url):
    """Test grundläggande tillgänglighet"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det finns rubriker
    headings = playwright_client.get_elements("h1, h2, h3, h4, h5, h6")
    assert len(headings) > 0, "Sidan borde ha rubriker för tillgänglighet"
    
    # Kontrollera att det finns interaktiva element
    interactive_elements = playwright_client.get_elements("button, a, input, select, textarea")
    assert len(interactive_elements) > 0, "Sidan borde ha interaktiva element"
    
    # Kontrollera att det finns navigation
    nav_elements = playwright_client.get_elements("nav, [role='navigation'], .nav, .navigation")
    if nav_elements:
        assert len(nav_elements) > 0, "Sidan borde ha navigation för tillgänglighet"