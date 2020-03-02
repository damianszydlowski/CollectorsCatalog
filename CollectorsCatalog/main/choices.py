# main/choices.py

from django.utils.translation import ugettext_lazy as _

BOOK_COVER_CHOICES = (
    ('S', _('Soft')),
    ('H', _('Hard'))
)

WATCH_MECHANISM_CHOICES = (
    ('Q', _('Qwartz (Battery)')),
    ('M', _('Manual (ETA)')),
)

STREET_CAR_MODEL_BODY_CHOICES = (
    ('W', _('Wagon')),
    ('S', _('Sedan')),
    ('H', _('Hatchback')),
    ('C', _('Coupe')),
    ('T', _('Pickup truck')),
    ('U', _('SUV')),
    ('X', _('Full-size truck')),
)

STREET_CAR_MODEL_ENGINE_TYPE_CHOICES = (
    ('I', _('Inline')),
    ('V', _('V')),
    ('W', _('W')),
    ('R', _('Rotary')),
    ('F', _('Flat')),
)

EVENT_TYPES = (
    ('R', _('Wyścig')),
    ('W', _('Rajd')),
    ('A', _('Wojenne')),
)

NOTIF_ADDED = 'ADDED'
NOTIF_PENDING = 'PENDING'
NOTIF_ACCEPTED = 'ACCEPTED'
NOTIF_WATCHED = 'WATCHED'

NOTIFICATION_TYPE_CHOICES = (
    (NOTIF_ADDED, _('added to his collection item:')),
    (NOTIF_ACCEPTED, _('Collectible added by you is accepted')),
    (NOTIF_WATCHED, _('added you to his watcn list')),
)