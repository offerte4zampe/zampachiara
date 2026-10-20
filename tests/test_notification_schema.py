import sqlite3
import unittest
from pathlib import Path

class NotificationSchemaTests(unittest.TestCase):
    def test_confirmation_purpose_and_outbox_uniqueness(self):
        db=sqlite3.connect(':memory:')
        db.executescript((Path(__file__).parents[1]/'worker/schema/0001_notifications.sql').read_text())
        with self.assertRaises(sqlite3.IntegrityError):
            db.execute("INSERT INTO notification_consent VALUES ('test','price_alert','active','test','2026-10-20',NULL,NULL)")
        db.execute("INSERT INTO notification_consent VALUES ('test','newsletter','active','test','2026-10-20','2026-10-20',NULL)")
        with self.assertRaises(sqlite3.IntegrityError):
            db.execute("INSERT INTO price_alert (id,contact_ref,offer_id,offer_identity,threshold_cents) VALUES ('a','test','shop:1','identity',1000)")
        db.execute("INSERT INTO notification_consent VALUES ('test','price_alert','active','test','2026-10-20','2026-10-20',NULL)")
        db.execute("INSERT INTO price_alert (id,contact_ref,offer_id,offer_identity,threshold_cents) VALUES ('a','test','shop:1','identity',1000)")
        db.execute("INSERT INTO notification_outbox VALUES ('event','a','pending','2026-10-20',NULL)")
        with self.assertRaises(sqlite3.IntegrityError):
            db.execute("INSERT INTO notification_outbox VALUES ('event','a','pending','2026-10-20',NULL)")
        db.close()
