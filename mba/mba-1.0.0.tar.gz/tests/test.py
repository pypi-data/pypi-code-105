import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from mba import db_connection
from mba.visualization.sales import Cart, Inventory
from mba.visualization.inventory import Storage
from mba.data import data_management
from mba.association import AssociationRule
from mba.data.data_management import DataFlow

# print(DataFlow().connect_to_mysql().execute("select * from product").fetchone())
# print(db_connection().execute("select * from product").fetchone())
print(AssociationRule().get_rules())
# Cart().carts_per_day(True)
Storage().department_distribution_pie(show=True)






