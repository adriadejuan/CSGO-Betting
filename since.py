import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time

# THIS CODE WILL GET ALL GAMES AND TEAM STATS FROM dateBreak (EXCLUDED)  UNTIL TODAY
def gamesSinceDate(dateBreak):
    # YYYY-MM-DD
    name = "games_since_" + dateBreak + ".csv"
    arx = open(name, "w")

    a = 1

    # GET LINKS ------------------------------------------------------------------------------------

    offset = 0
    links = []

    url = "https://www.hltv.org/results?offset=" + str(offset) + "&stars=1"
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")

    partits = soup.findAll("div", {"class" : "result-con"})

    for k in partits:
        link_detall = k.a.get("href")
        link = "https://www.hltv.org" + link_detall
        links.append(link)


    for i in range(1,3):
        offset = i * 100

        url = "https://www.hltv.org/results?offset=" + str(offset) + "&stars=1"
        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        partits = soup.findAll("div", {"class" : "result-con"})

        for j in partits:
            link_detall = j.a.get("href")
            link = "https://www.hltv.org" + link_detall
            links.append(link)

    print("Links from ", len(links), " games were loaded.")

    print("Completed 1/2")

    # ---------------------------------------------------------------------------------------------------

    partitsCompletats = 0

    for x in links:

        rPartit = requests.get(x)
        soupPartit = BeautifulSoup(rPartit.content, "html.parser")

        # DATE
        data = soupPartit.findAll("div", {"class" : "date"})
        dataStr = data[0].string
        dataStr = dataStr.replace("1st ","1 ")
        dataStr = dataStr.replace("nd "," ")
        dataStr = dataStr.replace("rd "," ")
        dataStr = dataStr.replace("th "," ")
        fullDate = datetime.strptime(dataStr, "%d of %B %Y")
        gameDate = str(fullDate)[0:10]

        if gameDate == dateBreak:
            break

        dateDayBeforeB = fullDate - relativedelta(days=1)
        dateDayBefore = str(dateDayBeforeB)[0:10]
        dateWeekBeforeB = fullDate - relativedelta(days=8)
        dateWeekBefore = str(dateWeekBeforeB)[0:10]
        dateMonthBeforeB = fullDate - relativedelta(months=1)
        dateMonthBefore = str(dateMonthBeforeB)[0:10]
        dateThreeMonthsBeforeB = fullDate - relativedelta(months=3)
        dateThreeMonthsBefore = str(dateThreeMonthsBeforeB)[0:10]

        # TEAMS
        equip = soupPartit.findAll("div", {"class" : "teamName"})
        equips = [equip[0].string, equip[1].string]

        # HOW MANY MAPS?
        mapholders = soupPartit.findAll("div", {"class" : "mapholder"})
        nMapholders = len(mapholders)

        # MAPS AND SCORES
        mapes = []
        scores = []
        for i in range(0, nMapholders):
            try:
                mapaSoup = soupPartit.findAll("div", {"class" : "mapname"})
                mapes.append(mapaSoup[i].string)
            except:
                mapes.append("")
                print("No ha trobat mapa ", i+1)
        for j in range(0, nMapholders*2):
            try:
                scoreSoup = soupPartit.findAll("div", {"class" : "results-team-score"})
                scores.append(scoreSoup[j].string)
            except:
                scores.append("-")
                print("No s'ha trobat marcador ", j+1)


        #STATS 1 WEEK, 1 MONTH, 3 MONTHS
        stats = []
        differentStartDates = [dateWeekBefore, dateMonthBefore, dateThreeMonthsBefore]
        for i in range(0,3):
            startDate = differentStartDates[i]
            urlStats = "https://www.hltv.org/stats/teams?startDate=" + startDate + "&endDate=" + dateDayBefore + "&rankingFilter=Top30"
            rStats = requests.get(urlStats)
            soupStats = BeautifulSoup(rStats.content, "html.parser")

            for j in range(0,2):
                try:
                    stats.append(str(soupStats.find(text=equip[j].string).findNext('td').contents[0]))
                    stats.append(str(soupStats.find(text=equip[j].string).findNext('td').findNext('td').contents[0]))
                    stats.append(str(soupStats.find(text=equip[j].string).findNext('td').findNext('td').findNext('td').contents[0]))
                    stats.append(str(soupStats.find(text=equip[j].string).findNext('td').findNext('td').findNext('td').findNext('td').contents[0]))
                except:
                    stats.append("")
                    stats.append("")
                    stats.append("")
                    stats.append("")

        # GENERATE DOCUMENT
        if nMapholders == 1:
            arx.write(str(gameDate) + "," + str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + str(mapes[0]) + "," + str(scores[0]) + "," + str(scores[1]) + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")

        if nMapholders == 3:
            arx.write(str(gameDate) + ","+str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + str(mapes[0]) + "," + str(scores[0]) + "," + str(scores[1]) + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")
            arx.write(str(gameDate) + "," + str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + str(mapes[1]) + "," + str(scores[2]) + "," + str(scores[3]) + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")
            arx.write(str(gameDate) + "," + str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + str(mapes[2]) + "," + str(scores[4]) + "," + str(scores[5]) + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")

        partitsCompletats = partitsCompletats + 1
        print(partitsCompletats)

        time.sleep(1)

    arx.close()
    print("Completed 2/2")