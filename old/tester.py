import subprocess as sp

print('Testing Rent Cabin...')
username = 'user1'
password = 'pass123'
reserve = ['', 'free']

def run():
	for month in range(1, 2):
		for day in range(30):
			for halfhour in range(16, 32):
				sp.run(['python3', 'rentcabin.py', username, password, str(month), str(day), str(halfhour/2), reserve[0]])
#run()

def reserveday():
	for halfhour in range(16, 32):
		sp.run(['python3', 'rentcabin.py', username, password, str(1), str(1), str(halfhour/2), reserve[0]])
reserveday()
