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
check
reserve
getindexfromtime
getday
getfreehalfhours
loadtimes
savetimes
auth
run
'''
import sys, streamlit as st, datetime

print('program for renting the cabin')

class RentCabin():
	def initday(self): return ['0' for i in range(8 * 2)]
	def initmonth(self, days): return [self.initday() for i in range(days)]
	def inityear(self): return [self.initmonth(self.dayspermonth[i]) for i in range(12)]
	
	def __init__(self):
		self.dayspermonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.dayssum = [0, 31, 59, 90, 120, 151, 181,  212, 243, 273, 304, 334, 365]
		self.year = self.inityear()
		self.usrname = ''
		self.pwd = ''
		self.mayreserve = False
		self.userslots = [{'date':'1.1.8'}, {'date':'1.1.9'}]
		if 'username' not in st.session_state: st.session_state["username"] = 'unknown';

	def loadtimes(self):
		try: data = open('times.txt', 'r').read().splitlines();# userdata = open('userslots.txt', 'r').read()
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
		
	def reserve(self, mode='reserve', served=False):
		if not served: self.halfhour = self.getindexfromtime()
		try:
#			halfhour = self.getindexfromtime()
			if mode == 'reserve':
				if not int(self.year[self.month][self.day][self.halfhour]):
					self.year[self.month][self.day][self.halfhour] = '1';
					print('Half-Hour', self.reservedslot, 'reserved');
					self.updateuserfile()
					return
				print('Error: Half-Hour already reserved'); return
			self.year[self.month][self.day][self.halfhour] = '0';
			print('Half-Hour', self.reservedslot, 'freed');
			return
		except Exception as e:
			print(e); print("bad input"); exit()
	
	def getindexfromtime(self):
		self.reservedslot = str(self.inpt) + '-' + str(self.inpt+.5)
		self.inpt -= 8
		if int(self.inpt) == self.inpt: return int(2*self.inpt)
		return int(2*int(self.inpt) + 1)
	
	def login(self):
		for usr in [{'name':'', 'password': ''},{'name':'1', 'password': ''},{'name':'user1', 'password': 'pass123'},{'name':'user2', 'password': 'pass123'}]:
			if usr['name'] == self.usrname and usr['password'] == self.pwd:
				st.success('Logged In'); st.session_state["loggedin"] = True; st.session_state["username"] = self.usrname; st.session_state["pwd"] = self.pwd; st.rerun(); return
		st.write('Login Failed'); return

	def logout(self):
		st.session_state["loggedin"] = False
		st.write('You logged out')
		st.rerun()
	
	def auth(self):
		self.usrname = st.text_input('Username')
		self.pwd = st.text_input('Password', type='password')
		if not st.session_state["loggedin"] and st.button('Login'): self.login()
		
	def on_click(self, item):
		self.inpt = float(item)
		self.halfhour = self.getindexfromtime()
		self.reserve('reserve', True)
		self.savetimes()
		self.loadtimes()
		st.rerun()
	
	def getprintableslot(self, date):
		date = date.split('.')
		return 'Month: '+date[1]+' Day: '+date[2]+' Slot: '+date[2]
	
	def remove_slot(self, date):
		self.userslots = [s for s in self.userslots if s['date'] != date]
		st.rerun()
	
	def showslots(self):
		self.loaduserslots()
		if len(self.userslots) == 1 and self.userslots[0] == '' : st.write('No slots reserved yet'); return
		st.write('Click on Slot to free')
		cols = st.columns(len(self.userslots))
		for col, slot in zip(cols, self.userslots):
			if col.button(self.getprintableslot(slot['date']), use_container_width=True): self.remove_slot(slot['date'])
		
	def showdatepicker(self):
		# Single date picker
		date = st.date_input("Pick a date", datetime.date.today())
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
		if "loggedin" not in st.session_state: st.session_state["loggedin"] = False
		if st.session_state["loggedin"]:
			if st.button('Logout'): self.logout()
			if self.mayreserve: self.showdatepicker()
			else: st.write('You have reserved 2/2 of your slots!')
			self.showslots()
		else: self.auth(); return
	
	def loaduserslots(self):
		try: self.userslots2 = open(st.session_state['username']+'.txt', 'r').read().split('-'); self.userslots = [{'date': self.userslots2[i].strip()} for i in range(len(self.userslots2))];
		except: self.userslots = []
	
	def updateuserfile(self):
		print('Saving Userfile', st.session_state['username'], '.txt')
		open(st.session_state['username']+'.txt', 'w').write('-'.join([s['date'] for s in self.userslots]))
		

rc = RentCabin()
rc.server()
#rc.updateuserfile()
