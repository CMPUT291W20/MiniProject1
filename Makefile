db:
	sqlite3 a2.db <a2-tables.sql
	sqlite3 a2.db <a2-data1.sql

output:
	sqlite3 a2.db <a2-tables.sql
	sqlite3 a2.db <a2-data1.sql
	sqlite3 a2.db <a2-queries.sql >a2-script.txt

clean:
	rm a2-script.txt
	rm a2.db
	if [-e mp1-script.txt]
	then
		rm mp1-script.txt
	fi