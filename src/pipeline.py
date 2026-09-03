import config
from extract import extract_food_sale
from load import load_food_sale


def run():
    print("Extracting...")
    df = extract_food_sale()
    print("  got", len(df), "rows")

    print("Loading...")
    n = load_food_sale(df)
    print("  wrote", n, "rows into", config.TARGET_TABLE)

    print("Done.")


if __name__ == "__main__":
    run()