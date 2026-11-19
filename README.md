# DSE Screener Platform

A learning project: a data pipeline and API for Dhaka Stock Exchange (DSE) prices. It loads historical and daily prices into PostgreSQL, scores stocks, backtests strategies, and serves the results through a FastAPI app.

**Status:** early development. So far there's a PostgreSQL database in Docker, a small FastAPI app, and a script that downloads the first price dataset.

## Stack
Python, FastAPI, PostgreSQL (Docker), SQLAlchemy, Alembic, dbt, pytest.

## Run it locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # then set a real password in .env
docker run --name dse-pg -e POSTGRES_PASSWORD=<your password> \
  -p 127.0.0.1:5432:5432 -v dse-pg-data:/var/lib/postgresql/data -d postgres:16
docker exec dse-pg psql -U postgres -c "CREATE DATABASE dse;"

python -m uvicorn app.main:app --reload
```
Then open http://127.0.0.1:8000/docs.

## Download the data
```bash
python scripts/download_data.py
```
Downloads the Mendeley price file (about 73 MB) into `data/raw/`. It skips the download if the file is already there with the right size, and checks the size again after downloading.

## Data
Historical prices come from open datasets (for example the [Mendeley DSE dataset](https://data.mendeley.com/datasets/5mww8rb9td/1), CC BY 4.0). Raw files are not stored in this repo; the script above downloads them into `data/raw/`.
