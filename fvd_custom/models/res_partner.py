from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class ResPartner(models.Model):
    _inherit = "res.partner"

    passport = fields.Char(string="Nº Pasaporte")
    birthdate = fields.Date(string="Fecha de Nacimiento")
    age = fields.Integer(string="Edad",compute="_compute_age")
    title = fields.Many2one(string="Id. Genero")
    nationality_ids = fields.Many2many("res.partner.nationality","partner_ids",string="Nacionalidad")

    @api.depends("birthdate", "age")
    def _compute_age(self):
        today = datetime.today().date()
        for record in self:
            if not record.birthdate:
                record.age = False
                continue
            record.age = (
                today.year
                - record.birthdate.year
                - ((today.month, today.day) < (record.birthdate.month, record.birthdate.day))
            )

    @api.constrains("birthdate")
    def _check_age(self):
        for record in self:
            if record.birthdate > datetime.today().date():
                raise ValidationError("La fecha de nacimiento no puede superar la fecha actual")
