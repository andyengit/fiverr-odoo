from odoo import fields, models


class ProjectTast(models.Model):
    _inherit = "project.task"

    partner_id = fields.Many2one("res.partner", string="Usuarix")
    invoice_ids = fields.Many2many("account.move", "task_ids", string="Facturas")
    company_currency_id = fields.Many2one("res.currency", related="company_id.currency_id")


