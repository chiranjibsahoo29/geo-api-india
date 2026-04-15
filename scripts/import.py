import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATA_FOLDER = "../data"


def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    # CSV file
    if ext == ".csv":
        return pd.read_csv(
            file_path,
            sep=None,
            engine="python",
            encoding="latin1",
            on_bad_lines="skip"
        )


    elif ext == ".xls":
        xls = pd.ExcelFile(file_path, engine="xlrd")
        if "Village Directory" in xls.sheet_names:
            return pd.read_excel(file_path, engine="xlrd", sheet_name="Village Directory")
        else:
            return pd.read_excel(file_path, engine="xlrd", sheet_name=0)


    elif ext == ".xlsx":
        xls = pd.ExcelFile(file_path, engine="openpyxl")
        if "Village Directory" in xls.sheet_names:
            return pd.read_excel(file_path, engine="openpyxl", sheet_name="Village Directory")
        else:
            return pd.read_excel(file_path, engine="openpyxl", sheet_name=0)

    else:
        raise ValueError(f"Unsupported file format: {file_path}")


conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


cur.execute("""
INSERT INTO country (name) VALUES ('India')
ON CONFLICT DO NOTHING;
""")
conn.commit()

cur.execute("SELECT id FROM country WHERE name='India';")
country_id = cur.fetchone()[0]

for filename in os.listdir(DATA_FOLDER):
    if not filename.lower().endswith((".csv", ".xls", ".xlsx")):
        continue

    file_path = os.path.join(DATA_FOLDER, filename)
    print(f"\n Processing: {filename}")

    try:
        df = load_file(file_path)

        df.columns = df.columns.str.strip().str.upper()

        df = df.rename(columns={
            "MDDS STC": "stc",
            "STATE NAME": "state",
            "MDDS DTC": "dtc",
            "DISTRICT NAME": "district",
            "MDDS SUB_DT": "subdt",
            "SUB-DISTRICT NAME": "subdistrict",
            "MDDS PLCN": "plc",
            "AREA NAME": "village",
            "AREA NAME.": "village"
        })

        required_cols = ["state", "stc", "district", "dtc", "subdistrict", "subdt", "plc", "village"]
        missing = [c for c in required_cols if c not in df.columns]

        if missing:
            print(f" Skipped {filename} | Missing columns: {missing}")
            continue

        df = df[required_cols]
        df = df.dropna()
        df = df.drop_duplicates()

        print(" Clean rows:", len(df))


        states = df[['state', 'stc']].drop_duplicates().values.tolist()

        execute_values(cur, """
            INSERT INTO state (name, code, country_id)
            VALUES %s
            ON CONFLICT DO NOTHING;
        """, [(s[0], str(s[1]), country_id) for s in states])

        conn.commit()

        cur.execute("SELECT id, name FROM state;")
        state_map = {name: id for id, name in cur.fetchall()}


        districts = df[['district', 'dtc', 'state']].drop_duplicates()

        district_data = [
            (row['district'], str(row['dtc']), state_map[row['state']])
            for _, row in districts.iterrows()
        ]

        execute_values(cur, """
            INSERT INTO district (name, code, state_id)
            VALUES %s
            ON CONFLICT DO NOTHING;
        """, district_data)

        conn.commit()

        cur.execute("SELECT id, name FROM district;")
        district_map = {name: id for id, name in cur.fetchall()}


        subdistricts = df[['subdistrict', 'subdt', 'district']].drop_duplicates()

        sub_data = [
            (row['subdistrict'], str(row['subdt']), district_map[row['district']])
            for _, row in subdistricts.iterrows()
        ]

        execute_values(cur, """
            INSERT INTO subdistrict (name, code, district_id)
            VALUES %s
            ON CONFLICT DO NOTHING;
        """, sub_data)

        conn.commit()

        cur.execute("SELECT id, name FROM subdistrict;")
        sub_map = {name: id for id, name in cur.fetchall()}

        
        village_data = [
            (row['village'], str(row['plc']), sub_map[row['subdistrict']])
            for _, row in df.iterrows()
        ]

        execute_values(cur, """
            INSERT INTO village (name, code, subdistrict_id)
            VALUES %s
            ON CONFLICT DO NOTHING;
        """, village_data, page_size=10000)

        conn.commit()

        print(f" DONE: {filename}")

    except Exception as e:
        conn.rollback()
        print(f" Error in {filename}: {e}")


cur.execute("SELECT COUNT(*) FROM state;")
print("\nSTATE ", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM district;")
print("DISTRICT ", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM subdistrict;")
print("SUBDISTRICT ", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM village;")
print("VILLAGE ", cur.fetchone()[0])

cur.close()
conn.close()

print("\n ALL  FILES IMPORTED ")