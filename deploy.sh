if [ ! -e data/database.db ]; then
	touch data/database.db;
fi;

source bin/activate
python application.py
