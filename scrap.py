from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import time
import re
from pytz import timezone
'''
Real-time scrapping
'''

def time_period(start,current):
	start_hour = int(start[:start.find('h')])
 	start_minute =int(start[start.find('h')+1:])
	current_hour = int(current[:current.find(':')])
	current_minute = int(current[current.find(':')+1:])
	period = ""
	if start_hour == 0:
		start_hour = 24
	if current_hour == 0:
		current_hour = 24
	if start_hour > current_hour:
		hour =24-start_hour+current_hour
	else:
		hour = current_hour-start_hour
 	minute= abs(current_minute-start_minute)
	period=str(hour)+':'+str(minute)
	return period

def scrapper():

	def sub_scrapper(writer):
		try :
			html = requests.get("https://paris-sportifs.pmu.fr/en-direct")
		except requests.exceptions.RequestException as e:
			print("Unable to fetch the source code due to the frequent request.We are trying Again...!!")
			return
		data = html.content
		soup= BeautifulSoup(data,"html.parser")
		current_date = str(datetime.now(timezone('Europe/Paris')).strftime("%Y-%m-%d"))
		#for i in soup.findAll('div',{"data-date":current_date}):
		for j in soup.findAll('div',{"class":"time_group"}):
				if j is not None:
					for l in j.findAll('div',{"data-remaining-seconds":"0"}):
						if l is not None :
							val = l.find('a',{"class":"trow--event tc-track-element-events"})['title']
							val = val.encode('utf-8')
							data= val.split(' - ')
							if data[2].find("//")==-1:
								data.pop(2)
							for m in l.findAll('span',{"class":"trow--event--score"}):
								if m.find('span',{"class":"score-both"}) is not None:
									 m=str(m.text).replace("\n","")
									 data.append(m)
									 break
								else:
									score = ""
									score =str(m.find('span',{"class":"score-home"}).text).replace("\n","")
									score=score+" "
									score = score+str(m.find('span',{"class":"score-away"}).text).replace("\n","")
									data.append(score)
							cote = ""
							count = 0
							for m in l.findAll('li',{"class":"col-sm-3 trow--odd--item"}):
								if m.find('a',{"data-name":"sportif.clic.paris_live.cote"}) is not None:
									cote= cote+str(m.find('a',{"data-name":"sportif.clic.paris_live.cote"}).text).replace('\n','')
									cote = re.sub('[\s+]', '', cote)
									if(count!=2):
										cote=cote+"-"
								count = count+1
							data.append(cote)
							data.append(str(datetime.now(timezone('Europe/Paris')).strftime("%H:%M:%S")))
							data.append(unicode(time_period(str(data[4]),str(datetime.now(timezone('Europe/Paris')).strftime("%H:%M"))),'utf-8'))
							visitor = ""
							for m in l.findAll('a',{"data-name":"sportif.clic.paris_live.nb_paris"}):
								visitor = str(m.text).replace('\n','')
								visitor = re.sub('[\s+]', '',visitor)
							visitor='+'+visitor
							visitor = unicode(visitor,'utf-8')
							data.append(visitor)
							href = l.find('a',{"class":"trow--event tc-track-element-events"})['href']
							href = "https://paris-sportifs.pmu.fr/en-direct"+href
							data.append(href)
							stat_href = "None"
							channel_name = "None"
							data_ev_status =""
							data_ev_displayed =""
							data_ev_mkt_status = ""
							for child in l.findAll('div',{"class":"obet365-event-list-grid-formatter-col col-rows col-xs-2"}):
								for subchild in child.findAll('div',{"class":"col-sm-3 obet365-event-list-grid-formatter-col trow--meta--item"}):
									for m in subchild.findAll('a',{"title":"Statistiques"}):
										onclick = m['onclick']
										stat_data = re.findall("'([^\"]*)'",onclick)
										stat_url = stat_data[0].split(',')[0]
										stat_url = stat_url.replace('\'','')
							 			stat_href = stat_url
									for m in subchild.findAll('div',{"class":"bet365-meta-live-active"}):
										if m['title']:
											channel_name = m['title']
							try :
								data_ev_status =l['data-ev_status']
							except Exception as e:
								data_ev_status = "None"
							try :
								data_ev_displayed =l['data-ev_displayed']
							except Exception as e:
								data_ev_displayed = "None"
							for child in l.findAll('div',{'class':'obet365-event-list-grid-formatter-col col-rows col-xs-3'}):
								for subchild in child.findAll('div',{'class':'col-sm-12 obet365-event-list-grid-formatter-col event-list-odds-wrapper'}):
									try:
										data_ev_mkt_status=subchild['data-ev_mkt_status']
									except Exception as e:
										data_ev_mkt_status="None"
							data.extend([stat_href,channel_name,data_ev_status,data_ev_displayed,data_ev_mkt_status])
							writer.writerow(data)

	with open('output.csv', 'wb') as outcsv:
		writer = csv.writer(outcsv)
		writer.writerow(["Game Name","Place","Team Name1 // Team Name2","Date","Started Time","Score-Both","1 N 2",
		"Time","Period_Of_Match(H:M)","Visitor","Match_bet365_Link","Match_Statistics_Link","Channel_Name","data-ev-status",
		"data-ev_displayed","data-ev_mkt_status"])
		try :
			while(True):
				#st =time.clock()
				sub_scrapper(writer)
				print('Taking Sleep for making Request hassle free...!!')
				time.sleep(0.0001)
				#print(time.clock()-st)
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
