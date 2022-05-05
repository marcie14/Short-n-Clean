# M E 369P - Team 4 - Short n' Clean 
# Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava
# RPS Environment File for Reinforcement Learning (Medium Mode)

# INSPIRATIONS:
# https://www.youtube.com/watch?v=9_91p4SuiA4
# https://www.youtube.com/watch?v=bD6V3rcr_54
# https://github.com/koushik4/RockPaperScissors/blob/master/probabilities.py

# centered around the use of a Markov chain to update probabilities
# KEY: 1 = cow, 2 = snake, 3 = bird


import numpy as np
import random
from copy import copy


class RPSEnv: #(Env):
    def __init__(self): 
        # generate initial environment by setting up state and transition matrices
        # __init__ state matrix is all 0s with a 1 placed randomly
        # __init__ transition matrix provides equal probabilities to all possible combos
        init_index = random.randint(0,2)
        self.state = [0,0,0]
        self.state[init_index] = 1
        self.transition = [[1/3,1/3,1/3],[1/3,1/3,1/3],[1/3,1/3,1/3]]

        # will store the past action that the transition matrix will use as a reference
        self.previous_user_action = init_index

        # will set an initial prediction based on initial 
        self.prediction = self.state.index(max(self.state)) 

        # sensitivity value; will converge faster if set higher
        self.reward_value = 0.2

    def step(self, user_action):
        # dictionary defining winning criteria
        action_dict = {0:1, 1:2, 2:1}

        # sets reward value based on sensitivity parameter, will add to successful prediction and subtract from unsuccessful
        reward = self.reward_value if self.prediction is user_action else -self.reward_value

        # reference for previous state; referenced whenever values need to be recalculated with adjusted reward for row to = 1
        previous_row = copy(self.transition[self.previous_user_action]) 

        # iterates through prediction row and adjusts transition parameters accordingly
        for play in range(0,3):
            key = True
            if play is self.prediction:
                self.transition[self.previous_user_action][play] += reward
                key = False
            else:
                self.transition[self.previous_user_action][play] -= reward/2

            # makes sure that each row of transition matrix does not have a term exceeding 0
            # through adjustment of reward parameter, checks that row sums up to 1
            if not 0 <= self.transition[self.previous_user_action][play] <= 1:
                if self.transition[self.previous_user_action][play] < 0:
                    reward = -previous_row[play]
                    self.transition[self.previous_user_action][play] = 0
                elif self.transition[self.previous_user_action][play] > 1:
                    reward = 1-previous_row[play]
                    self.transition[self.previous_user_action][play] = 1
                if key: reward *= -2
                
                for i in range(0,len(previous_row)):
                    if i < play:
                        if i is self.prediction:
                            reward_compare = reward
                        else: 
                            reward_compare = -reward/2

                        if abs(self.transition[self.previous_user_action][i]-previous_row[i]) > abs(reward_compare):
                            self.transition[self.previous_user_action][i] = previous_row[i] + reward_compare

        self.previous_user_action = user_action

        # markov chain operation to calculate new state and determine likely prediction
        # converting to np.arrays here as easier to work with for matrix multiplication of state*transition
        state_np, transition_np = np.array(self.state), np.array(self.transition)
        self.state = np.matmul(state_np, transition_np).tolist()
        self.prediction = self.state.index(max(self.state))
        self.action = action_dict[self.prediction]

        return self.prediction, self.action, self.previous_user_action

    def reset(): # return initial time step
        pass


