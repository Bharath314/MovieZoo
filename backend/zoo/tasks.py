import csv
import os

from flask import render_template
from jinja2 import Template

from zoo.models import User, Booking
from zoo.worker import celery_app
from zoo.cache import get_venue, get_shows_by_venue
from zoo.email import send_email

@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0,
        send_daily_reminder.s(),
        name='Daily Reminder'
    )

@celery_app.task()
def export_venue_csv(venue_id):
    venue = get_venue(venue_id)
    venue_shows = get_shows_by_venue(venue_id)
    address = "admin@moviezoo.com"
    subject = f"{venue['name']} details"

    with open("venue_analytics.csv", "w", newline='') as f:
        f = csv.writer(f, delimiter=',')
        f.writerow(['show_id', 'movie_id', 'movie_name', 'tickets_booked'])
        for show in venue_shows:
            f.writerow([show['id'], show['movie_id'], show['movie'], show['tickets_booked']])

    template_str = """
<p>Dear Admin, </p>
<br />
<p>
    Find the requested CSV report for {{ venue['name'] }}. Please bear in mind that this data is strictly confidential and is not be shared.
</p>
<br />
<p>
<em>This is an automatically generated email</em>
</p>
"""
    file = open("venue_analytics.csv", "rb")
    message = Template(template_str).render(venue=venue)
    send_email(address, subject, message, attachment=file, filename="venue_analytics.csv", subtype='csv')
    os.remove("venue_analytics.csv")

@celery_app.task()
def send_daily_reminder():
    template_str = """
<p>
    Dear Viewer,
</p>
<br />
<p>
    Looks like you haven't watched anything! Don't miss out on amazing experiences and book now!
</p>
<p>
    Happy Viewing,
    MovieZoo
</p>
"""
    users = User.query.all()
    bookings = Booking.query.all()

    booked_users = set()
    for booking in bookings:
        booked_users.add(booking.user_id)
    
    non_booked_users = set()
    for user in users:
        if user.id != 1 and user.id not in booked_users:
            message = Template(template_str).render()
            address = user.email
            subject = f"Do not miss out on entertainment!"

            send_email(address, subject, message)
    
    
