-- Prepared only; no remote database or binding is created by this repository.
-- Email addresses stay at the provider; no subscriber export or message body here.
PRAGMA foreign_keys = ON;
CREATE TABLE notification_consent (
  contact_ref TEXT NOT NULL,
  purpose TEXT NOT NULL CHECK (purpose IN ('newsletter','price_alert')),
  status TEXT NOT NULL CHECK (status IN ('pending','active','withdrawn')),
  notice_version TEXT NOT NULL,
  recorded_at TEXT NOT NULL,
  confirmed_at TEXT,
  withdrawn_at TEXT,
  PRIMARY KEY (contact_ref,purpose),
  CHECK (status != 'active' OR (confirmed_at IS NOT NULL AND withdrawn_at IS NULL)),
  CHECK (status != 'pending' OR confirmed_at IS NULL),
  CHECK (status != 'withdrawn' OR withdrawn_at IS NOT NULL)
);
CREATE TABLE price_alert (
  id TEXT PRIMARY KEY,
  contact_ref TEXT NOT NULL,
  purpose TEXT NOT NULL DEFAULT 'price_alert' CHECK (purpose = 'price_alert'),
  offer_id TEXT NOT NULL,
  offer_identity TEXT NOT NULL,
  threshold_cents INTEGER NOT NULL CHECK (threshold_cents BETWEEN 1 AND 100000000),
  last_price_cents INTEGER CHECK (last_price_cents > 0),
  last_observed_at TEXT,
  FOREIGN KEY (contact_ref,purpose) REFERENCES notification_consent(contact_ref,purpose) ON DELETE CASCADE
);
CREATE TABLE notification_outbox (
  event_key TEXT PRIMARY KEY,
  alert_id TEXT NOT NULL REFERENCES price_alert(id) ON DELETE CASCADE,
  status TEXT NOT NULL CHECK (status IN ('pending','cancelled','sent')),
  created_at TEXT NOT NULL,
  delivered_at TEXT,
  CHECK (status != 'sent' OR delivered_at IS NOT NULL)
);
