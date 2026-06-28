# res_users.py — Extension of Odoo's Built-in User Model
# ========================================================
# This file "inherits" (adds to) the existing res.users model.
# We don't create a new table — we ADD a field to the existing users table.
#
# This is called "extension inheritance" — same model, more fields.
# Compare with "classical inheritance" where _name creates a new model.
#
# The original res.users model is defined in Odoo's base module.
# By using _inherit WITHOUT _name, we EXTEND it instead of creating a new one.

from odoo import models, fields


class ResUsers(models.Model):
    # _inherit = "res.users" WITHOUT _name = we are ADDING to the existing model
    # No new database table is created!
    _inherit = "res.users"

    # One2many to show all properties assigned to this salesperson
    # domain filters which properties appear (only active/new ones)
    property_ids = fields.One2many(
        "estate.property",
        "sales_person_id",  # The Many2one on estate.property pointing here
        string="Properties",
        domain=[("state", "in", ("new", "offer_received"))],
    )
