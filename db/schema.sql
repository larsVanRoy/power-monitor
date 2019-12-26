BEGIN;

CREATE TABLE users(
  name varchar primary key,
  password varchar not null,
  ip varchar,
  start date,
  price varchar,
  kwhprice varchar not null,
  id serial not null,
  gasprice varchar not null,
  track_g boolean not null,
  track_el boolean not null,
  track_s0 boolean not null
);

CREATE TABLE statistics(
  name varchar primary key,
  query varchar not null
);

CREATE TABLE week_el(
  day integer,
  month integer,
  year integer,
  hour integer,
  watt integer not null,
  primary key (day, month, year, hour)
);

CREATE TABLE week_g(
  day integer,
  month integer,
  year integer,
  hour integer,
  liters integer not null,
  primary key (day, month, year, hour)
);

CREATE TABLE week_s0(
  day integer,
  month integer,
  year integer,
  hour integer,
  watt integer not null,
  primary key (day, month, year, hour)
);

CREATE TABLE year_el(
  day integer,
  month integer,
  year integer,
  watt integer not null,
  primary key (day, month, year)
);

CREATE TABLE year_g(
  day integer,
  month integer,
  year integer,
  liters integer not null,
  primary key (day, month, year)
);

CREATE TABLE year_s0(
  day integer,
  month integer,
  year integer,
  watt integer not null,
  primary key (day, month, year)
);

COMMIT;