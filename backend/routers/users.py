from typing import Annotated
from fastapi import APIRouter, Depends

from backend.core.dependencies import get_user_service
from backend.services.user_service import UserService


router = APIRouter()
