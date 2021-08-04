"""
Game environment

"""

# Author: Haneul Kim <haneulkim214@gmail.com>


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
        self.countries = sorted(countries, key=lambda x: x.land_size, reverse=False)
        self.assign_ally_policy(apc)
        self.betting_area = np.zeros((3,3))

    def assign_ally_policy(self, apc):
        """
        Assign appropriate ally policy to each country
        which depends on their land_size.

        Paramaters
        ---------
        apc : tuple
              tuple of policy in order of weakest to strongest
              (ally_policy1, ally_policy2, ally_policy3)
        """
        for i, country in enumerate(self.countries):
            country.ally_policy = apc[i]
            country.rank = i

    def step(self):
        """
        colonize played once
        """
        for country in self.countries:
            country.get_military(self.mil_p)
            country.prepare_war(self.countries)

        # take away 10% land from opponent who lost bet.
        for country in self.countries:
            n = len(country.attacked)
            for attacking_country in country.attacked:
                self.go2war(country, attacking_country, n)

    def reset(self):
        """
        Resets environment to initial conditions
        """

    @staticmethod
    def go2war(country, attacking_country, n):
        """
        Two countries go on war with each other and
        country with higher military power take over 10% of losers land

        Parameters
        ----------
        country, attacking_country : Object
                                     Country object
        n : int
            number of countries country need to fight
        """
        t_mil_size = country.military_size + attacking_country.military_size
        c_win_p = country.military_size / t_mil_size
        win = np.random.binomial(n=1, p=c_win_p)

        if win:
            reward = attacking_country.land_size * 0.1
            country.land_size += reward
            attacking_country.land_size -= reward

        else:
            reward = country.land_size * 0.1
            country.land_size -= reward
            attacking_country.land_size += reward



# colonize = Colonize(countries)

# for i in range(20000):
#     colonize.step()
#
# colonize.plot()