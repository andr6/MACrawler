# Malware-Analysis Crawler (CS3103 PROJECT)

## Requirements

- Python 2 (2.7.9 is used for development)
- `pip install -r requirements.txt` (may need `sudo`)
- PostgreSQL

## Setting up the environment for PostgreSQL (Linux only)

    1. In terminal: sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
	2. After installation: sudo -i -u postgres
	3. In #postgres: createuser group11 -P --interactive
	4. We set password as 12345 for now. Choose no, yes, yes
	5. createdb MACdb
	6. ctrl-d to exit postgres
	7. In terminal: sudo apt-get install python-psycopg2

## Running

1. Refresh db (DROP all tables and fill in queue table with seed).

	# Note: run this script once before running anything if the db schema is modified
	python utils.py

2. Run the crawler

    python crawler.py

3. Run the scanner to send results to VirusTotal

	python scanner.py

4. Run the retriever to retriver scan results to VirusTotal

	python retriever.py

## Running the Flask GUI

	export FLASK_APP=macrawler.py && flask run

## Contributors:

- @ChengKeJing
- @digawp
- @jftoh
- @greed-is-good
