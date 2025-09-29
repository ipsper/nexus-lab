"""
Environment Health Check - Kontrollera att miljön är uppe innan andra tester
"""
import pytest
import httpx
import time
from support.api_client import APIClient


@pytest.mark.health
@pytest.mark.order(1)  # Kör detta test först
def test_environment_ready(api_base_url, kong_base_url, nexus_base_url):
    """Kontrollera att alla tjänster är uppe och redo"""
    
    services = [
        ("FastAPI", api_base_url),
        ("Kong Gateway", kong_base_url), 
        ("Nexus", nexus_base_url)
    ]
    
    failed_services = []
    
    for service_name, url in services:
        print(f"\n🔍 Kontrollerar {service_name} på {url}...")
        
        try:
            # Försök ansluta med timeout
            response = httpx.get(url, timeout=5)
            
            if response.status_code in [200, 404, 502, 503, 307]:
                print(f"✅ {service_name} svarar (status: {response.status_code})")
            else:
                print(f"⚠️  {service_name} svarar med oväntat status: {response.status_code}")
                failed_services.append(f"{service_name} (status: {response.status_code})")
                
        except httpx.ConnectError:
            print(f"❌ {service_name} svarar inte - connection error")
            failed_services.append(f"{service_name} (connection error)")
        except httpx.TimeoutException:
            print(f"❌ {service_name} timeout efter 5s")
            failed_services.append(f"{service_name} (timeout)")
        except Exception as e:
            print(f"❌ {service_name} okänt fel: {e}")
            failed_services.append(f"{service_name} (error: {e})")
    
    # Om några tjänster misslyckades, misslyckas testet
    if failed_services:
        pytest.fail(
            f"\n\n💥 MILJÖN ÄR INTE REDO! Följande tjänster är inte tillgängliga:\n" +
            "\n".join(f"   • {service}" for service in failed_services) +
            "\n\n🚀 Starta tjänsterna först med: ./scripts/run.sh\n" +
            "   Vänta tills alla tjänster är igång, sedan kör testerna igen.\n"
        )
    
    print(f"\n🎉 Alla tjänster är uppe och redo!")


@pytest.mark.health
@pytest.mark.order(2)  # Kör efter basic health check
def test_api_endpoints_responding(api_client, kong_client):
    """Kontrollera att viktiga API-endpoints svarar"""
    
    # API endpoints (under /api/ prefix)
    api_endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/openapi.json", "OpenAPI schema")
    ]
    
    # Kong Gateway endpoints (under root)
    kong_endpoints = [
        ("/docs", "API dokumentation")
    ]
    
    failed_endpoints = []
    
    # Testa API endpoints
    for endpoint, description in api_endpoints:
        try:
            print(f"🔍 Testar {description} ({endpoint})...")
            response = api_client.get(endpoint)
            
            if response.status_code == 200:
                print(f"✅ {description} OK (200)")
            else:
                print(f"⚠️  {description} status: {response.status_code}")
                failed_endpoints.append(f"{description} ({endpoint}) - status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description} fel: {e}")
            failed_endpoints.append(f"{description} ({endpoint}) - error: {e}")
    
    # Testa Kong Gateway endpoints
    for endpoint, description in kong_endpoints:
        try:
            print(f"🔍 Testar {description} ({endpoint})...")
            response = kong_client.get(endpoint)
            
            if response.status_code == 200:
                print(f"✅ {description} OK (200)")
            else:
                print(f"⚠️  {description} status: {response.status_code}")
                failed_endpoints.append(f"{description} ({endpoint}) - status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description} fel: {e}")
            failed_endpoints.append(f"{description} ({endpoint}) - error: {e}")
    
    if failed_endpoints:
        pytest.fail(
            f"\n\n💥 API-ENDPOINTS SVARAR INTE KORREKT:\n" +
            "\n".join(f"   • {endpoint}" for endpoint in failed_endpoints) +
            "\n\n🔧 Kontrollera att FastAPI-tjänsten körs korrekt.\n"
        )
    
    print(f"\n🎉 Alla API-endpoints svarar korrekt!")
