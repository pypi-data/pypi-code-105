import matplotlib.pyplot as plt
import random
import time
import the_env


from stable_baselines3 import PPO, TD3
#model = PPO.load("ppo_best_model_same_weights")
#model = PPO.load("ppo_best_model_diffr_weights")
#model = PPO.load("ppo_best_model_diffr_weights_2nd")
#model = TD3.load("epidemic_td3")

# initial values ---------------------------------------------
epidemic_data = [14, 0.1] #incubation coef and fatality coef |
demographic_data = [100000, 3, 1000] #N, I, density           |
# ------------------------------------------------------------
custom_data = [epidemic_data, demographic_data]
env = the_env.MorEpiEnv(custom_data)

env.a_weights[0] = 1 #weight on A1
env.a_weights[1] = 1 #weight on A2
env.a_weights[2] = 1 #weight on A3
env.a_weights[3] = 1 #weight on A4
env.a_weights[4] = 1 #weight on A5
env.a_weights[5] = 1 #weight on A6
env.a_weights[6] = 1 #weight on A7

# to enable vaccination usage by the agent
# env.set_vaccination(True):

num_ep = 1

reward_avrg_list = []

action_list = []
for ep in range(num_ep):
    obs = env.reset()
    step_reward_list = []
    done = False
    while not done:
        #action, _ = model.predict(obs) #, deterministic=False)
        # or
        action = env.action_space.sample()

        obs, reward, done, info = env.step(action)

        env.render('IRD') # scores or graph or IRD
        
        #step_reward_list.append(reward)

    #print(len(step_reward_list))
    #print("episode score = ", sum(step_reward_list)/50)

##        if done:
##            print("episode: ", ep,  "finished at : ", step+1)
##            reward_avrg = sum(step_reward_list) / len(step_reward_list)
##            print("with average reward= ", reward_avrg)
##            
##    reward_avrg_list.append(reward_avrg)

env.close()

##import matplotlib.pyplot as plt
##fig2, ax2 = plt.subplots(nrows=1, ncols=1)
##plt.plot(s2s)
##fig2.show()


