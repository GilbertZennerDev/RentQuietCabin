data = open('times.txt', 'r').read().replace('1', '0')
open('times.txt', 'w').write(data)
