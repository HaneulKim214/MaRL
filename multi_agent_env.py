# from ray.rllib.env.multi_agent_env import MultiAgentEnv

import numpy as np
import random


class Colonize:
    """
    Description:
        Three countries(Agent) tries to take over much land as possible,
        countries cooperate with each other at times and also they go against
        each other to take over more land.

    Parameters
    ----------
    countries : list
                each element is country object

    land_size : int
                used to create land_size array
                filled with 0. where 0 => doesn't belong to
                anyone

    ally_str : dict
               all possible strategies for forming ally with
               others.
               Chosen depending on land_size

    mil_p : float
            ratio of military. ex: mil_p = 0.1 => military size is 10% of land_size

    betting_area: 3x3 matrix.
                  vertical countries place bet on country
                  on horizontal axis.
                  ex:
                                           receives
                                  country 1 | country 2 | country 3
                        country 1    0          0           3

                    Bet country 2   10          0           0

                        country 3    0          0           0
    """
    def __init__(self, countries, mil_p, apc):
        self.mil_p = mil_p
        # order them in ascending order w.r.t. land_size
        self.countries = sorted(countries, key=lambda x: x.land_size, reverse=True)
        self.assign_ally_policy(apc)
        self.betting_area = np.zeros((3,3))

    def assign_ally_policy(self, apc):
        """
        Assign appropriate ally policy to each country
        which depends on their land_size.

        Paramaters
        ---------
        apc : tuple
              tuple of policy in order of strongest to weakest
              (ally_policy1, ally_policy2, ally_policy3)
        """
        for i, country in enumerate(self.countries):
            country.ally_policy = apc[i]

    def bet(self, country, rnk):
        """
        Place bet on betting_area
        """

    def step(self):
        """
        :return:
        """
        for rnk, country in enumerate(self.countries):
            country.get_military(self.mil_p)
            country.gen_action(self.countries)
            self.bet(country, rnk)
        # take away land from each other depending on bet.

    def reset(self):
        """
        Resets environment to initial conditions
        """


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
        self.name = name
        self.land_size = land
        self.military_size = 0
        self.ally = []
        assert len(self.ally) <= 1, "You cannot have truth with all Countries"

    def get_military(self, mil_p):
        """
        assign military proportional to land_size

        :return:
        """
        self.military_size = self.land_size * mil_p

    def gen_action(self, countries):
        """
        Generate list of possible attackable countries
        depending on their ally_policy
        """
        if self.ally_policy == "no_ally":
            # bet on either country with 50/50 chance
            self.action_space = [c for c in countries if self.name != c.name]
            self.action = random.choice(self.action_space)

        elif self.ally_policy == "strongest":
            pass
        elif self.ally_policy == "2nd_strongest":
            pass
        elif self.ally_policy == "weakest":
            pass



# colonize = Colonize(countries)

# for i in range(20000):
#     colonize.step()
#
# colonize.plot()