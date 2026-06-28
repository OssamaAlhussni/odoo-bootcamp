from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        readonly=True,
        copy=False,
    )
    sales_person_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
        copy=False,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    def action_sell(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold."))
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled."))
            record.state = "cancelled"
        return True

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError(_("The expected price must be strictly positive."))

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price <= 0:
                raise ValidationError(_("The selling price must be positive."))

    @api.constrains("selling_price", "expected_price")
    def _check_valid_selling_price(self):
        for record in self:
            if (
                record.selling_price
                and record.expected_price
                and record.selling_price < record.expected_price * 0.9
            ):
                raise ValidationError(
                    _("Selling price cannot be lower than 90% of the expected price.")
                )

    _sql_constraints = [
        ("check_expected_price_positive", "CHECK(expected_price >= 0)", "The expected price must be strictly positive."),
        ("check_selling_price_positive", "CHECK(selling_price >= 0)", "The selling price must be positive."),
    ]
