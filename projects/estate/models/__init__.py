# This file imports all model files from the models/ folder.
# Each model class is defined in its own file for organization.
# Odoo needs ALL model files imported here so it can find them.

from . import estate_property        # Main estate.property model
from . import estate_property_type   # Categories/types for properties
from . import estate_property_offer  # Offers made on properties
from . import estate_property_tag    # Tags/labels for properties
from . import res_users              # Extension of the built-in user model
