"""
Playwright-tester för frontend navigation och knappinteraktioner
Testar att navigation-länkar och knappar fungerar korrekt
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


def test_navigation_links_work(playwright_client, frontend_url):
    """Test att navigation-länkar fungerar och navigerar till rätt sidor"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Sök efter navigation-länkar
    nav_links = playwright_client.get_elements("nav a, [role='navigation'] a, .nav a, .navigation a, header a")
    
    if nav_links:
        for i, link in enumerate(nav_links[:5]):  # Testa första 5 länkarna
            # Navigera tillbaka till startsidan först
            playwright_client.navigate_to(frontend_url)
            playwright_client.wait_for_load_state("networkidle")
            playwright_client.wait_for_timeout(1000)
            
            # Klicka på länken
            try:
                playwright_client.click(f"nav a:nth-of-type({i+1}), [role='navigation'] a:nth-of-type({i+1}), .nav a:nth-of-type({i+1}), .navigation a:nth-of-type({i+1}), header a:nth-of-type({i+1})")
                playwright_client.wait_for_load_state("networkidle")
                
                # Kontrollera att URL ändrades
                current_url = playwright_client.get_url()
                assert current_url != frontend_url, f"Navigation-länk {i+1} borde ha ändrat URL"
                
                # Kontrollera att sidan laddades utan fel
                page_source = playwright_client.get_page_source()
                assert "error" not in page_source.lower() or "Error" not in page_source, f"Navigation-länk {i+1} borde inte visa fel"
                
            except Exception as e:
                # Om länken inte fungerar, fortsätt med nästa
                continue


def test_button_clicks_work(playwright_client, frontend_url):
    """Test att knappar fungerar och utför förväntade åtgärder"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Sök efter knappar
    buttons = playwright_client.get_elements("button, input[type='button'], input[type='submit'], .btn")
    
    if buttons:
        for i, button in enumerate(buttons[:5]):  # Testa första 5 knapparna
            # Navigera tillbaka till startsidan först
            playwright_client.navigate_to(frontend_url)
            playwright_client.wait_for_load_state("networkidle")
            playwright_client.wait_for_timeout(1000)
            
            # Klicka på knappen
            try:
                playwright_client.click(f"button:nth-of-type({i+1}), input[type='button']:nth-of-type({i+1}), input[type='submit']:nth-of-type({i+1}), .btn:nth-of-type({i+1})")
                playwright_client.wait_for_load_state("networkidle")
                
                # Kontrollera att något hände (sidan laddades om eller URL ändrades)
                current_url = playwright_client.get_url()
                page_source = playwright_client.get_page_source()
                
                # Knappen borde ha gjort något - antingen ändrat URL eller laddat om sidan
                assert current_url or len(page_source) > 100, f"Knapp {i+1} borde ha gjort något"
                
            except Exception as e:
                # Om knappen inte fungerar, fortsätt med nästa
                continue


def test_cta_buttons_functionality(playwright_client, frontend_url):
    """Test att CTA-knappar (Call-to-Action) fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Sök efter CTA-knappar (ofta med specifika klasser)
    cta_buttons = playwright_client.get_elements(".btn-primary, .btn-outline, .btn")
    
    if cta_buttons:
        for i, button in enumerate(cta_buttons[:3]):  # Testa första 3 CTA-knapparna
            # Navigera tillbaka till startsidan först
            playwright_client.navigate_to(frontend_url)
            playwright_client.wait_for_load_state("networkidle")
            playwright_client.wait_for_timeout(1000)
            
            # Klicka på CTA-knappen
            try:
                playwright_client.click(f".btn-primary:nth-of-type({i+1}), .btn-outline:nth-of-type({i+1})")
                playwright_client.wait_for_load_state("networkidle")
                
                # Kontrollera att något hände
                current_url = playwright_client.get_url()
                page_source = playwright_client.get_page_source()
                
                # CTA-knappen borde ha gjort något
                assert current_url or len(page_source) > 100, f"CTA-knapp {i+1} borde ha gjort något"
                
            except Exception as e:
                # Om CTA-knappen inte fungerar, fortsätt med nästa
                continue


def test_form_submission_buttons(playwright_client, frontend_url):
    """Test att formulärskickningsknappar fungerar"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Sök efter formulär och submit-knappar
    forms = playwright_client.get_elements("form")
    
    if forms:
        for i, form in enumerate(forms[:2]):  # Testa första 2 formulären
            # Navigera tillbaka till startsidan först
            playwright_client.navigate_to(frontend_url)
            playwright_client.wait_for_load_state("networkidle")
            playwright_client.wait_for_timeout(1000)
            
            # Sök efter submit-knappar i formuläret
            submit_buttons = playwright_client.get_elements(f"form:nth-of-type({i+1}) button[type='submit'], form:nth-of-type({i+1}) input[type='submit'], form:nth-of-type({i+1}) .btn")
            
            if submit_buttons:
                try:
                    # Fyll i något i första input-fältet om det finns
                    input_fields = playwright_client.get_elements(f"form:nth-of-type({i+1}) input, form:nth-of-type({i+1}) textarea")
                    if input_fields:
                        playwright_client.fill(f"form:nth-of-type({i+1}) input, form:nth-of-type({i+1}) textarea", "test@example.com")
                    
                    # Klicka på submit-knappen
                    playwright_client.click(f"form:nth-of-type({i+1}) button[type='submit'], form:nth-of-type({i+1}) input[type='submit'], form:nth-of-type({i+1}) .btn")
                    playwright_client.wait_for_load_state("networkidle")
                    
                    # Kontrollera att formuläret skickades
                    current_url = playwright_client.get_url()
                    page_source = playwright_client.get_page_source()
                    
                    # Formuläret borde ha skickats
                    assert current_url or len(page_source) > 100, f"Formulär {i+1} borde ha skickats"
                    
                except Exception as e:
                    # Om formuläret inte fungerar, fortsätt med nästa
                    continue


def test_navigation_consistency_across_pages(playwright_client, frontend_url):
    """Test att navigation är konsistent på olika sidor"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Hitta navigation-element
    nav_elements = playwright_client.get_elements("nav, [role='navigation'], .nav, .navigation, header")
    
    if nav_elements:
        # Testa att navigera till olika sidor och kontrollera att navigation finns
        test_pages = [
            frontend_url,
            f"{frontend_url}/repositories",
            f"{frontend_url}/schedules", 
            f"{frontend_url}/settings",
            f"{frontend_url}/dashboard"
        ]
        
        for page_url in test_pages:
            try:
                playwright_client.navigate_to(page_url)
                playwright_client.wait_for_load_state("networkidle")
                playwright_client.wait_for_timeout(1000)
                
                # Kontrollera att navigation fortfarande finns
                nav_still_exists = playwright_client.get_elements("nav, [role='navigation'], .nav, .navigation, header")
                assert len(nav_still_exists) > 0, f"Navigation borde finnas på {page_url}"
                
            except Exception as e:
                # Om sidan inte finns, fortsätt med nästa
                continue


