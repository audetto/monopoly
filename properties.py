import pandas as pd


def get_properties():
    file_name = "properties.csv"
    df = pd.read_csv(file_name)
    return df
