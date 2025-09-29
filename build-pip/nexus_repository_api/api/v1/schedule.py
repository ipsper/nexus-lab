"""
Schema endpoints för att schemalägga API-anrop
"""
import asyncio
import uuid
import httpx
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from .models import (
    ScheduleRequest, 
    ScheduleUpdate,
    ScheduleResponse, 
    ScheduleExecution, 
    ScheduleFrequency,
    schedules,
    schedule_executions
)

# Skapa router för schema endpoints
router = APIRouter(
    prefix="/api/schedule",
    tags=["schema"],
    responses={404: {"description": "Schema inte hittat"}},
)


def calculate_next_execution(schedule: ScheduleResponse) -> Optional[datetime]:
    """Beräkna nästa körningstid baserat på frekvens"""
    now = datetime.now()
    
    if schedule.frequency == ScheduleFrequency.ONCE:
        return None  # Körs bara en gång
    
    elif schedule.frequency == ScheduleFrequency.DAILY:
        # Körs varje dag vid samma tid
        if schedule.last_execution:
            next_time = schedule.last_execution + timedelta(days=1)
        else:
            next_time = now + timedelta(minutes=1)  # Kör om 1 minut om första gången
        return next_time
    
    elif schedule.frequency == ScheduleFrequency.WEEKLY:
        # Körs varje vecka
        if schedule.last_execution:
            next_time = schedule.last_execution + timedelta(weeks=1)
        else:
            next_time = now + timedelta(minutes=1)
        return next_time
    
    elif schedule.frequency == ScheduleFrequency.MONTHLY:
        # Körs varje månad
        if schedule.last_execution:
            next_time = schedule.last_execution + timedelta(days=30)
        else:
            next_time = now + timedelta(minutes=1)
        return next_time
    
    return None


async def execute_schedule(schedule_id: str):
    """Kör ett schemalagt API-anrop"""
    if schedule_id not in schedules:
        return
    
    schedule = schedules[schedule_id]
    execution_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    # Skapa execution record
    execution = ScheduleExecution(
        id=execution_id,
        schedule_id=schedule_id,
        executed_at=start_time,
        status="running"
    )
    schedule_executions.append(execution)
    
    try:
        # Gör HTTP-anropet
        async with httpx.AsyncClient() as client:
            # Bygg fullständig URL
            base_url = "http://localhost:8000"  # API base URL
            full_url = f"{base_url}{schedule.endpoint}"
            
            # Gör anropet
            if schedule.method.upper() == "GET":
                response = await client.get(full_url, headers=schedule.headers or {})
            elif schedule.method.upper() == "POST":
                response = await client.post(full_url, json=schedule.data, headers=schedule.headers or {})
            elif schedule.method.upper() == "PUT":
                response = await client.put(full_url, json=schedule.data, headers=schedule.headers or {})
            elif schedule.method.upper() == "DELETE":
                response = await client.delete(full_url, headers=schedule.headers or {})
            else:
                raise ValueError(f"Unsupported HTTP method: {schedule.method}")
            
            # Uppdatera execution
            execution.status = "success"
            execution.response_status = response.status_code
            execution.response_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"text": response.text}
            
    except Exception as e:
        # Uppdatera execution med fel
        execution.status = "failed"
        execution.error_message = str(e)
    
    finally:
        # Uppdatera execution time
        execution.execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Uppdatera schedule
        schedule.last_execution = start_time
        schedule.execution_count += 1
        schedule.next_execution = calculate_next_execution(schedule)
        
        # Kontrollera om schemat ska stoppas
        if schedule.max_executions and schedule.execution_count >= schedule.max_executions:
            schedule.enabled = False
            schedule.next_execution = None


