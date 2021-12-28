from road_collisions_base import logger
from road_collisions_base.models.collision import Collisions


def main():

    # NOTE: If you're running into ram issues and want to play with stuff,
    # set region kwarg on load_all to ireland / us / uk to only use collisions
    # from those regions
    collisions = Collisions.load_all()

    logger.info('Loaded %s collisions', (len(collisions)))
    logger.info('Do something with the data in the variable \'collisions\'...')

    import pdb; pdb.set_trace()

    pass



if __name__ == '__main__':
    main()
