from __future__ import annotations

import asyncio
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from deployment.app.config import get_settings
from deployment.app.graph_service import run_graph


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("deployment.api")

settings = get_settings()
app = FastAPI(title="LangGraph Agent API", version="1.0.0")


class InvokeRequest(BaseModel):
    query: str = Field(min_length=3, max_length=4000, description="User query for the LangGraph workflow")


class InvokeResponse(BaseModel):
    request_id: str
    status: str
    environment: str
    model_name: str
    max_iterations: int
    iterations_used: int
    review_decision: str
    answer: str
    trace: list[str]


class HealthResponse(BaseModel):
    status: str
    environment: str
    model_name: str
    max_iterations: int
    timeout_seconds: int


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.environment,
        model_name=settings.model_name,
        max_iterations=settings.max_iterations,
        timeout_seconds=settings.request_timeout_seconds,
    )


@app.post("/invoke", response_model=InvokeResponse)
async def invoke(payload: InvokeRequest) -> InvokeResponse:
    logger.info(
        "invoke_start | environment=%s | query_length=%s",
        settings.environment,
        len(payload.query),
    )

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(run_graph, payload.query),
            timeout=settings.request_timeout_seconds,
        )
    except TimeoutError as exc:
        logger.warning("invoke_timeout | timeout_seconds=%s", settings.request_timeout_seconds)
        raise HTTPException(status_code=504, detail="Graph invocation timed out.") from exc
    except ValueError as exc:
        logger.warning("invoke_validation_error | error=%s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("invoke_failed")
        raise HTTPException(status_code=500, detail="Graph invocation failed.") from exc

    logger.info(
        "invoke_success | request_id=%s | iterations_used=%s",
        result["request_id"],
        result["iterations_used"],
    )
    return InvokeResponse(**result)
