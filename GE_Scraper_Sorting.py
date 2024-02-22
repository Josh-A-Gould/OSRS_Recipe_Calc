#!/usr/bin/env python

#A program to calculate merching opportunities in the game Old School Runescape.

#Importing of different required python modules

# python/py -m pip install [Request name]
import requests
import numpy
import pandas as pd
import time
import math as m
import time
import json
import pickle
from datetime import datetime
from decimal import Decimal
import locale
import sys
from operator import itemgetter

locale.setlocale(locale.LC_ALL, '')

#Importing item information

URL = 'https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json'

headers = {'User-Agent': 'Merching Calc - @Josh_Gould'}

response = requests.get(URL, headers=headers)

ItemInfoList = response.json()

#Removing defunct information from the end, otherwise it messes with the search in ID from name

ToRemove = ('%JAGEX_TIMESTAMP%', '%UPDATE_DETECTED%')

for x in ToRemove:
    ItemInfoList.pop(x, None)

#Gives numbers with comma delimination

def formatter(d):
    try:
        output = '{0:n}'.format(Decimal(d.item()))
    except:
        try:
            output = '{0:n}'.format(Decimal(d))
        except:
            output = d
    return output

#Profit fomula, taking into account the tax, value of produced items and cost to produce said items.
#There is no need to change this, it is relitively robust and will slot nicely into the program

def Profit(Value, Cost):
    Profit = int(m.ceil(Value*0.99) - Cost)
    return Profit

#A function to get the Name of an item from ID, just searches the list for the ID number.
#The search could possibly be more effeicent but is good enough for me, atleast for now

def NameFromID(ID):
    ID = str(ID)
    return(ItemInfoList[ID]['name'])

#A function to get the name of an item fron its ID, currently goes one by one through the item list to find a match  
#Needs to be refined further, not an effecient search

def IDFromName(Name):
    if type(Name) != list:
        Name = [Name]

    for x in ItemInfoList:
        if ItemInfoList[x]['name'] == Name[0]:
            return str((ItemInfoList[x]['id']))
            break

def IDFromNameExp(Name):
    if type(Name) != list:
        Name = [Name]

    return ItemInfoList[ItemInfoList['name'] == Name[0]]['id']
#This may work eventually, but the dictionary need to be stripped of its arbitrairy id's in order
#to propery translate into a dataframe

def DF_Transform2():
    ItemInfoListDF = pd.DataFrame()
    for x in ItemInfoList:
        ItemInfoListDF = pd.concat([ItemInfoListDF, pd.DataFrame([ItemInfoList[x]])], ignore_index = True)
    return ItemInfoListDF
   
def DF_Transform3():
    ItemInfoListDF = pd.DataFrame()
    z = lambda x : pd.concat([ItemInfoListDF, pd.DataFrame([ItemInfoList[x]])], ignore_index = True)
    for x in ItemInfoList:
        ItemInfoListDF = pd.concat([ItemInfoListDF, pd.DataFrame([ItemInfoList[x]])], ignore_index = True)
    return ItemInfoListDF

def IDFromNameTest(Name, DF_2):
    return(DF_2[DF_2['name'] == Name])

def ItemATPGrab():
    global ATPData
    global LastTime

    url = 'http://prices.runescape.wiki/api/v1/osrs/latest'

    try:
        if (time.time() - LastTime) > 30:
            raise ValueError
        else:
            pass
    except:
        try:     
            ATPData = json.loads(open('OSRS-ATP').read())
            with open('OSRS-ATP', 'rb') as file:
                ATPData = json.load(file) 

                LastTime = ATPData['Time']
                
                if (time.time() - LastTime) > 30:
                    raise

                ATPData = pd.DataFrame(ATPData['data'])

                file.close()

        except:
            response = requests.get(url, headers=headers)
            
            DataJson = response.json()

            Time = {"Time":time.time()}

            DataJson.update(Time)

            ATPData = DataJson['data']

            ATPData = pd.DataFrame(ATPData)
        
            file = open('OSRS-ATP', 'w')
            json.dump(DataJson, file)
            file.close()

        ATPData = ATPData.iloc[[2,0]]

    return ATPData

