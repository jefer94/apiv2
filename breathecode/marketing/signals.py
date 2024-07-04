"""
For each signal you want other apps to be able to receive, you have to
declare a new variable here like this:
"""

from django.dispatch import Signal

downloadable_saved = Signal()

form_entry_won_or_lost = Signal()
new_form_entry_deal = Signal()
