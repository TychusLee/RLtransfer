import numpy as np
import sys
import tkinter as tk
import time
import random
import itertools

UNIT = 40
MAP_H = 20
MAP_W = 20
MAP_HU = MAP_H * UNIT
MAP_WU = MAP_W * UNIT
OBS_MAXN = 35
OBS_MINN = 25
BEA_NUM = 3


class Map(tk.Tk, object):
    def __init__(self):
        super(Map, self).__init__()
        self.actions = ['u','d','l','r']
        self.action_n = 4
        self.title('Map')
        self.geometry('{0}x{1}'.format(MAP_HU, MAP_WU))
        self._build()
    

    def _build(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAP_HU,
                                width=MAP_WU)
        
        #create grid
        for column in range(0,MAP_WU,UNIT):
            x1 = column
            y1 = 0
            x2 = column
            y2 = MAP_HU
            self.canvas.create_line(x1,y1,x2,y2)
        for row in range(0,MAP_HU,UNIT):
            x1 = 0
            y1 = row
            x2 = MAP_WU
            y2 = row
            self.canvas.create_line(x1,y1,x2,y2)
        
        #create all coordinate
        self.coor_list = list(itertools.product(range(MAP_W),range(MAP_H)))

        #create beacon
        self._set_beacon()

        #create rectangle
        self._set()

        #pack all
        self.canvas.pack()

    def _set_beacon(self):
        #create beacons coordinate
        beacon_coor = random.sample(self.coor_list,BEA_NUM)
        self.beacon_list = []
        if (MAP_W-1,MAP_H-1) in self.beacon_list:
            new_coor = (MAP_W-1,MAP_H-1)
            while new_coor in beacon_coor:
                new_coor = random.sample(self.coor_list,1)[0]
            beacon_coor.append(new_coor)
        else:
            beacon_coor.append((MAP_W-1,MAP_H-1))


        #create beacon
        #print(beacon_coor)
        #print('\n')
        for coor in beacon_coor:
            x0 = coor[0]
            y0 = coor[1]
            beacon = self.canvas.create_oval(x0*UNIT+10,y0*UNIT+10,
                                        (x0+1)*UNIT-10,(y0+1)*UNIT-10,
                                        fill = 'black')
            self.beacon_list.append(beacon)

        

    def _set(self):
        #num of obstacle
        self.obstacle_n = np.random.randint(OBS_MINN,OBS_MAXN)

        #create coordinate of obstacle and target
        obs_coor = random.sample(self.coor_list,self.obstacle_n)

        #delete obstacle on origin or target
        #print(obs_coor)
        #print('\n')
        if (0,0) in obs_coor:
            new_coor = (0,0)
            while new_coor in obs_coor or new_coor == (MAP_W-1,MAP_H-1):
                new_coor = random.sample(self.coor_list,1)[0]
            obs_coor.remove((0,0))
            obs_coor.append(new_coor)

        if (MAP_W-1,MAP_H-1) in obs_coor:
            new_coor = (MAP_W-1,MAP_H-1)
            while new_coor in obs_coor or new_coor == (0,0):
                new_coor = random.sample(self.coor_list,1)[0]
            obs_coor.remove((MAP_W-1,MAP_H-1))
            obs_coor.append(new_coor)

        #print(obs_coor)
        #print('\n')
        #create obstacle and target
        self.obs_list = []
        #print(self.obstacle_n)
        #print('\n')
        for coor in obs_coor:
            #print(coor)
            x0 = coor[0]
            y0 = coor[1]
            #create obstacle
            obs = self.canvas.create_rectangle(x0*UNIT+5,y0*UNIT+5,(x0+1)*UNIT-5,(y0+1)*UNIT-5,fill='yellow')
            self.obs_list.append(obs)
        #print('\n')
        #create target
        self.tar = self.canvas.create_rectangle((MAP_W-1)*UNIT+5,(MAP_H-1)*UNIT+5,
                                            MAP_WU-5,MAP_HU-5,
                                            fill='green')
        #create agent
        self.agent = self.canvas.create_rectangle(5,5,UNIT-5,UNIT-5,fill='red')

    def reset(self):
        for x in self.obs_list:
            self.canvas.delete(x)
        for x in self.beacon_list:
            self.canvas.delete(x)
        self.canvas.delete(self.agent)
        self._set()
        self._set_beacon()
        time.sleep(0.5)
        self.update()
        return [0,0]

    def agent_reset(self):
        self.canvas.delete(self.agent)
        self.agent=self.canvas.create_rectangle(5,5,UNIT-5,UNIT-5,fill='red')
        time.sleep(0.5)
        self.update()
        return [0,0]

    def step(self, action):
        pos = self.canvas.coords(self.agent)
        if action == 0:
            if pos[1] > UNIT:
                self.canvas.move(self.agent,0,-UNIT)
        elif action == 1:
            if pos[1] < (MAP_H-1) * UNIT:
                self.canvas.move(self.agent,0,UNIT)
        elif action == 2:
            if pos[0] > UNIT:
                self.canvas.move(self.agent,-UNIT,0)
        elif action == 3:
            if pos[0] < (MAP_W-1) * UNIT:
                self.canvas.move(self.agent,UNIT,0)
                
        ns = self.canvas.coords(self.agent)
        if ns == self.canvas.coords(self.tar):
            reward = 1
            done = True
            ns = 'terminal'
        elif ns in [self.canvas.coords(i) for i in self.obs_list]:
            reward = -1
            done = True
            ns = 'terminal'
        else:
            reward = 0
            done = False

        #calculate beacon state
        sig = []
        x1,y1 = (ns[0]-5)/UNIT,(ns[1]-5)/UNIT
        for beacon in self.beacon_list:
            b_coor = self.canvas.coords(beacon)
            x2,y2 = (b_coor[0]-5)/UNIT,(b_coor[1]-5)/UNIT
            sig.append((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        self.render()
        return ns,sig,reward,done

    def render(self):
        time.sleep(0.2)
        self.update()

def test():
    for _ in range(10):
        env.agent_reset()
        for _ in range(20):
            s,sig,r,done = env.step(1)
            if done:
                break
    
if __name__ == '__main__':
    env = Map()
    env.after(100,test)
    env.mainloop()


