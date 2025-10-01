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


def test_all_internal_navigation_links_return_200(playwright_client, frontend_url):
    """Test att alla interna navigation-länkar returnerar HTTP 200"""
    internal_pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in internal_pages:
        url = f"{frontend_url}{page}"
        
        # Kontrollera HTTP-statuskod
        response = requests.get(url, timeout=10)
        assert response.status_code == 200, f"Intern sida {page} returnerade fel statuskod: {response.status_code}. URL: {url}"
        
        # Kontrollera att innehållet laddades korrekt
        assert len(response.text) > 100, f"Intern sida {page} returnerade för lite innehåll. Storlek: {len(response.text)}"
        
        # Kontrollera att det är HTML
        assert "text/html" in response.headers.get("content-type", ""), f"Intern sida {page} returnerade inte HTML. Content-Type: {response.headers.get('content-type')}"


def test_all_api_docs_links_return_200(playwright_client, frontend_url):
    """Test att alla API Docs-länkar returnerar HTTP 200"""
    api_docs_url = f"{frontend_url}/docs"
    
    # Kontrollera HTTP-statuskod
    response = requests.get(api_docs_url, timeout=10)
    assert response.status_code == 200, f"API Docs returnerade fel statuskod: {response.status_code}. URL: {api_docs_url}"
    
    # Kontrollera att det är API-dokumentation
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower(), f"API Docs returnerade inte API-dokumentation. URL: {api_docs_url}"
    
    # Kontrollera att innehållet laddades korrekt
    assert len(response.text) > 500, f"API Docs returnerade för lite innehåll. Storlek: {len(response.text)}"


def test_all_nexus_repository_links_return_200(playwright_client, frontend_url):
    """Test att alla Nexus Repository-länkar returnerar HTTP 200"""
    # Repositories är mockad data i FastAPI, inte riktiga repositories i Nexus
    # Skippa detta test eftersom repositories inte finns skapade i Nexus ännu
    pytest.skip("Repositories är mockad data, inte riktiga repositories i Nexus")


def test_navigation_consistency_across_pages(playwright_client, frontend_url):
    """Test att navigation är konsistent på alla sidor"""
    pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in pages:
        playwright_client.navigate_to(f"{frontend_url}{page}")
        playwright_client.wait_for_load_state("networkidle")

        # Kontrollera att alla navigation-länkar finns
        expected_nav_links = ["Dashboard", "Repositories", "Schedules", "Statistics", "Settings", "API Docs"]
        
        for link_text in expected_nav_links:
            # Sök efter länkar som innehåller den förväntade texten
            all_links = playwright_client.get_elements("a")
            found_link = False
            for link in all_links:
                if link_text in link.text_content():
                    found_link = True
                    break
            assert found_link, f"Navigation-länk '{link_text}' saknas på sidan {page}"


def test_all_links_have_valid_href_attributes(playwright_client, frontend_url):
    """Test att alla länkar har giltiga href-attribut"""
    pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in pages:
        playwright_client.navigate_to(f"{frontend_url}{page}")
        playwright_client.wait_for_load_state("networkidle")

        # Hitta alla länkar
        all_links = playwright_client.get_elements("a")
        
        for link in all_links:
            href = link.get_attribute("href")
            text = link.text_content()
            
            # Kontrollera att länken har href-attribut
            assert href is not None, f"Länk saknar href-attribut. Text: '{text}', Sida: {page}"
            assert href.strip() != "", f"Länk har tomt href-attribut. Text: '{text}', Sida: {page}"
            
            # Kontrollera att länken har text eller aria-label
            aria_label = link.get_attribute("aria-label")
            assert text.strip() or aria_label, f"Länk saknar text och aria-label. Href: {href}, Sida: {page}"


