from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryMember(models.Model):
    _name = "library.member"
    _description = "Library Member"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "name asc"

    name = fields.Char(string="Member Name", required=True, tracking=True)
    email = fields.Char(tracking=True)
    phone = fields.Char()
    photo = fields.Image(max_width=256, max_height=256)
    membership_date = fields.Date(default=fields.Date.today)
    expiry_date = fields.Date()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ("active", "Active"),
        ("expired", "Expired"),
        ("suspended", "Suspended"),
    ], default="active", tracking=True)
    borrow_ids = fields.One2many("library.borrow", "member_id", string="Borrows")
    borrow_count = fields.Integer(compute="_compute_borrow_count")
    current_borrow_ids = fields.One2many("library.borrow", "member_id",
        string="Current Borrows", domain=[("state", "=", "ongoing")])
    company_id = fields.Many2one("res.company", string="Company",
        default=lambda self: self.env.company)

    @api.depends("borrow_ids")
    def _compute_borrow_count(self):
        for record in self:
            record.borrow_count = len(record.borrow_ids)

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if record.email and "@" not in record.email:
                raise ValidationError("Invalid email address.")

    def action_expire(self):
        self.state = "expired"

    def action_suspend(self):
        self.state = "suspended"

    def action_reactivate(self):
        self.state = "active"
