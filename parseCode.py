#the table will be returned in a list of dataframe,for working with dataframe you need pandas
import pandas as pd
import os
import shutil
import regex
import emoji
import datetime


statements = r'/Users/quiana/Documents/PersonalFinances/accounting/newStatements'
oldStatements = r'/Users/quiana/Documents/PersonalFinances/accounting/oldStatements'
allStatements = r'/Users/quiana/Documents/PersonalFinances/accounting/personalAccounting/allStatements.csv'

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
    incomeKey = ["pasqual", "ucsd apach", "ucsd payrl", "asml", "interest", "deposit", "university of ca", "payroll", "uc san diego ucsd"]
    groceriesKey = ["trader joe", "ralph", "vons", "myprotein", "safeway", "food", "milk", "groceries", "fud", "tj's", "snax", "🥒🍅"]
    housingKey =   ["premiere", "canyon park", "time warner", "sd gas", "sewwer", "rent", "insurance", "wifi", "state farm", "util", "sdge", "🏠", "🚿", "🏡", "💡", "🔌"]  
    gasKey = ["rotten robbie", "7-eleven", "raley's", "valero", "chevron", "arco", "shell", "stars & stripes", "fort independence", " 76 ", "united pacifi",\
        "circle k", "texaco", "gas", "vroom vroom juice", "gaaaaaas", "⛽"]
    necesitiesKey = ["bookstore", "walmart", "toyota", "cvs", "cyclery", "regents of uc", "parking", "health", "foothill", "chegg", "postal", "bird app", \
        "irs treas", "franchise tax", "calibercollision", "doctor", "best buy", "lyft", "home depot", "automotive", "litter"]
    adventuresKey = ["rei", "mesa", "recreation", "ikon", "backcountry", "steepandcheap", "play it again", "airlines", "southwestair", "sportinggoods", "car rental", "best western", "hertz"]
    funFoodKey = ["fairbanks", "hdh", "bombay coast", "restaurants", "tajima", "primos", "chipotle", "poki", "rubio's", "ramen", "taco", "ballast point", \
        "rock bottom", "mammoth mtn food", "pete's coffee", "5guys", "mexican", "eatery", "shogun", "pizzeria", "art of espress", "starbucks", "subway", \
            "thai", "ramen", "creps", "pizza", "yums", "carls jr", "fooood", "lunch","acaii", "chicago 🔥 grill", "😋", "🌯", "🍔", "🍟", "🍺", "🍴", "🍕", "🍹", "🍦", "🍻", "🍣"]
    giftsKey = ["gofndme", "wpy", "jacquie lawson", "uncommongoods", "happy earth", "bernie", "4 ocean", "etsy"]
    shoppingKey = ["marshalls", "ross", "nordstrom", "wearlively", "dsw", "shopping", "forever 21", "poshmark", "lulus"]
    entertainmentKey = ["cinemas", "reel rock", "prime video", "spotify", "movie", "web town square", "🎥"]
    travelKey = ["alaska airlines", "hawaiian airlines", "southwestair"]
    otherKey = ["schwab"]

    keys = [incomeKey, groceriesKey, housingKey, gasKey, necesitiesKey, adventuresKey, funFoodKey, giftsKey, shoppingKey, entertainmentKey, travelKey, otherKey]
    return keys
keys = keywords()

