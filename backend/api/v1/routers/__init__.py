from fastapi import APIRouter, Depends, Request
from backend.api.dependency.providers.request import get_current_user_dependency
from backend.api.v1.routers.auth import router as auth_router
from backend.api.v1.routers.user import router as users_router
from backend.api.v1.routers.note import router as notes_router
from backend.api.v1.routers.task import router as tasks_router
from backend.api.v1.routers.team import router as team_router
from backend.api.v1.routers.column import router as column_router 
from backend.api.v1.routers.tag import router as tag_router 


v1_router = APIRouter(prefix='/v1')
PROTECTED = Depends(get_current_user_dependency)

v1_router.include_router(auth_router, tags=['auth'], prefix='/auth')
v1_router.include_router(users_router, tags=['users'], prefix='/user', dependencies=[PROTECTED])
v1_router.include_router(tasks_router, tags=['tasks'], prefix='/task', dependencies=[PROTECTED])
v1_router.include_router(team_router, tags=['teams'], prefix='/team', dependencies=[PROTECTED])
v1_router.include_router(notes_router, tags=['notes'], prefix='/note', dependencies=[PROTECTED])
v1_router.include_router(column_router, tags=['columns'], prefix='/column', dependencies=[PROTECTED])
v1_router.include_router(tag_router, tags=['tags'], prefix='/tag', dependencies=[PROTECTED])
