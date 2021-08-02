from ray.rllib.env.multi_agent_env import MultiAgentEnv
import numpy as np

class Colonize(MultiAgentEnv):
    """
    Description:
        Three countries(Agent) tries to take over much land as possible,
        countries cooperate with each other at times and also they go against
        each other to take over more land.

    Parameters
    ----------
    land_size : int
                used to create land_size array
                filled with 0. where 0 => doesn't belong to
                anyone

    """
    def __init__(self, land_size,):
        self.land = np.zeros(land_size)

        self.agents = [1,2,3]


    def step(self):
        """


        :return:
        """

    def reset(self):
        """
        Resets environment to initial conditions
        """


class Country:
    """

    Parameters
    ---------
    land : tuple
           (a,b) => land[a:b] is given to
           a country
    truth : list
            each element is country it has truth
            with.
            rules:
            1. Cannot attack country within truth
            2. Stay truth for 10 turns

    """
    def __init__(self, name, land):
        self.name = name
        self.land = land
        self.truth = []
        assert len(self.truth) <= 1, "You cannot have truth with all Countries"

        self.state =
        self.action =



Country("Korea", (0,10))
Country("Canada", (11,30))
Country("China", (50,100))


data = {
    "Agent1":[],
    "Agent2":[],
    "Agent3":[]
}