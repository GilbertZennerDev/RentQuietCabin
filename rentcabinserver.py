'''
the idea is to allow people to rend the cabin for specific time at a specific date via a website
so I need to be able to serve time units to people
Let's start with 1 hour time:
I split up each day to 8 hours and put a boolean: True (reserved), False (not reserved)

RentCabin:
initday
initmonth
inityear
__init__
reserve
getindexfromtime
getday
getfreehalfhours
loadtimes
savetimes
auth
run

today I change my tactics: only 1 slot allowed per person.
also I need to free a slot if it is removed by the user. so not just st.session_state['slot'] but also times
'''
import sys, streamlit as st, datetime, sqlite3
from handledb import HandleDb

print('program for renting the cabin')

class RentCabin():
	def initday(self): return ['0' for i in range(8 * 2)]
	def initmonth(self, days): return [self.initday() for i in range(days)]
	def inityear(self): return [self.initmonth(self.dayspermonth[i]) for i in range(12)]
	
	def __init__(self):
		self.dayspermonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.dayssum = [0, 31, 59, 90, 120, 151, 181,  212, 243, 273, 304, 334, 365]
		self.monthnames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		self.year = self.inityear()
		self.hdb = HandleDb()
#		self.hdb.createtable()
		if 'loggedin' not in st.session_state: st.session_state['loggedin'] = False

	def loadtimes(self):
		try: data = open('times.txt', 'r').read().splitlines();
		except: self.year = self.inityear(); self.savetimes(); print('times.txt generated. Run again to reserve/free'); exit()

		data = [line for line in data if 'Month' not in line]
		months = [data[self.dayssum[i]:self.dayssum[i+1]] for i in range(12)]
		for month in range(12):
			for d, day in enumerate(months[month]):
				day = day.replace(' ', '')
				for h, hour in enumerate(day):
					self.year[month][d][h] = hour
	def savetimes(self):
		getday = lambda month, day: " ".join(self.year[month][day])
		getmonth = lambda month: 'Month\n' + "\n".join([getday(month, i) for i in range(self.dayspermonth[month])])
		getyear = lambda: "\n".join([getmonth(i) for i in range(12)])
		open('times.txt', 'w').write(getyear())
		
	def reserve(self, mode='reserve'):
		try:
			if mode == 'reserve':
				if not int(self.year[self.month][self.day][self.halfhour]):
					self.year[self.month][self.day][self.halfhour] = st.session_state['username'];
					print('Half-Hour', self.reservedslot, 'reserved');
					self.savetimes()
					self.saveslot()
					st.rerun()
					return
				print('Error: Half-Hour already reserved'); return
			#else: free
			data = st.session_state['slot'].split('.')
			self.month = int(data[0])
			self.day = int(data[1])
			self.halfhour = int(data[2])
			self.year[self.month][self.day][self.halfhour] = '0';
			self.savetimes()
			st.session_state['slot'] = ''
			self.hdb.updateslot(st.session_state['username'], None)
		except Exception as e:
			print(e); print("bad input"); exit()
	
	def getindexfromtime(self):
		self.reservedslot = str(self.inpt) + '-' + str(self.inpt+.5)
		self.inpt -= 8
		if int(self.inpt) == self.inpt: return int(2*self.inpt)
		return int(2*int(self.inpt) + 1)
		
	def asknamepwd(self):
		st.session_state["username"] = st.text_input('Username')
		st.session_state["pwd"] = st.text_input('Password', type='password')
		st.session_state["email"] = st.text_input('Email')
	
	def login(self):
		if self.hdb.printuser(st.session_state["username"]) is not None:
			st.success('Logged In'); st.session_state["loggedin"] = True; st.rerun()
		st.write('Login Failed'); return
	
	def register(self):
		self.hdb.register(st.session_state["username"], st.session_state["pwd"], st.session_state["email"])
		st.rerun()

	def logout(self):
		st.session_state["loggedin"] = False
		st.success('You logged out')
		st.rerun()
	
	def auth(self):
		self.loadtimes()
		self.asknamepwd()
		if st.button('Login'): self.login()
		if st.button('Register'): self.register()
		
	def on_click(self, item):
		self.inpt = float(item)
		self.halfhour = self.getindexfromtime()
		self.reserve()
		st.rerun()
	
	def getprintableslot(self, date):
		date = date.split('.')
		if len(date) != 3: return 'empty'
		return self.monthnames[int(date[0])]+'/'+str(int(date[1])+1)+' Slot: '+str(8+int(date[2])*.5)
	
	def remove_slot(self, date):
		self.reserve('free')
		st.rerun()
	
	def showslots(self):
		try:
			self.loadslot()
			if not len(st.session_state['slot']) : st.write('No Slot reserved'); return
		except: return
		st.write('Click on Slot to free')
		#cols = st.columns(len(st.session_state['slot']))
		#for col, slot in zip(cols, st.session_state['slot']):
		#	if col.button(self.getprintableslot(st.session_state['slot']), use_container_width=True): self.remove_slot(st.session_state['slot'])
		if st.button(self.getprintableslot(st.session_state['slot'])): self.remove_slot(st.session_state['slot'])
		
	def showdatepicker(self):
		# Get today's date
		today = datetime.date.today()
		# Define the maximum date (1 month ahead)
		three_months_ahead = today + datetime.timedelta(days=90)
		# Single date picker
		date = st.date_input("Pick a date", value=today, min_value=today, max_value=three_months_ahead)
		self.month = int(str(date).split('-')[1])-1
		self.day = int(str(date).split('-')[2])-1
		self.loadtimes()
		halfs = [str(8+i*.5) for i, half in enumerate(self.year[self.month][self.day]) if not int(half)]
		if not len(halfs): st.write("No free slots available that day!"); return		
		cols = st.columns(len(halfs))
		for col, half in zip(cols, halfs):
			if col.button(half, use_container_width=True): self.on_click(half)
		
	def server(self):
		st.set_page_config(layout="wide")
		if st.session_state["loggedin"] and st.button('Logout'): self.logout()
		if not st.session_state["loggedin"]: self.auth(); return
		self.showslots()
		if st.session_state["slot"] is None: self.showdatepicker()

	
	def loadslot(self):
		try: st.session_state['slot'] = self.hdb.getslot(st.session_state['username'])
		except: st.session_state['slot'] = ''
		
	def saveslot(self):
		st.session_state['slot'] = str(self.month)+'.'+str(self.day)+'.'+str(self.halfhour)
		self.hdb.updateslot(st.session_state['username'], st.session_state['slot'])
		st.rerun()
		
rc = RentCabin()
rc.server()
