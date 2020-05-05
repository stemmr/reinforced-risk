from .player import Player
import torch
import torch.nn as nn
import pdb
import random

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

    def __init__(self, name, troops, context, terr_num, play_num):
        super().__init__(name, troops, context)
        self.dvn = DVN(terr_num, play_num)
        self.name = name
        self.troops = troops

    def placement_control(self, placeable, units, state, querystyle="default"):
        
        state = torch.FloatTensor(state)
        val = self.dvn(state)
        best_move = (-float("inf"), None)

        for name, country in placeable.items():
            trial_state = state.clone()
            trial_state[self.context.state_idx(country, self)] += 1
            print(trial_state)
            val = self.dvn(trial_state)
            if val > best_move[0]:
                best_move = (val, name)

        # Place a single unit on the best tile, calculated by DVN
        return best_move[1], 1
        

    def attack_control(self, att_lines, state):
        
        # Inialize with value of not taking an action
        best_val = (self.dvn(state.clone()), (None, None)) # keep track of the value of the best attack line
        
        for attacker, defender in att_lines:
            att_idx = self.context.state_idx(attacker, self)
            def_idx = self.context.state_idx(defender, defender.owner)

            if self == defender.owner:
                raise ValueError()
            
            # Attacker can have at max 3 die, can maximally attack with 3 units
            att_dice = min(attacker.units - 1, 3)
            # Defender always defends with full army and at most 2 dice
            def_dice = min(defender.units, 2)

            # https://web.stanford.edu/~guertin/risk.notes.html
            # Six possible matchups (max 3 for attack, max2 for defence)
            # First element is probability of Attacker losing 0 units, then 1 unit then 2
            lose_probs = {
                (1,2): (330/1296, 966/1296, 0),
                (1,1): (540/1296, 756/1296, 0),
                (2,1): (750/1296, 546/1296, 0),
                (3,1): (855/1296, 441/1296, 0),
                (2,2): (295/1296, 420/1296, 581/1296),
                (3,2): (2890/7776, 2611/7776, 2275/7776)
            }

            # Attacker (Defender) can lose between [0-2] units at a time
            att_0 = state.clone()
            att_0[att_idx] -= 0
            att_0[def_idx] -= def_dice # defender can lose at most def_dice units
            v_0 = self.dvn(att_0) * lose_probs[(att_dice, def_dice)][0] # weighted value of losing zero

            att_1 = state.clone()
            att_1[att_idx] -= 1
            att_1[def_idx] -= def_dice - 1 # defender can lose at most def_dice units
            v_1 = self.dvn(att_1) * lose_probs[(att_dice, def_dice)][1] # weighted value of losing zero

            if att_dice >= 2 and def_dice >= 2:
                # It is now possible for a player to lose two units 
                # making check to avoid negative values in state vector
                att_2 = state.clone()
                att_2[att_idx] -= 2
                att_2[def_idx] -= 0 # to stay explicit
                v_2 = self.dvn(att_2) * lose_probs[(att_dice, def_dice)][2]
            else:
                v_2 = 0

            if v_0 + v_1 + v_2 > best_val[0]:
                best_val = (v_0 + v_1 + v_2, (attacker, defender))

        return best_val[1] #tuple of the best attack line (att, def)

    def fortify_control(self, fort_lines, state):
        # First check value of not fortifying after move
        best_line = (self.dvn(state.clone()), (None, None, 0))

        for fro_tile, to_tile, num_units in fort_lines:
            
            test_state = state.clone()
            
            from_idx = self.context.state_idx(fro_tile, self)
            to_idx = self.context.state_idx(to_tile, self)
            
            test_state[from_idx] -= num_units
            test_state[to_idx] += num_units

            fortify_value = self.dvn(test_state)
            
            if  fortify_value > best_line[0]:
                best_line = (fortify_value, (fro_tile, to_tile, num_units))

        return best_line[1]

    def overtaking_tile(self, num_units, state):
        # stub for the time being
        return random.choice(num_units)

    def feedback(self, signal, data, state, next_state):
        pass


