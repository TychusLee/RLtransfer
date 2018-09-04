from RL import QLearning_Table
from RL import ShareTable
from env import Map


def run():
    for _ in range(5):
        agent_pos = map.reset()
        q_learning = QLearning_Table(actions=list(range(map.action_n)))
        while True:
            action = q_learning.choose_action(str(agent_pos))
            next_state, next_share, reward, done = map.step(action)
            q_learning.learning(str(agent_pos), action,
                                reward, str(next_state))
            share_learning.learning(
                str(agent_pos), action, reward, str(next_share))
            agent_pos = next_state
            if next_state == 'target':
                break
            if next_state == 'obstacle':
                map.agent_reset()


if __name__ == '__main__':
    map = Map()
    share_learning = ShareTable(actions=list(range(map.action_n)))

    map.after(100, run)
    map.mainloop()
