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

	def loadtimes(self):
		try: data = open('times.txt', 'r').read().splitlines()
		except: self.year = self.inityear(); self.savetimes(); self.loadtimes(); print('times.txt generated. Run again to reserve/free'); exit()

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
	
	def login(self, usrname, pwd):
		for usr in [{'name':'', 'password': ''},{'name':'user1', 'password': 'pass123'},{'name':'user2', 'password': 'pass123'}]:
			if usr['name'] == usrname and usr['password'] == pwd: st.write('Logged In'); st.session_state["loggedin"] = True; st.rerun(); return
		st.write('Login Failed'); return

	def logout(self):
		st.session_state["loggedin"] = False
		st.write('You logged out')
		st.rerun()
	
	def auth(self):
		if "loggedin" not in st.session_state: st.session_state["loggedin"] = False
		usrname = st.text_input('Username')
		pwd = st.text_input('Password', type='password')
		if not st.session_state["loggedin"] and st.button('Login'): self.login(usrname, pwd)
		
	def on_click(self, item):
		self.inpt = float(item)
		self.halfhour = self.getindexfromtime()
		st.write('debug item:', item, '.')
		self.reserve('reserve', True)
		self.savetimes()
		self.loadtimes()
		st.rerun()
	
	def freeaslot(self):
		pass
		
	def server(self):
		self.auth()
		if st.session_state["loggedin"]:
			if st.button('Logout'): self.logout()
			if st.button('free a slot'): self.freeaslot()
		else: return
		# Single date picker
		date = st.date_input("Pick a date", datetime.date.today())
		self.month = int(str(date).split('-')[1])-1
		self.day = int(str(date).split('-')[2])-1
		self.loadtimes()
		halfs = [str(8+i*.5) for i, half in enumerate(self.year[self.month][self.day]) if not int(half)]
		if not len(halfs): st.write("No free slots available that day!"); return		
		st.set_page_config(layout="wide")
		cols = st.columns([3] * len(halfs))
		for col, half in zip(cols, halfs):
			if col.button(half, use_container_width=True): self.on_click(half)

rc = RentCabin()
rc.server()