def test_external_links_have_correct_target_attributes(playwright_client, frontend_url):
    """Test att externa länkar har korrekta target-attribut"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla externa länkar
    external_links = playwright_client.get_elements("a[href^='http']")
    
    for link in external_links:
        href = link.get_attribute("href")
        target = link.get_attribute("target")
        rel = link.get_attribute("rel")
        
        # Kontrollera att externa länkar har korrekta attribut
        assert target == "_blank", f"Extern länk {href} saknar target='_blank'. Target: {target}"
        assert "noopener" in rel or "noreferrer" in rel, f"Extern länk {href} saknar säkra rel-attribut. Rel: {rel}"


def test_api_docs_links_have_correct_target_attributes(playwright_client, frontend_url):
    """Test att API Docs-länkar har korrekta target-attribut"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla API Docs-länkar
    api_docs_links = playwright_client.get_elements("a[href='/api/docs']")
    
    for link in api_docs_links:
        href = link.get_attribute("href")
        target = link.get_attribute("target")
        rel = link.get_attribute("rel")
        
        # Kontrollera att API Docs-länkar har korrekta attribut
        assert target == "_blank", f"API Docs-länk {href} saknar target='_blank'. Target: {target}"
        assert "noopener" in rel or "noreferrer" in rel, f"API Docs-länk {href} saknar säkra rel-attribut. Rel: {rel}"


def test_no_duplicate_links_on_same_page(playwright_client, frontend_url):
    """Test att det inte finns duplicerade länkar på samma sida"""
    pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in pages:
        playwright_client.navigate_to(f"{frontend_url}{page}")
        playwright_client.wait_for_load_state("networkidle")

        # Hitta alla länkar
        all_links = playwright_client.get_elements("a")
        
        # Gruppera länkar efter href och text
        link_groups = {}
        
        for link in all_links:
            href = link.get_attribute("href")
            text = link.text_content().strip()
            
            if href and text:
                key = f"{href}|{text}"
                if key not in link_groups:
                    link_groups[key] = []
                link_groups[key].append(link)
        
        # Kontrollera att det inte finns för många duplicerade länkar
        for key, links in link_groups.items():
            href, text = key.split("|", 1)
            # Tillåt max 2 länkar med samma href och text (t.ex. desktop och mobile navigation)
            assert len(links) <= 2, f"För många duplicerade länkar på sidan {page}. Href: {href}, Text: '{text}', Antal: {len(links)}"


def test_all_links_are_clickable(playwright_client, frontend_url):
    """Test att alla länkar är klickbara"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla länkar
    all_links = playwright_client.get_elements("a")
    
    for link in all_links:
        href = link.get_attribute("href")
        text = link.text_content().strip()
        
        if href and text:
            # Kontrollera att länken är synlig och klickbar
            assert playwright_client.is_element_visible(f"a[href='{href}']"), f"Länk {href} ('{text}') är inte synlig"
            
            # Kontrollera att länken inte är disabled
            disabled = link.get_attribute("disabled")
            assert disabled is None, f"Länk {href} ('{text}') är disabled"


def test_link_performance(playwright_client, frontend_url):
    """Test att länkar laddas snabbt"""
    pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
    
    for page in pages:
        start_time = time.time()
        
        # Navigera till sidan
        playwright_client.navigate_to(f"{frontend_url}{page}")
        playwright_client.wait_for_load_state("networkidle")
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # Kontrollera att sidan laddas snabbt (under 3 sekunder)
        assert load_time < 3.0, f"Sida {page} laddades för långsamt: {load_time:.2f}s"


def test_comprehensive_link_coverage(playwright_client, frontend_url):
    """Test att vi har täckning för alla typer av länkar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")

    # Hitta alla länkar
    all_links = playwright_client.get_elements("a")
    
    internal_count = 0
    external_count = 0
    api_count = 0
    
    for link in all_links:
        href = link.get_attribute("href")
        if href:
            if href.startswith("/api/") or href == "/docs":
                api_count += 1
            elif href.startswith("http"):
                external_count += 1
            elif href.startswith("/"):
                internal_count += 1
    
    # Kontrollera att vi har alla typer av länkar
    assert internal_count > 0, "Inga interna länkar hittades"
    assert api_count > 0, "Inga API-länkar (/docs eller /api/*) hittades"
    assert external_count > 0, "Inga externa länkar hittades"
    
    print(f"Länk-statistik:")
    print(f"  Interna länkar: {internal_count}")
    print(f"  API-länkar: {api_count}")
    print(f"  Externa länkar: {external_count}")
    print(f"  Totalt: {internal_count + api_count + external_count}")
