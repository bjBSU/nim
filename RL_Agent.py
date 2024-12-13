from typing import Tuple
import numpy as np

class QAgent:
    def __init__( self ):
        """
        Base class for the Q-learning agents. Methods include getting/adding Q-values, 
        selecting actions, and updating the Q-table.        
        """
        pass

    def get_q(self, obs, action: int) -> float:
        """
        Retrieve the Q-value for a given observation-action pair.
        Didn't end up utilizing this method.
        """
        return 0.
        
    def add_q(self, obs, action: int, val:float) -> int:
        """
        Update the Q-value for a specific observation action pairs by adding "val"
        Didn't end up utilizing this method.
        """
        return 0
        
    def get_next_action(self, obs, epsilon=0) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment
        if np.random.random() < epsilon:
            return self.get_random_action()

        # with probability (1 - epsilon) act greedily (exploit)
        else:
            return self.get_greedy_action(obs)[0]

    def get_random_action(self) -> int:
        """
        Returns a random action. Overriden in nim_Agent
        """
        return 0
        
    def get_greedy_action(self, obs) -> Tuple[int, float]:
        """
        Selects the action with the highest Q-value for the give observation.
        Didn't end up utilizing this method.
        """
        return 0, 0.
    
    def update(
        self,
        env,
        obs,
        epsilon: float = 0.2,
        learning_rate: float = 1.0,
        discount_factor: float = 1.0,
        training_error = None
    ):
        """Updates the Q-value using the temporal difference(TD) learning rule.
        Q(s,a) <-Q(s,a) + learning_rate * (reward +discount_factor * max(Q(s', a')) - Q(s, a)
        Parameters:
        -env: The environment object for taking actions and observing outcomes.
        -obs: Current observation (state).
        -epsilon: Exploration rate for epsilon-greedy policy.
        -learning_rate: Weight given to the new information in Q-value updates.
        -discount_factor: Discount rate for future rewards.
        -training_error: Optional list to store teh TD error for analysis.
        """
        action = self.get_next_action(obs, epsilon)
        next_obs, reward, terminated, truncated, info = env.step(action)
        #compute future Q-values
        future_q_value = (not terminated) * self.get_greedy_action(next_obs)[1]
        temporal_difference = (
            reward + discount_factor * future_q_value - self.get_q(obs,action)
        )
        self.add_q(obs, action, learning_rate * temporal_difference)
        if training_error:
            training_error.append(temporal_difference)
        return None if terminated or truncated else next_obs

class nimAgent(QAgent):
    def __init__(self, max_objects=20, max_removal=4):
        QAgent.__init__(self)#specialized implementation of QAgent for the game
        """Specialized implementation of 'QAgent' for the game of Nim. Initalizes the Q-table
        with dimensions [max_objects +1, max_removal], repersenting all possible states and actions.
        
        Parameters:
        -max_objects: Maximum number of objects in the game.
        -max_removal: Maximum objects a player can remove in a single move.
        """
        self.max_removal = max_removal
        self.max_objects = max_objects
        self.qTable = np.zeros((max_objects+1, max_removal))
        self.action_space = max_removal
        
    def obs_to_state(self, obs:int)->int:
        """
        Maps the current observation to its corresponding state index in the Q-table.
        """
        return self.qTable[obs]

    def get_q(self, obs:int, action: int) -> float:
        """
        Retrieves the Q-value for a given observation-action pair from the Q-table.
        """
        return self.obs_to_state(obs)[action]
        
    def add_q(self, obs:int, action: int, val:float) -> None:
        """
        Updates the Q-value for a given observation-action pair by adding 'val'.
        """
        self.obs_to_state(obs)[action] += val

    def get_random_action(self) -> int:
        """
        Returns a random action within the action space (0 to max_removal - 1).
        """
        return np.random.randint(4)
        
    def get_greedy_action(self, obs) -> Tuple[int,float]:
        """
        Implements a softmax selection policy to balance the exploration and exploitation.
        Returns the action and maximum Q-value.
        """
        state = self.obs_to_state(obs)
        logits_exp = np.exp(state)
        probs = logits_exp / np.sum(logits_exp)
        action = np.random.choice(4, p=probs)#possibly add probs back
        return action, max(self.qTable[action])
        
    def learn_policy(self, env):
        """
        Executes teh Q-learning policy within the environment and update the Q-value.
        """
        obs, info = env.reset()
        while obs is not None:
            obs = self.update(env, obs)
        
    def run_policy(self, env):
        """
        Executes the learned policy in the environment without exploration until the episode ends.
        """
        obs, _ = env.reset()
        done = False
        while not done:
            obs, reward, terminated, truncated, _ = env.step(self.get_next_action(obs))
            done = terminated or truncated
        return reward

#Hyperparameters      
epsilon = 0.02 #Inital exploration rate to encourage exploration
epsilon_final = 0.02 #Minimum exploration rate to ensure some randomness
epsilon_decay = 0.5 #Decay rate for epsilon

def set_epsilon(start, final, decay):
    """
     Configures teh exploration rate schedule.
     """
    global epsilon, epsilon_final, epsilon_decay
    epsilon = start
    epsilon_final = final
    epsilon_decay = decay
    
def get_epsilon():
    """
    Returns the current value of epsilon.
    """
    global epsilon
    return epsilon
                
def decay_epsilon():
    """
    Decays epsilon until it reachs the final value.
    """
    global epsilon
    epsilon = max(epsilon_final, epsilon - epsilon_decay)