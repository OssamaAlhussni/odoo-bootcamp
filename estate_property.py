from odoo import api, models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    
    name = fields.Char(required=True)
    location = fields.Text()
    bedrooms = fields.Integer()
    expected_price = fields.Float()
    selling_price = fields.Float()
    living_area = fields.Integer()
    garden_area = fields.Integer()
    has_garden = fields.Boolean()
    date_availability = fields.Date()

    total_area = fields.Integer(compute = "_compute_total_area")
    @api.depends("living_area", "has_garden", "garden_area")
    def _compute_total_area(self):
        for record in self:
            if record.has_garden:
                record.total_area=record.living_area+record.garden_area
            else:
                record.total_area=record.living_area


