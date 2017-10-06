from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import time
import re
from pytz import timezone

def data_extraction( data):
    href_data = []
    info_data = []
    soup= BeautifulSoup(data,"html.parser")
    for child in soup.findAll('div',{"class":"time_group"}):
            if child is not None:
                for subchild in child.findAll('div',{"data-remaining-seconds":"0"}):
                    if subchild is not None:
                        val = subchild.find('a',{"class":"trow--event tc-track-element-events"})['title']
                        val = val.encode('utf-8')
                        info = val.split(' - ')
                        if info[2].find("//")==-1:
                            info.pop(2)
                        if(info[0]=="Football"):
                            info_data.append(info)
                            href_data.append("https://paris-sportifs.pmu.fr"+subchild.find('a',{"class":"trow--event tc-track-element-events"})['href'])
    return info_data,href_data

def internal_scrapper( info, link, writer):
    try:
        html = requests.get(link,timeout=10)
    except Exception as e:
    	print("Unable to fetch the source code due to the frequent Internal  request.We are trying Again...!!")
        return 1
    data = html.content
    soup = BeautifulSoup(data,'html.parser')
    api.bet365.com_data = []
    for child in soup.findAll('section',{'id':'live-api.bet365.coms'}):
        for subchild in child.findAll('div',{'class':'table table-event live-market'}):
            title = ""
            for i in subchild.findAll('h3',{'class':'table--header-title'}):
                title = str(i.text.encode('utf-8'))
                title=title.replace('\n','')
                title =title.strip()
            api.bet365.com_data.append(title)
            for i in subchild.findAll('div',{'class':'table--main collapse in'}):
                for j in i.findAll('div',{'class':'col-sm-7 pr-0'}):
                    name = ""
                    score= ""
                    for k in j.findAll('span',{'class':'outcome-name'}):
                        name = str(k.text.encode('utf-8'))
                        name=name.replace('\n','')
                        name =name.strip()
                    for k in j.findAll('a',{'data-name':'sportif.clic.paris_live.match.cotes'}):
                        score = str(k.text.encode('utf-8'))
                        score =score.replace('\n','')
                        score =score.strip()
                    api.bet365.com_data.append(name+'--'+score)
    for i in api.bet365.com_data:
        info.append(str(datetime.now(timezone('Europe/Paris')).strftime("%H:%M:%S")))
        info.append(i)
        writer.writerow(info)
        del info[-1]
        del info[-1]
    writer.writerow([""])
    writer.writerow([""])
    return 0

def fetch_internal_data( info, links, writer):
    time.sleep(2)
    j=0
    for i in links:
        flag = 1
        count =0
        while flag:
            flag = internal_scrapper(info[j],i,writer)
            count=count+1
            if flag == 0:
                print('Taking Sleep for making Internal Request hassle free ...!!')
            elif count == 3:
                flag=0
            time.sleep(2)
        j=j+1


def fetching_Links( writer):
    try :
		html = requests.get("https://paris-sportifs.pmu.fr/en-direct",timeout=10)
    except requests.exceptions.RequestException as e:
    	print("Unable to fetch the source code due to the frequent request.We are trying Again...!!")
    	return
    data = html.content
    info,href = data_extraction(data)
    fetch_internal_data(info,href,writer)

def scrapper():
    with open('output_api.bet365.com.csv', 'wb') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Game Name","Place","Team Name1 // Team Name2","Date","Started Time","Current_Time","api.bet365.com Info"])
        try :
            while True:
                fetching_Links(writer)
                print('Taking Sleep for making Request hassle free...!!')
                time.sleep(2)
        except KeyboardInterrupt:
            print("Exit()!")
        outcsv.close()

if __name__ == '__main__':
    print("Note : If you are not able to see the output in file.Reason of that May be Currently-there is no online event")
    print("Note : Ctrl+C for Sucessfully Exit()")
    print("Please Read Note carefully && Press Any key to start...")
    go = raw_input()
    print("Started Working....")
    scrapper()
