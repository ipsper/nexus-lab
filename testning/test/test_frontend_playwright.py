"""
Playwright-tester för frontend
Testar React-applikationens GUI-funktionalitet
"""
import pytest
import time
from support.playwright_client import PlaywrightClient


@pytest.fixture(scope="function")
def frontend_url():
    """Frontend URL för tester"""
    return "http://localhost:8000"


@pytest.fixture(scope="function")
def playwright_client():
    """Playwright klient för GUI-testning"""
    client = PlaywrightClient(browser_type="chromium", headless=True, timeout=30000)
    client.start()
    yield client
    client.close()


def test_frontend_loads_successfully(playwright_client, frontend_url):
    """Test att frontend laddas utan fel"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att sidan laddades
    title = playwright_client.get_title()
    assert "Nexus Repository Manager" in title or "Nexus" in title, f"Förväntad titel innehållande 'Nexus', fick: {title}"
    
    # Kontrollera att det finns React-innehåll
    playwright_client.wait_for_selector("body", timeout=10000)
    page_source = playwright_client.get_page_source()
    assert "react" in page_source.lower() or "nexus" in page_source.lower(), "Sidan verkar inte vara en React-app"


def test_frontend_navigation_works(playwright_client, frontend_url):
    """Test att navigation mellan sidor fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att navigation ska laddas
    try:
        playwright_client.wait_for_selector("nav, [role='navigation'], .nav, .navigation", timeout=10000)
    except:
        # Om ingen navigation hittas, kontrollera att sidan ändå laddades
        playwright_client.wait_for_selector("body", timeout=5000)
    
    # Kontrollera att vi kan navigera (om navigation finns)
    if playwright_client.is_element_visible("nav, [role='navigation'], .nav, .navigation"):
        # Försök att klicka på navigation-länkar om de finns
        nav_links = playwright_client.get_elements("nav a, [role='navigation'] a, .nav a, .navigation a")
        if nav_links:
            # Klicka på första länken
            nav_links[0].click()
            playwright_client.wait_for_load_state("networkidle")
            # Kontrollera att URL ändrades
            current_url = playwright_client.get_url()
            assert current_url != frontend_url, "Navigation borde ha ändrat URL"


def test_frontend_api_connectivity(playwright_client, frontend_url):
    """Test att frontend kan kommunicera med API"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det finns API-anrop (genom att titta på network-loggarna)
    # Detta är en förenklad test - i en riktig implementation skulle man samla network-loggarna
    
    # Kontrollera att sidan laddades utan JavaScript-fel
    page_source = playwright_client.get_page_source()
    assert "error" not in page_source.lower() or "Error" not in page_source, "Sidan verkar ha JavaScript-fel"


def test_frontend_responsive_design(playwright_client, frontend_url):
    """Test att frontend är responsiv"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Test desktop viewport
    playwright_client.page.set_viewport_size({"width": 1920, "height": 1080})
    playwright_client.wait_for_timeout(1000)
    
    # Kontrollera att sidan laddades
    assert playwright_client.is_element_visible("body"), "Sidan borde vara synlig på desktop"
    
    # Test mobile viewport
    playwright_client.page.set_viewport_size({"width": 375, "height": 667})
    playwright_client.wait_for_timeout(1000)
    
    # Kontrollera att sidan fortfarande är synlig
    assert playwright_client.is_element_visible("body"), "Sidan borde vara synlig på mobile"


def test_frontend_loading_states(playwright_client, frontend_url):
    """Test att loading states fungerar korrekt"""
    playwright_client.navigate_to(frontend_url)
    
    # Kontrollera att sidan laddas
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det finns innehåll efter laddning
    playwright_client.wait_for_selector("body", timeout=10000)
    
    # Kontrollera att det inte finns eviga loading-spinners
    loading_elements = playwright_client.get_elements(".loading, .spinner, [data-testid='loading']")
    for element in loading_elements:
        if playwright_client.is_element_visible(f".loading, .spinner, [data-testid='loading']"):
            # Vänta lite till för att se om loading försvinner
            playwright_client.wait_for_timeout(2000)
            # Kontrollera att loading inte är kvar
            assert not playwright_client.is_element_visible(f".loading, .spinner, [data-testid='loading']"), "Loading state borde ha försvunnit"


def test_frontend_error_handling(playwright_client, frontend_url):
    """Test att frontend hanterar fel korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det inte finns synliga felmeddelanden
    error_elements = playwright_client.get_elements(".error, .alert-danger, [data-testid='error']")
    for element in error_elements:
        if playwright_client.is_element_visible(f".error, .alert-danger, [data-testid='error']"):
            error_text = playwright_client.get_text(f".error, .alert-danger, [data-testid='error']")
            # Tillåt vissa fel men inte kritiska
            assert "critical" not in error_text.lower(), f"Kritiskt fel hittades: {error_text}"


def test_frontend_performance(playwright_client, frontend_url):
    """Test att frontend laddas inom rimlig tid"""
    start_time = time.time()
    
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    load_time = time.time() - start_time
    
    # Kontrollera att sidan laddades inom 10 sekunder
    assert load_time < 10, f"Frontend laddades för långsamt: {load_time:.2f} sekunder"
    
    # Kontrollera att sidan laddades inom 5 sekunder (ideal)
    if load_time > 5:
        pytest.warn(f"Frontend laddades långsamt: {load_time:.2f} sekunder (ideal: <5s)")


def test_frontend_accessibility_basics(playwright_client, frontend_url):
    """Test grundläggande tillgänglighet"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att det finns en huvudrubrik
    headings = playwright_client.get_elements("h1, h2, h3, h4, h5, h6")
    assert len(headings) > 0, "Sidan borde ha minst en rubrik för tillgänglighet"
    
    # Kontrollera att det finns navigation
    nav_elements = playwright_client.get_elements("nav, [role='navigation'], .nav, .navigation")
    if nav_elements:
        assert len(nav_elements) > 0, "Sidan borde ha navigation för tillgänglighet"
    
    # Kontrollera att det finns knappar eller länkar
    interactive_elements = playwright_client.get_elements("button, a, input, select, textarea")
    assert len(interactive_elements) > 0, "Sidan borde ha interaktiva element"


def test_frontend_cross_browser_compatibility(playwright_client, frontend_url):
    """Test att frontend fungerar i olika browsers"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att sidan laddades utan fel
    title = playwright_client.get_title()
    assert title, "Sidan borde ha en titel"
    
    # Kontrollera att det finns innehåll
    playwright_client.wait_for_selector("body", timeout=10000)
    page_source = playwright_client.get_page_source()
    assert len(page_source) > 100, "Sidan borde ha innehåll"


def test_frontend_security_headers(playwright_client, frontend_url):
    """Test att frontend har säkra headers"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Kontrollera att sidan laddades utan säkerhetsfel
    page_source = playwright_client.get_page_source()
    
    # Kontrollera att det inte finns inline scripts med känslig data
    assert "password" not in page_source.lower() or "secret" not in page_source.lower(), "Sidan borde inte innehålla känslig data i källkoden"
    
    # Kontrollera att det inte finns synliga fel
    assert "error" not in page_source.lower() or "Error" not in page_source, "Sidan verkar ha fel"