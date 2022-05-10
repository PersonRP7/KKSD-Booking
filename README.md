# KKSD-Booking

It allows the users to request a booking which is then sent to the administrator. 
Backend logic written in Python performs both the admin and user input verification
to make sure no double booking occurs.

A secondary service implemented using django management commands and pythonanywhere's
scheduling functionality periodically cleans the database of expired bookings.
