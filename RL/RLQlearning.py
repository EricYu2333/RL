import math
import numpy as np
import pandas as pd

ACTIONS = ['N', 'S', 'W', 'E']

class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.epsilon_start = 0.01
        self.epsilon_end = 0.99
        self.epsilon_decay = 500
        self.q_table = None
        self.quorums = None

    def restore(self, worldId):
        q_tablefile = "World"+str(worldId)+"Qtable.csv"
        quorumsfile = "World"+str(worldId)+"Quorum.csv"
        try:
            self.q_table = pd.read_csv(q_tablefile, index_col=0)
            self.q_table.columns = self.actions
        except:
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        try:
            self.quorums = pd.read_csv(quorumsfile, index_col=0)
            self.quorums.columns = self.actions
        except:
            self.quorums = pd.DataFrame(columns=self.actions, dtype=np.float64)
        
    def backup(self, worldId):
        q_tablefile = "World"+str(worldId)+"Qtable.csv"
        quorumsfile = "World"+str(worldId)+"Quorum.csv"
        try:
            self.q_table.to_csv(q_tablefile)
        except:
            self.q_table.to_csv(q_tablefile+".copy")
        try:
            self.quorums.to_csv(quorumsfile)
        except:
            self.quorums.to_csv(quorumsfile+".copy")
        
    def set_lr(self, episode):
        self.lr = 1/(episode+1)

    def choose_action(self, observation):
        self.check_state_exist(observation)

        # The probability to select a random action, is is log decayed
        self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * math.exp(-1. * len(self.q_table) / self.epsilon_decay)
        # e-greedy policy
        print("E-greedy: "+str(self.epsilon))
        
        # action selection
        if np.random.uniform() < self.epsilon:
##            action = np.argmax(self.q_table[observation])
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
            print("Max of "+observation+" Action: "+ACTIONS[action])
        else:
            # choose random action
            action = np.random.choice(self.actions)
            print("Radom of "+observation+" Action: "+ACTIONS[action])
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)

##        self.lr = 1/len(self.q_table)

        q_predict = self.q_table.loc[s, a]
        if s_ != 'None':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
            self.check_quorums_exist(s)
            self.quorums.loc[s, a] = r
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
##            self.q_table = self.q_table.append(
##                pd.Series(
##                    [0]*len(self.actions),
##                    index=self.q_table.columns,
##                    name=state,
##                )
##            )

            self.q_table.loc[state] = [0]*len(self.actions)

    def check_quorums_exist(self, state):
        if state not in self.quorums.index:
            # append new state to q table
##            self.quorums = self.quorums.append(
##                pd.Series(
##                    [0]*len(self.actions),
##                    index=self.quorums.columns,
##                    name=state,
##                )
##            )

            self.quorums.loc[state] = [0]*len(self.actions)
