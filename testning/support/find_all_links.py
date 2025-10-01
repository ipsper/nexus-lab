#!/usr/bin/env python3
"""
Skript för att hitta alla länkar i frontenden
"""
import requests
from playwright_client import PlaywrightClient

def find_all_links():
    """Hitta alla länkar i frontenden"""
    frontend_url = "http://localhost:8000"
    
    # Starta Playwright
    client = PlaywrightClient(browser_type="chromium", headless=True, timeout=30000)
    client.start()
    
    try:
        # Navigera till alla sidor
        pages = ["/", "/repositories", "/schedules", "/statistics", "/settings"]
        all_links = set()
        
        for page in pages:
            url = f"{frontend_url}{page}"
            print(f"\n=== Analyserar {url} ===")
            
            client.navigate_to(url)
            client.wait_for_load_state("networkidle")
            
            # Hitta alla länkar
            links = client.get_elements("a")
            
            for link in links:
                href = link.get_attribute("href")
                text = link.text_content()
                target = link.get_attribute("target")
                
                if href:
                    link_info = {
                        'href': href,
                        'text': text.strip() if text else '',
                        'target': target,
                        'page': page
                    }
                    all_links.add(tuple(sorted(link_info.items())))
                    
                    print(f"  Länk: {href}")
                    print(f"    Text: '{text.strip() if text else ''}'")
                    print(f"    Target: {target}")
                    print(f"    Sidan: {page}")
                    print()
        
        print(f"\n=== SAMMANFATTNING ===")
        print(f"Totalt antal unika länkar: {len(all_links)}")
        
        # Gruppera länkar efter typ
        internal_links = []
        external_links = []
        api_links = []
        asset_links = []
        
        for link_tuple in all_links:
            link_dict = dict(link_tuple)
            href = link_dict['href']
            
            if href.startswith('/api/'):
                api_links.append(link_dict)
            elif href.startswith('/assets/') or href.startswith('/vite.svg'):
                asset_links.append(link_dict)
            elif href.startswith('http'):
                external_links.append(link_dict)
            elif href.startswith('/'):
                internal_links.append(link_dict)
        
        print(f"\nInterna länkar ({len(internal_links)}):")
        for link in internal_links:
            print(f"  {link['href']} - '{link['text']}' (sida: {link['page']})")
        
        print(f"\nAPI länkar ({len(api_links)}):")
        for link in api_links:
            print(f"  {link['href']} - '{link['text']}' (sida: {link['page']})")
        
        print(f"\nExterna länkar ({len(external_links)}):")
        for link in external_links:
            print(f"  {link['href']} - '{link['text']}' (sida: {link['page']})")
        
        print(f"\nAsset länkar ({len(asset_links)}):")
        for link in asset_links:
            print(f"  {link['href']} - '{link['text']}' (sida: {link['page']})")
            
    finally:
        client.close()

if __name__ == "__main__":
    find_all_links()
