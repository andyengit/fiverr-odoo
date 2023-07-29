from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    task_ids = fields.Many2many("project.task", "invoice_ids")
