import rospy
from ros-vosk.msg import speech_recognition
from std_msgs.msg import String
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
        jointMessage = JointState ()
        
        if (frame > len (yawInterpolator.frames) - 1 and frame > len (pitchInterpolator) - 1):
            frame = yawInterpolator.frames) - 1
        
        jointMessage.header.stamp = rospy.get_rostime()
        jointMessage.header.frame_id = "Torso"
        jointMessage.name.append ("HeadYaw")
        jointMessage.name.append ("HeadPitch")
        jointMessage.position.append (yawInterpolator.frames [frame])
        jointMessage.position.append (pitchInterpolator.frame [frame])
    
        publisher.publish (jointMessage)
        frame += 1
        rate.sleep ()

def looker():
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('looker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        joint_states = JointState()
        joint_states.header.stamp = rospy.get_rostime()
        joint_states.header.frame_id="Torso"
        joint_states.name.append("HeadYaw")
        joint_states.name.append("HeadPitch")

        joint_states.position.append(0.17)
        joint_states.position.append(-0.39)
        pub.publish(joint_states)
        rate.sleep()        

def speechCallback (data):
    if (data.isSpeech_recognized):
        speechCommand (final_result)
    else:
        rospy.loginfo (rospy.get_caller_id () + "Waiting for speech to be recognized")
        
def speechListener ():
    rospy.init_node ('speechListener')
    rospy.Subscriber ("speech_recognition/vosk_result", speech_recognition, speechCallback)
    
    rospy.spin ()
    
def speechCommand (speech):
    if (speech.find ('hand') > -1):
        looker ()
    else if (speech.find ('point') > -1):
        keyframeAnimator ()
    else:
        rospy.loginfo (rospy.get_caller_id () + "Invalid command")        
    
if __name__ == '__main__':
    speechListener ()