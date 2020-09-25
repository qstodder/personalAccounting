#the table will be returned in a list of dataframe,for working with dataframe you need pandas
import pandas as pd
import os
import regex
import emoji
import datetime

statements = r'/Users/quiana/Documents/PersonalFinances/accounting 2.0/newStatements'
allStatements = r'/Users/quiana/Documents/PersonalFinances/accounting 2.0/allStatements.csv'

def addTable(finalTable, addition):
    if finalTable.size == 0:
        finalTable = addition
    else:
        finalTable = finalTable.append(addition, ignore_index=True)
    return finalTable

def toDatetime(d, isStandard=True):
    if isStandard:
        nums = d.split("/")
        if len(nums[2])<4:
            dateOutput = datetime.datetime(int("20" + nums[2]), int(nums[0]), int(nums[1]))
        else:
            dateOutput = datetime.datetime(int(nums[2]), int(nums[0]), int(nums[1]))
    else:
        dateAndTime = d.split("T")
        nums = dateAndTime[0].split("-")
        dateOutput = datetime.datetime(int(nums[0]), int(nums[1]), int(nums[2]))
    return dateOutput

def listEmojis(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list

def keywords():
    incomeKey = ["pasqual", "ucsd apach", "ucsd payrl", "asml", "interest", "deposit", "university of ca"]
    groceriesKey = ["trader joe's", "ralph", "vons", "myprotein", "safeway", "food", "milk", "groceries", "fud", "tj's", "snax", "🥒🍅"]
    housingKey =   ["premiere", "canyon park", "time warner", "sd gas", "sewwer", "insurance", "wifi", "state farm", "util", "sdge", "🏠", "🚿", "🏡", "💡", "🔌"]  
    gasKey = ["rotten robbie", "7-eleven", "raley's", "valero", "chevron", "arco", "shell", "stars & stripes", "fort independence", " 76 ", "united pacifi",\
        "circle k", "texaco", "gas", "vroom vroom juice", "gaaaaaas", "⛽"]
    necesitiesKey = ["bookstore", "walmart", "toyota", "cvs", "cyclery", "regents of uc", "parking", "health", "foothill", "postal", "bird app", \
        "irs treas", "franchise tax", "calibercollision", "doctor", "best buy", "lyft", "home depot", "automotive", "litter"]
    adventuresKey = ["rei", "mesa", "recreation", "ikon", "backcountry", "steepandcheap", "play it again", "airlines", "sportinggoods", "car rental", "best western"]
    funFoodKey = ["fairbanks", "hdh", "bombay coast", "restaurants", "tajima", "primos", "chipotle", "poki", "rubio's", "ramen", "taco", "ballast point", \
        "rock bottom", "mammoth mtn food", "pete's coffee", "5guys", "mexican", "eatery", "shogun", "pizzeria", "art of espress", "starbucks", "subway", \
            "thai", "ramen", "creps", "pizza", "yums", "fooood", "lunch","acaii", "chicago 🔥 grill", "😋", "🌯", "🍔", "🍟", "🍺", "🍴", "🍕", "🍹", "🍦", "🍻"]
    giftsKey = ["gofndme", "wpy", "jacquie lawson", "uncommongoods", "happy earth", "bernie", "4 ocean", "etsy"]
    shoppingKey = ["marshalls", "ross", "nordstrom", "wearlively", "dsw", "shopping", "forever 21"]
    entertainmentKey = ["cinemas", "reel rock", "prime video", "spotify", "movie", "🎥"]
    otherKey = ["schwab"]

    keys = [incomeKey, groceriesKey, housingKey, gasKey, necesitiesKey, adventuresKey, funFoodKey, giftsKey, shoppingKey, entertainmentKey, otherKey]
    return keys
keys = keywords()
    
def debit(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df = df[::-1]
    df[4] = df[4].str.lower()
    outTable = pd.DataFrame(None,index=range(len(df)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    skip=["venmo", "discover e-payment", "paypal", "online transfer", "wf credit card"]
    for iRow, row in df.iterrows():
        found = False
        # print(row[4])
        outTable['Date'][iRow] = toDatetime(row[0])
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
                    
def credit(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df = df[::-1]
    df[4] = df[4].str.lower()
    outTable = pd.DataFrame(None,index=range(len(df)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    skip=["automatic payment"]
    for iRow, row in df.iterrows():
        found = False
        outTable['Date'][iRow] = toDatetime(row[0])
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

def discover(file):
    df = pd.read_csv(statements+"/"+file)
    df = df[::-1]
    df["Description"] = df["Description"].str.lower()
    df["Amount"] = -df["Amount"].astype(float)  
    outTable = pd.DataFrame(None,index=range(len(df)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    skip=["directpay full", "internet payment", "cashback bonus"]
    for iRow, row in df.iterrows():
        found = False
        outTable['Date'][iRow] = toDatetime(row["Trans. Date"])
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

def venmo(file):
    df = pd.read_csv(statements+"/"+file)
    df = df[pd.notnull(df["Note"])]
    df = df.reset_index(drop=True)
    df["Note"] = df["Note"].str.lower()
    outTable = pd.DataFrame(None,index=range(len(df)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown', 'Details'])
    for iRow, row in df.iterrows():
        found = False
        outTable['Date'][iRow] = toDatetime(row["Datetime"], isStandard=False)
        outTable['Source'][iRow] = 'venmo'
        outTable['Details'][iRow] = row["Note"]
        amount = float(row["Ammount (total)"].replace("$",""))
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row["Note"]:
                    outTable['Description'][iRow] = key
                    outTable.iloc[iRow, c+3] = amount
                    found = True
        if not found:
            outTable['Unknown'][iRow] = amount
            outTable['Details'][iRow] = row["Note"] + (' '.join(thing for thing in [' ', row["From"], row["Type"], row["To"]]))
            if listEmojis(row["Note"]):
                emojis = (' '.join(emoji for emoji in listEmojis(row["Note"])))
                print(row["Note"] + emojis)


    return outTable


# read all files in statements folder
files = [x[2] for x in os.walk(statements)]
finalTable = pd.read_csv(allStatements, index_col=0)
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
filename = "allStatements_" + str(datetime.date.today()) + ".csv" 
finalTable.to_csv(filename)

# create analysis: monthly summation
dates = pd.to_datetime(finalTable['Date']).sort_values()
months = dates.dt.strftime("%m/%y").unique().tolist()
months_dt = [datetime.datetime(int("20" + d.split('/')[1]), int(d.split('/')[0]), 1) for d in months]

aggMonths = pd.DataFrame(None,index=range(len(months)), columns=['Month', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Other', 'Unknown'])
aggMonths['Month'] = months_dt

finalTable['Date'] = pd.to_datetime(finalTable['Date']).dt.strftime("%m/%y")


for i in range(len(aggMonths)):
    for c in range(len(aggMonths.columns)):
        if c > 0:
            aggMonths.iloc[i,c] = finalTable[finalTable['Date'] == months[i]].iloc[:,c+2].astype(float).sum()
        
# Calculate new columns
aggMonths['Net'] = aggMonths.iloc[:,1:].sum(axis=1)
aggMonths['AllSpending'] = aggMonths['Net'] - aggMonths['Income']
aggMonths['Living'] = aggMonths['Groceries'] + aggMonths['Housing'] + aggMonths['Necesities'] + aggMonths['Gas']
aggMonths['NonLiving'] = aggMonths['AllSpending'] - aggMonths['Living']
aggMonths['AvgGroceries'] = [round(num,2) for num in aggMonths['Groceries']/4.5]
aggMonths['AvgFood'] = [round(num,2) for num in (aggMonths['Groceries'] + aggMonths['Fun_Food'])/4.5]


print(aggMonths.head())
# print(months_dt)


# output as seperate csv
filename = "Aggregated Months" + str(datetime.date.today()) + ".csv"
aggMonths.to_csv(filename, index=False)
