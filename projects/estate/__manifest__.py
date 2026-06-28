# Odoo Module Manifest
# Every Odoo module MUST have this file — it tells Odoo about the module.

# Key concepts:
# - "name": display name in the Apps menu
# - "depends": list of other modules this needs (base is always required)
# - "data": XML and CSV files to load (order matters — security first!)
# - "application": True means it shows in the Apps list
{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "application": True,
    "data": [
        # Security must come first so users can access the views
        "security/ir.model.access.csv",
        # Views define UI layout (menus should be last)
        "views/estate_menus.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users_views.xml",
    ],
}
