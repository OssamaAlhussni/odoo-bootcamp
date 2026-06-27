from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Book"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name asc"
    _rec_name = "name"

    name = fields.Char(string="Title", required=True, tracking=True)
    author = fields.Char(tracking=True)
    isbn = fields.Char(string="ISBN", size=13, tracking=True)
    publisher = fields.Char()
    date_published = fields.Date()
    pages = fields.Integer()
    price = fields.Float(digits=(6, 2))
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("available", "Available"),
        ("borrowed", "Borrowed"),
        ("lost", "Lost"),
        ("damaged", "Damaged"),
    ], string="Status", default="draft", tracking=True, group_expand="_expand_states")
    description = fields.Html()
    cover = fields.Image(max_width=512, max_height=512)
    category_id = fields.Many2one("library.category", string="Category", tracking=True)
    member_ids = fields.Many2many("library.member", string="Borrowers",
        compute="_compute_member_ids", store=False)
    borrow_ids = fields.One2many("library.borrow", "book_id", string="Borrow History")
    current_borrow_id = fields.Many2one("library.borrow", string="Current Borrow",
        compute="_compute_current_borrow", store=False)
    company_id = fields.Many2one("res.company", string="Company",
        default=lambda self: self.env.company)

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, _ in self._fields["state"].selection]

    @api.depends("borrow_ids", "borrow_ids.state")
    def _compute_current_borrow(self):
        for record in self:
            record.current_borrow_id = record.borrow_ids.filtered(
                lambda b: b.state == "ongoing"
            )[:1]

    @api.depends("borrow_ids", "borrow_ids.member_id")
    def _compute_member_ids(self):
        for record in self:
            record.member_ids = record.borrow_ids.mapped("member_id")

    @api.constrains("isbn")
    def _check_isbn(self):
        for record in self:
            if record.isbn and len(record.isbn) != 13:
                raise ValidationError(_("ISBN must be exactly 13 characters."))

    @api.onchange("price")
    def _onchange_price(self):
        if self.price and self.price < 0:
            self.price = 0

    def action_available(self):
        self.state = "available"

    def action_lost(self):
        self.state = "lost"

    def action_damaged(self):
        self.state = "damaged"
