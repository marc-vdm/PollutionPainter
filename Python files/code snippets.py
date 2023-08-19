


def random_on_off(p, dots=240):
    """Create a list of 'dots' items and randomly assign each item to be on or off with probability 'p'."""

    if p > 0 or p < 1:
        print('probability value given was outside of 0-1 range, assuming 0.5')
        p = 0.5
    # make a list of 'dots' items with probability 'p' of randomly being True
    rand_list = np.random.choice([False, True], size=(dots,), p=[1-p, p])

    # convert the random True/False values to RGB on/off values
    dot_list = [(255, 255, 255) for i in rand_list if i]
    return dot_list