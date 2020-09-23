#the table will be returned in a list of dataframe,for working with dataframe you need pandas
import pandas as pd
import os

statements = r'/Users/quiana/Documents/PersonalFinances/accounting 2.0/statements'

def keywords():
    incomeKey = ["pasqual", "ucsd apach", "ucsd payrl", "asml", "interest", "deposit", "university of ca"]
    groceriesKey = ["trader joe's", "ralphs", "vons", "myprotein", "safeway", "food", "milk"]
    housingKey =   ["premiere", "canyon park", "time warner", "sd gas", "wifi", "state farm", "üè°", "üîå"]   #house
    gasKey = ["rotten robbie", "7-eleven", "raley's", "valero", "chevron", "arco", "shell", "stars & stripes", "fort independence", " 76 ", "united pacifi",\
        "circle k", "texaco", "gas"]
    necesitiesKey = ["bookstore", "walmart", "toyota", "cvs", "cyclery", "regents of uc", "parking", "health", "foothill", "postal", "bird app", \
        "irs treas", "franchise tax", "calibercollision", "doctor", "best buy", "lyft", "home depot", "automotive"]
    adventuresKey = ["rei", "mesa", "recreation", "ikon", "backcountry", "steepandcheap", "play it again", "airlines", "sportinggoods", "car rental", "best western"]
    funFoodKey = ["fairbanks", "hdh", "bombay coast", "restaurants", "tajima", "primos", "chipotle", "poki", "rubio's", "ramen", "taco", "ballast point", \
        "rock bottom", "mammoth mtn food", "pete's coffee", "5guys", "mexican", "eatery", "shogun", "pizzeria", "art of espress", "starbucks", "subway", \
            "thai", "ramen", "creps", "üåØ"] #burrito
    giftsKey = ["gofndme", "wpy", "jacquie lawson", "uncommongoods", "happy earth", "bernie", "4 ocean", "etsy"]
    shoppingKey = ["marshalls", "ross", "nordstrom", "wearlively", "dsw", "shopping", "forever 21"]
    entertainmentKey = ["cinemas", "reel rock", "prime video", "spotify"]
    otherKey = ["schwab"]

    return keys = [incomeKey, groceriesKey, housingKey, gasKey, necesitiesKey, adventuresKey, funFoodKey, giftsKey, shoppingKey, entertainmentKey, otherKey]

keys = keywords()

# venmo sorter
def venmo(file):
    df = pd.read_csv(statements+"/"+file)
    df = df[pd.notnull(df["Note"])]
    df["Note"] = df["Note"].str.lower()
    outTable = pd.DataFrame(None,index=range(len(df.index)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    for iRow, row in df.iterrows():
        found = False
        outTable['Date'][iRow] = row["Datetime"]
        outTable['Source'][iRow] = 'venmo'
        outTable['Details'][iRow] = row["Note"]
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row["Note"]:
                    outTable['Description'][iRow] = key
                    outTable.iloc[iRow, c+3] = row["Amount (total)"]
                    found = True
        if not found:
            outTable['Unknown'][iRow] = row["Amount (total)"]

    return outTable
    
# debit sorter
def debit(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df = df[::-1]
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
def credit(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df = df[::-1]
    df[4] = df[4].str.lower()
    outTable = pd.DataFrame(None,index=range(len(df.index)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    skip=["automatic payment"]
    for iRow, row in df.iterrows():
        found = False
        outTable['Date'][iRow] = row[0]
        outTable['Source'][iRow] = 'credit'
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

# discover sorter
def discover(file):
    df = pd.read_csv(statements+"/"+file)
    df = df[::-1]
    df["Description"] = df["Description"].str.lower()
    df["Amount"] = -df["Amount"].astype(float)  
    outTable = pd.DataFrame(None,index=range(len(df.index)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    skip=["directpay full", "internet payment", "cashback bonus"]
    for iRow, row in df.iterrows():
        found = False
        outTable['Date'][iRow] = row["Trans. Date"]
        outTable['Source'][iRow] = 'discover'
        outTable['Details'][iRow] = row["Description"]
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row["Description"]:
                    outTable['Description'][iRow] = key
                    outTable.iloc[iRow, c+3] = row["Amount"]
                    found = True
        if not found:
            if row[4] == "Supermarkets":
                outTable['Description'][iRow] = "Supermarket"
                outTable['Groceries'][iRow] = row["Amount"]
            elif row[4] == "Restaurants":
                outTable['Description'][iRow] = "Restaurant"
                outTable['Fun_Food'][iRow] = row["Amount"]
            elif row[4] == "Government Services":
                outTable['Description'][iRow] = "Gov. Service"
                outTable['Necesities'][iRow] = row["Amount"]
            elif row[4] == "Department Stores":
                outTable['Description'][iRow] = "Department Store"
                outTable['Shopping'][iRow] = row["Amount"]
            elif row[4] == "Gasoline":
                outTable['Description'][iRow] = "gas"
                outTable['Gas'][iRow] = row["Amount"]
            else:
                outTable['Unknown'][iRow] = row["Amount"]
        for x in skip:
            if x in row["Description"]:
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
    elif "credit" in file:
        creditData = credit(file)
        finalTable = addTable(finalTable, creditData)
    elif "discover" in file:
        discData = discover(file)
        finalTable = addTable(finalTable, discData)
    elif "venmo" in file:
        venmoData = venmo(file)
        finalTable = addTable(finalTable, venmoData)

print(finalTable.head())
finalTable.to_csv("allStatements.csv")


