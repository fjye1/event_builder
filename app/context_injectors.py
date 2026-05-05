from app.models import EventStatus

BOOTSTRAP_CLASS = {
    EventStatus.generated: "status--generated",
    EventStatus.pending: "status--pending",
    EventStatus.confirmed: "status--confirmed",
    EventStatus.cancelled: "status--cancelled",
}

def inject_status_colours():
    result = {
        "STATUS_COLOURS": {status.value: cls for status, cls in BOOTSTRAP_CLASS.items()}
    }

    return result