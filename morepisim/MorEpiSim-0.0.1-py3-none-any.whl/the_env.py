
import matplotlib.pyplot as plt
import numpy as np
import random
import gym
from gym import spaces

from graph import showNet
from scores import plot_scores
from IRD import plot_ird

class MorEpiEnv(gym.Env): 
    def __init__(self, custom_data):
        self.observation_space = spaces.Box(
            low= 0,
            high= 1,
            shape=(4,),
            dtype=np.float32
        )
        self.action_space = spaces.Box(
            low= -1,
            high= 1,
            shape=(7,),
            dtype=np.float32
        )

        print('Initializing the env ...')
        # exactly the reset function
        self.epidemic_data = custom_data[0]
        self.demographic_data = custom_data[1]
        
        I, N = self.demographic_data[1], self.demographic_data[0]
        FI, ReI, Nxt_I, U, K, R, D = 1, 0, 1, 1, 1, 1, 0
        self.quantities = [I, N, FI, ReI, Nxt_I, U, K, R, D]

        self.R0 = 2
        #self.R0 = np.interp(self.R0, [1.4, 2.4], [0.01, 0.8])    # R0 forced between 0.1 and 0.8

        self.TI_TD = [25, 2]
        self.Te = 0
        self.a_weights = [1, 1, 1, 1, 1, 1, 1]  
        self.vaccination = False
        self.St = 0
        
        self.reward = 0
        self.h_score = 0
        self.e_score = 1
        self.h_w_sum = 0
        self.e_w_sum = 0

        self.ep = 0
        self.steps = 0
        
        a = np.random.rand(7)
        Density = self.demographic_data[2]
        
        s1 = (1 - (a[0]+ a[1]+ a[2]+ a[3] - self.St)/4) * Density * (self.R0 + (self.quantities[3]/(self.quantities[1]+0.00001)))
        s1 = s1 - (s1*a[6]*0.92)
        s2 = self.epidemic_data[0] * a[4]
        s3 = self.epidemic_data[1] * a[5]
        s4 = (1 - a[6]) * 0.46
        
        self.states = np.array([s1, s2, s3, s4], dtype=np.float32)
        self.actions = a
        self.done = False

        self.actions_list = []
        self.showN = False
        
        print('env successfully initialized ======_======= \n')

    def set_showN(self, showN):
        self.showN = showN
        
    def set_TI_TD(self, TI_TD):
        self.TI_TD = TI_TD

    def set_Te(self, Te):
        self.Te = Te
        
    def set_a_weights(self, wts):
        self.a_weights[0] = wts[0] 
        self.a_weights[1] = wts[1] 
        self.a_weights[2] = wts[2]
        self.a_weights[3] = wts[3]
        self.a_weights[4] = wts[4]
        self.a_weights[5] = wts[5]
        self.a_weights[6] = wts[6]


    def set_vaccination(self, vaccine):
        self.vaccination = vaccine

    def set_St(self, st):
        self.st = st

    def set_R0(self, R0):
        #self.R0 = np.interp(R0, [1.4, 2.4], [0.01, 0.8])    # This is what's declared in the paper
        self.R0 = R0  # This is what's used in the validation and in PYPI

    def reset(self):
        I, N = self.demographic_data[1], self.demographic_data[0]
        FI, ReI, Nxt_I, U, K, R, D = 1, 0, 1, 1, 1, 1, 0
        self.quantities = [I, N, FI, ReI, Nxt_I, U, K, R, D]

        self.R0 = 2
        #self.R0 = np.interp(self.R0, [1.4, 2.4], [0.01, 0.8])    # R0 forced between 0.1 and 0.8
        

        self.TI_TD = [25, 2]
        self.Te = 0
        self.a_weights = [1, 1, 1, 1, 1, 1, 1]  
        self.vaccination = False
        
        self.reward = 0
        self.h_score = 0
        self.e_score = 1
        self.h_w_sum = 0
        self.e_w_sum = 0

        self.steps = 0
        
        a = np.random.rand(7)
        Density = self.demographic_data[2]
        
        s1 = (1 - (a[0]+ a[1]+ a[2]+ a[3]- self.St)/4) * Density * (self.R0 + (self.quantities[3]/(self.quantities[1]+0.00001)))
        s1 = s1 - (s1*a[6]*0.92)
        s2 = self.epidemic_data[0] * a[4]
        s3 = self.epidemic_data[1] * a[5]
        s4 = (1 - a[6]) * 0.46
        
        self.states = np.array([s1, s2, s3, s4], dtype=np.float32)
        self.actions = a
        self.done = False

        self.actions_list = []

        info = {}
        return self.states #you must return states only if using stable-baselines3 (ni done, ni info, ...)

    def step(self, action):
        # actions of the model are between -1 and 1
        a = action
        # remap actions to be between 0 and 1,
        # add small random value to prevent 0 and for little stochasticity
        a = np.interp(a, [-1, 1], [0, 1]) 

        self.actions_list.append(a) 
                                             
        Density = self.demographic_data[2]
        Density = np.interp(Density, [3, 1000000], [0.02, 0.8])  # density forced between 0.1 and 0.8
        IN = self.quantities[0]/(self.quantities[1]+0.000001)  # IN is certainly between 0 and 1

        incubation = self.epidemic_data[0]
        incubation = np.interp(incubation, [5.6, 12.5], [0.1, 0.9]) #incubation forced between 0.1 and 0.9

        fatality = self.epidemic_data[1] + random.uniform(0, 0.08)

        if self.vaccination == True:
            pass
        else:
            a[6] = 0 #no vaccination

        nxt_s1 = (1 - ((a[0]+ a[1]+ a[2]+ a[3]- self.St)/4)) * Density * (self.R0+IN)
        nxt_s1 = nxt_s1 - (nxt_s1*a[6]*0.92)
        nxt_s2 = (1 - incubation) * a[4]
        nxt_s3 = (1 - a[5]) * fatality
        nxt_s4 = (1 - a[6]) * 0.08

        self.states = np.array([nxt_s1, nxt_s2, nxt_s3, nxt_s4], dtype=np.float32)
        
        #below is : I = I + U          
        I = self.quantities[0] + self.quantities[5]
        #below is : N= N - Nxt_I + R
        N = self.quantities[1] - self.quantities[4] + self.quantities[7]
        FI = int(N* nxt_s1)
        ReI = int(nxt_s4*self.quantities[7])
        Nxt_I = FI + ReI
        U = int(Nxt_I*(1-nxt_s2))
        K = int(Nxt_I*nxt_s2)
        R = int(K*(1-nxt_s3))
        D = int(K*nxt_s3)
        self.quantities = [I, N, FI, ReI, Nxt_I, U, K, R, D]

        ww = self.a_weights
        if self.vaccination == False:
            ww[6] = 0
        self.e_score = 1 - ((ww[0]*a[0]+ ww[1]*a[1]+ ww[2]*a[2]+ ww[3]*a[3]+ ww[4]*a[4]+ ww[5]*a[5] + ww[6]*a[6])/sum(ww))

        if N<=0:
            if self.showN==True:
                print("No normal people left! at step: ", self.steps)
            self.reward=-10
            self.done = True
            self.ep = self.ep + 1
            info = {}
            return self.states, self.reward, self.done, info
        else:
            if Nxt_I < self.TI_TD[0] and D < self.TI_TD[1]:
                self.h_score = (self.TI_TD[0] - Nxt_I) / self.TI_TD[0]
            else:
                self.h_score = 0
            
            if self.h_score > 0 and self.e_score > self.Te: 
                self.reward = self.e_score + self.h_score
            else:
                self.reward = 0.00000
                
            self.reward = float("{:.4f}".format(self.reward))
            self.steps = self.steps + 1
            info = {}
            if self.steps == 360:  #360days #50 for tests
                self.done = True
                self.ep = self.ep + 1
    ##            print('h_score, e_score : ', self.h_score, self.e_score)
    ##            print('s1, s2, s3, s4 : ', nxt_s1, nxt_s2, nxt_s3, nxt_s4)
    ##            print('last reward : ', self.reward)
    ##            print('TI, TD, Te, St : ', self.TI_TD[0], self.TI_TD[1], self.Te, self.St)
    ##            print('a weights: ', self.a_weights)
    ##            print('vaccination: ', self.vaccination)
                print("\n -------- episode: ", self.ep,  " is finished ----------- \n")
                return self.states, self.reward, self.done, info
            else:
                #print('R0 : ', self.R0)
