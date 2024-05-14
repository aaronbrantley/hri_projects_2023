# !/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState

class Interpolator:
    def __init__ (self, start, end, frameCount):
        self.start = start
        self.end = end
        self.frameCount = frameCount
        self.frames = []
        
        self.interpolateFrames ()
		
	def interpolateFrames (self):
		for frame in range (self.frameCount + 1): 
			self.frames.append ((frame * (self.start + self.end)) / self.frameCount)

def keyframeAnimator ():
    rospy.init_node ('animator')
    
    publisher = rospy.Publisher ('joint_states', JointState, queue_size = 10)
    rate = rospy.Rate (10)
    frame = 0
    yawInterpolator = Interpolator (0.17, 0.5, 50)
    pitchInterpolator = Interpolator (-0.39, -0.5, 50)
    # change 0.5 and -0.5 to appropriate values
    
    while (not rospy.is_shutdown ()):
        if (frame > len (yawInterpolator.frames) - 1 and frame > len (pitchInterpolator) - 1):
            frame = yawInterpolator.frames) - 1
    
        jointMessage = JointState ()
        
        jointMessage.header.stamp = rospy.get_rostime()
        jointMessage.header.frame_id = "Torso"
        jointMessage.name.append ("HeadYaw")
        jointMessage.name.append ("HeadPitch")
        jointMessage.position.append (yawInterpolator.frames [frame])
        jointMessage.position.append (pitchInterpolator.frame [frame])
    
        publisher.publish (jointMessage)
        frame += 1
        rate.sleep ()
        
            
if __name__ == '__main__':
    keyframeAnimator ()