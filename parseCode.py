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
    df[4] = df[4].str.lower()
    outTable = pd.DataFrame(index=range(len(df.index)-1), columns=['Date', 'Source', 'Description', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Notes'])
    print(outTable.head())
    skip=["venmo", "discover e-payment"]
    for iRow, row in df.iterrows():
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row[4]:
                    
        
        # if(x in row[4] for i, x in enumerate(skip)):
        #     continue
        # elif (x in row[4] for i, x in enumerate(groceriesKey)):
        #     outTable['Date'], outTable['Description'], outTable['Groceries'] = df[0], grocerisKey, df[1]
        # elif (x in row[4] for i, x in enumerate(housingKey)):
        #     outTable['Date'], outTable['Description'], outTable['Housing'] = df[0], df[4], df[1]
        # elif (x in row[4] for i, x in enumerate(gasKey)):
        #     outTable['Date'], outTable['Description'], outTable['Gas'] = df[0], df[4], df[1]
        # elif (x in row[4] for i, x in enumerate(necesitiesKey)):
        #     outTable['Date'], outTable['Description'], outTable['Necesities'] = df[0], df[4], df[1]
        # elif (x in row[4] for i, x in enumerate(adventuresKey)):
        #     outTable['Date'], outTable['Description'], outTable['Adventures'] = df[0], df[4], df[1]
        # else:
        #     outTable['Date'], outTable['Description'], outTable['Adventures'] = df[0], df[4], df[1]

# credit sorter

# discover sorter


# read all files in statements folder
files = [x[2] for x in os.walk(statements)]
for f, file in enumerate(files[0]):
    if "debit" in file:
        debit(file)

# get data
# sort into categories


# output: 
# date, source, description, categories aligned, unknown, notes (if unknown)

