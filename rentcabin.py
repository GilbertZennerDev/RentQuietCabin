'''
the idea is to allow people to rend the cabin for specific time at a specific date via a website
so I need to be able to serve time units to people
Let's start with 1 hour time:
I split up each day to 8 hours and put a boolean: True (reserved), False (not reserved)
'''
import sys

print('program for renting the cabin')

class RentCabin():
	def initday(self): return [False for i in range(8 * 2)]
	def initmonth(self, days): return [self.initday() for i in range(days)]
	def inityear(self): return [self.initmonth(self.dayspermonth[i]) for i in range(12)]
	
	def __init__(self):
		self.dayspermonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.year = self.inityear()

	def reserve(self, month, day, hour):
		try:
			if not self.year[month][day][hour]: self.year[month][day][hour] = True; print('Half-Hour', hour, 'reserved'); return
			print('Error: Half-Hour already reserved')
		except Exception as e:
			print(e)
			exit()

	def show(self, what='free'):
		if what == 'free':
			for halfhour in range(8 * 2):
				if not self.year[0][0][halfhour]: print('HalfHour', 8+halfhour*.5, 'is free')
	def getindexfromtime(self, giventime):
		#time will be 8 or 8.5. must be converted to 8 or 9. until 15.30 -> 16
		# 8 -> 0, 8.5 -> 1, 9 -> 2, 9.5 -> 3, 10 -> 4, 10.3 -> 5
		# 9 -> 8*
		giventime -= 8
		print(giventime, int(2*giventime), int(2*giventime + 1))
		if int(giventime) == giventime:
			return int(2*giventime)
		return int(2*int(giventime) + 1)
				
	def run(self):
		inpt = ''
		while inpt != 'exit':
			inpt = input("Enter time to reserve: ")
			if inpt != 'exit':
				try:
					self.inpt = float(inpt)
					self.reserve(0,0,self.getindexfromtime(self.inpt))
				except Exception as e:
					print(e)
rc = RentCabin()
#rc.reserve(0, 0, 0)
#rc.reserve(0, 0, 0)
#rc.reserve(0, 0, 1)
#rc.reserve(0, 0, 1)
#rc.show('free')
rc.run()
