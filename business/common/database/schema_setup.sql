-- Database: pesaloop

-- DROP DATABASE IF EXISTS pesaloop;

CREATE DATABASE pesaloop
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE pesaloop TO PUBLIC;

GRANT ALL ON DATABASE pesaloop TO dbadmin;

GRANT ALL ON DATABASE pesaloop TO postgres;