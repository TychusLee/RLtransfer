import numpy as np
import pandas as pd


class QLearning_Table:
    def __init__(self, actions, learning_rate=0.9, reward_decay=0.9, e_greedy=0.7):
        self.actions = actions
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.e_greedy = e_greedy
        self.qtable = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state(self, state):
        # print(state)
        if state not in self.qtable.index:
            self.qtable = self.qtable.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.qtable.columns,
                    name=state
                )
            )

    def learning(self, s, a, r, ns):
        print(self.qtable.loc[s, :])
        self.check_state(ns)
        q_pre = self.qtable.loc[s, a]
        if ns != 'terminal':
            q_target = r + self.reward_decay * self.qtable.loc[ns, :].max()
        else:
            q_target = r
        self.qtable.loc[s, a] += self.learning_rate * (q_target - q_pre)

    def choose_action(self, position):
        self.check_state(position)
        # epsilon_greedy
        if np.random.uniform() < self.e_greedy:
            choose_action = self.qtable.loc[position, :]
            choose_action = choose_action.reindex(
                np.random.permutation(choose_action.index))
            action = choose_action.idxmax()
        else:
            # random
            action = np.random.choice(self.actions)
        return action


class ShareTable:
    def __init__(self, actions, learning_rate=0.9, reward_decay=0.9):
        self.actions = actions
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.qtable = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state(self, state):
        if state not in self.qtable.index:
            self.qtable = self.qtable.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.qtable.columns,
                    name=state
                )
            )

    def learning(self, s, a, r, ns):
        self.check_state(ns)
        self.check_state(s)
        q_pre = self.qtable.loc[s, a]
        if ns != 'terminal':
            q_target = r + self.reward_decay * self.qtable.loc[ns, :].max()
        else:
            q_target = r
        self.qtable.loc[s, a] += self.learning_rate * (q_target - q_pre)
