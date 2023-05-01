import pandas as pd

from RLGridworld import GridWorld
from RLQlearning import QLearningTable


def update():

    worldId = 7
    RL.restore(worldId)
    for episode in range(100):
        # initial observation
        env.title('GridWorld'+" World "+str(worldId)+" Episode "+str(episode))
        observation = env.reset(worldId, RL.quorums)
##        RL.set_lr(episode)
        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action,worldId)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            print(RL.q_table)
            # break while loop when end of this episode
            if done:
                RL.backup(worldId)
                break
            # swap observation
            observation = observation_

    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = GridWorld()
    RL = QLearningTable(actions=list(range(env.n_actions)),
                        learning_rate=0.01, reward_decay=0.9, e_greedy=0.9)

    env.after(100, update)
    env.mainloop()
