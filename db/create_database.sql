CREATE ROLE youlessadmin WITH LOGIN PASSWORD 'admin';
ALTER ROLE youlessadmin CREATEDB;
ALTER ROLE youlessadmin SUPERUSER;
CREATE DATABASE youlessmonitor owner youlessadmin;
