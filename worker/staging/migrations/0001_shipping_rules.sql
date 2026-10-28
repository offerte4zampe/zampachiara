-- Prepared for staging. No D1 binding or remote migration is activated.
PRAGMA foreign_keys = ON;
CREATE TABLE shop (
 id TEXT PRIMARY KEY, name TEXT NOT NULL
);
CREATE TABLE shipping_rule (
 id INTEGER PRIMARY KEY,
 shop_id TEXT NOT NULL REFERENCES shop(id),
 zone TEXT NOT NULL DEFAULT 'IT',
 std_cents INTEGER CHECK(std_cents IS NULL OR (typeof(std_cents)='integer' AND std_cents>=0)),
 free_from_cents INTEGER CHECK(free_from_cents IS NULL OR (typeof(free_from_cents)='integer' AND free_from_cents>=0)),
 threshold_mode TEXT NOT NULL DEFAULT 'unknown' CHECK(threshold_mode IN ('inclusive','exclusive','unknown')),
 max_weight_g INTEGER CHECK(max_weight_g IS NULL OR (typeof(max_weight_g)='integer' AND max_weight_g>0)),
 over_weight_note TEXT,
 status TEXT NOT NULL CHECK(status IN ('verified','uncertain','unknown')),
 source_url TEXT, notes TEXT,
 verified_at TEXT NOT NULL, verified_until TEXT NOT NULL,
 valid_from TEXT NOT NULL, valid_to TEXT,
 UNIQUE(shop_id,zone,valid_from),
 CHECK(julianday(verified_at) IS NOT NULL AND julianday(verified_until) IS NOT NULL AND julianday(verified_until)>=julianday(verified_at)),
 CHECK(julianday(valid_from) IS NOT NULL),
 CHECK(valid_to IS NULL OR (julianday(valid_to) IS NOT NULL AND julianday(valid_to)>julianday(valid_from))),
 CHECK(status='verified' OR (std_cents IS NULL AND free_from_cents IS NULL)),
 CHECK(status!='verified' OR std_cents IS NOT NULL)
);
CREATE INDEX idx_ship_shop ON shipping_rule(shop_id,zone,valid_from DESC,valid_to);

-- Reject overlaps with already-staged rows as well as within generated batches.
CREATE TRIGGER shipping_rule_no_overlap_insert BEFORE INSERT ON shipping_rule
WHEN EXISTS (SELECT 1 FROM shipping_rule r WHERE r.shop_id=new.shop_id AND r.zone=new.zone
 AND r.valid_from!=new.valid_from
 AND (r.valid_to IS NULL OR julianday(new.valid_from)<julianday(r.valid_to))
 AND (new.valid_to IS NULL OR julianday(r.valid_from)<julianday(new.valid_to)))
BEGIN SELECT RAISE(ABORT,'overlapping shipping rules'); END;
CREATE TRIGGER shipping_rule_no_overlap_update BEFORE UPDATE ON shipping_rule
WHEN EXISTS (SELECT 1 FROM shipping_rule r WHERE r.id!=old.id AND r.shop_id=new.shop_id AND r.zone=new.zone
 AND (r.valid_to IS NULL OR julianday(new.valid_from)<julianday(r.valid_to))
 AND (new.valid_to IS NULL OR julianday(r.valid_from)<julianday(new.valid_to)))
BEGIN SELECT RAISE(ABORT,'overlapping shipping rules'); END;
