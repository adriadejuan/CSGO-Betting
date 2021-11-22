import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date
import time

# THIS CODE WILL GET ALL STATS FOR TODAY'S GAMES
def gamesToday():

    arx = open("games_" + str(date.today()) + ".csv", "w")

    a = 1

    # GET LINKS
    offset = 0
    links = []

    url = "https://www.hltv.org/matches?predefinedFilter=top_tier"
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")

    partits = soup.findAll("div", {"class" : "upcomingMatchesSection"})

    for k in partits:
        for i in k:
            try:
                link_detall = i.a.get("href")
                link = "https://www.hltv.org" + link_detall
                links.append(link)
            except:
                pass

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

        if gameDate != str(date.today()):
            continue

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

        # HOW MANY GAMES?
        mapholders = soupPartit.findAll("div", {"class" : "mapholder"})
        nMapholders = len(mapholders)

        # STATS 1 WEEK, 1 MONTH, 3 MONTHS
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

        # GENERAR DOCUMENT
        if nMapholders == 1:
            arx.write(str(gameDate) + "," + str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + "," + "," + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")

        if nMapholders == 3:
            arx.write(str(gameDate) + "," + str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + "," + "," + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")
            arx.write(str(gameDate) + "," + str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + "," + "," + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")
            arx.write(str(gameDate) + "," + str(x) + "," + str(equips[0]) + "," + str(equips[1]) + "," + "," + "," + ",")
            for i in stats:
                arx.write(i)
                arx.write(",")
            arx.write("\n")

        time.sleep(3)

    arx.close()