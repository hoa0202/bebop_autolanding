#현 소스코드는 20cm*20cm aruco marker 1번 으로 테스트 되었습니다.
# -*- coding: utf-8 -*-
#!/usr/bin/env python

import rospy
import sys
import termios
import tty
import time

from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist, Vector3 , Vector3Stamped

posex=float(0)
posey=float(0)
posez=float(0)


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def takeoff():
	takeoff_pub.publish(Empty())

def land():
	land_pub.publish(Empty())

def forward():
	tw = Twist()
	tw.linear.x = 0.3
	tw.linear.y = 0.0
	tw.linear.z = 0.0

	control_pub.publish(tw)

def back():
	tw = Twist()
	tw.linear.x = -0.3
	tw.linear.y = 0.0
	tw.linear.z = 0.0

	control_pub.publish(tw)

def left():
	tw = Twist()
	tw.linear.x = 0.0
	tw.linear.y = 0.3
	tw.linear.z = 0.0

	control_pub.publish(tw)

def right():
	tw = Twist()
	tw.linear.x = 0.0
	tw.linear.y = -0.3
	tw.linear.z = 0.0

	control_pub.publish(tw)

def right_2():
	tw = Twist()
	tw.linear.x = 0.0
	tw.linear.y = 0.0
	tw.linear.z = 0.0
	tw.angular.z = -0.3

	control_pub.publish(tw)

def left_2():
	tw = Twist()
	tw.linear.x = 0.0
	tw.linear.y = 0.0
	tw.linear.z = 0.0
	tw.angular.z = 0.3

	control_pub.publish(tw)

def up():
	tw = Twist()
	tw.linear.x = 0.0
	tw.linear.y = 0.0
	tw.linear.z = 0.3

	control_pub.publish(tw)

def down():
	tw = Twist()
	tw.linear.x = 0.0
	tw.linear.y = 0.0
	tw.linear.z = -0.3

	control_pub.publish(tw)

def stop():
	tw = Twist()
	tw.linear.x = 0.0
	tw.linear.y = 0.0
	tw.linear.z = 0.0

	control_pub.publish(tw)

def position_sub(data):
	global posex
	global posey
	global posez

	posex = float(data.vector.x)
	posey = float(data.vector.y)
	posez = float(data.vector.z)

def menu():
	print("o: takeoff")
	print("l: land")
	print("w: foward")
	print("a: left")
	print("s: back")
	print("q: left_2")
	print("e: right_2")
	print("j: up")
	print("k: down")
	print("b: auto landing")

def control(x, y, z):
	tw = Twist()
	tw.linear.x = x
	tw.linear.y = y
	tw.linear.z = z
	
	control_pub.publish(tw)
	

def camera_control():
	camera_control_cmd = Twist()
	camera_control_cmd.angular.y = -90
	camera_control_pub.publish(camera_control_cmd)

	


if __name__ == '__main__':
	x = 0
	y = 0
	z = 0
	val = 0.01
	spd = 0

	rospy.init_node('example_node', anonymous=True)
	takeoff_pub = rospy.Publisher("bebop/takeoff", Empty, queue_size=10)
	land_pub = rospy.Publisher("bebop/land", Empty, queue_size=10)

	control_pub = rospy.Publisher("bebop/cmd_vel", Twist, queue_size=10)

	camera_control_pub = rospy.Publisher('/bebop/camera_control', Twist, queue_size=10)
	
	rospy.Subscriber("/aruco_single/position", Vector3Stamped , callback=position_sub)

	menu()
	

	while True:
		camera_control()
		char = getch()

		if (char == "w"):
			print("forward")
			forward()
	
		elif (char == "a"):
			print("left")
			left()
	
		elif (char == "s"):
			print("backward")
			back()
		elif (char == "d"):
			print("right")
			right()
		elif (char == "j"):
			print("up")
			up()
	
		elif (char == "k"):
			print("down")
			down()
	
		elif (char == "q"):
			print("left yaw")
			left_2()
	
		elif (char == "e"):
			print("right yaw")
			right_2()
	
		elif (char == "o"):
			print("takeoff")
			takeoff()
		elif (char == "l"):
			print("land")
			land()

		elif (char == "b"):
			while True:
				if posez>1.5:
					max_x = 0.28
					min_x = -0.16
					max_y = 0.25
					min_y = -0.16
					val = 0.025

				elif posez>0.7:
					max_x = 0.2
					min_x = -0.08
					max_y = 0.17
					min_y = -0.08
					val = 0.02

				elif posez>0.6:
					max_x = 0.15
					min_x = -0.03
					max_y = 0.12
					min_y = -0.03
					val = 0.015
				else:
					max_x = 0.1
					min_x = 0.02
					max_y = 0.07
					min_y = 0.02
					val = 0.01

				if posex > 0.08:
					y = -val
					if posey > 0.05:
						x = -val
					else:
						x = val
						if 0.03 < posey < 0.05:
							x=0
				else:
					y = val
					if posey > 0.05:
						x = -val
					else:
						x = val
						if  0.03 < posey < 0.05:
							x=0
					if 0.04 < posex < 0.8:
						y=0
				if (min_y < posey < max_y) & (min_x < posex < max_x):
					spd += 0.00001
					if spd > 0.15:
						spd = 0.15
			
					z = -(val+spd)
					if posez < 0.19:
						print("landing compleate")
						land()
						break
				else:
					z= 0
					spd=0
		
				print(posex,posey,posez)
				print(x,y,z)
				print("\n")

				control(x, y, z)

		else:
			break
