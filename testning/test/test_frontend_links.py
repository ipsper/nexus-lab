import pytest
import time
import requests
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


def test_all_navigation_links_work(playwright_client, frontend_url):
    """Test att alla navigation-länkar fungerar korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Lista över alla navigation-länkar som ska finnas
    expected_links = [
        {"text": "Dashboard", "href": "/", "expected_url": "/"},
        {"text": "Repositories", "href": "/repositories", "expected_url": "/repositories"},
        {"text": "Schedules", "href": "/schedules", "expected_url": "/schedules"},
        {"text": "Statistics", "href": "/statistics", "expected_url": "/statistics"},
        {"text": "Settings", "href": "/settings", "expected_url": "/settings"},
    ]

    for link_info in expected_links:
        # Navigera tillbaka till startsidan först
        playwright_client.navigate_to(frontend_url)
        playwright_client.wait_for_load_state("networkidle")

        # Hitta länken
        link_elements = playwright_client.get_elements(f"a[href='{link_info['href']}']")
        assert len(link_elements) > 0, f"Länk '{link_info['text']}' med href '{link_info['href']}' hittades inte"
        link_element = link_elements[0]

        # Klicka på länken
        link_element.click()
        playwright_client.wait_for_load_state("networkidle")

        # Kontrollera att URL har ändrats korrekt
        current_url = playwright_client.get_url()
        assert link_info['expected_url'] in current_url, f"Länk '{link_info['text']}' navigerade till fel URL. Förväntat: {link_info['expected_url']}, Faktiskt: {current_url}"

        # Kontrollera att sidan laddades utan fel
        assert playwright_client.is_element_visible("body"), f"Sidan för '{link_info['text']}' laddades inte korrekt"


def test_api_docs_links_work(playwright_client, frontend_url):
    """Test att alla API Docs-länkar fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla API Docs-länkar
    api_docs_links = playwright_client.get_elements("a[href='/docs']")
    assert len(api_docs_links) > 0, "Inga API Docs-länkar hittades"

    for i, link in enumerate(api_docs_links):
        # Navigera tillbaka till startsidan först
        playwright_client.navigate_to(frontend_url)
        playwright_client.wait_for_load_state("networkidle")

        # Klicka på länken
        link.click()
        playwright_client.wait_for_load_state("networkidle")

        # Kontrollera att URL har ändrats till API docs eller att nytt fönster öppnades
        current_url = playwright_client.get_url()
        # API Docs-länkar öppnas i nytt fönster, så vi kontrollerar att länken har rätt attribut
        target = link.get_attribute("target")
        href = link.get_attribute("href")
        assert target == "_blank" or "/docs" in current_url or "swagger" in current_url, f"API Docs-länk {i+1} har fel target eller navigerade inte korrekt. Target: {target}, URL: {current_url}, Href: {href}"

        # Kontrollera att API dokumentation laddades
        assert playwright_client.is_element_visible("body"), f"API dokumentation laddades inte korrekt för länk {i+1}"


def test_repository_links_work(playwright_client, frontend_url):
    """Test att repository-länkar fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Navigera till repositories-sidan
    playwright_client.navigate_to(f"{frontend_url}/repositories")
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla repository-länkar
    repository_links = playwright_client.get_elements("a[href*='http']")
    
    if repository_links:
        for i, link in enumerate(repository_links[:3]):  # Testa första 3 repository-länkarna
            # Hämta href-attributet
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                # Klicka på länken
                link.click()
                playwright_client.wait_for_load_state("networkidle")

                # Kontrollera att URL har ändrats
                current_url = playwright_client.get_url()
                assert href in current_url or current_url.startswith("http"), f"Repository-länk {i+1} navigerade inte korrekt. Förväntat: {href}, Faktiskt: {current_url}"

                # Gå tillbaka till repositories-sidan
                playwright_client.navigate_to(f"{frontend_url}/repositories")
                playwright_client.wait_for_load_state("networkidle")


def test_cta_buttons_navigate_correctly(playwright_client, frontend_url):
    """Test att CTA-knappar navigerar korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla CTA-knappar
    cta_buttons = playwright_client.get_elements(".btn-primary, .btn-outline")
    
    for i, button in enumerate(cta_buttons):
        # Navigera tillbaka till startsidan först
        playwright_client.navigate_to(frontend_url)
        playwright_client.wait_for_load_state("networkidle")

        # Hämta knapptext
        button_text = button.text_content()
        
        # Klicka på knappen
        button.click()
        playwright_client.wait_for_load_state("networkidle")

        # Kontrollera navigation baserat på knapptext
        current_url = playwright_client.get_url()
        
        if "Kom igång" in button_text:
            assert "/repositories" in current_url, f"CTA-knapp '{button_text}' navigerade inte till repositories. URL: {current_url}"
        elif "API Dokumentation" in button_text or "API Docs" in button_text:
            # API Docs-knappar öppnas i nytt fönster
            target = button.get_attribute("target")
            href = button.get_attribute("href")
            assert target == "_blank" or "/api/docs" in current_url or "swagger" in current_url, f"CTA-knapp '{button_text}' har fel target eller navigerade inte till API docs. Target: {target}, URL: {current_url}, Href: {href}"
        elif "Hantera Repositories" in button_text:
            assert "/repositories" in current_url, f"CTA-knapp '{button_text}' navigerade inte till repositories. URL: {current_url}"


