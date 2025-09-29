"""
Support för schemaläggningstester
"""
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class SchedulerTestHelper:
    """Helper-klass för schemaläggningstester"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.schedule_url = f"{base_url}/schedule"
    
    def create_schedule(self, schedule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Skapa ett schema"""
        print(f"DEBUG: create_schedule called with schedule_url: {self.schedule_url}")
        response = httpx.post(
            self.schedule_url,
            headers={"Content-Type": "application/json"},
            json=schedule_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_all_schedules(self) -> list:
        """Hämta alla scheman"""
        response = httpx.get(self.schedule_url)
        response.raise_for_status()
        return response.json()
    
    def get_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Hämta specifikt schema"""
        response = httpx.get(f"{self.schedule_url}/{schedule_id}")
        response.raise_for_status()
        return response.json()
    
    def update_schedule(self, schedule_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Uppdatera schema"""
        response = httpx.put(
            f"{self.schedule_url}/{schedule_id}",
            headers={"Content-Type": "application/json"},
            json=update_data
        )
        response.raise_for_status()
        return response.json()
    
    def enable_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Aktivera schema"""
        response = httpx.post(f"{self.schedule_url}/{schedule_id}/enable")
        response.raise_for_status()
        return response.json()
    
    def disable_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Inaktivera schema"""
        response = httpx.post(f"{self.schedule_url}/{schedule_id}/disable")
        response.raise_for_status()
        return response.json()
    
    def execute_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Kör schema manuellt"""
        response = httpx.post(f"{self.schedule_url}/{schedule_id}/execute")
        response.raise_for_status()
        return response.json()
    
    def get_schedule_executions(self, schedule_id: str) -> list:
        """Hämta körningshistorik för schema"""
        response = httpx.get(f"{self.schedule_url}/{schedule_id}/executions")
        response.raise_for_status()
        return response.json()
    
    def delete_schedule(self, schedule_id: str) -> None:
        """Ta bort schema"""
        response = httpx.delete(f"{self.schedule_url}/{schedule_id}")
        response.raise_for_status()
    
    def create_test_schedule_data(self, 
                                 name: str = "Test Schema",
                                 endpoint: str = "/api/health",
                                 method: str = "GET",
                                 frequency: str = "daily",
                                 start_time: Optional[datetime] = None,
                                 **kwargs) -> Dict[str, Any]:
        """Skapa testdata för schema"""
        if start_time is None:
            start_time = datetime.now() + timedelta(minutes=1)
        
        data = {
            "name": name,
            "endpoint": endpoint,
            "method": method,
            "frequency": frequency,
            "start_time": start_time.isoformat() + "Z",
            **kwargs
        }
        return data
    
    def cleanup_schedule(self, schedule_id: str) -> None:
        """Rensa upp schema (ignorera fel)"""
        try:
            self.delete_schedule(schedule_id)
        except:
            pass  # Ignorera fel vid cleanup