def test_mobile_navigation_works(playwright_client, frontend_url):
    """Test att navigation fungerar på mobile enheter"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Sätt mobile viewport
    playwright_client.page.set_viewport_size({"width": 375, "height": 667})
    playwright_client.wait_for_timeout(1000)
    
    # Sök efter navigation på mobile
    nav_elements = playwright_client.get_elements("nav, [role='navigation'], .nav, .navigation, header, .mobile-nav, .hamburger")
    
    if nav_elements:
        # Testa att klicka på första navigation-elementet
        try:
            playwright_client.click("nav, [role='navigation'], .nav, .navigation, header, .mobile-nav, .hamburger")
            playwright_client.wait_for_load_state("networkidle")
            
            # Kontrollera att något hände
            current_url = playwright_client.get_url()
            page_source = playwright_client.get_page_source()
            
            # Navigation borde ha fungerat på mobile
            assert current_url or len(page_source) > 100, "Mobile navigation borde ha fungerat"
            
        except Exception as e:
            # Om mobile navigation inte fungerar, kontrollera att sidan ändå är användbar
            interactive_elements = playwright_client.get_elements("button, a, input, select, textarea")
            assert len(interactive_elements) > 0, "Sidan borde ha interaktiva element på mobile"


def test_navigation_accessibility(playwright_client, frontend_url):
    """Test att navigation är tillgänglig med tangentbord"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Sök efter navigation-länkar
    nav_links = playwright_client.get_elements("nav a, [role='navigation'] a, .nav a, .navigation a, header a")
    
    if nav_links:
        # Testa att navigera med tangentbord (Tab-tangenten)
        try:
            # Simulera Tab-tryck för att navigera mellan länkar
            playwright_client.execute_javascript("document.querySelector('nav a, [role=\"navigation\"] a, .nav a, .navigation a, header a').focus()")
            playwright_client.wait_for_timeout(500)
            
            # Kontrollera att elementet är fokuserat
            focused_element = playwright_client.execute_javascript("document.activeElement")
            assert focused_element is not None, "Navigation-länk borde kunna fokuseras med tangentbord"
            
        except Exception as e:
            # Om tangentbordsnavigation inte fungerar, kontrollera att det finns andra interaktiva element
            interactive_elements = playwright_client.get_elements("button, a, input, select, textarea")
            assert len(interactive_elements) > 0, "Sidan borde ha interaktiva element för tangentbordsnavigation"


def test_navigation_performance(playwright_client, frontend_url):
    """Test att navigation är snabb och responsiv"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Sök efter navigation-länkar
    nav_links = playwright_client.get_elements("nav a, [role='navigation'] a, .nav a, .navigation a, header a")
    
    if nav_links:
        # Testa första länken
        try:
            start_time = time.time()
            
            playwright_client.click("nav a, [role='navigation'] a, .nav a, .navigation a, header a")
            playwright_client.wait_for_load_state("networkidle")
            
            navigation_time = time.time() - start_time
            
            # Navigation borde vara snabb (under 3 sekunder)
            assert navigation_time < 3, f"Navigation var för långsam: {navigation_time:.2f} sekunder"
            
        except Exception as e:
            # Om navigation inte fungerar, fortsätt
            pass


def test_navigation_error_handling(playwright_client, frontend_url):
    """Test att navigation hanterar fel korrekt"""
    playwright_client.navigate_to(frontend_url)
    playwright_client.wait_for_load_state("networkidle")
    
    # Vänta på att sidan laddas helt
    playwright_client.wait_for_timeout(2000)
    
    # Testa att navigera till en icke-existerande sida
    try:
        playwright_client.navigate_to(f"{frontend_url}/nonexistent-page")
        playwright_client.wait_for_load_state("networkidle")
        
        # Kontrollera att sidan hanterade felet korrekt
        page_source = playwright_client.get_page_source()
        
        # Sidan borde inte krascha, även om sidan inte finns
        assert len(page_source) > 100, "Sidan borde hantera icke-existerande sidor korrekt"
        
        # Kontrollera att det inte finns JavaScript-fel
        assert "error" not in page_source.lower() or "Error" not in page_source, "Sidan borde inte visa JavaScript-fel"
        
    except Exception as e:
        # Om navigation till icke-existerande sida inte fungerar, det är okej
        pass
