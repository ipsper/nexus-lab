"""
Debug-test för Swagger UI
"""
import pytest
from support.playwright_client import PlaywrightClient
from support.fastapi_gui_support import navigate_to_docs, wait_for_swagger_ui_loaded

# Inaktivera asyncio för Playwright-tester
pytestmark = pytest.mark.asyncio(mode="off")


@pytest.mark.gui
def test_debug_swagger_content(api_base_url):
    """Debug Swagger UI-innehåll"""
    with PlaywrightClient(headless=True) as client:
        navigate_to_docs(client, api_base_url)
        wait_for_swagger_ui_loaded(client)
        
        # Ta skärmdump (om tillgängligt)
        try:
            client.take_screenshot("swagger_debug.png")
        except:
            print("Skärmdump inte tillgänglig")
        
        # Hämta sidans innehåll
        page_content = client.get_page_source()
        
        print(f"\n=== SIDANS TITEL ===")
        print(client.get_title())
        
        print(f"\n=== SIDANS URL ===")
        try:
            print(client.get_current_url())
        except:
            print("URL inte tillgänglig")
        
        print(f"\n=== SIDANS INNEHÅLL (första 2000 tecken) ===")
        print(page_content[:2000])
        
        print(f"\n=== SÖK EFTER SPECIFIKA ORD ===")
        search_terms = ["health", "repositories", "swagger", "openapi", "GET", "POST", "endpoints"]
        for term in search_terms:
            count = page_content.lower().count(term.lower())
            print(f"'{term}': {count} gånger")
        
        print(f"\n=== SÖK EFTER ENDPOINTS ===")
        endpoint_terms = ["/health", "/repositories", "/packages", "/stats", "/formats", "/config"]
        for term in endpoint_terms:
            count = page_content.lower().count(term.lower())
            print(f"'{term}': {count} gånger")
        
        # Kontrollera att Swagger UI-element finns
        print(f"\n=== SWAGGER UI ELEMENT ===")
        swagger_ui_visible = client.is_element_visible(".swagger-ui")
        print(f"Swagger UI synlig: {swagger_ui_visible}")
        
        # Kontrollera om det finns några knappar eller länkar
        print(f"\n=== KNAPPAR OCH LÄNKAR ===")
        try:
            buttons = client.get_elements("button")
            links = client.get_elements("a")
            print(f"Antal knappar: {len(buttons)}")
            print(f"Antal länkar: {len(links)}")
        except:
            print("Kunde inte hämta knappar/länkar")
        
        # Kontrollera om det finns några div-element med specifika klasser
        print(f"\n=== DIV ELEMENT ===")
        try:
            divs = client.get_elements("div")
            print(f"Antal div-element: {len(divs)}")
        except:
            print("Kunde inte hämta div-element")
        
        # Sök efter specifika Swagger UI-klasser
        print(f"\n=== SWAGGER UI KLASSER ===")
        swagger_classes = ["swagger-ui", "opblock", "endpoint", "operation"]
        for class_name in swagger_classes:
            try:
                elements = client.get_elements(f".{class_name}")
                print(f"Element med klass '{class_name}': {len(elements)}")
            except:
                print(f"Kunde inte söka efter klass '{class_name}'")
        
        # Kontrollera om det finns JavaScript-fel
        print(f"\n=== JAVASCRIPT KONSOLLOGGAR ===")
        try:
            logs = client.get_console_logs()
            for log in logs:
                print(f"Console: {log}")
        except:
            print("Kunde inte hämta console-loggarna")
        
        # Grundläggande kontroller
        assert client.is_element_visible(".swagger-ui"), "Swagger UI-element inte synligt"
        assert "swagger" in page_content.lower() or "openapi" in page_content.lower(), "Ingen Swagger/OpenAPI-referens hittades"
