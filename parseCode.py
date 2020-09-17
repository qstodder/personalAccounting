#the table will be returned in a list of dataframe,for working with dataframe you need pandas
import pandas as pd
import os

statements = r'/Users/quiana/Documents/PersonalFinances/accounting 2.0/statements'

incomeKey = ["pasqual", "ucsd apach", "ucsd payrl", "asml", "interest", "deposit", "university of ca"]
groceriesKey = ["trader joe's", "ralphs", "vons", "myprotein", "safeway"]
housingKey =   ["premiere", "canyon park", "time warner", "sd gas", "wifi"]
gasKey = ["rotten robbie", "7-eleven", "raley's", "valero", "chevron", "arco", "shell", "stars & stripes", "fort independence", "76", "united pacifi",\
     "circle k", "texaco"]
necesitiesKey = ["bookstore", "walmart", "toyota", "cvs", "cyclery", "regents of uc", "parking mobil", "health", "foothill", "postal", "bird app", \
    "irs treas", "franchise tax", "calibercollision", "doctor"]
adventuresKey = ["rei", "mesa", "recreation", "ikon", "backcountry", "steepandcheap"]
funFoodKey = ["fairbanks", "hdh", "bombay coast", "restaurants", "tajima", "primos", "chipotle", "poki", "rubio's", "ramen", "taco", "ballast point", \
    "rock bottom", "mammoth mtn food", "pete's coffee", "5guys", "mexican", "eatery", "shogun", "pizzeria", "art of espress"]
giftsKey = ["gofndme", "wpy", "jacquie lawson"]
shoppingKey = ["marshalls", "ross", "nordstrom", "wearlively", "dsw", "shopping"]
entertainmentKey = ["cinemas", "reel rock"]
otherKey = ["schwab"]

keys = [incomeKey, groceriesKey, housingKey, gasKey, necesitiesKey, adventuresKey, funFoodKey, giftsKey, shoppingKey, entertainmentKey, otherKey]

print(len(keys))

# venmo sorter
# def venmo(file):
    
# debit sorter
def debit(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df[::-1]
    df[4] = df[4].str.lower()
    outTable = pd.DataFrame(None,index=range(len(df.index)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    skip=["venmo", "discover e-payment", "paypal", "online transfer", "wf credit card"]
    for iRow, row in df.iterrows():
        found = False
        # print(row[4])
        outTable['Date'][iRow] = row[0]
        outTable['Source'][iRow] = 'debit'
        outTable['Details'][iRow] = row[4]
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row[4]:
                    outTable['Description'][iRow] = key
                    outTable.iloc[iRow, c+3] = row[1]
                    found = True
        if not found:
            outTable['Unknown'][iRow] = row[1]
        for x in skip:
            if x in row[4]:
                outTable['Date'][iRow] = 0

    outTable = outTable[outTable.Date != 0]
    return outTable
                    
# credit sorter

# discover sorter
def discover(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df[::-1]
    df[2] = df[2].str.lower()
    df[3] = -df[3]     
    outTable = pd.DataFrame(None,index=range(len(df.index)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    skip=["directpay full", "internet payment", "cashback bonus"]
    for iRow, row in df.iterrows():
        found = False
        outTable['Date'][iRow] = row[0]
        outTable['Source'][iRow] = 'discover'
        outTable['Details'][iRow] = row[2]
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row[4]:
                    outTable['Description'][iRow] = key
                    outTable.iloc[iRow, c+3] = row[1]
                    found = True
        if not found:
            outTable['Unknown'][iRow] = row[1]
        for x in skip:
            if x in row[4]:
                outTable['Date'][iRow] = 0

    outTable = outTable[outTable.Date != 0]
    return outTable

def addTable(finalTable, addition):
    if finalTable.size == 0:
        finalTable = addition
    else:
        finalTable = finalTable.append(addition, ignore_index=True)
    return finalTable

# read all files in statements folder
files = [x[2] for x in os.walk(statements)]
finalTable = pd.DataFrame()
for f, file in enumerate(files[0]):
    if "debit" in file:
        debitData = debit(file)
        finalTable = addTable(finalTable, debitData)
    if "discover" in file:
        discData = discover(file)
        finalTable = addTable(finalTable, discData)

print(finalTable.head())
finalTable.to_csv("allStatements.csv")


