import pdb
import Tkinter
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt




def error(f, x, y):
    return sp.sum((f(x)-y)**2)


pdb.set_trace()

data = sp.genfromtxt('data/web_traffic.csv', delimiter=',')
#print(data[:10])
#print(data.shape)

#seperate array into two vectors
x = data[:,0]
y = data[:,1]

print sp.sum(sp.isnan(y))

#remove nan value in y
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

#print x
#print y

plt.scatter(x,y)
plt.title('web traffic over the last month')
plt.xlabel('Time')
plt.ylabel('Hits/Hour')
plt.xticks([w*7*24 for w in range(10)], ['week %i'%w for w in range(10)])
plt.autoscale(tight=True)
plt.grid()
#plt.show()

# y=ax+b
# fp1=(a,b)
# 
fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
f1 = sp.poly1d(fp1)
print "f1=%s" % f1
print error(f1, x, y)

fx = sp.linspace(0, x[-1], 1000)
plt.plot(fx, f1(fx), linewidth=4, color='g')
plt.legend(["d=%i" % f1.order], loc="upper left")


f2p = sp.polyfit(x, y, 2)
f2 = sp.poly1d(f2p)
print "f2=%s" % f2
print error(f2, x, y)

fx = sp.linspace(0, x[-1], 1000)
plt.plot(fx, f2(fx), linewidth=4, color='r')
plt.legend(["d=%i" % f2.order], loc="upper left")


f3p = sp.polyfit(x, y, 3)
f3 = sp.poly1d(f3p)
print "f3=%s" % f3
print error(f3, x, y)

fx = sp.linspace(0, x[-1], 1000)
plt.plot(fx, f3(fx), linewidth=4, color='b')
plt.legend(["d=%i" % f3.order], loc="upper left")


f100p = sp.polyfit(x, y, 100)
f100 = sp.poly1d(f100p)
print "f100=%s" % f100
print error(f100, x, y)

fx = sp.linspace(0, x[-1], 1000)
plt.plot(fx, f100(fx), linewidth=4, color='y')
plt.legend(["d=%i" % f100.order], loc="upper left")
plt.show()

