from odoo import api, fields, models

class Dafo(models.Model):
    _name = "fvd_custom.dafo"

    expedient_number = fields.Integer(string="Nro de expediente")
    employee_id = fields.Many2one("hr.employee", string="Empleado")

    points_to_improve = fields.Text(string="Puntos a mejorar")
    strengths = fields.Text(string="Puntos fuertes")

    start_date = fields.Date(string="Fecha de realización")
    check_date = fields.Date(string="Fecha de revisión")
