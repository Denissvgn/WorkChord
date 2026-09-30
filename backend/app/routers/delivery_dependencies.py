"""Versioned delivery prerequisite commands."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.task_domain import domain_result
from app.services.delivery_dependency_service import DeliveryDependencyService

router = APIRouter()
DeliveryDatabase = Annotated[AsyncSession, Depends(get_db, scope="function")]


class DeliveryDependencyInput(BaseModel):
    kind: Literal["task", "milestone"]
    target_id: int = Field(gt=0)
    expected_version: int = Field(gt=0)


@router.get("/tasks/{task_id}/delivery-dependencies")
async def list_delivery_dependencies(task_id: int, db: DeliveryDatabase):
    return await domain_result(DeliveryDependencyService(db).projection(task_id))


@router.post("/tasks/{task_id}/delivery-dependencies")
async def add_delivery_dependency(task_id: int, data: DeliveryDependencyInput, db: DeliveryDatabase):
    return await domain_result(DeliveryDependencyService(db).add(task_id, data.kind, data.target_id, data.expected_version))


@router.delete("/tasks/{task_id}/delivery-dependencies/{edge_id}")
async def remove_delivery_dependency(task_id: int, edge_id: int, db: DeliveryDatabase, expected_version: int = Query(gt=0)):
    return await domain_result(DeliveryDependencyService(db).remove(task_id, edge_id, expected_version))
