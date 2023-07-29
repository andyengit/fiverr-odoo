from odoo import fields, models


class ResPartnerNationality(models.Model):
    _name = "res.partner.nationality"

    name = fields.Char("Nombre")
    country_id = fields.Char("res.country")
    partner_ids = fields.Many2many("res.partner", "nationality_ids")
