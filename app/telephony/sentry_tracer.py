import time
import logging
from contextlib import contextmanager
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class SentryAgentTracer:
    """
    Traces audio stream latency, Gemma token processing, TabPFN evaluation, and TTS synthesis.
    Integrates with Sentry Performance Monitoring SDK when DSN is present,
    with local telemetry logging fallback.
    """

    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn or settings.SENTRY_DSN
        self.initialized = False
        self._init_sentry()

    def _init_sentry(self):
        if not self.dsn:
            return
        try:
            import sentry_sdk
            sentry_sdk.init(
                dsn=self.dsn,
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
                release=f"hisaabdost@{settings.VERSION}",
                environment="development" if settings.DEBUG else "production"
            )
            self.initialized = True
            logger.info("Sentry Agent Tracing initialized successfully.")
        except ImportError:
            logger.warning("sentry-sdk not installed. Running local span tracer.")
        except Exception as e:
            logger.warning(f"Sentry init failed: {e}. Running local span tracer.")

    @contextmanager
    def trace_span(self, op: str, description: str):
        """
        Traces execution latency of an operation across audio, LLM, or TabPFN.
        """
        start_time = time.perf_counter()
        span_data: Dict[str, Any] = {"op": op, "description": description}

        # If live Sentry SDK is active, wrap in sentry span
        sentry_span = None
        if self.initialized:
            try:
                import sentry_sdk
                sentry_span = sentry_sdk.start_span(op=op, description=description)
                sentry_span.__enter__()
            except Exception:
                pass

        try:
            yield span_data
        finally:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            span_data["elapsed_ms"] = round(elapsed_ms, 2)
            if sentry_span:
                try:
                    sentry_span.__exit__(None, None, None)
                except Exception:
                    pass
            logger.info(f"[Trace] {op} - {description} completed in {span_data['elapsed_ms']}ms")

tracer = SentryAgentTracer()
