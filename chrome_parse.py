#Chrome Parser
#Author: Mari DeGrazia
#http://az4n6.blogspot.com/
#arizona4n6@gmail.com
#
#This will parse the Google Chrome Internet and Download history from the Google Chrome history database
#The "History" file is located under: C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default
#usage: chrome_parse -f -r History >> output.tsv
#
#
#This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can view the GNU General Public License at <http://www.gnu.org/licenses/>
#
# Version History:
# v1.0 08/19/2016



import argparse
import sqlite3 as lite
import datetime
import os
import calendar
import time


parser =  argparse.ArgumentParser(description='This will parse the history and download files from ')
parser.add_argument('-f', '--file', dest="database",help="Path to Chrome History file",required=True)
parser.add_argument('-t', '--tln', action ='store_true',dest="tln",help="TLN format",required=False,default=False )
parser.add_argument('-r', '--history', action ='store_true',dest="history",help="Parse visited URLs",default=False,required=False)
parser.add_argument('-d', '--downloads',action ='store_true', dest="downloads",help="Parse downloaded files",required=False,default=False)
parser.add_argument('-s', '--hostname', dest="host",help="Optional hostname for TLN format",required=False,default="")
parser.add_argument('-u', '--username', dest="user",help="Optional username for TLN format",required=False,default="")


args = parser.parse_args()
db=args.database

def toEpoch(date_string):
	#use calendar.timegm as the date_string passed is in UTC
	epoch = calendar.timegm(time.strptime(date_string, "%Y-%m-%d %H:%M:%S"))
	return epoch 
count = 0

con = lite.connect(db)

with con:	
	cur = con.cursor()
	if(args.history):
		
		sql = "SELECT url, title, visit_count,datetime(urls.last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') AS last_visit from urls"
		cur.execute(sql)
		try:
			cur.execute(sql)
		except:
			print "Error executing SQL. May not be a valid sqlite database, or may not contain the proper fields."
			print "Error may also occur with older versions of sqlite.dll on Windows. Update instructions here: https://deshmukhsuraj.wordpress.com/2015/02/07/windows-python-users-update-your-sqlite3/ "
			exit()
		
		rows = cur.fetchall()
		if not args.tln:
			print "Last Visit Time\tURL\tTitle\tVisit Count\tLast Visit Time(UTC)\n"
		for row in rows:
		
			if (args.tln):
				try:
					host
				except NameError:
					host = ""
				try:
					user
				except NameError:
					user = ""
				
				description = "[URL: " + row[0].encode('ascii','ignore') + "] [Title: " + row[1].encode('ascii','ignore') + "] [Visits: " + str(row[2]) + "]"
				
				print str(toEpoch(row[3])) + "|Chrome History|" + host + "|" + user + "|" + description
				
			else:
				
				visits = str(row[2])
				print row[3].encode('ascii','ignore') + "\t" + row[0].encode('ascii','ignore') + "\t" + row[1].encode('ascii','ignore') + "\t" + visits
				
				#print  + "\t" + row[1].encode('ascii','ignore') + "\t" + visits + "\t" + row[3].encode('ascii','ignore')
	if(args.downloads):
	
		sql = "SELECT current_path, target_path, total_bytes, received_bytes, opened, datetime(start_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') AS start_time,datetime(end_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch') AS end_time from downloads"
		cur.execute(sql)
		try:
			cur.execute(sql)
		except:
			print "Error executing SQL. May not be a valid sqlite database, or may not contain the proper fields."
			print "Error may also occur with older versions of sqlite.dll on Windows. Update instructions here: https://deshmukhsuraj.wordpress.com/2015/02/07/windows-python-users-update-your-sqlite3/ "
			exit()
		
		rows = cur.fetchall()
		if not args.tln:
			print "Current Path\tTarget Path\tTotal bytes\tReceived Bytes\tOpened\tStart Time\tEnd Time\n"
			
		for row in rows:
			if (args.tln):
					try:
						host
					except NameError:
						host = ""
					try:
						user
					except NameError:
						user = ""
					
					if row[4] == 1:
						opened = "True"
					else:
						opened = "False"
					description = "[Current Path: " + row[0].encode('ascii','ignore') + "] [Target Path: " + row[1].encode('ascii','ignore') + "] [Total Bytes: " + str(row[2])+ "] [Received Bytes: " + str(row[3]) + "] [Opened: " + opened + "]"
					
					print str(toEpoch(row[5])) + "|Chrome Downloads|" + host + "|" + user + "|" + "Start time " + description
					
					print str(toEpoch(row[6])) + "|Chrome Downloads|" + host + "|" + user + "|" + "End time " + description
			
					
		
			else:
				
				print row[0].encode('ascii','ignore') + "\t" + row[1].encode('ascii','ignore') + "\t" + str(row[2])+ "\t" + str(row[3]) + "\t" + str(row[4]) + "\t" +  str(row[5]) + "\t" + str(row[6])
		