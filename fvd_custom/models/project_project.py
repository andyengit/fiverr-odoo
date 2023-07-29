from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    partner_id = fields.Many2one(string="Usuarix")
