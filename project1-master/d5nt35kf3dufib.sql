-- Adminer 4.6.3-dev PostgreSQL dump

\connect "d5nt35kf3dufib";

DROP TABLE IF EXISTS "locations";
DROP SEQUENCE IF EXISTS location_location_id_seq;
CREATE SEQUENCE location_location_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."locations" (
    "location_id" integer DEFAULT nextval('location_location_id_seq') NOT NULL,
    "zip_code" character varying(64) NOT NULL,
    "city" character varying(64) NOT NULL,
    "state" character varying(64) NOT NULL,
    "latitude" character varying(64) NOT NULL,
    "longitude" character varying(64) NOT NULL,
    "population" character varying(64) NOT NULL,
    "review" character(1024)
) WITH (oids = false);


DROP TABLE IF EXISTS "states";
DROP SEQUENCE IF EXISTS state_state_id_seq;
CREATE SEQUENCE state_state_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."states" (
    "state_id" integer DEFAULT nextval('state_state_id_seq') NOT NULL,
    "full_name" character varying(64) NOT NULL,
    "abbreviation" character(2) NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS "Users_user_id_seq";
CREATE SEQUENCE "Users_user_id_seq" INCREMENT  MINVALUE  MAXVALUE  START 1 CACHE ;

CREATE TABLE "public"."users" (
    "user_id" integer DEFAULT nextval('"Users_user_id_seq"') NOT NULL,
    "username" character varying NOT NULL,
    "password" character varying NOT NULL,
    "first_name" character varying NOT NULL,
    "last_name" character varying NOT NULL
) WITH (oids = false);


-- 2018-07-12 21:48:45.827072+00
