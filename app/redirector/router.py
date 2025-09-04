from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.common.db import get_db
from app.common import models
from app.adapters.analytics_client import record_click
from app.common.metrics import record_request
from app.common.logging_config import get_logger

logger = get_logger("redirector")

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    record_request("redirector") 
    link = db.query(models.Link).filter_by(short_code=code).first()
    if not link:
        logger.warning(f"Redirect failed: {code} not found")
        raise HTTPException(404, "Link not found")

    # Always call via adapter (thread or HTTP depending on MODE)
    logger.info(f"Redirecting {code} -> {link.long_url}")
    record_click(code)

    return RedirectResponse(url=link.long_url)
