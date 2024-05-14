import rospy
from ros_vosk.msg import speech_recognition
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

def looker():
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
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
        speechCommand (data.final_result)
    else:
        rospy.loginfo (rospy.get_caller_id () + ": waiting for speech to be recognized")

def speechListener ():
    rospy.Subscriber ("speech_recognition/vosk_result", speech_recognition, speechCallback)

    rospy.spin ()

def speechCommand (speech):
    if (speech.find ('hand') > -1):
        looker ()
    elif (speech.find ('point') > -1):
        keyframeAnimator ()
    else:
        rospy.loginfo (rospy.get_caller_id () + "Invalid command")

if __name__ == '__main__':
    rospy.init_node ('speechCommands')
    speechListener ()
