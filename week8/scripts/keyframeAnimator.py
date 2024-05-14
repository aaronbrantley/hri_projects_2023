# !/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
import tf2_ros

class Interpolator:
	def __init__ (self, start, end, frameCount):
		self.start = start
		self.end = end
		self.frameCount = frameCount
		self.frames = []

		self.interpolateFrames ()

	def __len__ (self):
		return len (self.frames)

	def interpolateFrames (self):
		for frame in range (self.frameCount + 1):
			self.frames.append ((frame * (self.start + self.end)) / self.frameCount)

def keyframeAnimator ():
	rospy.init_node ('animator')

	publisher = rospy.Publisher ('joint_states', JointState, queue_size = 10)
	rate = rospy.Rate (10)
	frame = 0
	'''
	This is the code to get the transform between the head and the hand
	But it cannot run while the joint controller is running, since the joint controller publishes over the animator
	But these transforms are only published when the joint controller is running

	transformBuffer = tf2_ros.Buffer ()
	transformListener = tf2_ros.TransformListener (transformBuffer)
	transform = transformBuffer.lookup_transform ('Head', 'r_wrist', rospy.Time (0), rospy.Duration (3.0))
	'''
	yawInterpolator = Interpolator (0.17, 1.15, 50)
	pitchInterpolator = Interpolator (-0.39, 0.41, 50)

	while (not rospy.is_shutdown ()):
		if (frame >= len (yawInterpolator.frames) and frame >= len (pitchInterpolator)):
			frame = len (yawInterpolator.frames) - 1

		jointMessage = JointState ()

		jointMessage.header.stamp = rospy.get_rostime()
		jointMessage.header.frame_id = "Torso"
		jointMessage.name.append ("HeadYaw")
		jointMessage.name.append ("HeadPitch")
		jointMessage.position.append (yawInterpolator.frames [frame])
		jointMessage.position.append (pitchInterpolator.frames [frame])

		publisher.publish (jointMessage)
		frame += 1
		rate.sleep ()


if __name__ == '__main__':
	keyframeAnimator ()
