from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

from celery import Celery

from .media import scan_media

BROKER_URL = os.environ.get("CELERY_BROKER_URL", "memory://")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "cache+memory://")
celery_app = Celery(__name__, broker=BROKER_URL, backend=RESULT_BACKEND)
celery_app.conf.update(
    task_track_started=True,
    task_always_eager=os.environ.get("CELERY_TASK_ALWAYS_EAGER", "1") == "1",
    task_store_eager_result=True,
)


@celery_app.task(bind=True)
def scan_media_task(self, path: str) -> Dict[str, object]:
    """Scan *path* for media files and report progress."""
    directory = Path(path)
    files, skipped, logs, total = scan_media(
        directory,
        progress_cb=lambda cur, tot, recent: self.update_state(
            state="PROGRESS", meta={"current": cur, "total": tot, "logs": recent}
        ),
    )
    summary: Dict[str, int] = {}
    for item in files:
        label = item.get("label")
        if label:
            summary[label] = summary.get(label, 0) + 1
    return {
        "files": files,
        "skipped": skipped,
        "logs": logs,
        "summary": summary,
        "current": total,
        "total": total,
    }
