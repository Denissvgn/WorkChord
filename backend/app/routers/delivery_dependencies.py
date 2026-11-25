"""Versioned delivery prerequisite commands."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.task_domain import domain_result
from app.schemas.delivery_dependency import DeliveryDependencyInput, DeliveryDependencyRetarget
from app.services.delivery_dependency_service import DeliveryDependencyService

router = APIRouter()
DeliveryDatabase = Annotated[AsyncSession, Depends(get_db, scope="function")]


@router.get("/tasks/{task_id}/delivery-dependencies")
async def list_delivery_dependencies(task_id: int, db: DeliveryDatabase):
    return await domain_result(DeliveryDependencyService(db).projection(task_id))


@router.post("/tasks/{task_id}/delivery-dependencies")
async def add_delivery_dependency(task_id: int, data: DeliveryDependencyInput, db: DeliveryDatabase):
    return await domain_result(DeliveryDependencyService(db).add(task_id, data.kind, data.target_id, data.expected_version, data.target_branch))


@router.patch("/tasks/{task_id}/delivery-dependencies/{edge_id}")
async def retarget_delivery_dependency(task_id: int, edge_id: int, data: DeliveryDependencyRetarget, db: DeliveryDatabase):
    """Change or clear the branch on which a task prerequisite's accepted code must be merged."""
    return await domain_result(DeliveryDependencyService(db).retarget(task_id, edge_id, data.expected_version, data.target_branch))


@router.delete("/tasks/{task_id}/delivery-dependencies/{edge_id}")
async def remove_delivery_dependency(task_id: int, edge_id: int, db: DeliveryDatabase, expected_version: int = Query(gt=0)):
    return await domain_result(DeliveryDependencyService(db).remove(task_id, edge_id, expected_version))
