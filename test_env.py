import itertools

from multi_agent_env import Colonize, Country

Korea = Country("Korea", 30)
Canada = Country("Canada", 25)
China = Country("China", 20)

countries = [Korea, Canada, China]

n_rounds = 20000
mil_p = 0.1

strongest_country_p = ["no_ally", "weakest", "2nd_strongest"]
sec_strongest_country_p = ["no_ally", "strongest", "weakest"]
weakest_country_p = ["no_ally", "strongest", "2nd_strongest"]

lst = [strongest_country_p,
       sec_strongest_country_p,
       weakest_country_p]

ally_policy_combs = list(itertools.product(*lst))

for apc in ally_policy_combs:
    colonize = Colonize(countries, mil_p, apc)
    for i in range(n_rounds):
        colonize.step()
        break
    break