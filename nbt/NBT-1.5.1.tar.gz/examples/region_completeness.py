#!/usr/bin/env python
"""
Checks if all chunks are generated in each region (within a given radius from spawn)
"""

import locale, os, sys
import math

# local module
try:
    import nbt
except ImportError:
    # nbt not in search path. Let's see if it can be found in the parent folder
    extrasearchpath = os.path.realpath(os.path.join(__file__,os.pardir,os.pardir))
    if not os.path.exists(os.path.join(extrasearchpath,'nbt')):
        raise
    sys.path.append(extrasearchpath)
    import nbt

from nbt.world import WorldFolder

def main(world_folder, radius = 2048):
    # block radius to region radius
    try:
        radius = max(int(math.ceil(radius/512)), 1)
        world = WorldFolder(world_folder)
        for x in range(-radius, radius):
            print(x)
            for z in range(-radius, radius):
                region = world.get_region(x,z)
                chunk_count = region.chunk_count()
                if chunk_count != 1024:
                    print(x, z, chunk_count)
                # Somehow, Python does not clean up properly
                region.close()
    except KeyboardInterrupt as err:
        return 75 # EX_TEMPFAIL
    return 0 # NOERR

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print("No playerdata folder specified!")
        sys.exit(64) # EX_USAGE
    if (len(sys.argv) >= 3):
        try:
            radius = int(sys.argv[2])
        except ValueError:
            print("Invalid radius %s" % sys.argv[2])
            sys.exit(64) # EX_USAGE
    else:
        radius = 2048
    world_folder = sys.argv[1]
    # clean path name, eliminate trailing slashes:
    world_folder = os.path.normpath(world_folder)
    if (not os.path.exists(world_folder)):
        print("No such folder as "+world_folder)
        sys.exit(72) # EX_IOERR
    
    sys.exit(main(world_folder, radius))
