import pandas as pd
import config


# use config.py's values when the caller doesn't pass its own
def extract_food_sale(path=None, sheet_name=None):
    if path is None:
        path = config.SOURCE_XLSX_PATH
    if sheet_name is None:
        sheet_name = config.SHEET_NAME

    # row 0 is the "2022" label, row 1 is the real header
    df = pd.read_excel(path, sheet_name=sheet_name, header=1)

    # drops the blank row "2022"
    # label row, and the repeated header row further down the sheet
    first_col = df["ID"].astype(str)
    df = df[first_col.str.startswith("ID") & (first_col != "ID")]
    df = df.reset_index(drop=True)

    # fix data types
    df["Date"] = pd.to_datetime(df["Date"])
    df["Qty"] = pd.to_numeric(df["Qty"]).astype(int)
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"])
    df["TotalPrice"] = pd.to_numeric(df["TotalPrice"])

    return df


if __name__ == "__main__":
    df = extract_food_sale()
    print(df.shape)
    print(df.dtypes)
    print(df["Date"].dt.year.value_counts())
