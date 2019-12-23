BEGIN;

CREATE TABLE Users(
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

CREATE TABLE Statistics(
  query varchar primary key,
  name varchar not null,
  columns varchar[] not null
);

CREATE TABLE Week_El(
  day integer,
  month integer,
  year integer,
  hour integer,
  watt integer not null,
  primary key (day, month, year, hour)
);

CREATE TABLE Week_G(
  day integer,
  month integer,
  year integer,
  hour integer,
  liters integer not null,
  primary key (day, month, year, hour)
);

CREATE TABLE Week_S0(
  day integer,
  month integer,
  year integer,
  hour integer,
  watt integer not null,
  primary key (day, month, year, hour)
);

CREATE TABLE Year_El(
  day integer,
  month integer,
  year integer,
  watt integer not null,
  primary key (day, month, year)
);

CREATE TABLE Year_G(
  day integer,
  month integer,
  year integer,
  liters integer not null,
  primary key (day, month, year)
);

CREATE TABLE Year_S0(
  day integer,
  month integer,
  year integer,
  watt integer not null,
  primary key (day, month, year)
);

COMMIT;