import os
from dotenv import load_dotenv


load_dotenv()

# postgreSQL connection

POSTGRES_DB = os.getenv("POSTGRES_DB", "challenge")
POSTGRES_USER = os.getenv("POSTGRES_USER", "root")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "DataEngineer_2024")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5440"))

# source data 
SOURCE_XLSX_PATH = os.getenv("SOURCE_XLSX_PATH", "data/de_challenge_data.xlsx")
SHEET_NAME = os.getenv("SHEET_NAME", "FoodSales")

# target table 
TARGET_TABLE = os.getenv("TARGET_TABLE", "food sales")


def get_db_url():
    """SQLAlchemy connection URL: postgresql+psycopg2://user:pass@host:port/dbname"""
    return (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )