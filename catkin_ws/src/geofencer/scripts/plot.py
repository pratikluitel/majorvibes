#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import rospy
from std_msgs.msg import Float32MultiArray, String

def callback(data):
    gps = data.data
    points.append([gps[0],gps[1],gps[2]])
    global time
    time+=1

def geocallback(data):
    breach = data.data
    breaches.append(breach) 

def listener():
    rospy.init_node('main', anonymous=True)

    rate = rospy.Rate(100)
    rospy.Subscriber('/GPSdata', Float32MultiArray, callback)
    rospy.Subscriber('/geofence_status',String, geocallback)

    while not rospy.is_shutdown():
        rate.sleep()

def plot_traj(x,y,t,mask,axs,col='blue'):
    xb =[]
    yb =[]
    tb =[]

    st = t[mask][0]
    prev_i=st-1
    for i in t[mask]:
        if i-prev_i>1 or i ==t[mask][-1]:
            xb.append(x[st:prev_i+2])
            yb.append(y[st:prev_i+2])
            tb.append(t[st:prev_i+2])
            st=i
            prev_i=st-1
        prev_i+=1

    for j in range(len(tb)):
        axs[0].plot(tb[j],xb[j],col)
        axs[1].plot(tb[j],yb[j],col)
        axs[2].plot(xb[j],yb[j],col)


points = []
breaches = []
col='blue'
time=0
listener()

#plotting
mask = np.array(breaches) == ' '
fig, axs = plt.subplots(3)
x = np.array([point[0] for point in points])
y = np.array([point[1] for point in points])
t = np.array(range(time))

plot_traj(x,y,t,mask,axs)
plot_traj(x,y,t,np.logical_not(mask),axs,'red')

axs[0].set(ylabel='x')
axs[1].set(ylabel='y')
axs[2].set(ylabel='y')

axs[0].set(xlabel='time (sec)')
axs[1].set(xlabel='time (sec)')
axs[2].set(xlabel='x')

plt.show()
