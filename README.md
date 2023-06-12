# LAMAS Project

We implemented the game of Kemps, using epistemic logic principles, such as higher-order theory of
mind and public announcements. The code can be run through the command ``py main.py``, in which
case a pygame console starts, through which the user can play against two epistemic logic model
(Model 1 and Model 2). The ``requirements.txt`` file specifies compatible 
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