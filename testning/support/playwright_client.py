"""
Playwright Client för GUI-testning
"""
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from typing import Optional, Dict, Any
import time


class PlaywrightClient:
    """Playwright klient för GUI-testning"""
    
    def __init__(self, 
                 browser_type: str = "chromium", 
                 headless: bool = True,
                 timeout: int = 30000):
        self.browser_type = browser_type
        self.headless = headless
        self.timeout = timeout
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def start(self) -> 'PlaywrightClient':
        """Starta Playwright och browser"""
        self.playwright = sync_playwright().start()
        
        # Välj browser typ
        if self.browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(headless=self.headless)
        elif self.browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=self.headless)
        elif self.browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=self.headless)
        else:
            raise ValueError(f"Okänd browser typ: {self.browser_type}")
        
        # Skapa context och page
        self.context = self.browser.new_context()
        self.context.set_default_timeout(self.timeout)
        self.page = self.context.new_page()
        
        return self
    
    def navigate_to(self, url: str) -> None:
        """Navigera till URL"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        self.page.goto(url)
    
    def wait_for_selector(self, selector: str, timeout: Optional[int] = None) -> None:
        """Vänta på att element ska visas"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        wait_timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, timeout=wait_timeout)
    
    def click(self, selector: str) -> None:
        """Klicka på element"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        self.page.click(selector)
    
    def fill(self, selector: str, text: str) -> None:
        """Fyll i text i input-fält"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Hämta text från element"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.text_content(selector) or ""
    
    def get_title(self) -> str:
        """Hämta sidans titel"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.title()
    
    def get_url(self) -> str:
        """Hämta nuvarande URL"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.url
    
    def screenshot(self, path: str) -> None:
        """Ta skärmdump"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        self.page.screenshot(path=path)
    
    def wait_for_load_state(self, state: str = "networkidle") -> None:
        """Vänta på att sidan ska ladda"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        self.page.wait_for_load_state(state)
    
    def is_element_visible(self, selector: str) -> bool:
        """Kontrollera om element är synligt"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.is_visible(selector)
    
    def is_element_enabled(self, selector: str) -> bool:
        """Kontrollera om element är aktiverat"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.is_enabled(selector)
    
    def get_element_count(self, selector: str) -> int:
        """Räkna antal element som matchar selector"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.locator(selector).count()
    
    def wait_for_timeout(self, timeout: int) -> None:
        """Vänta i angivet antal millisekunder"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        self.page.wait_for_timeout(timeout)
    
    def execute_javascript(self, script: str) -> Any:
        """Kör JavaScript kod"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.evaluate(script)
    
    def get_page_source(self) -> str:
        """Hämta sidans HTML-källkod"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        return self.page.content()
    
    def get_elements(self, selector: str) -> list:
        """Hämta alla element som matchar selector"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        locator = self.page.locator(selector)
        count = locator.count()
        elements = []
        for i in range(count):
            elements.append(locator.nth(i))
        return elements
    
    def get_console_logs(self) -> list:
        """Hämta console-loggarna"""
        if not self.page:
            raise RuntimeError("Browser inte startad. Kör start() först.")
        # Detta är en förenklad implementation
        # I en riktig implementation skulle man samla loggar under sidans livslängd
        return []
    
    def close(self) -> None:
        """Stäng browser och Playwright"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def __enter__(self) -> 'PlaywrightClient':
        """Context manager start"""
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager cleanup"""
        self.close()
