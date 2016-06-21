from pylab import *
import math

def v0_theta0(v0, theta0):
	dt, g = 0.01, 9.8
	x, y, vx, vy = [0], [0], [], []
	vx_0 = v0*cos(theta0*pi/180)
	vy_0 = v0*sin(theta0*pi/180)
	vx.append(vx_0)
	vy.append(vy_0)
	while y[-1] >= 0:
		tem_x = vx[-1]*dt + x[-1]
		tem_y = vy[-1]*dt + y[-1]
		v = (vx[-1])**2 + (vy[-1])**2
		ro = (1 - (6.5*10**(-3)*y[-1])/300)**2.5
		tem_vx = vx[-1] - ro*0.00004*vx[-1]*(v)**0.5*dt
		tem_vy = vy[-1] - ro*g*dt - 0.00004*vy[-1]*(v)**0.5*dt
		x.append(tem_x)
		y.append(tem_y)
		vx.append(tem_vx)								
		vy.append(tem_vy)
	v0_t0 = [x[-1], y[-1], x , y ]
	return v0_t0
#print v0_theta0(700, 55)

def v0_theta0_y0(v0, theta0, y0):
	dt, g = 0.01, 9.8
	x, y, vx, vy = [0], [0], [], []
	vx_0 = v0*cos(theta0*pi/180)
	vy_0 = v0*sin(theta0*pi/180)
	vx.append(vx_0)
	vy.append(vy_0)
	while True:
		tem_x = vx[-1]*dt + x[-1]
		tem_y = vy[-1]*dt + y[-1]
		v = (vx[-1])**2 + (vy[-1])**2
		ro = (1 - (6.5*10**(-3)*y[-1])/300)**2.5
		tem_vx = vx[-1] - ro*0.00004*vx[-1]*(v)**0.5*dt
		tem_vy = vy[-1] - ro*g*dt - 0.00004*vy[-1]*(v)**0.5*dt
		x.append(tem_x)
		y.append(tem_y)
		vx.append(tem_vx)                               
		vy.append(tem_vy)
		if ((vy[-1] < 0) and (y[-1] < y0)):
			break
	v0_t0_y0 = [x[-1], y[-1]]
	return v0_t0_y0
#print v0_theta0_y0(700, 55, 3000)

def findmax(matrix):
	max_s, max_i = 0, 0
	min_s, min_i = 10**9, 0
	for i in range(len(matrix)):
		if matrix[i] > max_s:
			max_s = matrix[i]
			max_i = i
		if matrix[i] < min_s:
			min_s = matrix[i]
			min_i = i
		findm = [max_s, max_i, min_s, min_i]
	return findm

def findplace(matrix, target):
	place = []
	for i in range(len(matrix)):
		if matrix[i] > target:
			place.append(i-1)
			place.append(i)
			break
	return place

h = [0, 2, 4, 5]
#print findmax(h)
#print findplace(h, 3)

class shell:
	def __init__(self, x0 = 100., y0 = 100., xt = 200., yt = 200., dt = 0.01, g = 9.8, v0 = 700. ):
		self.x0, self.y0, self.xt, self.yt = x0, y0, xt, yt
		self.vx, self.vy, self.x, self.y = [], [], [], []
		self.dx = abs(xt - x0)
		self.dy = abs(yt - y0)
		self.dt = dt
		self.g = g
		self.v0 = v0
	
	def update(self): #to find the best theta	
		self.theta_b, self.theta_e = 20., 80.		
		deta_theta = (self.theta_e - self.theta_b)/10.
		self.x_cor = []
		for i in range(10):
			self.theta = self.theta_b + (deta_theta*i)
			self.x_cor.append(v0_theta0_y0(self.v0, self.theta, self.dy)[0])
#		print self.x_cor
#		print findmax(self.x_cor)[0]
#		print findplace(self.x_cor, self.dx)
		if (self.dx > self.x_cor[0]) and (self.dx < findmax(self.x_cor)[0]):			
			self.theta_b = self.theta_b + findplace(self.x_cor, self.dx)[0]*deta_theta
#			print self.theta_b
#			print deta_theta
			self.x_cor = []
			deta_theta = deta_theta/10.0
#			print deta_theta
			for j in range(10):
				self.theta = self.theta_b + (deta_theta*j)
				self.x_cor.append(v0_theta0_y0(self.v0, self.theta, self.dy)[0])
#			print self.x_cor
			self.k = findplace(self.x_cor, self.dx)[0]
			self.h = (self.theta_b + deta_theta*self.k)
#			print self.h
#			print self.k
#			print self.x_cor[self.k]
		elif (self.dx < self.x_cor[0]):
			print 'dx is two small'
		else:
			print 'dx is two large'

	def calculate(self):
		self.d = v0_theta0(self.v0, self.h)[2]
		self.e = v0_theta0(self.v0, self.h)[3]
		for i in range(len(self.d)):
			self.d[i] = self.d[i] + self.x0
			self.e[i] = self.e[i] + self.y0
	
	def unuse(self):
		self.m = []
		self.n = []
		for i in range(1000):
			self.m.append(25000 + 4*i)
			self.n.append(2000)

	def fire(self):
		plot(self.d, self.e, '--', label = 'flying shell')
		plot(self.m, self.n, label = 'flying plane')
		#label = '(%d,%d)to(%d,%d)'%(self.x0,self.y0,self.xt,self.yt))
		plot([500, 25000], [300, 2000], 'r^')
#		plot([1903, 30000], [200, 1200], 'bs')

s = shell(500, 300, 25000, 2000)
s.update()
s.unuse()
s.calculate()
s.fire()
			
#s = shell(1903, 200, 30000, 1200)
#s.update()
#s.calculate()
#s.fire()

legend(loc = 'best')
show()	
