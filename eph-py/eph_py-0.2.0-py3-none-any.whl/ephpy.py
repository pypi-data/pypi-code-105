from compute_poverty import compute_poverty
from get_micro_data import get_micro_data
from get_poverty_lines import get_poverty_lines

def print_poverty(year):
    basket = get_poverty_lines(regional=False)
    base = get_micro_data(year,trimester = 1,base_type='individual')
    compute_poverty(base,basket)


if __name__ == '__main__':
    for year in range(2017,2021):
        print(year)
        print_poverty(year)
    
