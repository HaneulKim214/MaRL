"""
Game environment

Development legend(should be deleted once done):
  *** = todos,
  ??? = questions
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
        self.n_countries = len(countries)
        self.assign_ally_policy(apc)
        self.betting_area = np.zeros((self.n_countries, self.n_countries), dtype=object)
        self.n_steps = 0

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

    def fill_betting_area(self, country, attacked_country):
        """Prepare war by filling betting_area

        Parameters
        ----------
        country : Country Object
                  attacking country

        attacked_c_rank : int
                          rank of attacked country
        """
        self.betting_area[country.rank][attacked_country.rank] = country.military_size

    def step(self):
        """
        colonize played once
        """
        # *** develop dynamic ally policy -> ally policy chosen at each step

        for country in self.countries:
            country.get_military(self.mil_p)
            attacked_country = country.who2attack(self.countries)
            self.fill_betting_area(country, attacked_country)

        # take away 10% land from opponent who lost bet.
        for country in self.countries:
            n = len(country.attacked)
            for attacking_country in country.attacked:
                self.go2war(country, attacking_country, n)
        self.n_steps += 1


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

        # !!! need to fix: check if land_size < 0, if so episode finishes
        if win:
            reward = attacking_country.land_size * 0.1
            country.land_size += reward
            attacking_country.land_size -= reward

        else:
            reward = country.land_size * 0.1
            country.land_size -= reward
            attacking_country.land_size += reward

# ally polices
strongest_country_p = ["no_ally", "weakest", "2nd_strongest"]
sec_strongest_country_p = ["no_ally", "strongest", "weakest"]
weakest_country_p = ["no_ally", "strongest", "2nd_strongest"]


# colonize = Colonize(countries)

# for i in range(20000):
#     colonize.step()
#
# colonize.plot()