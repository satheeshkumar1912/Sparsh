"""Form notification email helpers.

This module must stay free of Django imports at import time so settings can
load ``resolve_smtp_security`` while Django is still starting.
"""
import logging

logger = logging.getLogger(__name__)


def resolve_smtp_security(port, use_ssl, use_tls):
    """Return (use_ssl, use_tls) for Django's SMTP backend.

    Port 465 is implicit SSL. Django rejects connections when both
    EMAIL_USE_SSL and EMAIL_USE_TLS are true, so TLS is forced off on 465.
    """
    try:
        port = int(port)
    except (TypeError, ValueError):
        port = 465
    use_ssl = bool(use_ssl)
    use_tls = bool(use_tls)
    if port == 465:
        return True, False
    if use_ssl and use_tls:
        return True, False
    return use_ssl, use_tls


def send_form_notification(*, subject, body, recipient, kind, record_id):
    """Send a staff notification. Return True only when the backend accepts it.

    A failure is logged without the message body or any credential. The caller
    should keep the saved database row either way.
    """
    from django.conf import settings
    from django.core.mail import send_mail

    recipient = (recipient or "").strip()
    if not recipient:
        logger.error(
            "%s notification skipped: no recipient configured (record_id=%s)",
            kind,
            record_id,
        )
        return False
    try:
        sent = send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "%s notification email failed (record_id=%s)",
            kind,
            record_id,
        )
        return False
    if sent < 1:
        logger.error(
            "%s notification email was not accepted by the mail backend (record_id=%s)",
            kind,
            record_id,
        )
        return False
    return True
