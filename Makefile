db:
	sqlite3 mp1.db <tables.sql
	sqlite3 mp1.db <data.sql

output:
	sqlite3 mp1.db <tables.sql
	sqlite3 mp1.db <data.sql
	sqlite3 mp1.db <mp1-queries.sql >mp1-script.txt

clean:
	rm mp1.db
	if [-e mp1-script.txt]
	then
		rm mp1-script.txt
	fi