def test_mobile_navigation_links_work(playwright_client, frontend_url):
    """Test att navigation-länkar finns på mobile"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Sätt mobile viewport
    playwright_client.page.set_viewport_size({"width": 375, "height": 667})
    playwright_client.wait_for_timeout(1000)

    # Kontrollera att sidan fortfarande är användbar på mobile
    assert playwright_client.is_element_visible("body"), "Sidan är inte synlig på mobile"
    
    # Kontrollera att navigation-länkarna finns även på mobile
    nav_links = playwright_client.get_elements("a[href^='/']")
    assert len(nav_links) > 0, "Inga navigation-länkar hittades på mobile"
    
    # Kontrollera att länkarna har korrekta href-attribut
    expected_hrefs = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    found_hrefs = []
    
    for link in nav_links:
        href = link.get_attribute("href")
        if href and href.startswith("/"):
            found_hrefs.append(href)
    
    # Kontrollera att minst några av de förväntade länkarna finns
    assert any(href in found_hrefs for href in expected_hrefs), f"Förväntade navigation-länkar saknas på mobile. Hittade: {found_hrefs}"


def test_external_links_have_correct_attributes(playwright_client, frontend_url):
    """Test att externa länkar har korrekta attribut"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla externa länkar
    external_links = playwright_client.get_elements("a[target='_blank']")
    
    for link in external_links:
        # Kontrollera att externa länkar har korrekta attribut
        target = link.get_attribute("target")
        rel = link.get_attribute("rel")
        
        assert target == "_blank", f"Extern länk saknar target='_blank'. Target: {target}"
        assert "noopener" in rel or "noreferrer" in rel, f"Extern länk saknar säkra rel-attribut. Rel: {rel}"


def test_all_pages_have_consistent_navigation(playwright_client, frontend_url):
    """Test att alla sidor har konsistent navigation"""
    pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in pages:
        playwright_client.navigate_to(f"{frontend_url}{page}")
        playwright_client.wait_for_load_state("networkidle")

        # Kontrollera att navigation finns på alla sidor
        nav_elements = playwright_client.get_elements("nav, [role='navigation']")
        assert len(nav_elements) > 0, f"Navigation saknas på sidan {page}"

        # Kontrollera att huvudnavigation-länkarna finns
        expected_nav_links = ["Dashboard", "Repositories", "Schedules", "Statistics", "Settings"]
        for link_text in expected_nav_links:
            # Sök efter länkar som innehåller den förväntade texten
            all_links = playwright_client.get_elements("a")
            found_link = False
            for link in all_links:
                if link_text in link.text_content():
                    found_link = True
                    break
            assert found_link, f"Navigation-länk '{link_text}' saknas på sidan {page}"


