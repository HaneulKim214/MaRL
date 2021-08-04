"""
Agents(Countries)

"""

# Author: Haneul Kim <haneulkim214@gmail.com>

import random


class Country:
    """

    Parameters
    ---------
    land_size : int
                국력

    ally : list
            each element is country it has truth
            with.
            rules:
            1. Cannot attack country within truth
            2. Stay truth for 10 turns
    ally_policies : list
                    each element consist of ally_policy

    action_space : list
                   containing country objects which it can attack.

    """
    def __init__(self, name, land):
        self.ally = []
        self.attacked = []
        self.name = name
        self.land_size = land
        self.military_size = 0
        assert len(self.ally) <= 1, "You cannot have truth with all Countries"


    def get_military(self, mil_p):
        """
        assign military proportional to land_size

        :return:
        """
        self.military_size = self.land_size * mil_p

    def prepare_war(self, countries):
        """
        pick country to attack from list of possible attackable countries
        depending on ally_policy
        """
        if self.ally_policy == "no_ally":
            # bet on either country with 50/50 chance
            self.action_space = [c for c in countries if self.name != c.name]
            self.action = random.choice(self.action_space)
            self.action.attacked.append(self)

        elif self.ally_policy == "strongest":
            pass
        elif self.ally_policy == "2nd_strongest":
            pass
        elif self.ally_policy == "weakest":
            pass