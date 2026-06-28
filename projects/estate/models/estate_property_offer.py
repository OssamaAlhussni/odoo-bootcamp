# estate_property_offer.py — Property Offer Model
# =================================================
# Represents an offer made by a customer/partner to buy a property.
# Related to estate.property via the property_id Many2one field.
#
# Key Odoo concepts demonstrated:
# - Computed fields with inverse
# - Action methods that modify RELATED records
# - SQL constraints vs Python constraints
# - Selection (dropdown) fields
# - _order for default sorting

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    # _order = default sort when listing records
    # "price desc" = highest price first (useful for auctions)
    _order = "price desc"

    # ---- FIELDS ----
    price = fields.Float(string="Price", required=True)

    # Status workflow: draft (no status) → accepted or refused
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,  # When duplicating an offer, reset the status
    )

    # Many2one to the partner/contact who made the offer
    partner_id = fields.Many2one(
        "res.partner",  # Odoo's built-in contacts/partners model
        string="Partner",
        required=True,
    )

    # Many2one back to the property this offer is for
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )

    # ---- COMPUTED FIELD WITH INVERSE ----
    # validity = number of days the offer is valid
    validity = fields.Integer(string="Validity (days)", default=7)

    # date_deadline = computed from create_date + validity
    # It has BOTH compute AND inverse
    #   compute → reads validity to calculate deadline
    #   inverse → lets user edit deadline to UPDATE validity
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        # create_date = the date/time when the record was created
        # fields.Date.to_date() converts datetime to date
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.to_date(
                    record.create_date
                    + relativedelta(days=record.validity)
                )

    def _inverse_date_deadline(self):
        # Inverse method = user changed the deadline → update validity
        # Opposite of compute: calculate validity from deadline
        for record in self:
            if record.date_deadline and record.create_date:
                delta = fields.Date.to_date(record.date_deadline) - fields.Date.to_date(
                    record.create_date
                )
                record.validity = delta.days

    # ---- ACTION METHODS ----
    # These are triggered by buttons in the form view.

    def action_accept(self):
        # When accepting an offer:
        # 1. Check no other offer was already accepted
        # 2. Set this offer's status to "accepted"
        # 3. Update the PROPERTY with buyer, selling price, and state
        for record in self:
            # filtered() returns only offers where status == "accepted"
            already_accepted = record.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            if already_accepted:
                raise UserError(
                    _("An offer has already been accepted for this property.")
                )

            record.status = "accepted"
            # write() updates multiple fields at once (more efficient than individual assignments)
            # This modifies the RELATED property (not this offer record)
            record.property_id.write({
                "buyer_id": record.partner_id.id,
                "selling_price": record.price,
                "state": "offer_accepted",  # Move the property workflow forward
            })
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state == "accepted":
                raise UserError(_("Accepted offers cannot be refused."))
            record.status = "refused"
        return True

    # ---- SQL CONSTRAINTS ----
    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]
