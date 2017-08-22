#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spidev
import time
import math as m
import numpy as np
from MPU9250 import MPU9250

def init():
    imu = MPU9250()
    imu.initialize()
    i=1
    g0=np.zeros(3)
    while i<=100:
        m6a,m6g=imu.getMotion6()
        g0=g0+m6g
        i+=1
    return g0/100

def getAcangle():
        a,g=imu.getMotion6()
	a=a*10
        roll=m.atan(a[1]/a[2])
        pitch=m.atan(-a[0]/m.sqrt(m.pow(a[1],2)+m.pow(a[2],2)))
        ang=np.array([m.atan(-a[0]/m.sqrt(m.pow(a[1],2)+m.pow(a[2],2))),m.atan(a[1]/a[2]),0])
        return ang

def getAcintGy(ang0,dt,gv):
        a,g=imu.getMotion6()
        g=(g-gv)/180*np.pi
        ang_a=np.array([m.atan(-a[0]/m.sqrt(a[1]*a[1]+a[2]*a[2])),m.atan(a[1]/a[2]),0])
        B=np.array([[0,m.cos(ang0[1]),-m.sin(ang0[1])],
[1,m.sin(ang0[1])*m.tan(ang0[0]),m.cos(ang0[1])*m.tan(ang0[0])],
[0,m.sin(ang0[1])/m.cos(ang0[0]),m.cos(ang0[1])/m.cos(ang0[0])]])
        ang_g=ang0+np.dot(B,g)*dt
        return ang_a,ang_g,np.dot(B,g)


if __name__ == '__main__':
	imu = MPU9250()
	imu.initialize()
	gv=init()
	ang_0=np.zeros([3,])
        tau=0.2
        ts=0.01
        i=1
        while i<=1000:
                ang_0+=getAcangle()
                i+=1
        ang_a0=ang_0/1000
        ang_g0=ang_a0

        while(1):
                t=time.time()
                ang_a,ang_g,ang_v=getAcintGy(ang_g0,ts,gv)
                ang_a=(ang_a0+ang_a*ts/tau)/(1+ts/tau) #ローパスフィルタ
                ang_g[:2]=ang_g[:2]-(ang_g0[:2]+ang_g[:2]*ts/tau)/(1+ts/tau)
                ang=ang_a+ang_g
                print  "{:+7.3f}".format(ang[0]*180/np.pi),",","{:+7.3f}".format(ang[1]*180/np.pi),",","{:+7.3f}".format(ang[2]*180/np.pi)
                ang_g0=ang_g
                ang_a0=ang_a
                time.sleep(ts-time.time()+t)
		#print time.time()-t
