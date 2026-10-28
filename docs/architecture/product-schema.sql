-- Portable SQLite-compatible target schema. The live site currently publishes
-- the same relations as versioned JSON snapshots; no database is provisioned.
PRAGMA foreign_keys = ON;
CREATE TABLE product (
 id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, gtin TEXT, brand TEXT NOT NULL,
 name TEXT NOT NULL, category TEXT, species TEXT, line TEXT, recipe TEXT,
 weight_g REAL CHECK(weight_g > 0), volume_ml REAL CHECK(volume_ml > 0),
 pieces INTEGER CHECK(pieces > 0), matching_method TEXT NOT NULL,
 matching_confidence REAL NOT NULL CHECK(matching_confidence BETWEEN 0 AND 1)
);
CREATE TABLE offer (
 id TEXT PRIMARY KEY, product_id TEXT NOT NULL REFERENCES product(id),
 shop_id TEXT NOT NULL, price_cents INTEGER NOT NULL CHECK(price_cents > 0),
 shipping_min_cents INTEGER CHECK(shipping_min_cents >= 0),
 available INTEGER NOT NULL CHECK(available IN(0,1)), merchant_url TEXT NOT NULL,
 last_seen TEXT NOT NULL, quantity_verified INTEGER NOT NULL CHECK(quantity_verified IN(0,1))
);
CREATE TABLE price_history (
 offer_id TEXT NOT NULL REFERENCES offer(id), price_cents INTEGER NOT NULL CHECK(price_cents > 0),
 observed_at TEXT NOT NULL, PRIMARY KEY(offer_id, observed_at)
);
CREATE INDEX offer_product_shop ON offer(product_id,shop_id);
CREATE INDEX product_gtin ON product(gtin);
-- Multiple offers in the same shop count as one shop.
CREATE VIEW product_coverage AS
 SELECT product_id,COUNT(DISTINCT shop_id) AS active_shops
 FROM offer WHERE available=1 AND quantity_verified=1
 AND datetime(last_seen)>=datetime('now','-36 hours') GROUP BY product_id;
