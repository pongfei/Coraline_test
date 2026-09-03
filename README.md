# Coraline Data Engineering Challenge

This project loads the `FoodSales` sheet from `de_challenge_data.xlsx` into a
PostgreSQL table (all years together), and then creates a summary table `cat_reg`
with the total price per category for each region.

It can be run as a normal Python script, or through an Airflow DAG.

## Tech used

- Python (pandas, SQLAlchemy, psycopg2)
- PostgreSQL (in Docker)
- Apache Airflow (in Docker) for scheduling/orchestration
- Docker Compose to run everything

## Requirements

- Docker Desktop
That's the only thing you need installed. 
Python and PostgreSQL run inside Docker.

## Setup

Copy the example env file:

```bash
cp .env.example .env
```

The values already match the challenge (`challenge` / `root` / `DataEngineer_2024`).

Note: `POSTGRES_PORT` is set to `5440` instead of `5432`, because my machine
already had PostgreSQL running on 5432 and 5433. If 5440 is also used on your
machine, just change it in `.env`.

## How to run with Airflow

Start everything:

```bash
docker compose up -d
```
You can check the logs with:

```bash
docker compose logs -f airflow
```

Press Ctrl+C to stop watching
(the container keeps running).

Then:

- Go to http://localhost:8080
- Login user is `admin`. Get the password with:
  ```bash
  docker compose exec airflow cat /opt/airflow/standalone_admin_password.txt
  ```
- Turn on the `food_sales_dag` (switch on the left).
- Click the play button to run it.
- Open the Graph view and check that `ingest` and `build_cat_reg` both turn green.


## How to run without Airflow

Start only the database:

```bash
docker compose up -d postgres
pip install -r requirements.txt
```

Run the pipeline:

```bash
python src/pipeline.py
```

Then run the SQL script to build `cat_reg`

```bash
docker compose exec -T postgres psql -U root -d challenge < sql/create_cat_reg.sql
```

## How to check the result

```bash
docker compose exec postgres psql -U root -d challenge -c 'SELECT COUNT(*) FROM "food sales";'
docker compose exec postgres psql -U root -d challenge -c 'SELECT * FROM cat_reg;'
```

You should get 244 rows in `food sales`, and this in `cat_reg`

```
  Category   | East  | West  | Grand Total
-------------+-------+-------+-------------
 Bars        |  6355 |  4180 |       10536
 Cookies     | 10684 |  6529 |       17212
 Crackers    |  3026 |   314 |        3340
 Snacks      |  1460 |   778 |        2238
 Grand Total | 21525 | 11801 |       33326
```

## Configuration

All settings are in the `.env` file, nothing is hard-coded:

| Variable | Default | What it is |
|----------|---------|------------|
| POSTGRES_DB | challenge | database name |
| POSTGRES_USER | root | database user |
| POSTGRES_PASSWORD | DataEngineer_2024 | database password |
| POSTGRES_HOST | localhost | host (the Airflow container uses `postgres`) |
| POSTGRES_PORT | 5440 | port on the host machine |
| SOURCE_XLSX_PATH | data/de_challenge_data.xlsx | the Excel file |
| SHEET_NAME | FoodSales | sheet to read |
| TARGET_TABLE | food sales | table to load into |

## Project structure

```
.
├── docker-compose.yml      # postgres + airflow
├── .env / .env.example     # configuration
├── requirements.txt
├── data/
│   └── de_challenge_data.xlsx
├── src/
│   ├── config.py           # reads the .env values
│   ├── extract.py          # read the Excel file and clean it
│   ├── load.py             # load the data into PostgreSQL
│   └── pipeline.py         # runs extract then load
├── sql/
│   └── create_cat_reg.sql  # creates the cat_reg table
└── dags/
    └── food_sales_dag.py   # Airflow DAG (ingest -> build_cat_reg), runs daily
```

## Notes

- The `FoodSales` sheet has two tables stacked on top of each other, each with its
  own header row and a year label, split by an empty row. The second year label
  says `2022` but the data under it is actually 2023. Because of this, `extract.py`
  reads the sheet with no header and keeps only the rows where the first column
  looks like an ID (`ID` + numbers), which skips all the header/label/blank rows.
- The data is only ~244 rows, so pandas is enough. Spark would be overkill here.
- The pipeline can be run multiple times without breaking: `load.py` uses
  `if_exists="replace"` and the SQL script uses `DROP TABLE IF EXISTS`.
- Airflow is set up with `SequentialExecutor` and `standalone` mode to keep it
  simple (no Celery or Redis, which aren't needed for this).
- `cat_reg` values are rounded to whole numbers to match the challenge document.

## Things I would improve with more time

- Use a custom Dockerfile for Airflow instead of installing libraries on startup.
- Add a check for row count / nulls before loading.
- Add unit tests for `extract.py`.
