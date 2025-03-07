import random
import time

def random_pauser(kb_listener,lower_bound=None, upper_bound=None, add_random=False):
    """
    Pause execution for a random duration, checking frequently for a stop signal.
    
    If no bounds are provided, it sleeps for a random time between 0 and 10 second.
    Otherwise, it sleeps for a random time between the provided bounds.

    If add_random is True, the sleep time is increased by a random amount by a 0-25% of the bound provided.
    """
    if lower_bound is None and upper_bound is None:
        total_sleep = random.random()
    else:
        if lower_bound is None:
            lower_bound = 0.0
        if upper_bound is None:
            upper_bound = 10.0
        if upper_bound < lower_bound:
            raise ValueError("upper_bound must be greater than lower_bound")
        total_sleep = random.uniform(lower_bound, upper_bound)
        if add_random:
            total_sleep += random.uniform(0, 0.25 * (upper_bound - lower_bound))
    
    sleep_increment = 0.01  # Check every 10ms
    elapsed = 0.0
    while elapsed < total_sleep:
        if kb_listener.check_stop_key():
            raise KeyboardInterrupt("Stop key pressed, exiting sleep early.")
        time.sleep(sleep_increment)
        elapsed += sleep_increment
