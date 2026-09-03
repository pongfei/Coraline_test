import pandas as pd
from sqlalchemy import create_engine
import config

def load_food_sale(df):

    #open connection
    engine = create_engine(config.get_db_url())

    #write the rows into table (if exist -> replace, dont store pandas row as a col)
    df.to_sql(config.TARGET_TABLE, engine, if_exists="replace", index=False)

    #return how many rows
    return len(df)

if __name__ == "__main__":
    from extract import extract_food_sale

    df = extract_food_sale()
    row_count = load_food_sale(df)
    print("Loaded", row_count, "rows into", config.TARGET_TABLE)