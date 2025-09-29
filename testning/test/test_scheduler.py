"""
Test för schemaläggningsfunktionaliteten
"""
import pytest
import time
from datetime import datetime, timedelta
from support.scheduler_support import SchedulerTestHelper


@pytest.fixture
def scheduler_helper(api_base_url):
    """Fixture för scheduler helper"""
    return SchedulerTestHelper(api_base_url)


@pytest.fixture(autouse=True)
def cleanup_schedules(scheduler_helper):
    """Automatisk cleanup efter varje test"""
    yield
    # Hämta alla scheman och ta bort dem
    try:
        schedules = scheduler_helper.get_all_schedules()
        for schedule in schedules:
            scheduler_helper.cleanup_schedule(schedule["id"])
    except:
        pass  # Ignorera fel vid cleanup


@pytest.mark.scheduler
def test_create_daily_schedule(scheduler_helper):
    """Test 1: Skapa dagligt schema"""
    schedule_data = scheduler_helper.create_test_schedule_data(
        name="Test Dagligt Schema",
        endpoint="/api/health",
        method="GET",
        frequency="daily"
    )
    
    data = scheduler_helper.create_schedule(schedule_data)
    
    # Validera response
    assert data["name"] == "Test Dagligt Schema"
    assert data["endpoint"] == "/api/health"
    assert data["method"] == "GET"
    assert data["frequency"] == "daily"
    assert data["enabled"] is True
    assert "id" in data
    assert "next_execution" in data
    assert "created_at" in data
    
    # Validera att next_execution är i framtiden
    next_exec = datetime.fromisoformat(data["next_execution"].replace("Z", "+00:00"))
    assert next_exec > datetime.now()


@pytest.mark.scheduler
def test_get_all_schedules(scheduler_helper):
    """Test 2: Hämta alla scheman"""
    data = scheduler_helper.get_all_schedules()
    
    # Validera att response är en lista
    assert isinstance(data, list)
    
    # Om det finns scheman, validera strukturen
    if data:
        schedule = data[0]
        required_fields = ["id", "name", "endpoint", "method", "frequency", "enabled", "created_at"]
        for field in required_fields:
            assert field in schedule, f"Field {field} missing from schedule"


@pytest.mark.scheduler
def test_create_weekly_schedule_with_limits(scheduler_helper):
    """Test 3: Skapa veckovis schema med begränsningar"""
    schedule_data = scheduler_helper.create_test_schedule_data(
        name="Test Veckovis Schema",
        endpoint="/api/repositories/",
        method="GET",
        frequency="weekly",
        max_executions=10,
        headers={
            "User-Agent": "Scheduler-Test/1.0",
            "X-Test-Header": "test-value"
        }
    )
    
    data = scheduler_helper.create_schedule(schedule_data)
    
    # Validera response
    assert data["name"] == "Test Veckovis Schema"
    assert data["endpoint"] == "/api/repositories/"
    assert data["method"] == "GET"
    assert data["frequency"] == "weekly"
    assert data["max_executions"] == 10
    assert data["enabled"] is True


@pytest.mark.scheduler
def test_schedule_management_operations(scheduler_helper):
    """Test 4: Hantera schema (uppdatera, aktivera, inaktivera)"""
    # Skapa ett schema först
    schedule_data = scheduler_helper.create_test_schedule_data(
        name="Test Management Schema",
        endpoint="/api/health",
        method="GET",
        frequency="daily"
    )
    
    schedule = scheduler_helper.create_schedule(schedule_data)
    schedule_id = schedule["id"]
    
    # Testa att hämta specifikt schema
    retrieved_schedule = scheduler_helper.get_schedule(schedule_id)
    assert retrieved_schedule["id"] == schedule_id
    assert retrieved_schedule["enabled"] is True
    
    # Testa att inaktivera schema
    scheduler_helper.disable_schedule(schedule_id)
    
    # Verifiera att schema är inaktiverat
    retrieved_schedule = scheduler_helper.get_schedule(schedule_id)
    assert retrieved_schedule["enabled"] is False
    
    # Testa att aktivera schema igen
    scheduler_helper.enable_schedule(schedule_id)
    
    # Verifiera att schema är aktiverat igen
    retrieved_schedule = scheduler_helper.get_schedule(schedule_id)
    assert retrieved_schedule["enabled"] is True
    
    # Testa att uppdatera schema
    update_data = {
        "name": "Uppdaterat Schema",
        "frequency": "weekly"
    }
    
    updated_schedule = scheduler_helper.update_schedule(schedule_id, update_data)
    assert updated_schedule["name"] == "Uppdaterat Schema"
    assert updated_schedule["frequency"] == "weekly"


@pytest.mark.scheduler
def test_schedule_execution_and_history(scheduler_helper):
    """Test 5: Köra schema och hämta körningshistorik"""
    # Skapa ett schema först
    schedule_data = scheduler_helper.create_test_schedule_data(
        name="Test Execution Schema",
        endpoint="/api/health",
        method="GET",
        frequency="once"
    )
    
    schedule = scheduler_helper.create_schedule(schedule_data)
    schedule_id = schedule["id"]
    
    # Testa manuell körning
    scheduler_helper.execute_schedule(schedule_id)
    
    # Vänta lite för att låta körningen slutföras
    time.sleep(2)
    
    # Hämta körningshistorik
    executions = scheduler_helper.get_schedule_executions(schedule_id)
    assert isinstance(executions, list)
    
    # Om det finns körningar, validera strukturen
    if executions:
        execution = executions[0]
        required_fields = ["id", "schedule_id", "executed_at", "status"]
        for field in required_fields:
            assert field in execution, f"Field {field} missing from execution"
        
        assert execution["schedule_id"] == schedule_id
        assert execution["status"] in ["running", "completed", "failed"]