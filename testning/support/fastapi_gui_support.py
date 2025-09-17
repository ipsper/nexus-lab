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
    """Klicka på en endpoint i Swagger UI"""
    endpoint_selector = f".opblock-get .opblock-summary-path[data-path='{endpoint_path}']"
    playwright_client.wait_for_selector(endpoint_selector, timeout=5000)
    playwright_client.click(endpoint_selector)


def try_it_out(playwright_client: PlaywrightClient) -> None:
    """Klicka på 'Try it out' knappen"""
    try_it_button = ".btn.try-out__btn"
    playwright_client.wait_for_selector(try_it_button, timeout=5000)
    playwright_client.click(try_it_button)


def execute_request(playwright_client: PlaywrightClient) -> None:
    """Klicka på 'Execute' knappen"""
    execute_button = ".btn.execute"
    playwright_client.wait_for_selector(execute_button, timeout=5000)
    playwright_client.click(execute_button)


def get_response_status(playwright_client: PlaywrightClient) -> str:
    """Hämta status från senaste API-svar"""
    response_status = ".response-col_status"
    playwright_client.wait_for_selector(response_status, timeout=10000)
    return playwright_client.get_text(response_status)


def get_response_body(playwright_client: PlaywrightClient) -> str:
    """Hämta response body från senaste API-anrop"""
    response_body_selector = ".response-col_description .microlight"
    if playwright_client.is_element_visible(response_body_selector):
        return playwright_client.get_text(response_body_selector)
    return ""


def check_endpoint_visible(playwright_client: PlaywrightClient, endpoint_path: str) -> bool:
    """Kontrollera om endpoint är synlig i dokumentationen"""
    endpoint_selector = f".opblock-summary-path[data-path='{endpoint_path}']"
    return playwright_client.is_element_visible(endpoint_selector)


def set_viewport_size(playwright_client: PlaywrightClient, width: int, height: int) -> None:
    """Sätt viewport storlek"""
    playwright_client.page.set_viewport_size({"width": width, "height": height})


def scroll_to_bottom(playwright_client: PlaywrightClient) -> None:
    """Scrolla till botten av sidan"""
    playwright_client.execute_javascript("window.scrollTo(0, document.body.scrollHeight)")
    playwright_client.wait_for_timeout(1000)
