from pathlib import Path

import pandas as pd
import os

abs_path = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)
parent_path = Path(dir_path).parent
db_base_location = os.path.join(parent_path, "static\\db")


def get_db_from_csv_to_json(_db_name: str):
    _db_path = os.path.join(db_base_location, _db_name + ".csv")
    if os.path.exists(_db_path):
        _db = pd.read_csv(_db_path, index_col=False)
        return _db.loc[_db["enabled"]].to_dict(orient="records")
