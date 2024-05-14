import rospy
from ros-vosk.msg import speech_recognition
from std_msgs.msg import String

class SpeechResponse:
    def __init__ (self):
        self.questions = ['Have you had any snacks today?', 'Have you vaccumed your room in the past week?', 'Is today a weekday?']
        self.currentQuestion = 0
        rospy.init_node ('speechResponse')
        self.publisher = rospy.Publisher ('tts/phrase', String, queue_size = 10)
        rospy.Subscriber ('speech_recognition/vosk_result', speech_recognition, self.speechCallback)
        rospy.spin ()

    def speechCallback (self, data):
        if (data.isSpeech_recognized):
            self.respondSpeech (final_result)
        else:
            self.currentQuestion += 1
            
            if (self.currentQuestion >= len (self.questions)):
                self.currentQuestion = 0
            
            self.publisher.publish (self.questions [self.currentQuestion])
    
    def respondSpeech (self, speech):
        response = ''
        
        if (speech.find ('yes') > -1 and self.currentQuestion == 0):
            response = 'Oh, I was hoping you get me something to eat!'
        elif (speech.find ('no') > -1 and self.currentQuestion == 0):
            response = 'Could you get some food for me if you decide to eat later?'
        elif (speech.find ('yes') > -1 and self.currentQuestion == 1):
            response = 'You must be a very clean person!'
        elif (speech.find ('no') > -1 and self.currentQuestion == 1):
            response = "Hey, maybe your room isn't that messy to begin with!"
        elif (speech.find ('yes') > -1 and self.currentQuestion == 2):
            response = "I can't wait till the weekend!"
        elif (speech.find ('no') > -1 and self.currentQuestion == 2):
            response = "I'm glad it's the weekend!"
            
        self.publisher.publish (response)
    
if __name__ == '__main__':
    node = SpeechResponse ()