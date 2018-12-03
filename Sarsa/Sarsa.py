import random
import numpy as np

# world height
WORLD_HEIGHT = 7

# world width
WORLD_WIDTH = 10

# allowed action move directions
DIRECTIONS = 8

# wind strength for each column
WIND = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

# possible actions
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3
ACTION_UP_RIGHT = 4
ACTION_DOWN_RIGHT = 5
ACTION_DOWN_LEFT = 6
ACTION_UP_LEFT = 7
# ACTION_STAY = 8

# probability for exploration
EPSILON = 0.1

# Sarsa step size (learning rate)
ALPHA = 0.5

# discount rate (undiscounted task)
GAMMA = 1

# reward for each step
REWARD = -1.0

START = [3, 0]
GOAL = [3, 7]
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
           ACTION_UP_RIGHT, ACTION_DOWN_RIGHT, ACTION_DOWN_LEFT, ACTION_UP_LEFT]


def get_next_state(state, action):
    i, j = state
    if action == ACTION_UP:
        return [max(i - 1 - WIND[j], 0), j]
    elif action == ACTION_DOWN:
        return [max(min(i + 1 - WIND[j], WORLD_HEIGHT - 1), 0), j]
    elif action == ACTION_LEFT:
        return [max(i - WIND[j], 0), max(j - 1, 0)]
    elif action == ACTION_RIGHT:
        return [max(i - WIND[j], 0), min(j + 1, WORLD_WIDTH - 1)]
    elif action == ACTION_UP_RIGHT:
        return [max(i - 1 - WIND[j], 0), min(j + 1, WORLD_WIDTH - 1)]
    elif action == ACTION_DOWN_RIGHT:
        return [max(min(i + 1 - WIND[j], WORLD_HEIGHT - 1), 0), min(j + 1, WORLD_WIDTH - 1)]
    elif action == ACTION_DOWN_LEFT:
        return [max(min(i + 1 - WIND[j], WORLD_HEIGHT - 1), 0), max(j - 1, 0)]
    elif action == ACTION_UP_LEFT:
        return [max(i - 1 - WIND[j], 0), max(j - 1, 0)]
    # elif action == ACTION_STAY:
    #     return [max(i - WIND[j], 0), j]
    else:
        assert False


# play for an episode
def next_episode(q_value):

    # track the total time steps in this episode
    time = 0

    # track the path of action in this episode
    path = []

    # initialize state
    state = START

    # choose an action based on epsilon-greedy algorithm
    if random.random() < EPSILON:
        action = np.random.choice(ACTIONS)
    else:
        values = q_value[state[0], state[1], :]
        action = np.random.choice([index for index, value in enumerate(values) if value == np.max(values)])

    # keep going until reach the goal state
    while state != GOAL:
        next_state = get_next_state(state, action)
        # print("actions", action)
        path.append(action)
        if random.random() < EPSILON:
            next_action = np.random.choice(ACTIONS)
        else:
            values = q_value[next_state[0], next_state[1], :]
            next_action = np.random.choice([index for index, value in enumerate(values) if value == np.max(values)])

        # Sarsa function
        q_st_at = q_value[state[0], state[1], action]
        q_st1_at1 = q_value[next_state[0], next_state[1], next_action]
        td_error = REWARD + GAMMA * q_st1_at1 - q_st_at
        q_st_at += ALPHA * td_error

        q_value[state[0], state[1], action] = q_st_at
        state = next_state
        action = next_action
        time += 1

    assert (time == len(path)), "path and actions should be same size"
    return time, path


# on-policy TD control Sarsa
def sarsa():
    q_value = np.zeros((WORLD_HEIGHT, WORLD_WIDTH, DIRECTIONS))
    episode_limit = 8000
    target_step = 7

    step = WORLD_WIDTH * WORLD_HEIGHT
    path = []
    ep = 0
    print("\nInitial Q Values :\n{}".format(q_value))
    while step > target_step:
    # while ep < episode_limit:
        step, path = next_episode(q_value)
        ep += 1
        print("\nMinimum Steps In Episode", ep, " :", step)
    print("\nQ Values :\n{}".format(q_value))

    # display current optimal policy
    optimal_policy = []
    for i in range(0, WORLD_HEIGHT):
        optimal_policy.append([])
        for j in range(0, WORLD_WIDTH):
            if [i, j] == GOAL:
                optimal_policy[-1].append('G')
                continue
            if [i, j] == START:
                optimal_policy[-1].append('S')
                continue
            best_action = np.argmax(q_value[i, j, :])
            arrow = get_print_arrows(best_action)
            optimal_policy[-1].append(arrow)
    print("\nCurrent Optimal Policy :")
    for row in optimal_policy:
        print(row)
    print("Wind Strength For Each Column:\n{}".format([str(w) for w in WIND]))
    print("\nOptimal Path :\n{}".format(path))

    # display optimal action move path
    current = START
    new_policy = []
    for i in range(0, WORLD_HEIGHT):
        new_policy.append([])
        for j in range(0, WORLD_WIDTH):
            new_policy[-1].append('|')
            if [i, j] == GOAL:
                new_policy[i][j] = 'G'
    while current != GOAL:
        pop = path.pop(0)
        new_policy[current[0]][current[1]] = get_print_arrows(pop)
        current = get_next_state(current, pop)
    for row in new_policy:
        print(row)
    print("Wind Strength For Each Column:\n{}".format([str(w) for w in WIND]))


# get unicode of arrows
def get_print_arrows(best_action):
    if best_action == ACTION_UP:
        return '\u2191'
    elif best_action == ACTION_DOWN:
        return '\u2193'
    elif best_action == ACTION_LEFT:
        return '\u2190'
    elif best_action == ACTION_RIGHT:
        return '\u2192'
    elif best_action == ACTION_UP_RIGHT:
        return '\u2197'
    elif best_action == ACTION_DOWN_RIGHT:
        return '\u2198'
    elif best_action == ACTION_DOWN_LEFT:
        return '\u2199'
    elif best_action == ACTION_UP_LEFT:
        return '\u2196'
    # elif best_action == ACTION_STAY:
    #     return '\u21BB'
    else:
        assert False


sarsa()
