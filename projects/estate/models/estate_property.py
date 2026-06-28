# estate_property.py — Main Real Estate Property Model
# =====================================================
# This is the core model of the Real Estate module.
# Each property has details like price, size, location, owner, and status.
#
# Odoo Model Types:
# - models.Model:    Regular model — creates a database table, stores data permanently
# - TransientModel:  For wizards — data is temporary, auto-deleted
# - AbstractModel:   No database table — used for mixins/reusable code
#
# We use models.Model here because properties are permanent business data.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    # _name = the technical name (used in code, XML, and becomes the DB table)
    #   The dots (.) become underscores (_) in the DB: estate.property → estate_property
    # _description = human-readable label shown in Odoo's technical menus
    _name = "estate.property"
    _description = "Estate Property"

    # ---- BASIC FIELDS ----
    # Each field type maps to a database column.
    # Common types: Char (short text), Text (long text), Float (decimal),
    # Integer, Boolean, Date, Datetime, Selection (dropdown), Binary (files/images).

    name = fields.Char(string="Name", required=True)
    # string= controls the label shown in the UI
    # required=True = user MUST fill this in before saving

    description = fields.Text(string="Description")
    # Text = multi-line text area

    date_availability = fields.Date(
        string="Available From",
        # default = 3 months from today (lambda = function, evaluated per-record)
        # DateTime.today() gives today's date in the user's timezone
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,  # Don't copy this field when duplicating a record
    )

    # ---- FINANCIAL FIELDS ----
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,  # Users can't edit it manually — only set by code
        copy=False,
    )

    # ---- PROPERTY DETAILS ----
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)

    # Boolean = checkbox (True/False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Float(string="Garden Area (sqm)")

    # Selection = dropdown menu — value pairs are (stored_value, display_label)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )

    # ---- COMPUTED FIELDS ----
    # Computed fields are NOT stored in the database by default.
    # They calculate their value from other fields on the fly.
    # Add store=True if you want them saved (needed for searching/sorting).

    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",  # Name of the method that calculates it
        # NOTE: no store=True → recalculated every time you view it
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )

    # ---- RELATIONAL FIELDS ----
    # Many2one = child → parent (this record references ONE parent)
    #   DB stores the parent's ID as a foreign key
    property_type_id = fields.Many2one(
        "estate.property.type",  # Name of the OTHER model
        string="Property Type",
    )

    # Many2one to res.partner (built-in Odoo contact model)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        readonly=True,
        copy=False,
    )

    # Many2one to res.users (built-in Odoo user model)
    # default = current logged-in user (self.env.user)
    sales_person_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )

    # One2many = parent → children (reverse of Many2one)
    #   First param = child model, second param = field on child that points back here
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",  # The Many2one field on estate.property.offer
        string="Offers",
    )

    # Many2many = both sides can have multiple records
    #   Creates a hidden "relation table" in the DB
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )

    # ---- STATE / WORKFLOW ----
    # Selection = dropdown with fixed options
    # This tracks the property's lifecycle: New → Offer Received → Offer Accepted → Sold/Cancelled
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",  # Every new property starts as "New"
        copy=False,     # Don't copy the state when duplicating
    )

    # ---- COMPUTED FIELD METHODS ----
    # The @api.depends decorator tells Odoo when to recalculate.
    # When living_area OR garden_area changes, Odoo re-runs this method.

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        # self is a RECORDSET (can contain 1 or many records)
        # Always loop over self even if you expect 1 record
        for record in self:
            # Compute total = living + garden (simple addition)
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            # mapped() extracts field values from related records
            # max() finds the highest price among all offers
            # If no offers exist, set best_price to 0
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    # ---- ACTION METHODS ----
    # Action methods are called when a user clicks a button in the UI.
    # They should return True or an action dictionary.

    def action_sell(self):
        # Prevent selling cancelled properties
        for record in self:
            if record.state == "cancelled":
                raise UserError(
                    _("Cancelled properties cannot be sold.")  # _() marks text for translation
                )
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled."))
            record.state = "cancelled"
        return True

    # ---- CONSTRAINTS ----
    # @api.constrains runs validation when the listed fields are modified.
    # Raise ValidationError to reject the change.

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            if record.expected_price and record.expected_price <= 0:
                raise ValidationError(
                    _("The expected price must be strictly positive.")
                )

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price <= 0:
                raise ValidationError(_("The selling price must be positive."))

    @api.constrains("selling_price", "expected_price")
    def _check_valid_selling_price(self):
        # Selling price can't be less than 90% of expected price
        for record in self:
            if (
                record.selling_price
                and record.expected_price
                and record.selling_price < record.expected_price * 0.9
            ):
                raise ValidationError(
                    _("Selling price cannot be lower than 90% of the expected price.")
                )

    # ---- SQL CONSTRAINTS ----
    # These are enforced at the DATABASE level (not Python).
    # Format: (name, SQL_expression, error_message)
    # Useful for: unique checks, positive value checks, etc.

    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price >= 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]
