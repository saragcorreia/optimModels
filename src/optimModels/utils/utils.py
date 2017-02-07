def merge_two_dicts(x, y):
    """
        Merge two dictinaries, if the key are present in both, value of y[key] are maintained
        :param x: dictionary
        :param y: dictionary
        """
    z = x.copy()
    z.update(y)
    return z

