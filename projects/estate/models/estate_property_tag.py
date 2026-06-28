# estate_property_tag.py — Property Tag Model
# ============================================
# Tags are labels that can be applied to properties via Many2many.
# Each tag has a name and a color (used in the UI for visual distinction).
#
# Demonstrates: Many2many partner model, Integer field for color picker

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)

    # Color is an Integer that maps to Odoo's built-in color palette
    # In views, use widget="color" to show a color picker
    # 0 = no color, 1-11 = various colors
    color = fields.Integer(string="Color")

    # SQL constraint: tag names must be unique
    _sql_constraints = [
        (
            "unique_tag_name",
            "UNIQUE(name)",
            "Property tag name must be unique.",
        ),
    ]
