import sys
import numpy as np
import time
#retico
from mistypy.Robot import Robot
import retico_core
from retico_core import abstract
from retico_vision.vision import ExtractedObjectsIU, ObjectFeaturesIU
from retico_core.dialogue import GenericDictIU


class NimModule(retico_core.AbstractModule):
    """A module that takes in an image and counts the number of objects in the image"""

    @staticmethod
    def name():
        return "Nim module that detects how many objects have been detected by clip.",
        "Then it decides what move to make based on the suggested number provided by the nim algorithm"
    
    @staticmethod
    def description():
        return ""

    @staticmethod
    def input_ius():
        return [ExtractedObjectsIU]

    @staticmethod
    def output_iu():
        return None

    def __init__(self, ip, **kwargs):
        super().__init__(**kwargs)
        self.robot = Robot(ip)  

    def process_update(self, update_message):
        self.humanTurn = False
        self.MistyTurn = False
        self.GameOver = False
        self.currentState = 15
        self.bestMove = 0
        self.iu_list = []
        print("got to the nim module")
        for iu,um in update_message:
            if um == abstract.UpdateType.ADD:
                self.process_iu(iu)
                self.iu_list.append(iu)
                if len(self.iu_list) > 500:
                    self.iu_list = self.iu_list[-500:]
            else:
                continue
    
    def process_iu(self, iu):
        #output_iu = self.create_iu(iu)
        self.numObj = iu.payload['num_objects']
        print("Number of objects detected: ", self.numObj)
        #Start by saying Hello and then saying who is going to start
        self.robot.speak("Hello I am Misty, lets play the game of Nim. I will start.")
        self.robot.move_head(pitch=100)

        #Get the payload and count the amount of values(boxes) from the clip image
        self.robot.speak("Please place 15 objects in front of us.")
        while self.numObj != 15:
            self.numObj = self.get_latest_num_objects()
            print("Number of objects detected: ", self.numObj)
            time.sleep(5)
            #self.robot.speak("Please place 15 objects in front of us.")
        
        while(self.GameOver!=True & self.numObj <= 15):
            print("Number of objects detected: ", self.numObj)
            #If its is misty then read in the amount of objects and plug that into the algorithm
            if self.MistyTurn == True:
                self.bestMove = 1 #algorithm(currentState)
                self.robot.speak(f"Please remove {self.bestMove} for me.")
                time.sleep(5.0)
                self.curentState = self.currentState - self.bestMove
                #add a sleep to give them a second to move the blocks
                #timer.sleep
                #check to make sure they removed the blocks
                if self.currentState != self.numObj:
                    self.robot.speak(f"Please remove {self.bestMove} for me.")
                else:
                    self.humanTurn = True
                    self.MistyTurn = False
                    self.robot.speak("Thank you, its now your turn.")
            #This is the case when it is the humans turn
            else:
                if self.numObj != self.currentState:
                    self.currentState = self.numObj
                    self.humanTurn = False
                    self.MistyTurn = True
                    self.robot.speak("Thank you, its now my turn.")


        if self.GameOver == True:
            #check if it was Mistys turn 
            if self.MistyTurn == True & self.currentState == 1:
                self.MistyLoss()
            elif self.MistyTurn == True & self.currentState == 0:
                self.MistyWon()

    def MistyWon(self):
        self.robot.speak("I win, good game!")
        
    
    def MistyLoss(self):
        self.robot.speak("I Lost, good game!")

    def get_latest_num_objects(self):
        if self.iu_list:
            return self.iu_list[-1].payload['num_objects']
        return 0
        



