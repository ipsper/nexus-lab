"""
FastAPI GUI support functions - rena hjälpfunktioner för Playwright
"""
from support.playwright_client import PlaywrightClient
from typing import List


def navigate_to_docs(playwright_client: PlaywrightClient, base_url: str) -> None:
    """Navigera till docs-sidan och vänta på att den laddas"""
    playwright_client.navigate_to(f"{base_url.rstrip('/')}/docs")
    playwright_client.wait_for_load_state()
    playwright_client.wait_for_selector(".swagger-ui", timeout=10000)


def click_endpoint(playwright_client: PlaywrightClient, endpoint_path: str) -> None:
    """Klicka på en endpoint i Swagger UI - med förbättrade selektorer"""
    # Flera möjliga selektorer för endpoints
    possible_selectors = [
        f".opblock .opblock-summary-path[data-path='{endpoint_path}']",
        f".opblock-summary-path[data-path='{endpoint_path}']", 
        f"[data-path='{endpoint_path}']",
        f".opblock-summary:has-text('{endpoint_path}')",
        f".opblock-summary-path:has-text('{endpoint_path}')"
    ]
    
    clicked = False
    for selector in possible_selectors:
        try:
            if playwright_client.is_element_visible(selector):
                playwright_client.click(selector)
                clicked = True
                break
        except:
            continue
    
    if not clicked:
        # Fallback: leta efter endpoint i hela dokumentet
        playwright_client.execute_javascript(f"""
            (() => {{
                const elements = document.querySelectorAll('*');
                for (let el of elements) {{
                    if (el.textContent && el.textContent.includes('{endpoint_path}')) {{
                        el.click();
                        break;
                    }}
                }}
            }})()
        """)


def try_it_out(playwright_client: PlaywrightClient) -> None:
    """Klicka på 'Try it out' knappen - med förbättrade selektorer"""
    possible_selectors = [
        ".btn.try-out__btn",
        "button.try-out__btn",
        "[class*='try-out']",
        "button:has-text('Try it out')",
        ".try-out__btn"
    ]
    
    for selector in possible_selectors:
        try:
            if playwright_client.is_element_visible(selector):
                playwright_client.click(selector)
                return
        except:
            continue
    
    # Fallback
    playwright_client.execute_javascript("""
        (() => {
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.textContent && btn.textContent.includes('Try it out')) {
                    btn.click();
                    break;
                }
            }
        })()
    """)


def execute_request(playwright_client: PlaywrightClient) -> None:
    """Klicka på 'Execute' knappen - med förbättrade selektorer"""
    possible_selectors = [
        ".btn.execute",
        "button.execute",
        "[class*='execute']",
        "button:has-text('Execute')",
        ".execute"
    ]
    
    for selector in possible_selectors:
        try:
            if playwright_client.is_element_visible(selector):
                playwright_client.click(selector)
                return
        except:
            continue
    
    # Fallback
    playwright_client.execute_javascript("""
        (() => {
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.textContent && btn.textContent.includes('Execute')) {
                    btn.click();
                    break;
                }
            }
        })()
    """)


def get_response_status(playwright_client: PlaywrightClient) -> str:
    """Hämta status från senaste API-svar - med förbättrade selektorer"""
    possible_selectors = [
        ".response-col_status",
        ".response .status",
        "[class*='response'] [class*='status']",
        ".responses-wrapper .response .status",
        ".response-col_status .status",
        ".response .response-col_status",
        ".opblock-response .response-col_status",
        ".opblock-response .status"
    ]
    
    for selector in possible_selectors:
        try:
            if playwright_client.is_element_visible(selector):
                text = playwright_client.get_text(selector)
                if text and text.strip():
                    return text.strip()
        except:
            continue
    
    # Fallback: leta efter status-text med JavaScript
    status_text = playwright_client.execute_javascript("""
        (() => {
            // Leta efter status-kod i olika element
            const selectors = [
                '.response-col_status',
                '.response .status',
                '[class*="response"] [class*="status"]',
                '.responses-wrapper .response .status',
                '.opblock-response .response-col_status',
                '.opblock-response .status'
            ];
            
            for (let selector of selectors) {
                const elements = document.querySelectorAll(selector);
                for (let el of elements) {
                    if (el.textContent && el.textContent.trim()) {
                        return el.textContent.trim();
                    }
                }
            }
            
            // Leta efter status-kod i hela dokumentet
            const allElements = document.querySelectorAll('*');
            for (let el of allElements) {
                if (el.textContent && el.textContent.match(/\\b[0-9]{3}\\b/)) {
                    return el.textContent.trim();
                }
            }
            
            return '';
        })()
    """)
    
    return status_text or "unknown"


