db:
	sqlite3 mp1.db <tables.sql
	sqlite3 mp1.db <prj-data.sql

output:
	sqlite3 mp1.db <tables.sql
	sqlite3 mp1.db <prj-data.sql
	sqlite3 mp1.db <mp1_queries.sql >mp1-script.txt

clean:
	rm mp1.db
	if [-e mp1-script.txt]
	then
		rm mp1-script.txt
	fi