# !/usr/bin/env python
import rospy
from std_msgs.msg import String

def moveSquare ():
    pub = rospy.Publisher ('cmd_vel', Twist, queue_size = 10)
    rate = rospy.Rate (10)

    moveMessage = Twist ()
    moved = False
    forwardSpeed = 1.0
    squareAngle = 1.0
    stopped = 0

    while not rospy.is_shutdown ():
        if (moved):
            moveMessage.linear.x = stopped
            moveMessage.linear.y = stopped
            moveMessage.linear.z = squareAngle
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

        moved = not moved # probably need to change this to check the robot's current angle

        pub.publish (moveMessage)
        rate.sleep ()

def moveFigureEight ():
    pub = rospy.Publisher ('cmd_vel', Twist, queue_size = 10)
    rate = rospy.Rate (10)

    turned360 = False
    forwardSpeed = 1.0
    figureEightAngle = 6.28

    while not rospy.is_shutdown ():
        if (turned360):
            moveMessage.linear.x = forwardSpeed
            moveMessage.linear.y = stopped
            moveMessage.linear.z = figureEightAngle
            moveMessage.angular.x = stopped
            moveMessage.angular.y = stopped
            moveMessage.angular.z = stopped
        else:
            moveMessage.linear.x = forwardSpeed
            moveMessage.linear.y = stopped
            moveMessage.linear.z = figureEightAngle * -1
            moveMessage.angular.x = stopped
            moveMessage.angular.y = stopped
            moveMessage.angular.z = stopped


        turned360 = not turned360 # probably need to change this to check the robot's current angle

        pub.publish (moveMessage)
        rate.sleep ()

def moveTriangle ():
    pub = rospy.Publisher ('cmd_vel', Twist, queue_size = 10)
    rospy.init_node ('moveTalker', anonymous = True)
    rate = rospy.Rate (10)

    moved = False
    forwardSpeed = 1.0
    triangleAngle = 3.0
    stopped = 0

    while not rospy.is_shutdown ():
        if (moved):
            moveMessage.linear.x = stopped
            moveMessage.linear.y = stopped
            moveMessage.linear.z = triangleAngleAngle
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


        moved = not moved # probably need to change this to check the robot's current angle

        pub.publish (moveMessage)
        rate.sleep ()

if __name__ == '__main__':
    rospy.init_node ('chooseMovement')
    try:
        rospy.loginfo (rospy.get_caller_id () + ": 1. Square")
        rospy.loginfo (rospy.get_caller_id () + ": 2. Figure-eight")
        rospy.loginfo (rospy.get_caller_id () + ": 3. Triangle")
        selection = input ()

        if (selection == 1 or selection.lower () == "square"):
            moveSquare ()
        elif (selection == 2 or selection.lower () == "figure-eight"):
            moveFigureEight ()
        elif (selection == 3 or selection.lower () == "triangle"):
            moveTriangle ()

    except rospy.ROSInterruptException:
        pass
