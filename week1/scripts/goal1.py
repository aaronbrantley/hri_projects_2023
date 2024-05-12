# !/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def validValue (inputRange, inputMin, inputMax):
    return inputRange >= inputMin and inputRange =< inputMax

def closestReading (data):
    initialValue = False
    result = float (-1)
    minRange = data.range_min
    maxRange = data.range_max
    
    for index in data.ranges:
        currentRange = data.ranges [index]
        
        if (!initialValue and validValue (currentRange, minRange, maxRange)):
            initialValue = True
            result = data.ranges [index]
        
        if (initialValue and validValue (currentRange, minRange, maxRange) and currentRange < result):
            result = currentRange
            
    rospy.loginfo (rospy.get_caller_id () + "Closest reading: %s", result)
        
    
def scanListener ():
    rospy.init_node ('scanListener', anonymous = True)

    rospy.Subscriber ("base_scan", sensor_msgs.msg.LaserScan, closestReading)

    # spin () simply keeps python from exiting until this node is stopped
    rospy.spin ()

if __name__ == '__main__':
    scanListener ()