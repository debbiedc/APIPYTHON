from fastapi import APIRouter, HTTPException
from app.core.database import get_supabase
from app.models.task import Task, TaskCreate
from supabase import Client

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[Task])
async def list_tasks():
    supabase: Client = get_supabase()
    response = supabase.table("tasks").select("*").execute()
    return response.data

@router.post("/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    supabase: Client = get_supabase()
    response = supabase.table("tasks").insert(task.dict()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create task")
    return response.data[0]