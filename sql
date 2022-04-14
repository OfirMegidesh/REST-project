CREATE TABLE "users" (
	"id_AI"	INTEGER,
	"full_name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"real_id"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_AI" AUTOINCREMENT)
);
CREATE TABLE "tickets" (
	"ticket_id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"flight_id"	INTEGER NOT NULL,
	PRIMARY KEY("ticket_id" AUTOINCREMENT),
	FOREIGN KEY("flight_id") REFERENCES "flights"("flight_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id_AI")
);
CREATE TABLE "flights" (
	"flight_id"	INTEGER,
	"timestamp"	DATETIME NOT NULL,
	"remaining_seats"	INTEGER NOT NULL,
	"origin_country_id"	INTEGER NOT NULL,
	"dest_country_id"	INTEGER NOT NULL,
	PRIMARY KEY("flight_id" AUTOINCREMENT),
	FOREIGN KEY("dest_country_id") REFERENCES "countries"("Code_AI"),
	FOREIGN KEY("origin_country_id") REFERENCES "countries"("code_AI"
);
CREATE TABLE "countries" (
	"Code_AI"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("Code_AI" AUTOINCREMENT)
);
