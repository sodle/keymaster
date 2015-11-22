DROP TABLE IF EXISTS uploaded_key CASCADE;
CREATE TABLE uploaded_key (
  upload_id SERIAL,
  upload_time timestamp DEFAULT current_timestamp,
  public_key text,
  expire_time timestamp DEFAULT current_timestamp + interval '30 minutes'
);
