import matplotlib.pyplot as plt
import numpy as np

n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
count = [57, 72, 94, 117, 137, 161, 190, 209, 264, 273, 300, 348, 368, 379, 385]

equation = "25.76*N + 17.45"
N = np.array(n)

plt.plot(n, count, marker='o', label='Experimental results')
plt.plot(N, eval(equation), label='Linear Approximation')
plt.xlabel("Number of nodes")
plt.ylabel("Number of received packets")
plt.legend(loc='best')
plt.savefig("secarp_flood_receive.png")
plt.show()

