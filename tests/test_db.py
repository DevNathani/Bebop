from bebop.core.history.db import init_db
from bebop.core.history.devices import get_devices
from bebop.core.history.received_files import get_received_history
from bebop.core.history.sent_files import get_sent_history

init_db()
print("\nDEVICES")
print(get_devices())

print("\nSENT")
print(get_sent_history())

print("\nRECEIVED")
print(get_received_history())
