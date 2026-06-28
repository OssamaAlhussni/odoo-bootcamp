# estate_property_type.py — Property Type/Category Model
# =======================================================
# Simple model for categorizing properties (e.g., House, Apartment, Villa).
# Properties are linked via Many2one on estate.property.
#
# This is a simple "helper" model — just a name with a reverse relationship.
# Demonstrates: One2many, SQL unique constraint, _order

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    # _order sorts records alphabetically by name by default
    _order = "name asc"

    name = fields.Char(string="Name", required=True)

    # One2many = reverse of Many2one on estate.property.property_type_id
    # This lets you see all properties of a given type from the type's form view
    property_ids = fields.One2many(
        "estate.property",  # The other model
        "property_type_id",  # The field on estate.property that points here
        string="Properties",
    )

    # SQL constraint: cannot have two types with the same name
    _sql_constraints = [
        (
            "unique_type_name",
            "UNIQUE(name)",
            "Property type name must be unique.",
        ),
    ]
