from odoo import models, fields

class SocialReport(models.Model):
    _name = "fvd_custom.social_report"

    area_emisor = fields.Many2one("hr.department", "Area o Programa emisor")
    area_receptor = fields.Many2one("hr.department", "Area o programa receptora")
    date = fields.Date("Fecha")
    trabajador = fields.Many2one("hr.employee", "Trabajador/a Social que emite el informe")
    motivo = fields.Char("Motivo")
    partner_id = fields.Many2one("res.partner", "USUARIX")

    situacion_familiar = fields.Text("Situacion Familiar")
    situacion_economica = fields.Text("Situacion Familiar")
    vivienda = fields.Text("Vivienda")
    salud = fields.Text("Salud")
    Valoracion_profesional = fields.Text("Valoracion Profesional")


