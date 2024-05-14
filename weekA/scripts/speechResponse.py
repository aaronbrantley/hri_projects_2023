import rospy
from ros_vosk.msg import speech_recognition
from std_msgs.msg import String

currentQuestion = 0
questions = ['Have you had any snacks today?', 'Have you vaccumed your room in the past week?', 'Is today a weekday?']

def speechCallback (data):
    if (data.isSpeech_recognized):
        respondSpeech (data.final_result)
    else:
        rospy.loginfo (rospy.get_caller_id () + ": waiting for speech to be recognized")

def speechListener ():
    rospy.Subscriber ("speech_recognition/vosk_result", speech_recognition, speechCallback)

    rospy.spin ()

def respondSpeech (speech):
    responsePublisher = rospy.Publisher ('tts/phrase', String, queue_size = 10)
    response = ''

    if (speech.find ('yes') > -1 and currentQuestion == 0):
        response = 'Oh, I was hoping you get me something to eat!'
    elif (speech.find ('no') > -1 and currentQuestion == 0):
        response = 'Could you get some food for me if you decide to eat later?'
    elif (speech.find ('yes') > -1 and currentQuestion == 1):
        response = 'You must be a very clean person!'
    elif (speech.find ('no') > -1 and currentQuestion == 1):
        response = "Hey, maybe your room isn't that messy to begin with!"
    elif (speech.find ('yes') > -1 and currentQuestion == 2):
        response = "I can't wait till the weekend!"
    elif (speech.find ('no') > -1 and currentQuestion == 2):
        response = "I'm glad it's the weekend!"

    responsePublisher.publish (response)

def askQuestion ():
    questionPublisher = rospy.Publisher ('tts/phrase', String, queue_size = 10)

    questionPublisher.publish (questions [currentQuestion])

if __name__ == '__main__':
    rospy.init_node ('speechResponse')

    for index in range (len (questions)):
        rospy.loginfo (rospy.get_caller_id () + ": " + questions [index])
        currentQuestion = index

        askQuestion ()
        speechListener ()