@router.post("/", response_model=ScheduleResponse)
async def create_schedule(schedule_request: ScheduleRequest):
    """Skapa ett nytt schema"""
    schedule_id = str(uuid.uuid4())
    
    # Validera endpoint
    if not schedule_request.endpoint.startswith("/"):
        raise HTTPException(status_code=400, detail="Endpoint måste börja med /")
    
    # Skapa schedule
    schedule = ScheduleResponse(
        id=schedule_id,
        name=schedule_request.name,
        endpoint=schedule_request.endpoint,
        method=schedule_request.method,
        frequency=schedule_request.frequency,
        next_execution=calculate_next_execution(ScheduleResponse(
            id=schedule_id,
            name=schedule_request.name,
            endpoint=schedule_request.endpoint,
            method=schedule_request.method,
            frequency=schedule_request.frequency,
            next_execution=None,
            last_execution=None,
            execution_count=0,
            max_executions=schedule_request.max_executions,
            enabled=schedule_request.enabled,
            created_at=datetime.now()
        )),
        last_execution=None,
        execution_count=0,
        max_executions=schedule_request.max_executions,
        enabled=schedule_request.enabled,
        created_at=datetime.now()
    )
    
    schedules[schedule_id] = schedule
    
    return schedule


@router.get("/", response_model=List[ScheduleResponse])
async def list_schedules():
    """Lista alla scheman"""
    return list(schedules.values())


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(schedule_id: str):
    """Hämta specifikt schema"""
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail="Schema inte hittat")
    return schedules[schedule_id]


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(schedule_id: str, schedule_update: ScheduleUpdate):
    """Uppdatera ett schema"""
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail="Schema inte hittat")
    
    schedule = schedules[schedule_id]
    
    # Uppdatera endast de fält som skickades med
    if schedule_update.name is not None:
        schedule.name = schedule_update.name
    if schedule_update.endpoint is not None:
        schedule.endpoint = schedule_update.endpoint
    if schedule_update.method is not None:
        schedule.method = schedule_update.method
    if schedule_update.frequency is not None:
        schedule.frequency = schedule_update.frequency
    if schedule_update.max_executions is not None:
        schedule.max_executions = schedule_update.max_executions
    if schedule_update.enabled is not None:
        schedule.enabled = schedule_update.enabled
    
    # Beräkna nästa körning om något relevant ändrades
    if any([schedule_update.frequency, schedule_update.enabled]):
        schedule.next_execution = calculate_next_execution(schedule)
    
    return schedule


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str):
    """Ta bort ett schema"""
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail="Schema inte hittat")
    
    del schedules[schedule_id]
    return {"message": "Schema borttaget"}


@router.post("/{schedule_id}/execute")
async def execute_schedule_now(schedule_id: str, background_tasks: BackgroundTasks):
    """Kör ett schema omedelbart"""
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail="Schema inte hittat")
    
    background_tasks.add_task(execute_schedule, schedule_id)
    return {"message": "Schema-körning startad"}


@router.get("/{schedule_id}/executions", response_model=List[ScheduleExecution])
async def get_schedule_executions(schedule_id: str, limit: int = 50):
    """Hämta körningshistorik för ett schema"""
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail="Schema inte hittat")
    
    executions = [exec for exec in schedule_executions if exec.schedule_id == schedule_id]
    executions.sort(key=lambda x: x.executed_at, reverse=True)
    
    return executions[:limit]


@router.post("/{schedule_id}/enable")
async def enable_schedule(schedule_id: str):
    """Aktivera ett schema"""
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail="Schema inte hittat")
    
    schedule = schedules[schedule_id]
    schedule.enabled = True
    schedule.next_execution = calculate_next_execution(schedule)
    
    return {"message": "Schema aktiverat"}


@router.post("/{schedule_id}/disable")
async def disable_schedule(schedule_id: str):
    """Inaktivera ett schema"""
    if schedule_id not in schedules:
        raise HTTPException(status_code=404, detail="Schema inte hittat")
    
    schedule = schedules[schedule_id]
    schedule.enabled = False
    schedule.next_execution = None
    
    return {"message": "Schema inaktiverat"}


# Background task för att köra scheman
async def run_scheduled_tasks():
    """Kör schemalagda uppgifter (körs i bakgrunden)"""
    while True:
        try:
            now = datetime.now()
            
            for schedule in schedules.values():
                if (schedule.enabled and 
                    schedule.next_execution and 
                    schedule.next_execution <= now):
                    
                    # Kontrollera om schemat fortfarande ska köras
                    if schedule.max_executions and schedule.execution_count >= schedule.max_executions:
                        schedule.enabled = False
                        schedule.next_execution = None
                        continue
                    
                    # Kör schemat
                    await execute_schedule(schedule.id)
            
            # Vänta 1 minut innan nästa kontroll
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Error in scheduled tasks: {e}")
            await asyncio.sleep(60)
