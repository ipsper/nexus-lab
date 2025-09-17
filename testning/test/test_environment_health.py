"""
Environment Health Check - Kontrollera att miljön är uppe innan andra tester
"""
import pytest
import requests
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
            response = requests.get(url, timeout=5)
            
            if response.status_code in [200, 404, 502, 503]:
                print(f"✅ {service_name} svarar (status: {response.status_code})")
            else:
                print(f"⚠️  {service_name} svarar med oväntat status: {response.status_code}")
                failed_services.append(f"{service_name} (status: {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {service_name} svarar inte - connection error")
            failed_services.append(f"{service_name} (connection error)")
        except requests.exceptions.Timeout:
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
def test_api_endpoints_responding(api_client):
    """Kontrollera att viktiga API-endpoints svarar"""
    
    endpoints_to_check = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/docs", "API dokumentation"),
        ("/openapi.json", "OpenAPI schema")
    ]
    
    failed_endpoints = []
    
    for endpoint, description in endpoints_to_check:
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
    
    if failed_endpoints:
        pytest.fail(
            f"\n\n💥 API-ENDPOINTS SVARAR INTE KORREKT:\n" +
            "\n".join(f"   • {endpoint}" for endpoint in failed_endpoints) +
            "\n\n🔧 Kontrollera att FastAPI-tjänsten körs korrekt.\n"
        )
    
    print(f"\n🎉 Alla API-endpoints svarar korrekt!")


@pytest.mark.health
@pytest.mark.order(3)  # Kör efter API health check
def test_kong_gateway_routing(kong_client):
    """Kontrollera att Kong Gateway routing fungerar"""
    
    routes_to_check = [
        ("/api", "FastAPI route"),
        ("/nexus", "Nexus route")
    ]
    
    failed_routes = []
    
    for route, description in routes_to_check:
        try:
            print(f"🔍 Testar {description} ({route})...")
            response = kong_client.get(route)
            
            if response.status_code in [200, 404, 502, 503]:
                print(f"✅ {description} routing OK (status: {response.status_code})")
            else:
                print(f"⚠️  {description} oväntat status: {response.status_code}")
                failed_routes.append(f"{description} ({route}) - status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description} fel: {e}")
            failed_routes.append(f"{description} ({route}) - error: {e}")
    
    if failed_routes:
        pytest.fail(
            f"\n\n💥 KONG GATEWAY ROUTING FUNGERAR INTE:\n" +
            "\n".join(f"   • {route}" for route in failed_routes) +
            "\n\n🔧 Kontrollera Kong Gateway konfiguration.\n"
        )
    
    print(f"\n🎉 Kong Gateway routing fungerar!")


@pytest.mark.health
@pytest.mark.slow
@pytest.mark.order(4)  # Kör sist bland health checks
def test_full_system_integration(api_client, kong_client, nexus_client):
    """Omfattande systemintegration health check"""
    
    print(f"\n🔍 Testar fullständig systemintegration...")
    
    # Test 1: FastAPI direkt
    try:
        api_response = api_client.get("/health")
        assert api_response.status_code == 200
        api_data = api_response.json()
        assert api_data["status"] == "healthy"
        print(f"✅ FastAPI direkt: OK")
    except Exception as e:
        pytest.fail(f"❌ FastAPI direkt misslyckades: {e}")
    
    # Test 2: FastAPI genom Kong
    try:
        kong_api_response = kong_client.get("/api/health")
        assert kong_api_response.status_code == 200
        kong_api_data = kong_api_response.json()
        assert kong_api_data["status"] == "healthy"
        print(f"✅ FastAPI genom Kong: OK")
    except Exception as e:
        pytest.fail(f"❌ FastAPI genom Kong misslyckades: {e}")
    
    # Test 3: Nexus genom Kong (mer tolerant)
    try:
        nexus_response = kong_client.get("/nexus")
        # Nexus kan vara 200, 404 eller 503 under startup
        assert nexus_response.status_code in [200, 404, 503]
        print(f"✅ Nexus genom Kong: OK (status: {nexus_response.status_code})")
    except Exception as e:
        print(f"⚠️  Nexus genom Kong: {e} (kan vara OK under startup)")
    
    # Test 4: Nexus direkt (mer tolerant)
    try:
        nexus_direct_response = nexus_client.get("/")
        assert nexus_direct_response.status_code in [200, 404, 503]
        print(f"✅ Nexus direkt: OK (status: {nexus_direct_response.status_code})")
    except Exception as e:
        print(f"⚠️  Nexus direkt: {e} (kan vara OK under startup)")
    
    print(f"\n🎉 Systemintegration fungerar! Miljön är redo för tester.")


@pytest.mark.health
def test_wait_for_services_ready():
    """Vänta på att tjänsterna ska bli redo (retry-logik)"""
    
    max_retries = 30
    retry_delay = 2
    
    services = [
        ("http://host.docker.internal:8000/api/health", "FastAPI"),
        ("http://host.docker.internal:8000", "Kong Gateway")
    ]
    
    for url, service_name in services:
        print(f"\n⏳ Väntar på {service_name}...")
        
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, timeout=3)
                if response.status_code in [200, 404]:
                    print(f"✅ {service_name} är redo efter {attempt} försök!")
                    break
            except:
                pass
            
            if attempt < max_retries:
                print(f"🔄 Försök {attempt}/{max_retries} - väntar {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                pytest.fail(f"❌ {service_name} blev inte redo efter {max_retries} försök")
    
    print(f"\n🎉 Alla tjänster är redo!")
