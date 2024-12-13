import copy # used for deep copying complex objects, ensureing independent copies
import functools #provides high-order functions like reduce uses in calculating the nim-sum
import gymnasium as gym #main library for defining RL environments
import numpy as np #useful for handling arrays and mathmatical operations
from gymnasium import spaces #Provides predefined space types for actions and observations
from enum import Enum #allows for defing enumerated constants for actions in the game


#Custom Gymnastic environment for a single-pile game of nim
class NimEnv(gym.Env):
    """
    Players take turns removing objects from pile. The player who removes the last object in the pile loses.
    This environement supports RL agents to learn strategies
    """

    #game configurtaions
    def __init__(self):
        self.maxHeapSize = 15 #Inital size of the heap
        self.max_removal = 3 # Max. number of objects that can be removed in one turn
        self.current_pile = self.maxHeapSize # Inital size of the pile
        
        #Defines the action space (0, 1, 2 -> remove 1, 2, 3 objects respectively)
        self.action_space = spaces.Discrete(self.max_removal)
        self.observation_space = spaces.Discrete(self.maxHeapSize + 1)#Define obs space
        self.action_history = [] #tracks game state

        # Reward scheme
        self.win_reward = 1 #reward for winning the game
        self.loss_reward = -1 #Penalty for lossing the game
        self.transition_reward = 0.1 #Small reward for transitioning states
        self.invalid_move_reward = -0.5 #Penalty for invalid moves
        return


    def step(self, action):
        """
        Executes a step in the environemnt based on the given action.
        parameters:
        action: number of objects to remove
        returns:
        tuple(pbservation, reward, done, truncated, info)
        -observation: Updates pile size.
        -reward: Reward for the action.
        -done: True if the game has ended, False otherwise.
        -truncated: Always False(not used in this custom env)
        -info: Additional debugging information
        """
        #converts the action to the actual number of objects to remove
        action = action + 1
        
        #validate the action
        if not (1 <= action <= min(self.max_removal, self.current_pile)):
            #return the current state with a penalty for a invalid action
            return self.current_pile, self.invalid_move_reward, False, False, {"error":"Invalid Move"}
        
        #remove items based on action
        self.current_pile -= action

        #checks if the game is over
        done = self.current_pile == 0
        
        reward = self.win_reward if done else (self.current_pile/self.maxHeapSize) * self.transition_reward
        self.action_history.append(("Player", action))
        
        #return the updates state, reward, and game completion, and truncated
        return self.current_pile, reward, done, False, {}

    def reset(self, *, seed=None, options=None):
        """
        Resets the environemnet to the inital pile configuration
        
        Parameters:
        tuple: (observation, info)
        -observation: Inital pile size
        -info: Empty dictionary for additional information
        """
        super().reset(seed=seed)
        self.current_pile = self.maxHeapSize
        self.action_history = []
        return self.current_pile, {}

    def render(self, mode='human'):
        """
        Displays the current state of each heap
        
        Parameters:
        mode: The rendering mode
        
        Returns:
        str(optonal): String repersentation of the games state.
        """
        if mode == 'human':
            #prints the current pile size and action history
            print(f"Current pile: {self.curr_state} objects remaining")
            if self.action_space:
                print("Action history:")
                for turn, (player, action) in enumerate (self.action_space, start=1):
                    print(f"Turn {turn}: Player {player}, removed {action} objects")
        elif mode == 'ansi':
            return f"Current pile: {self.curr_state} objects remaining" +\
            "\n".join([f"Turn {turn}: Player {player} removed {action} objects"
                       for turn, (player, action) in enumerate(self.action_space, start=1)])
        else:
            super().render(mode=mode)
