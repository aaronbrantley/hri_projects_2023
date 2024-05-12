# !/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
    
class ObstacleCheck:
    def __init__ (self):
        self.obstacle = True
        rospy.Subscriber ("base_scan", sensor_msgs.msg.LaserScan, closestReading)
        rospy.spin ()
        
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
                
        self.obstacle = result < 1.0     

def obstacleStopAndTurn ():
    rospy.init_node ('obstacleStop')
    pub = rospy.Publisher ('cmd_vel', Twist, queue_size = 10)    
    rate = rospy.Rate (10)
    
    moveMessage = Twist ()
    obstacleChecker = ObstacleCheck ()
    forwardSpeed = 1.0
    turnAngle = 1.0
    stopped = 0
    
    while not rospy.is_shutdown ():
        if (obstacleChecker.obstacle):
            moveMessage.linear.x = stopped
            moveMessage.linear.y = stopped
            moveMessage.linear.z = turnAngle
            moveMessage.angular.x = stopped
            moveMessage.angular.y = stopped
            moveMessage.angular.z = stopped
        else:
            moveMessage.linear.x = forwardSpeed
            moveMessage.linear.y = stopped
            moveMessage.linear.z = stopped
            moveMessage.angular.x = stopped
            moveMessage.angular.y = stopped
            moveMessage.angular.z = stopped
        
        pub.publish (moveMessage)
        rate.sleep ()
        
if __name__ == '__main__':
    try:
        obstacleStopAndTurn ()
        
    except rospy.ROSInterruptException:
        pass