import os
import random
chars = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm"

L = 5
k1 = ""
k2 = ""
k3 = ""
for i in range (L):
     k1 +=random.choice(chars)
     k2 +=random.choice(chars)
     k3 +=random.choice(chars)
print(k1 + "-" + k2 + "-" + k3)
os.system("pause")
