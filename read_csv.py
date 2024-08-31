import pandas as pd
# get all the values from the initial index
def get_category(category):
    df = pd.read_csv("Book1.csv")
    # print(dfs.columns)
    # usecols = [ "Fruits", "Vegetables", "Car Brands", "Anime"]
    # df = pd.read_csv("Book1.csv",usecols = usecols)
    
    #print(df["Fruits"])
    return df[category]

print(get_category("Fruits"))