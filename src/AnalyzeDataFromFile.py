#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
#from sodapy import Socrata
import matplotlib.pyplot as plt
import math

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
#client = Socrata("data.cdc.gov", None)

# Example authenticated client (needed for non-public datasets):
#client = Socrata("data.cdc.gov", "2x5FE7rZpUcHgxdN5CtjorJAq", username="as1o28wgsajgfr2nqoyi9defr", password="3ja1zufytzxwm5orvyewzlk30m0o7ieb43c0anb7ktmrvpnv19")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
#results = client.get("y5bj-9g5w", limit=25)

# Convert to pandas DataFrame
#results_df = pd.DataFrame.from_records(results)

#plt.plot(results_df)
#plt.legend()
#plt.show()

#print("start")

class Entry:
    def __init__(self, year, week, agegroup, deaths):
        self.year = int(year)
        self.week = int(week)
        self.agegroup = agegroup
        self.deaths = int(deaths)
            
    def format(self):
        ans = str(self.year)+": week "+str(self.week)
        ans+="\t|\tagegroup"+str(getAgeGroupNum(self.agegroup))+": "+self.agegroup+"\t|\tDeaths: "+str(self.deaths)
        return ans

def getAgeGroupNum(str):
    if(str == "Under 25 years"):
        return 1
    elif(str == "25-44 years"):
        return 2
    elif(str == "45-64 years"):
        return 3
    elif(str == "65-74 years"):
        return 4
    elif(str == "75-84 years"):
        return 5
    elif(str == "85 years and older"):
        return 6
    else:
        return -1

def numToAgeGroup(n):
    if(n == 1):
        return "Under 25 years"
    elif(n == 2):
        return "25-44 years"
    elif(n == 3):
        return "45-64 years"
    elif(n == 4):
        return "65-74 years"
    elif(n == 5):
        return "75-84 years"
    elif(n == 6):
        return "85 years and older"
    else:
        return "Unknown Age Group"

def getAgeGroup(list, age):
    ans = []
    for T in list:
        if(getAgeGroupNum(T.agegroup) == age):
            ans.append(T)
    return ans

def getYear(list, yr):
    ans = []
    for T in list:
        if(T.year == yr):
            ans.append(T)
    return ans

def getDeaths(list, age, year):
    list = getYear(getAgeGroup(list, age), year)
    ans = []
    # for T in list:
    #     ans.append(T.deaths)
    # if(year==2020):
    #     for T in ans:
    #         print(T)
    if(year!=2020):
        for T in list:
            ans.append(T.deaths)
    else:
        for i in range(49):
            ans.append(list[i].deaths)
        while(len(ans) < 52):
            ans.append(list[48].deaths)
    return ans

def byDate(E):
    return (100*E.year)+E.week

def byAge(E):
    return getAgeGroupNum(E.agegroup)

def sortByDate(E):
    return (10*byDate(E))+byAge(E)

def sortByAge(E):
    return 100000*byAge(E)+(byDate(E))

def interpretLine(str):
    data = str.split(',')
    # print(data)
    if(data[8] != 'Unweighted'):
        return None
    return Entry(data[3], data[4], data[5], data[6])


FILE_NAME = "cdc_us_deaths_data_2020_complete.csv"
#FILE_NAME = "cdc_us_deaths_data.csv"
FILE_NAME = "..\\Data\\"+FILE_NAME

file = open(FILE_NAME, "r")
contents = file.read()
lines = file.readlines()
stripped = contents.split("\n")

dataset = []

for line in stripped[1:]:
    temp = interpretLine(line)
    if(temp == None):
        continue
    dataset.append(temp)

#choice = input("How do you want to sort the data?\n[1]Chronologically\n[2]By Age\nInput: ")
#if(choice=='1'):
#    dataset.sort(key=sortByDate)
#elif(choice=='2'):
#    dataset.sort(key=sortByAge)

#for data in dataset:
#    print(data.format())

nrow = 2
ncol = 3
fig, axes = plt.subplots(nrow, ncol)

df_list = []
years = ['2015', '2016', '2017', '2018', '2019', '2020']
colors = ['purple', 'navy', 'darkgreen', 'olive', 'darkgoldenrod', 'red']
def plotAgeGroup(n):
    y2015 = getDeaths(dataset, n, 2015)
    y2016 = getDeaths(dataset, n, 2016)
    y2017 = getDeaths(dataset, n, 2017)
    y2018 = getDeaths(dataset, n, 2018)
    y2019 = getDeaths(dataset, n, 2019)
    y2020 = getDeaths(dataset, n, 2020)

#Debugging
    # print("n = "+str(n))

    # print("2015: "+str(len(y2015)))
    # print("2016: "+str(len(y2016)))
    # print("2017: "+str(len(y2017)))
    # print("2018: "+str(len(y2018)))
    # print("2019: "+str(len(y2019)))
    # print("2020: "+str(len(y2020)))


    # Data  
    df_list.insert(n-1, pd.DataFrame({'2015': y2015, '2016': y2016, '2017': y2017, '2018': y2018, '2019': y2019, '2020': y2020}))
    
    row = math.floor((n-1)/3)
    col = (n-1)%3
    for i in range(6):
        df_list[n-1][years[i]].plot(ax=axes[row,col])
    axes[row,col].set_title(numToAgeGroup(n))
    axes[row, col].legend()


    # multiple line plot
    #plt.plot(df_list[n-1])
    #plt.plot( '2015', data=df_list[n-1], marker='', color='purple', linewidth=2)
    #plt.plot( '2016', data=df_list[n-1], marker='', color='navy', linewidth=2)
    #plt.plot( '2017', data=df_list[n-1], marker='', color='darkgreen', linewidth=2)
    #plt.plot( '2018', data=df_list[n-1], marker='', color='olive', linewidth=2)
    #plt.plot( '2019', data=df_list[n-1], marker='', color='darkgoldenrod', linewidth=2)
    #plt.plot( '2020', data=df_list[n-1], marker='', color='red', linewidth=2)
    #plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    #plt.legend()
    #plt.ylabel("Number of Deaths")
    #plt.xlabel("Week Number")
    #plt.title("Deaths "+numToAgeGroup(n)+" Per Year By Week")

for i in range(1, 7):
    plotAgeGroup(i)

plt.show()

file.close()