#the table will be returned in a list of dataframe,for working with dataframe you need pandas
import pandas as pd
import os

statements = r'/Users/quiana/Documents/PersonalFinances/accounting 2.0/statements'

groceriesKey = ["trader joe's", "ralphs", "vons", "myprotein"]
housingKey =   ["premiere", "canyon park", "time warner", "sd gas", "wifi", "rent"]
gasKey = ["rotten robbie", "7-eleven", "raley's", "valero", "chevron", "arco", "shell", "stars & stripes"]
necesitiesKey = ["bookstore", "walmart", "toyota", "cvs", "cyclery"]
adventuresKey = ["rei", "mesa", "recreation"]
funFoodKey = ["fairbanks", "hdh", "bombay coast", "restaurants"]
giftsKey = ["gofundme", "wpy"]
shoppingKey = ["marshalls", "ross", "nordstrom"]
entertainmentKey = ["cinemas"]
incomeKey = ["pasqual", "ucsd apach", "ucsd payrl", "asml", "interest", "deposit"]

keys = [groceriesKey, housingKey, gasKey, necesitiesKey, adventuresKey, funFoodKey, giftsKey, shoppingKey, entertainmentKey, incomeKey]

print(len(keys))

# venmo sorter
# def venmo(file):
    
# debit sorter
def debit(file):
    # date, source, description, income, unknown, notes = [], [], [], [], [], []
    # groceries, housing, gas, necesities, adventure, funFood, gifts, shopping, entertainment, other = [], [], [], [], [], [], [], [], []
    df = pd.read_csv(statements+"/"+file, header=None)
    print(df.head())
    df[4] = df[4].str.lower()
    print(df.head())
    outTable = pd.DataFrame(0,index=range(len(df.index)-1), columns=['Date', 'Source', 'Description', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Notes'])
    skip=["venmo", "discover e-payment"]
    for iRow, row in df.iterrows():
        found = False
        print(row[4])
        outTable['Date'][iRow] = row[0]
        outTable['Source'][iRow] = 'debit'
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row[4]:
                    outTable['Description'][iRow] = key
                    outTable[[c+3]][iRow] = row[1]
                    found = True
        if not found:
            outTable['Unknown'][iRow] = row[1]
            outTable['Notes'][iRow] = row[4]
    for iRow, row in outTable.iterrows():
        for x in skip:
        
    print(outTable.head())
    return outTable
                    
# credit sorter

# discover sorter


# read all files in statements folder
files = [x[2] for x in os.walk(statements)]
finalTable = pd.DataFrame(columns=['Date', 'Source', 'Description', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Notes'])
for f, file in enumerate(files[0]):
    if "debit" in file:
        finalTable = debit(file)

print(finalTable.head())

# get data
# sort into categories


# output: 
# date, source, description, categories aligned, unknown, notes (if unknown)