def get_response_body(playwright_client: PlaywrightClient) -> str:
    """Hämta response body från senaste API-anrop"""
    possible_selectors = [
        ".response-col_description .microlight",
        ".response-body",
        ".response .body",
        "[class*='response'] [class*='body']",
        ".response-col_description",
        ".opblock-response .response-col_description",
        ".response .response-col_description",
        ".microlight"
    ]
    
    for selector in possible_selectors:
        try:
            if playwright_client.is_element_visible(selector):
                text = playwright_client.get_text(selector)
                if text and text.strip():
                    return text.strip()
        except:
            continue
    
    # Fallback: leta efter JSON i hela dokumentet
    json_text = playwright_client.execute_javascript("""
        (() => {
            const elements = document.querySelectorAll('*');
            for (let el of elements) {
                if (el.textContent && el.textContent.includes('{') && el.textContent.includes('}')) {
                    return el.textContent.trim();
                }
            }
            return '';
        })()
    """)
    
    return json_text or ""


def check_endpoint_visible(playwright_client: PlaywrightClient, endpoint_path: str) -> bool:
    """Kontrollera om endpoint är synlig i dokumentationen - med förbättrade selektorer"""
    possible_selectors = [
        f".opblock-summary-path[data-path='{endpoint_path}']",
        f"[data-path='{endpoint_path}']",
        f".opblock-summary:has-text('{endpoint_path}')",
        f".opblock:has-text('{endpoint_path}')"
    ]
    
    for selector in possible_selectors:
        try:
            if playwright_client.is_element_visible(selector):
                return True
        except:
            continue
    
    # Fallback: sök i hela dokumentet
    found = playwright_client.execute_javascript(f"""
        (() => {{
            const elements = document.querySelectorAll('*');
            for (let el of elements) {{
                if (el.textContent && el.textContent.includes('{endpoint_path}')) {{
                    return true;
                }}
            }}
            return false;
        }})()
    """)
    
    return bool(found)


def set_viewport_size(playwright_client: PlaywrightClient, width: int, height: int) -> None:
    """Sätt viewport storlek"""
    playwright_client.page.set_viewport_size({"width": width, "height": height})


def scroll_to_bottom(playwright_client: PlaywrightClient) -> None:
    """Scrolla till botten av sidan"""
    playwright_client.execute_javascript("window.scrollTo(0, document.body.scrollHeight)")
    playwright_client.wait_for_timeout(1000)


def wait_for_swagger_ui_loaded(playwright_client: PlaywrightClient) -> None:
    """Vänta på att Swagger UI ska ladda helt"""
    # Vänta på grundläggande Swagger UI
    playwright_client.wait_for_selector(".swagger-ui", timeout=10000)
    
    # Vänta lite extra för att API-schemat ska ladda
    playwright_client.wait_for_timeout(2000)
    
    # Kontrollera att endpoints har laddats
    playwright_client.execute_javascript("""
        // Vänta på att endpoints ska visas
        let attempts = 0;
        const checkEndpoints = () => {
            const endpoints = document.querySelectorAll('.opblock, [class*="opblock"]');
            if (endpoints.length > 0 || attempts > 10) {
                return;
            }
            attempts++;
            setTimeout(checkEndpoints, 500);
        };
        checkEndpoints();
    """)
    
    playwright_client.wait_for_timeout(1000)
