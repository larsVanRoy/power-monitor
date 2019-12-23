PGPASSWORD=postgres psql -d postgres -U postgres -f ./create_database.sql
PGPASSWORD=admin psql -d YouLessMonitor -U YouLessAdmin -f ./schema.sql