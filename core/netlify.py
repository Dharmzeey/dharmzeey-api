"""Trigger a Netlify rebuild when public content changes.

Set NETLIFY_BUILD_HOOK_URL in the environment (Site configuration →
Build & deploy → Build hooks on Netlify). If unset, this is a no-op,
so dev environments are unaffected.
"""
import logging
import os
import threading
import urllib.request

from django.db import transaction
from django.db.models.signals import post_delete, post_save

logger = logging.getLogger(__name__)

# Collapse bursts of saves (e.g. seed.py, bulk admin actions) into one build.
DEBOUNCE_SECONDS = 10

_lock = threading.Lock()
_timer = None


def _fire():
    url = os.getenv("NETLIFY_BUILD_HOOK_URL")
    if not url:
        return
    try:
        req = urllib.request.Request(url, data=b"", method="POST")
        urllib.request.urlopen(req, timeout=10)
        logger.info("Triggered Netlify build hook")
    except Exception:
        logger.exception("Failed to trigger Netlify build hook")


def _schedule(**kwargs):
    if not os.getenv("NETLIFY_BUILD_HOOK_URL"):
        return

    def start_timer():
        global _timer
        with _lock:
            if _timer is not None:
                _timer.cancel()
            _timer = threading.Timer(DEBOUNCE_SECONDS, _fire)
            _timer.daemon = True
            _timer.start()

    transaction.on_commit(start_timer)


def watch(*models):
    """Rebuild the frontend whenever any of these models is saved or deleted."""
    for model in models:
        post_save.connect(_schedule, sender=model, weak=False)
        post_delete.connect(_schedule, sender=model, weak=False)
