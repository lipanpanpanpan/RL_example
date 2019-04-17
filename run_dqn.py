#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 21:06:40 2019

@author: clytie
"""

if __name__ == "__main__":
    import numpy as np
    from tqdm import tqdm
    from env.dist_env import BreakoutEnv
    from algorithms.dqn import ReplayBuffer, DQN

    memory = ReplayBuffer(max_size=200000)
    env = BreakoutEnv(49999, num_envs=20)
    env_ids, states, rewards, dones = env.start()
    print("pre-train: \n")
    for _ in tqdm(range(5000)):
        env_ids, states, rewards, dones = env.step(env_ids, np.random.randint(env.action_space, size=env.num_srd))
    trajs = env.get_episodes()

    memory.add(trajs)
    DQNetwork = DQN(env.action_space, env.state_space)
    
    print("start train: \n")
    for step in range(10000000):
        for _ in range(20):
            actions = DQNetwork.get_action(np.asarray(states))
            env_ids, states, rewards, dones = env.step(env_ids, actions)
        if step % 100 == 0:
            print(f'>>>>{env.mean_reward}, nth_step{step}\n')
        trajs = env.get_episodes()
        memory.add(trajs)
        batch_samples = memory.sample(32)
        DQNetwork.update(batch_samples)

    env.close()