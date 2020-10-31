import pandas as pd
def read_as_dataframe(file):
    df = pd.read_csv(file)
    print(df)
    return df
def visually_inspect(df):
    print(df.head())
    print(df.tail())
    print(df.column())
    print(df.shape())
    print(df.info())
    print(df.describe())
    print(df['major'].value_counts(dropna=False)
    print(df['median'].value_counts(dropna=False)
    print(df['unemployment'].value_counts(dropna=False)
def cleaning(df):
    df['major'] = df['major'].astype(str)
    df['median'] = df['median'].astype(int)
    df['unemployment'] = df['unemployment'].astype(int)
    return df
def main():
    df = read_as_dataframe(all_ages.csv)
    visually_inspect(df)
    cleaning(df)
main()