# Prisoner's dilema with trust.

Prisoners have a common pool of trust. They gauge its level as part of
the decision process with which they choose to cooperate or defect.

One thousand simulations of two hundred time steps are run and plotted.

## Run it

You might want to install the required libraries. Perhaps within a [virtualenv](http://virtualenv.org) do:

    $ pip install -r requirements.txt


Each simulation has a python script which handles de runs and
plotting, the pd_trust library implements agent logic. Run them thusly:

    $ ./run_all.sh


## Tit for tat

Agents do onto their acomplice as their acomplice did to them in the
prior time step.

<img width="220" src="plots/tit_for_tat_multi.png">

# Proportional Tit for Tat

Agents do onto their acomplice as their acomplice in average did to them in all prior time steps.

<img width="220" src="plots/proportional_tit_for_tat_multi.png">


# altruist_differential_fitness

<img width="220" src="plots/altruist_differential_fitness.png">

# selfish_memory

<img width="220" src="plots/selfish_memory.png">

# different_memories_tit_for_tat

<img width="220" src="plots/different_memories_tit_for_tat.png">

# selfish_perfect_memory

<img width="220" src="plots/selfish_perfect_memory.png">

# proportional_tit_for_tat

<img width="220" src="plots/proportional_tit_for_tat.png">

# tit_for_tat

<img width="220" src="plots/tit_for_tat.png">

# random_strategy

<img width="220" src="plots/random_strategy.png">