##                print('N : ', self.quantities[1])
##                print('last reward : ', self.reward)
                return self.states, self.reward, self.done, info

    def render(self, mode=None, save=False):
        if mode=='scores' or mode== None:
            if save==True:
                plt.close(1)
                plt.close(3)
                figgg = plot_scores(self.h_score, self.e_score, self.ep,
                            self.steps, self.reward, self.R0, self.Te, show=not save, save=save)
                return figgg
            if save==False:
                plt.close(1)
                plt.close(3)
                plot_scores(self.h_score, self.e_score, self.ep,
                            self.steps, self.reward,  self.R0, self.Te, show=not save, save=save)

        if mode=='IRD':
            if save==True:
                plt.close(1)
                plt.close(2)
                figgg = plot_ird(self.quantities[4], self.quantities[7],
                            self.quantities[8], self.ep, self.steps, self.reward,
                                 self.R0, show=not save, save=save)
                return figgg
            if save==False:
                plt.close(1)
                plt.close(2)
                plot_ird(self.quantities[4], self.quantities[7],
                            self.quantities[8], self.ep, self.steps, self.reward,
                                 self.R0, show=not save, save=save)


        if mode=='graph':
            if save==True:
                plt.close(2)
                plt.close(3)
                figgg = showNet(self.ep, self.steps, self.states, self.quantities,
                        self.h_score, self.e_score, self.reward,  self.R0, show=not save, save=save)
                return figgg
            
            if save==False:
                plt.close(2)
                plt.close(3)
                showNet(self.ep, self.steps, self.states, self.quantities,
                        self.h_score, self.e_score, self.reward,  self.R0, show=not save, save=save)
        else:
            pass
    

    def close(self):
        plt.close('all')

    def interpret_policy(self, show, k=20): #k = w: window size
        w = k
        aaa = self.actions_list
        a1 = []
        a2 = []
        a3 = []
        a4 = []
        a5 = []
        a6 = []
        a7 = []
        for x in aaa:
            a1.append(x[0])
            a2.append(x[1])
            a3.append(x[2])
            a4.append(x[3])
            a5.append(x[4])
            a6.append(x[5])
            a7.append(x[6])
            
        interpreted1 = []
        interpreted2 = []
        interpreted3 = []
        interpreted4 = []
        interpreted5 = []
        interpreted6 = []
        interpreted7 = []
        for i in range(int(len(a1)/w)):
            x1 = a1[i*w: (i+1)*w]
            interpreted1.append(np.mean(x1))  
            x2 = a2[i*w: (i+1)*w]
            interpreted2.append(np.mean(x2))
            x3 = a3[i*w: (i+1)*w]
            interpreted3.append(np.mean(x3))
            x4 = a4[i*w: (i+1)*w]
            interpreted4.append(np.mean(x4))
            x5 = a5[i*w: (i+1)*w]
            interpreted5.append(np.mean(x5))
            x6 = a6[i*w: (i+1)*w]
            interpreted6.append(np.mean(x6))
            x7 = a7[i*w: (i+1)*w]
            interpreted7.append(np.mean(x7))

        interpreted = [interpreted1, interpreted2, interpreted3,
                       interpreted4, interpreted5, interpreted6,
                       interpreted7]

        if show==True:
            # get the last sequence of actions with k avrerage
            j = 1
            for i in interpreted:
                plt.subplot(7,1,j)
                plt.plot(i)
                j = j+1
            plt.show()
        else:
            return interpreted
            
        

