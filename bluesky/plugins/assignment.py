""" BlueSky plugin template. The text you put here will be visible
    in BlueSky as the description of your plugin. """
from random import randint
import numpy as np
# Import the global bluesky objects. Uncomment the ones you need
from bluesky import core, stack, traf, tools  #, settings, navdb, sim, scr, tools
from bluesky.tools import areafilter

### Initialization function of your plugin. Do not change the name of this
### function, as it is the way BlueSky recognises this file as a plugin.
def init_plugin():
    ''' Plugin initialisation function. '''
    # Instantiate our example entity
    example = Assignment()

    # Configuration parameters
    config = {
        # The name of your plugin
        'plugin_name':     'ASSIGNMENT',

        # The type of this plugin. For now, only simulation plugins are possible.
        'plugin_type':     'sim',
        }

    # init_plugin() should always return a configuration dict.
    return config


### Entities in BlueSky are objects that are created only once (called singleton)
### which implement some traffic or other simulation functionality.
### To define an entity that ADDS functionality to BlueSky, create a class that
### inherits from bluesky.core.Entity.
### To replace existing functionality in BlueSky, inherit from the class that
### provides the original implementation (see for example the asas/eby plugin).
class Assignment(core.Entity):
    ''' Example new entity object for BlueSky. '''
    def __init__(self):
        super().__init__()
        # All classes deriving from Entity can register lists and numpy arrays
        # that hold per-aircraft data. This way, their size is automatically
        # updated when aircraft are created or deleted in the simulation.
        with self.settrafarrays():
            self.npassengers = np.array([])

        stack.stack('Cre KL123, A320, EHAM, RWY18L')
        stack.stack('ADDWPT KL123 HELEN')
        stack.stack('SPD KL123 250')

        stack.stack('POLY polytest 60,0,60,10,50,10,50,0,60,0')
        stack.stack('COLOR polytest red')

    def create(self, n=1):
        ''' This function gets called automatically when new aircraft are created. '''
        # Don't forget to call the base class create when you reimplement this function!
        super().create(n)
        # After base creation we can change the values in our own states for the new aircraft
        self.npassengers[-n:] = [randint(0, 150) for _ in range(n)]

    # Functions that need to be called periodically can be indicated to BlueSky
    # with the timed_function decorator
    @core.timed_function(name='example', dt=5)
    def update(self):
        ''' Periodic update function for our example entity. '''
        stack.stack('ECHO Example update: creating a random aircraft')
        stack.stack('MCRE 1')

        # if areafilter.checkInside("polytest", 52, 5, 300):
        #     print("AMS inside!")

        ac_idx = traf.id2idx("KL123") #traf.id['KL123']
        print(ac_idx)
        # if areafilter.checkInside("polytest", traf.lat[ac_idx], traf.lon[ac_idx], traf.alt[ac_idx]):
        #     traf.delete(ac_idx)

    # You can create new stack commands with the stack.command decorator.
    # By default, the stack command name is set to the function name.
    # The default argument type is a case-sensitive word. You can indicate different
    # types using argument annotations. This is done in the below function:
    # - The acid argument is a BlueSky-specific argument with type 'acid'.
    #       This converts callsign to the corresponding index in the traffic arrays.
    # - The count argument is a regular int.
    @stack.command
    def passengers(self, acid: 'acid', count: int = -1):
        ''' Set the number of passengers on aircraft 'acid' to 'count'. '''
        if count < 0:
            return True, f'Aircraft {traf.id[acid]} currently has {self.npassengers[acid]} passengers on board.'

        self.npassengers[acid] = count
        return True, f'The number of passengers on board {traf.id[acid]} is set to {count}.'
