import random

with open("./analysis/test.txt",'w') as f:
    ran_number = random.randrange(1000)
    f.write(str(ran_number))