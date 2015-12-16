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

## Proportional Tit for Tat

Agents do onto their acomplice as their acomplice in average did to them in all prior time steps.

<img width="220" src="plots/proportional_tit_for_tat_multi.png">

## altruist differential fitness

<img width="220" src="plots/altruist_differential_fitness_multi.png">

## selfish_memory

<img width="220" src="plots/selfish_memory_multi.png">

## different memory sizes tit for tat

<img width="220" src="plots/different_memories_tit_for_tat_multi.png">

## selfish perfect memory

<img width="220" src="plots/selfish_perfect_memory_multi.png">

## tit for tat

<img width="220" src="plots/tit_for_tat_multi.png">

## Random strategy

<img width="220" src="plots/random_strategy_multi.png">

# Single runs
<table>
<tr><td><img width="150" src="plots/single_runs/memory_10_1.png"></td>
             <td><img width="150" src="plots/single_runs/memory_10_2_venganza.png"></td>
    <td><img width="150" src="plots/single_runs/memory_20_1.png"></td>
             <td><img width="150" src="plots/single_runs/memory_5_1.png"></td>
</tr>
<tr><td><img width="150" src="plots/single_runs/memory_5_2.png"></td>
             <td><img width="150" src="plots/single_runs/memory_5_3.png"></td>
    <td><img width="150" src="plots/single_runs/memory_5_4.png"></td>
             <td><img width="150" src="plots/single_runs/memory_5_5.png"></td>
</tr>
<tr><td><img width="150" src="plots/single_runs/memory_5_6_trivialoide.png"></td>
             <td><img width="150" src="plots/single_runs/memory_5_7.png"></td>
    <td><img width="150" src="plots/single_runs/proportional_2.png"></td>
             <td><img width="150" src="plots/single_runs/proportional_3.png"></td>
</tr>
<tr><td><img width="150" src="plots/single_runs/proportional_4.png"></td>
             <td><img width="150" src="plots/single_runs/proportional_5.png"></td>
    <td><img width="150" src="plots/single_runs/proportional.png"></td>
             <td></td>
</tr>
</table>