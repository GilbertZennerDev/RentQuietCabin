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
import sys

print('program for renting the cabin')

class RentCabin():
	def initday(self): return ['0' for i in range(8 * 2)]
	def initmonth(self, days): return [self.initday() for i in range(days)]
	def inityear(self): return [self.initmonth(self.dayspermonth[i]) for i in range(12)]
	
	def __init__(self):
		self.dayspermonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.dayssum = [0, 31, 59, 90, 120, 151, 181,  212, 243, 273, 304, 334, 365]
		self.year = self.inityear()
		self.dateset = False
		self.skipdaymonth = False
		self.skipinpt = False
	
	def check(self):
		if (self.inpt - int(self.inpt)) not in [0, 0.5]:
			print('Only full hour or half-hour allowed: 8 or 8.5');exit()
		if int(self.inpt) >= 16 or int(self.inpt) < 8:
			print('Outside of allowed times: 8-15.5');exit()
	def loadtimes(self):
		data = open('times.txt', 'r').read().splitlines()
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

	def reserve(self):
		try:
			halfhour = self.getindexfromtime()
			if not int(self.year[self.month][self.day][halfhour]):
				self.year[self.month][self.day][halfhour] = '1';
				print('Half-Hour', self.reservedslot, 'reserved');
				return
			print('Error: Half-Hour already reserved')
		except Exception as e:
			print(e); print("bad input"); exit()

	def getindexfromtime(self):
		self.reservedslot = str(self.inpt) + '-' + str(self.inpt+.5)
		self.inpt -= 8
		if int(self.inpt) == self.inpt: return int(2*self.inpt)
		return int(2*int(self.inpt) + 1)
		
	def getint(self, value, what='day'):
		if what == 'day': return int(value)-1
		return int(value)-1

	def getday(self):
		if self.skipinpt: return
		try:
			if not self.skipdaymonth:
				getint(input("Enter Month: "), 'month')
				getint(input("Enter Day: "))
#				self.month = int(input("Enter Month: "))-1
#				self.day = int(input("Enter Day: "))-1
			self.getfreehalfhours()
			self.inpt = float(input("Enter time to reserve: ").replace(',','.'))
		except: exit()

	def getfreehalfhours(self):
		for h, half in enumerate(self.year[self.month][self.day]):
			if not int(half): print('Half-Hour Slot', str(8+h*.5), '-', str(8+(h+1)*.5), 'is free')
	
	def auth(self):
		users = [{'name':'user1', 'password': 'pass123'},{'name':'user2', 'password': 'pass123'}]
		for user in users:
			if len(sys.argv) >= 3 and user['name'] == sys.argv[1] and user['password'] == sys.argv[2]: 
				if len(sys.argv) >= 5: 
					self.month = self.getint(sys.argv[3], 'month'); self.day = self.getint(sys.argv[4]); self.skipdaymonth = True
					if len(sys.argv) == 6:
						self.inpt = float(sys.argv[5].replace(',','.')); self.skipinpt = True
				print(sys.argv[1], 'authed successfully'); return
		print('Auth failed'); exit()
	
	def run(self):
		try: self.loadtimes(); self.auth(); self.getday(); self.check(); self.reserve(); self.savetimes()
		except: exit()

rc = RentCabin()
rc.run()
