# This module adds accounting features to the Real Estate module.
# It depends on both "estate" (our module) and "account" (Odoo Accounting).
# When both modules are installed, properties get accounting fields.
{
    "name": "Real Estate Account",
    "version": "1.0",
    "depends": ["estate", "account"],
    "application": True,
    "data": [
        "views/estate_property_views.xml",
    ],
}
