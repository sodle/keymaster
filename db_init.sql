DROP TABLE IF EXISTS uploaded_key CASCADE;
CREATE TABLE uploaded_key (
  upload_id int PRIMARY KEY,
  upload_time timestamp DEFAULT current_timestamp,
  public_key text,
  expire_time timestamp DEFAULT current_timestamp + interval '30 minutes'
);

DROP TABLE IF EXISTS installed_key CASCADE;
CREATE TABLE installed_key (
  install_id serial PRIMARY KEY,
  install_time timestamp DEFAULT current_timestamp,
  upload_id int REFERENCES uploaded_key(upload_id),
  install_site varchar(80),
  install_user_name varchar(80),
  install_key_name varchar(80),
  install_success int
);
