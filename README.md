# LAMAS Project

We implemented the game of Kemps, using epistemic logic principles, such as higher-order theory of
mind and public announcements. The code can be run through the command ``py main.py``, in which
case a pygame console starts, through which the user can play against two epistemic logic model
(Model 1 and Model 2).  The user chooses what kind of agents to play against:either Greedy, 
KB Greedy or KB Blocking (default: Greedy strategy). The cards on the left of the interface corresponds to 
Model 1 and the cards on the right of the interface corresponds to Model 2. The user can interact with the 
table and hand cards by swapping one card for another: simply click on a table card and a hand card (or vice versa).
If the user clicks on any part of the interface that is not meant to be clickable 
(anything other than the table and hand cards and the Next turn button) the interface 
momentarily freezes BUT it does not crash. If this happens, let it run for a few seconds
without clicking on anything else. Note that the game ends abruptly after 9 Kemps have been completed.
This is the maximum number of Kemps formations with 52 playing cards. 

The ``requirements.txt`` file specifies compatible 
package versions for Python 3.10 (we cannot guarantee compatibility for 
other Python versions). 

Code functionality is distributed across files and folders as follows:
* ``agent.py`` - implements the strategies of the agents
* ``announcements.py`` - implements agent moves as public announcements
* ``card.py`` - implements the card and deck classes
* ``knowledge_base.py`` - implements the knowledge base of an agent (keep track of all
52 cards in a deck of cards)
* ``main.py`` - main code, which implements the user interface and communication with
the models
* ``test_agent.py`` - environment to test the functionality of the models (not part of
the main pipeline)
* ``view.py`` - utility functions for the user interface 
* ``card_design`` - folder containing images used for card display
