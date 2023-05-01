import numpy as np
import pandas as pd
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

from RLGame import *


UNIT = 20   # pixels
MAZE_H = 40  # grid height
MAZE_W = 40  # grid width


class GridWorld(tk.Tk, object):
    def __init__(self):
        super(GridWorld, self).__init__()
        self.action_space = ['N', 'S', 'W', 'E']
        self.n_actions = len(self.action_space)
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        self._build_maze()
        self.gridworld = RLGame(GWURL, SCOREURL, RESETURL, OTP, TEAMID, USERID, APIKEY)

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

##        # create origin
##        origin = np.array([UNIT/2, MAZE_H*UNIT-UNIT/2])
##
##        # create red rect
##        self.rect = self.canvas.create_rectangle(
##            origin[0] - 8, origin[1] - 8,
##            origin[0] + 8, origin[1] + 8,
##            fill='red', tag="rectangle")

        # pack all
        self.canvas.pack()

    def reset(self, worldId, quorums):
        self.gridworld.ResetMyTeam()
        self.gridworld.EnterWorld(str(worldId))
        self.state = [0,0]
        self.update()
        time.sleep(0.5)

        self.canvas.delete("rectangle")
        
        for state in quorums.index:
            pos = eval(state)
            origin = np.array([pos[0]*UNIT+UNIT/2, MAZE_H*UNIT-pos[1]*UNIT-UNIT/2])
            r = 0
            for action in range(self.n_actions):
                r += quorums.loc[state, action]
            if r > 0:
                rect = self.canvas.create_rectangle(
                    origin[0] - 8, origin[1] - 8,
                    origin[0] + 8, origin[1] + 8,
                    fill='yellow', tag="rectangle")
            else:
                rect = self.canvas.create_rectangle(
                    origin[0] - 8, origin[1] - 8,
                    origin[0] + 8, origin[1] + 8,
                    fill='black', tag="rectangle")

        origin = np.array([UNIT/2, MAZE_H*UNIT-UNIT/2])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 8, origin[1] - 8,
            origin[0] + 8, origin[1] + 8,
            fill='red', tag="rectangle")

        return self.state

    def step(self, action, worldId):
        info = self.gridworld.MakeMove(self.action_space[action], str(worldId))
        print(info)
        if info["code"]=="OK":
            time.sleep(3)
            reward = info["reward"]
            scoreInc = info["scoreIncrement"]
            newState = info["newState"]
            if newState:
                state_ = [int(newState["x"]), int(newState["y"])]

                if self.state != state_:
                    x_d = state_[0]-self.state[0]
                    y_d = state_[1]-self.state[1]
                    x_move = x_d*UNIT
                    y_move = -y_d*UNIT
                    self.canvas.move(self.rect, x_move, y_move)  # move agent
                    self.state = state_  # next state
##                    reward = abs(reward) #x_d+y_d
##                    if reward > 0:
##                        reward = -reward
##                    if reward > 0:
##                        reward = - reward
                else:
                    reward = -2
                done = False
            else:
                self.state = None
                # reward function
##                if reward == QUORUM:
##                    reward = 1
##                else:
##                    reward = 0
                done = True
        else:
            reward = 0
            done = True

        return self.state, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break

if __name__ == '__main__':
    env = GridWorld()
    env.after(100, update)
    env.mainloop()
