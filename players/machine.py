from .player import Player
import torch
import torch.nn as nn
import pdb

"""
Due to the complexity of modelling a game with more than two players, we will first consider
a game of risk with only two players, as an extension it may be possible to explore 2+ players.

The entire state of a game of risk can be modelled by:
- N*M tiles, N tiles, M players
- 4 one-hot encoded states of current action (placement/attack/forify/overtaking) 
"""

class DVN(nn.Module):
    def __init__(self, terr_num, play_num):
        super(DVN, self).__init__()
        # Input is number of territories plus one hot encoded state
        infeats = terr_num*play_num + 3
        self.fc1 = nn.Linear(infeats, 20)
        self.fc2 = nn.Linear(20, 1)

    def forward(self, x):
        x = torch.tanh(self.fc1(x))
        return self.fc2(x)

class Machine(Player):
    """
    A Machine player, should be capable of handling learned actions autonomously
    all functionality should be in Player, where this just provides a way to act as a player 
    """

    def __init__(self, name, troops, terr_num, play_num):
        super().__init__(name, troops)
        self.dvn = DVN(terr_num, play_num)
        self.name = name
        self.troops = troops

    def placement_control(self, placeable, state, querystyle="default"):
        state = torch.FloatTensor(state)
        val = self.dvn(state)
        print(val, placeable)
        pdb.set_trace()
        

    def attack_control(self, att_lines, state):
        pass

    def fortify_control(self, fort_lines, state):
        pass

    def overtaking_tile(self, num_units, state):
        pass


