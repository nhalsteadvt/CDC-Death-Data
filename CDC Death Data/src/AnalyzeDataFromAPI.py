import requests
import lxml.html as lh
import matplotlib.pyplot as plt
import math
import pandas as pd

jurisdiction = "United%20States"
years = ["2015", "2016", "2017", "2018", "2019", "2020"]
ages = ["Under 25 years", "25-44 years", "45-64 years", "65-74 years", "75-84 years", "85 years and older"]
weight = ["Unweighted", "Predicted%20(weighted)"]

dataset = []


class Entry:
    def __init__(self, year, week, agegroup, deaths):
        self.year = int(year)
        self.week = int(week)
        self.agegroup = str(agegroup)
        self.deaths = int(deaths)
            
    def format(self):
        ans = str(self.year)+": week "+str(self.week)
        ans+="\t|\tAge Group #"+str(getAgeGroupNum(self.agegroup))+": "+self.agegroup+"\t|\tDeaths: "+str(self.deaths)
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


def parseJSON(json, data):
    json = json.replace("[", "")
    json = json.replace("]", "")
    arr = json.split(",{")
    for ele in arr:
        fields = ["\"year\"", "\"week\"", "\"age_group\"", "\"number_of_deaths\""]
        #print("element: "+ele)
        for i in range(len(fields)):
            idx1 = ele.find(fields[i]) + len(fields[i]) + 2 #the '+ 3' is to skip over the ' :" ' in the JSON
            idx2 = ele[idx1:].find("\",\"") + idx1 # the - 1 is to skip over the closing quotation mark
            #print("indices for "+fields[i]+": "+str(idx1)+" - "+str(idx2))
            fields[i] = ele[idx1:idx2]
        temp = Entry(fields[0], fields[1], fields[2], fields[3])
        if(temp.week <= 52):
            dataset.append(temp)
        


# url = "https://data.cdc.gov/resource/y5bj-9g5w.json?$offset=0&type=Unweighted&jurisdiction="+jurisdiction+"&year="+years[0]+"&age_group="+ages[0].replace(" ", "%20")
# page = requests.get(url)
# doc = lh.fromstring(page.content)
# info = doc.xpath('text()')
#parseJSON(info[0], dataset)



for year in years:
    print("Parsing year "+year)
    for age in ages:
        age = age.replace(" ", "%20")
        url = "https://data.cdc.gov/resource/y5bj-9g5w.json?$offset=0&type="+weight[0]+"&jurisdiction="+jurisdiction+"&year="+year+"&age_group="+age
        #Create a handle, page, to handle the contents of the website
        page = requests.get(url)
        #Store the contents of the website under doc
        doc = lh.fromstring(page.content)
        info = doc.xpath('text()')
        parseJSON(info[0], dataset)


for data in dataset:
    print(data.format())




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
    for T in list:
            ans.append(T.deaths)

    #below is used to chop off everything after week 48 for 2020
    #this was originally done due to the dynamic dataset the CDC supplies
    #meaning, the ending weeks of 2020 were incomplete and therefore drastically lower numbers were found
    #this threw off the scaling of the chart due to incomplete data

    # if(year!=2020):
    #     for T in list:
    #         ans.append(T.deaths)
    # else:
    #     for i in range(49):
    #         ans.append(list[i].deaths)
    #     while(len(ans) < 52):
    #         ans.append(list[48].deaths)
    return ans



nrow = 2
ncol = 3
fig, axes = plt.subplots(nrow, ncol)

df_list = []
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