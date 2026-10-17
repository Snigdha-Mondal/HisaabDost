import asyncio
import logging
from app.config import settings
from app.workflows.closing_workflow import DailyClosingWorkflow, HAS_TEMPORAL
from app.workflows.activities import (
    initiate_closing_call_activity,
    execute_audit_activity,
    send_caregiver_summary_activity
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_worker():
    """
    Connects to the Temporal service and starts listening on the HisaabDost task queue.
    """
    if not HAS_TEMPORAL:
        logger.warning(
            "Temporal Python SDK ('temporalio') is not installed in current environment. "
            "Install with 'pip install temporalio' to run worker daemon. "
            "Local test workflow harness remains fully functional."
        )
        return

    from temporalio.client import Client
    from temporalio.worker import Worker

    logger.info(f"Connecting to Temporal cluster at {settings.TEMPORAL_HOST_URL}...")
    client = await Client.connect(settings.TEMPORAL_HOST_URL)

    worker = Worker(
        client,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
        workflows=[DailyClosingWorkflow],
        activities=[
            initiate_closing_call_activity,
            execute_audit_activity,
            send_caregiver_summary_activity
        ]
    )

    logger.info(f"Temporal worker started on task queue '{settings.TEMPORAL_TASK_QUEUE}'. Listening for calls...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(start_worker())
