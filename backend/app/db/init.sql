-- app/db/init.sql

-- Products (one row per ASIN)
CREATE TABLE IF NOT EXISTS products (
  asin              VARCHAR(20) PRIMARY KEY,
  title             VARCHAR(512),
  category          VARCHAR(128),
  brand             VARCHAR(128),
  bsr               INTEGER,
  buybox_price      DOUBLE PRECISION,
  fba_fees          DOUBLE PRECISION,
  referral_fee_pct  DOUBLE PRECISION,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Batches (named groups of ASINs you upload)
CREATE TABLE IF NOT EXISTS batches (
  id         SERIAL PRIMARY KEY,
  name       VARCHAR(128) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Items inside a batch
CREATE TABLE IF NOT EXISTS batch_items (
  id               SERIAL PRIMARY KEY,
  batch_id         INTEGER NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
  asin             VARCHAR(20) NOT NULL,
  cost             DOUBLE PRECISION,
  price            DOUBLE PRECISION,
  roi              DOUBLE PRECISION,
  profit_per_unit  DOUBLE PRECISION,
  risk_band        VARCHAR(16),
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_batch_items_batch_id ON batch_items(batch_id);
CREATE INDEX IF NOT EXISTS idx_batch_items_asin     ON batch_items(asin);
