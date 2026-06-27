from odoo import api, models, fields


class LibraryCategory(models.Model):
    _name = "library.category"
    _description = "Book Category"
    _order = "name asc"

    name = fields.Char(string="Category Name", required=True, translate=True)
    description = fields.Text()
    book_ids = fields.One2many("library.book", "category_id", string="Books")
    book_count = fields.Integer(compute="_compute_book_count", string="Book Count")

    @api.depends("book_ids")
    def _compute_book_count(self):
        for record in self:
            record.book_count = len(record.book_ids)