#Gets the ID of an item from it's name and then asks for its recent prices
#This as a function is perfectly acceptable & does not need to be altered
  
def RecentPrices(List):
    ItemATPGrab()
    global ATPData
    PricesList = []
    if len(List) == 1:
        List = List[0]
        if str(List).isdecimal() == True:
            Data = ATPData[x]
        else:
            Data = ATPData[IDFromName(List)]
        PricesList.append(Data)
    else:
        for List in List:
            if str(List).isdecimal() == True:
                Data = ATPData[List]
            else:
                Data = ATPData[IDFromName(List)]
            PricesList.append(Data)
    return PricesList

#Runs repetitions of the Banded recent prices formula for a list of different items and adds the results to a list

def BestPrice(List, Quantities, Direction):
    Data = RecentPrices(List)

    PricesList = []

    y = 0

    if Direction == "Low":
        for x in Data:
            PricesList.append(Data[y].iloc[0]*Quantities[y])
            y += 1
        return List[PricesList.index(min(PricesList))], Quantities[PricesList.index(min(PricesList))], round(Data[PricesList.index(min(PricesList))].iloc[0],0)
    elif Direction == "High":
        for x in Data:
            PricesList.append(Data[y].iloc[1]*Quantities[y])
            y += 1
        return List[PricesList.index(max(PricesList))], Quantities[PricesList.index(max(PricesList))], round(Data[PricesList.index(max(PricesList))].iloc[1],0)
    else:
        raise ValueError
    
#A formula which calculates all possible recipe sets
#it is supposed to be able to take ID's and Item names in the format:

#Recipe(['ID1',...,'IDn'], ['Num1',...,'Numn'], repeat with different values)
#being in the format (Input items, respective quantities, Output items, respective quantities)
#the square brackets are only needed for tuples
#in a future possible consumer facing program it may be necessary
#to have a seperate function which converts user inputs into lists
#if necessary, also a drop down look up/selection function to avoid errors.
    
def Recipe(Inputs, QuantitiesIn, Outputs, QuantitiesOut, ExtraCost = 0):

    if type(Inputs) != list:
        Inputs = [Inputs]
    if type(QuantitiesIn) != list:
        QuantitiesIn = [QuantitiesIn]
    if type(Outputs) != list:
        Outputs = [Outputs]
    if type(QuantitiesOut) != list:
        QuantitiesOut = [QuantitiesOut]
    
    y = 0
    for X in Inputs:
        
        if type(X) == list:
            Name, Quantity, Price = BestPrice(X, QuantitiesIn[y],"Low")
            Inputs[y], QuantitiesIn[y] = Name, Quantity
            #print("Buy", Name, "for components at:", f(Price), "each")
        y += 1
    
    y = 0
    for X in Outputs:
        
        if type(X) == list:
            Name, Quantity, Price = BestPrice(X, QuantitiesOut[y],"High")
            Outputs[y], QuantitiesOut[y] = Name, Quantity
            #print("Produce", Name, "to sell at:", f(Price))
        y += 1

    BuyPricesList = RecentPrices(Inputs)
    SellPricesList = RecentPrices(Outputs)
    
    UnitCost = 0
    UnitValue = 0
    x = 0

    LowList = []
    HighList = []

    while x < len(Inputs):
        LowList.append(BuyPricesList[x].iloc[0])
        x += 1

    x = 0

    while x < len(Outputs):
        HighList.append(SellPricesList[x].iloc[1])
        x += 1
    
    x = 0
    y = 0

    while x < len(Inputs):
        UnitCost += float(QuantitiesIn[x]) * LowList[x]
        x += 1
    
    while y < len(Outputs):
        UnitValue += float(QuantitiesOut[y]) * HighList[y]
        y += 1
    
    #print('Your profit from making', Outputs[0] ,'would be:', f(Profit(UnitValue - ExtraCost, UnitCost)))
    return(Inputs, LowList, Outputs, HighList, Profit(UnitValue - ExtraCost, UnitCost))

