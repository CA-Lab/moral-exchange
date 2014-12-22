# Game Theory Trust Network

We're modeling networks of prisoner's dilema players.


### Async vs sync

Synchronous version works much like a cellular automata: using data from the current time frame we compute the future time frame.

The async version takes a random node at a time and has it play with all its neighbors.

The multithread version implements random walkers that go from edge to edge and have the nodes at each side play. Walker moves through connected edges. It starts from another random edge if it reaches a dead end.
