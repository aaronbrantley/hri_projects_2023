import rospy
from ros-vosk.msg import speech_recognition
from std_msgs.msg import String

def speechCallback (data):
    if (data.isSpeech_recognized):
        repeatSpeech (final_result)
    else:
        rospy.loginfo (rospy.get_caller_id () + "Waiting for speech to be recognized")
        
def speechListener ():
    rospy.init_node ('speechListener')
    rospy.Subscriber ("speech_recognition/vosk_result", speech_recognition, speechCallback)
    
    rospy.spin ()
    
def repeatSpeech (speech):
    publisher = rospy.Publisher ('tts/phrase', String, queue_size = 10)
    publisher.publish (speech)
    
if __name__ == '__main__':
    speechListener ()