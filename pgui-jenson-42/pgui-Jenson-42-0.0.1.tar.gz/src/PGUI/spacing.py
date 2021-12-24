def space_elements(
            elements: "list[int]",
            size: int,
            spacing: int,
            padding: int,
            position: int = 0
        ) -> tuple:
    """ Set size and position of elements to space them correctly in a
        given distance."""

    """Calculate each element's width."""
    ##Remove padding from either end of distance.
    size -= padding*2
    ##Calculate total element space without padding or spacing.
    element_space = size - spacing * (len(elements)-1)
    ##Divide total space by sum of the ratio between elements.
    multiplier = element_space/sum(elements)
    ##Multiply by ratio to get each element width.
    element_widths = [round(e*multiplier) for e in elements]

    """Calculate each element's position."""
    element_positions = []
    ##Calculate position and add to list.
    for i in range(len(elements)):
        element_positions.append(round(
            spacing * i
            + sum(element_widths[:i]) ##Add previous element widths.
            + padding
            + position
        ))
    
    return element_positions, element_widths