def SingleBestPrice(Inputs, Quantities):
    if type(Inputs) == list:
        Name, Quantity, Price = BestPrice(Inputs, Quantities,"Low")
        #print("Buy", Name, "for components at:", f(Price), "each")
        return Name, Quantity

#Runs all current pre-defined calcs
#In the future pre-defined calcs should be shifted to the recipe function
#with a pre-defined calc being writted, at most, to do the specific work
#I.E which zenyte to make / which thing to break down to make masori/torva
#this work should be done pre-running the recipe function instead of selecting best
#in order to limit the number of API calls which are neccecitated.
    
def Calcs():
    Output = []

    with open('MerchingList.pkl', 'rb') as f:
        merchingList = pickle.load(f)

    for x in merchingList:
        
        Output.append(Recipe(x[0], x[1], x[2], x[3]))

    Name, Quantity = SingleBestPrice(["Bandos chestplate","Bandos tassets"], [1/3,1,1/2])
    Output.append(Recipe(["Torva full helm (damaged)", Name], [1, Quantity], "Torva full helm", 1))
    Output.append(Recipe(["Torva platebody (damaged)", Name], [1, 2*Quantity], "Torva platebody", 1))
    Output.append(Recipe(["Torva platelegs (damaged)", Name], [1, 2*Quantity], "Torva platelegs", 1))

    Name, Quantity = SingleBestPrice(["Armadyl helmet","Armadyl chestplate","Armadyl chainskirt"], [1,1/4,1/3,1])
    Output.append(Recipe(["Masori mask", Name], [1, Quantity], "Masori mask (f)", 1))
    Output.append(Recipe(["Masori body", Name], [1, 4*Quantity], "Masori body (f)", 1))
    Output.append(Recipe(["Masori chaps", Name], [1, 3*Quantity], "Masori chaps (f)", 1))

    Name, Quantity = SingleBestPrice(["Crystal weapon seed", "Crystal tool seed", "Enhanced crystal teleport seed", "Crystal armour seed", "Enhanced crystal weapon seed"], [1/10, 1/100, 1/150, 1/250, 1/1500])
    Output.append(Recipe([["Bow of faerdhinen (inactive)","Blade of saeldor (inactive)"], Name],[[1,1], 250*Quantity],"Enhanced crystal weapon seed",1))
    Output.append(Recipe(["Enhanced crystal weapon seed", Name],[1, 100*Quantity],"Bow of faerdhinen (inactive)",1))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print("\n")

    ProduceArray = []
    PartsArray = []
    tmpOutput = []

    Output = sorted(Output, key=itemgetter(-1))

    for x in Output:
        y = 1
        for z in x[0]:
            ProduceArray.append(x[2][0])
            PartsArray.append(z)

            if z == x[0][0]:
                tmpOutput.append((z, x[1][0], x[2][0], x[3][0], x[4]))
            else:
                tmpOutput.append((z, x[1][y]))
                y += 1

    Output = tmpOutput

    tuples = list(zip(ProduceArray, PartsArray))

    index = pd.MultiIndex.from_tuples(tuples, names=["Produce", "Parts"])

    Output = pd.DataFrame(Output, columns=['Inputs', 'Input Price', 'Output', 'Output Price', 'Profit'], index = index)

    Output = Output.drop(["Inputs", "Output"], axis = 1).fillna("") 

    Output['Output Price'] = Output['Output Price'].apply(lambda x: formatter(x))
    Output['Input Price'] = Output['Input Price'].apply(lambda x: formatter(x))
    Output['Profit'] = Output['Profit'].apply(lambda x: formatter(x))

    print(Output.to_string())

    return(Output)
    
#Basically just calls the Calcs() function at regular intervals
#would be much more useful if/when i have a server to run this on
#& a way of posting messages to discord or chosen platform from python.
    
starttime = time.time()
Word = "Go"
def RepCalcs():
    while True:
        Calcs()
        Word = input('Say "stop" to discontinue the program.\n')
        if Word == "stop":
            break
        else:
            print("Your next update will be in 30s time.")
            time.sleep(45)

if __name__ == '__main__':
    Calcs()