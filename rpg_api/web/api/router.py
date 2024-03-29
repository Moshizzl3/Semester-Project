from typing import Any

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from rpg_api.db.dependencies import get_db_session
from rpg_api.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)


@api_router.get("/")
def hello_world() -> str:
    """Hello World."""
    return "Hello world"


@api_router.get("/base-char")
async def get_base_chars(
    dbsession: AsyncSession = Depends(get_db_session),
) -> list[dict[str, Any]]:
    """Just a test end point."""
    result = await dbsession.execute(text("SELECT * FROM character_details_view"))
    rows = result.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="No data found")

    columns = result.keys()
    return [dict(zip(columns, row)) for row in rows]
