-- ============================================
-- Chicken Kitchen HR — Supabase Migration
-- Paste this into: Supabase Dashboard > SQL Editor > New Query > Run
-- ============================================

-- 1. Verification codes
CREATE TABLE IF NOT EXISTS verifications (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email       TEXT NOT NULL,
    code        TEXT NOT NULL,
    sent_at     TIMESTAMPTZ DEFAULT now(),
    verified_at TIMESTAMPTZ,
    ip_address  TEXT
);

CREATE INDEX idx_verifications_email ON verifications (email, sent_at DESC);

-- 2. Applications
CREATE TABLE IF NOT EXISTS applications (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email           TEXT NOT NULL,
    name            TEXT NOT NULL,
    phone           TEXT,
    store_code      TEXT NOT NULL,
    store_name      TEXT NOT NULL,
    status          TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    signature_b64   TEXT,
    admin_token     TEXT UNIQUE,
    created_at      TIMESTAMPTZ DEFAULT now(),
    approved_at     TIMESTAMPTZ,
    approved_by     TEXT
);

CREATE INDEX idx_applications_store ON applications (store_code, status);
CREATE INDEX idx_applications_token ON applications (admin_token);

-- 3. Documents (PDFs + identity uploads)
CREATE TABLE IF NOT EXISTS documents (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    application_id  UUID REFERENCES applications(id) ON DELETE CASCADE,
    filename        TEXT NOT NULL,
    doc_type        TEXT NOT NULL,
    file_b64        TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_documents_app ON documents (application_id);

-- 4. Row-Level Security (public read/write via anon key for now)
ALTER TABLE verifications  ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications   ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents      ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all verifications"  ON verifications  FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all applications"   ON applications   FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all documents"      ON documents      FOR ALL USING (true) WITH CHECK (true);
