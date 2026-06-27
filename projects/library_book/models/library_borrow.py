from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LibraryBorrow(models.Model):
    _name = "library.borrow"
    _description = "Book Borrow Record"
    _order = "borrow_date desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    book_id = fields.Many2one("library.book", string="Book", required=True, tracking=True)
    member_id = fields.Many2one("library.member", string="Member", required=True, tracking=True)
    borrow_date = fields.Date(default=fields.Date.today, required=True, tracking=True)
    return_date = fields.Date(tracking=True)
    expected_return_date = fields.Date(required=True, tracking=True)
    state = fields.Selection([
        ("ongoing", "Ongoing"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ], default="ongoing", tracking=True)
    notes = fields.Text()
    company_id = fields.Many2one("res.company", string="Company",
        default=lambda self: self.env.company)

    @api.constrains("book_id", "state", "borrow_date")
    def _check_already_borrowed(self):
        for record in self:
            if record.state == "ongoing":
                existing = self.search([
                    ("book_id", "=", record.book_id.id),
                    ("state", "=", "ongoing"),
                    ("id", "!=", record.id),
                ])
                if existing:
                    raise UserError(_("This book is already borrowed."))

    @api.onchange("expected_return_date")
    def _onchange_expected_return(self):
        if self.expected_return_date and self.borrow_date:
            if self.expected_return_date < self.borrow_date:
                self.expected_return_date = self.borrow_date

    def action_return(self):
        today = fields.Date.today()
        for record in self:
            record.write({
                "return_date": today,
                "state": "returned",
            })
            record.book_id.state = "available"

    @api.model
    def _cron_check_overdue(self):
        today = fields.Date.today()
        overdue = self.search([
            ("state", "=", "ongoing"),
            ("expected_return_date", "<", today),
        ])
        overdue.write({"state": "overdue"})
        return True