def test_link_accessibility(playwright_client, frontend_url):
    """Test att länkar är tillgängliga"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla länkar
    all_links = playwright_client.get_elements("a")
    
    for link in all_links:
        # Kontrollera att länkar har text eller aria-label
        link_text = link.text_content()
        aria_label = link.get_attribute("aria-label")
        
        assert link_text or aria_label, f"Länk saknar text och aria-label: {link.get_attribute('href')}"
        
        # Kontrollera att länkar inte är tomma
        assert link_text.strip() or aria_label, f"Länk har tom text: {link.get_attribute('href')}"


def test_navigation_performance(playwright_client, frontend_url):
    """Test att navigation är snabb"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Testa navigation till olika sidor och mät tid
    pages = ["/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in pages:
        start_time = time.time()
        
        # Navigera till sidan
        playwright_client.navigate_to(f"{frontend_url}{page}")
        playwright_client.wait_for_load_state("networkidle")
        
        end_time = time.time()
        navigation_time = end_time - start_time
        
        # Kontrollera att navigation är snabb (under 3 sekunder)
        assert navigation_time < 3.0, f"Navigation till {page} tog för lång tid: {navigation_time:.2f}s"


def test_broken_links_handling(playwright_client, frontend_url):
    """Test att trasiga länkar hanteras korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Testa navigation till en icke-existerande sida
    playwright_client.navigate_to(f"{frontend_url}/nonexistent-page")
    playwright_client.wait_for_load_state("networkidle")

    # Kontrollera att sidan hanterar 404-felet gracefully
    current_url = playwright_client.get_url()
    
    # Antingen ska vi vara på 404-sidan eller omdirigerade tillbaka
    assert "/nonexistent-page" in current_url or current_url == f"{frontend_url}/", f"Trasig länk hanterades inte korrekt. URL: {current_url}"


def test_all_frontend_pages_return_200(playwright_client, frontend_url):
    """Test att alla frontend-sidor returnerar HTTP 200"""
    pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in pages:
        url = f"{frontend_url}{page}"
        
        # Kontrollera HTTP-statuskod
        response = requests.get(url, timeout=10)
        assert response.status_code == 200, f"Sida {page} returnerade fel statuskod: {response.status_code}. URL: {url}"
        
        # Kontrollera att innehållet laddades korrekt
        assert len(response.text) > 100, f"Sida {page} returnerade för lite innehåll. Storlek: {len(response.text)}"
        
        # Kontrollera att det är HTML
        assert "text/html" in response.headers.get("content-type", ""), f"Sida {page} returnerade inte HTML. Content-Type: {response.headers.get('content-type')}"


def test_all_navigation_links_return_200(playwright_client, frontend_url):
    """Test att alla navigation-länkar returnerar HTTP 200"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla interna länkar
    internal_links = playwright_client.get_elements("a[href^='/']")
    
    for link in internal_links:
        href = link.get_attribute("href")
        if href and href.startswith("/") and not href.startswith("/api/"):
            url = f"{frontend_url}{href}"
            
            # Kontrollera HTTP-statuskod
            response = requests.get(url, timeout=10)
            assert response.status_code == 200, f"Navigation-länk {href} returnerade fel statuskod: {response.status_code}. URL: {url}"
            
            # Kontrollera att innehållet laddades korrekt
            assert len(response.text) > 100, f"Navigation-länk {href} returnerade för lite innehåll. Storlek: {len(response.text)}"


def test_api_docs_links_return_200(playwright_client, frontend_url):
    """Test att API Docs-länkar returnerar HTTP 200"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla API Docs-länkar
    api_docs_links = playwright_client.get_elements("a[href='/api/docs']")
    
    for link in api_docs_links:
        href = link.get_attribute("href")
        url = f"{frontend_url}{href}"
        
        # Kontrollera HTTP-statuskod
        response = requests.get(url, timeout=10)
        assert response.status_code == 200, f"API Docs-länk returnerade fel statuskod: {response.status_code}. URL: {url}"
        
        # Kontrollera att det är API-dokumentation
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower(), f"API Docs-länk returnerade inte API-dokumentation. URL: {url}"


def test_external_links_are_valid(playwright_client, frontend_url):
    """Test att externa länkar är giltiga"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla externa länkar
    external_links = playwright_client.get_elements("a[href^='http']")
    
    for link in external_links:
        href = link.get_attribute("href")
        if href and href.startswith("http"):
            # Hoppa över repository-länkar som returnerar från FastAPI
            if "/repository/" in href:
                print(f"Hoppar över repository-länk (hanteras av FastAPI): {href}")
                continue
            
            try:
                # Kontrollera HTTP-statuskod för externa länkar
                response = requests.get(href, timeout=10, allow_redirects=True)
                assert response.status_code == 200, f"Extern länk {href} returnerade fel statuskod: {response.status_code}"
                
                # Kontrollera att länken inte är trasig
                assert len(response.text) > 50, f"Extern länk {href} returnerade för lite innehåll. Storlek: {len(response.text)}"
                
            except requests.exceptions.RequestException as e:
                # Om extern länk inte är tillgänglig, det är OK för testet
                print(f"Extern länk {href} är inte tillgänglig: {e}")


def test_all_cta_buttons_have_valid_links(playwright_client, frontend_url):
    """Test att alla CTA-knappar har giltiga länkar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla CTA-knappar
    cta_buttons = playwright_client.get_elements(".btn-primary, .btn-outline")
    
    for button in cta_buttons:
        # Kontrollera om knappen är en länk genom att kolla href-attributet
        href = button.get_attribute("href")
        if href:
            # Hoppa över repository-länkar
            if "/repository/" in href:
                print(f"Hoppar över repository-länk: {href}")
                continue
            
            if href.startswith("/"):
                url = f"{frontend_url}{href}"
            else:
                url = href
            
            # Kontrollera HTTP-statuskod
            response = requests.get(url, timeout=10)
            assert response.status_code == 200, f"CTA-knapp med länk {href} returnerade fel statuskod: {response.status_code}. URL: {url}"


def test_no_broken_internal_links(playwright_client, frontend_url):
    """Test att inga interna länkar är trasiga"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla interna länkar
    internal_links = playwright_client.get_elements("a[href^='/']")
    
    broken_links = []
    
    for link in internal_links:
        href = link.get_attribute("href")
        if href and href.startswith("/") and not href.startswith("/api/"):
            url = f"{frontend_url}{href}"
            
            try:
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    broken_links.append(f"{href} -> {response.status_code}")
            except requests.exceptions.RequestException:
                broken_links.append(f"{href} -> Connection error")
    
    assert len(broken_links) == 0, f"Trasiga interna länkar hittades: {broken_links}"
