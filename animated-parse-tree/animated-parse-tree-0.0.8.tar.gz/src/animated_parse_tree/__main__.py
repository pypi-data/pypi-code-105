from .parse_tree import ParseTree


# REPL Simulation
def main():
    '''
    Runs the animated_parse_tree program interactively

    Parameters
    ----------
    **kwargs
        Keyword arguments to be passed to ParseTree().animate.

    Returns
    -------
    None
        This program does not return anything.

    Examples
    --------
    ```bash
    ?> 1 + 2
    1 + 2 = 3

     +
    / \\
    1 2
    ```
    '''
    expression = input('?> ')
    while expression != '':
        t = ParseTree()
        t.read(expression)
        print(expression, '=', t.evaluate())
        print()
        print(str(t))
        expression = input('?> ')
    print('Bye :)')


if __name__ == '__main__':
    main()