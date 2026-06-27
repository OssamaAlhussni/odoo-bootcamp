from odoo import models


class ReportLibraryBook(models.AbstractModel):
    _name = "report.library_book.report_book"
    _description = "Book Report"

    def _get_report_values(self, docids, data=None):
        docs = self.env["library.book"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "library.book",
            "docs": docs,
        }
