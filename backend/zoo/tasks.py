from zoo.worker import celery_app
from zoo.cache import get_venue
from zoo.email import send_email

@celery_app.task()
def export_venue_csv(venue_id):
    venue = get_venue(venue_id)
    address = "admin@moviezoo.com"
    subject = f"{venue['name']} details"
    message = "Test"
    send_email(address, subject, message, attachment=None, filename=None, subtype=None)
