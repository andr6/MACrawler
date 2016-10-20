# Malware-Analysis Crawler (CS3103 PROJECT)

## Requirements

- Python 2 (2.7.9 is used for development)
- `pip install -r requirements.txt`

## Running the crawler

    python crawler.py

## Setting up the environment for PostgreSQL (Linux only)

    1. In terminal: sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
	2. After installation: sudo -i -u postgres
	3. In #postgres: createuser group11 -P --interactive
	4. We set password as 12345 for now. Choose no, yes, yes
	5. createdb MACdb
	6. ctrl-d to exit postgres
	7. In terminal: sudo apt-get install python-psycopg2
	8. To import into crawler.py: from database import db

## Running the scanner to send results to VirusTotal

	python scanner.py

## Running the CLI to list results
	
	python vt-cli.py list

## Contributors:

- @ChengKeJing
- @digawp
- @jftoh
- @boxin