def makeTable(df, agg=False):
    if agg:
        outTable = pd.DataFrame(None,index=range(len(df)), columns=['Month', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Travel', 'Other', 'Unknown'])
    else:
        outTable = pd.DataFrame(None,index=range(len(df)), columns=['Date', 'Source', 'Description', 'Income', 'Groceries', 'Housing', 'Gas', 'Necesities', 'Adventures', 'Fun_Food', 'Gifts/Charity', 'Shopping', 'Entertainment', 'Travel', 'Other', 'Unknown', 'NumCategories', 'Details'])
    return outTable
    
def debit(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df = df[::-1]
    df[4] = df[4].str.lower()
    outTable = makeTable(df)
    skip=["venmo", "discover e-payment", "paypal", "online transfer", "wf credit card"]
    for iRow, row in df.iterrows():
        found = False
        count = 0
        outTable.loc[iRow, 'Date'] = toDatetime(row[0])
        outTable.loc[iRow, 'Details'] = row[4]
        outTable.loc[iRow, 'Source'] = 'debit'
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row[4]:
                    outTable.loc[iRow, 'Description'] = key
                    outTable.iloc[iRow, c+3] = row[1]
                    found = True
                    count += 1
        if not found:
            outTable.loc[iRow, 'Unknown'] = row[1]
            count += 1
        for x in skip:
            if x in row[4]:
                outTable.loc[iRow, 'Date'] = 0
        outTable['NumCategories'] = count

    outTable = outTable[outTable.Date != 0]
    return outTable
                    
def credit(file):
    df = pd.read_csv(statements+"/"+file, header=None)
    df = df[::-1]
    df[4] = df[4].str.lower()
    outTable = makeTable(df)
    skip=["automatic payment"]
    for iRow, row in df.iterrows():
        found = False
        count = 0
        outTable.loc[iRow, 'Date'] = toDatetime(row[0])
        outTable.loc[iRow, 'Source'] = 'credit'
        outTable.loc[iRow, 'Details'] = row[4]
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row[4]:
                    outTable.loc[iRow, 'Description'] = key
                    outTable.iloc[iRow, c+3] = row[1]
                    found = True
                    count += 1
        if not found:
            outTable.loc[iRow, 'Unknown'] = row[1]
            count += 1
        for x in skip:
            if x in row[4]:
                outTable.loc[iRow, 'Date'] = 0
        outTable['NumCategories'] = count

    outTable = outTable[outTable.Date != 0]
    return outTable

def discover(file):
    df = pd.read_csv(statements+"/"+file)
    df = df[::-1]
    df["Description"] = df["Description"].str.lower()
    df["Amount"] = -df["Amount"].astype(float)  
    outTable = makeTable(df)
    skip=["directpay full", "internet payment", "cashback bonus"]
    for iRow, row in df.iterrows():
        found = False
        count = 0
        outTable.loc[iRow, 'Date'] = toDatetime(row["Trans. Date"])
        outTable.loc[iRow, 'Source'] = 'discover'
        outTable.loc[iRow, 'Details'] = row["Description"]
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row["Description"]:
                    outTable.loc[iRow, 'Description'] = key
                    outTable.iloc[iRow, c+3] = row["Amount"]
                    found = True
                    count += 1
        if not found:
            if row[4] == "Supermarkets":
                outTable.loc[iRow, 'Description'] = "Supermarket"
                outTable.loc[iRow, 'Groceries'] = row["Amount"]
            elif row[4] == "Restaurants":
                outTable.loc[iRow, 'Description'] = "Restaurant"
                outTable.loc[iRow, 'Fun_Food'] = row["Amount"]
            elif row[4] == "Government Services":
                outTable.loc[iRow, 'Description'] = "Gov. Service"
                outTable.loc[iRow, 'Necesities'] = row["Amount"]
            elif row[4] == "Department Stores":
                outTable.loc[iRow, 'Description'] = "Department Store"
                outTable.loc[iRow, 'Shopping'] = row["Amount"]
            elif row[4] == "Gasoline":
                outTable.loc[iRow, 'Description'] = "gas"
                outTable.loc[iRow, 'Gas'] = row["Amount"]
            else:
                outTable.loc[iRow, "Unknown"] = row["Amount"]
            count += 1
        for x in skip:
            if x in row["Description"]:
                outTable.loc[iRow, 'Date'] = 0
        outTable['NumCategories'] = count

    outTable = outTable[outTable.Date != 0]
    return outTable

def venmo(file):
    df = pd.read_csv(statements+"/"+file, header=2)
    df = df[pd.notnull(df["Note"])]
    df = df.reset_index(drop=True)
    df["Note"] = df["Note"].str.lower()
    outTable = makeTable(df)
    for iRow, row in df.iterrows():
        found = False
        count = 0
        outTable.loc[iRow, 'Date'] = toDatetime(row["Datetime"], isStandard=False)
        outTable.loc[iRow, 'Source'] = 'venmo'
        outTable.loc[iRow, 'Details'] = row["Note"]
        amount = row['Amount (total)']
        amount = amount.replace(" ","").replace("(","-").replace(")","").replace(",","")
        amount = float(amount.replace("$",""))
        for c in range(len(keys)):
            for k, key in enumerate(keys[c]):
                if key in row["Note"]:
                    outTable.loc[iRow, 'Description'] = key
                    outTable.iloc[iRow, c+3] = amount
                    found = True
                    count += 1
        if not found:
            count += 1
            outTable.loc[iRow, 'Unknown'] = amount
            outTable.loc[iRow, 'Details'] = row["Note"] + (' '.join(thing for thing in [' ', row["From"], row["Type"], row["To"]]))
            if listEmojis(row["Note"]):
                emojis = (' '.join(emoji for emoji in listEmojis(row["Note"])))
                print(row["Note"] + emojis)
        outTable['NumCategories'] = count

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

# move new statements to old statements folder
for f, file in enumerate(files[0]):
    shutil.move(statements+"/"+file, oldStatements+"/"+file)

print(finalTable.tail())
filename = allStatements
finalTable.to_csv(filename)

# create analysis: monthly summation
dates = pd.to_datetime(finalTable['Date']).sort_values()
months = dates.dt.strftime("%m/%y").unique().tolist()
cleanedMonths = [x for x in months if str(x) != 'nan']
months = cleanedMonths
months_dt = [datetime.datetime(int("20" + d.split('/')[1]), int(d.split('/')[0]), 1) for d in months]

aggMonths = makeTable(months, agg=True)
aggMonths['Month'] = months_dt

finalTable['Date'] = pd.to_datetime(finalTable['Date']).dt.strftime("%m/%y")

print(len(aggMonths))
for i in range(len(aggMonths)):
    for c in range(len(aggMonths.columns)):
        if c > 0:
            aggMonths.iloc[i,c] = finalTable[finalTable['Date'] == months[i]].iloc[:,c+2].astype(float).sum()
        
# Calculate new columns
aggMonths['Net'] = aggMonths.iloc[:,1:].sum(axis=1)
aggMonths['AllSpending'] = aggMonths['Net'] - aggMonths['Income']
aggMonths['Living'] = aggMonths['Groceries'] + aggMonths['Housing'] + aggMonths['Gas'] + aggMonths['Necesities']
aggMonths['NonLiving'] = aggMonths['AllSpending'] - aggMonths['Living'] - aggMonths['Other']
aggMonths['AvgGroceries'] = [round(num,2) for num in aggMonths['Groceries']/4.5]
aggMonths['AvgFood'] = [round(num,2) for num in (aggMonths['Groceries'] + aggMonths['Fun_Food'])/4.5]



print(aggMonths.tail())
# print(months_dt)


# output as seperate csv
filename = "Aggregated Months.csv"
aggMonths.to_csv(filename, index=False)
