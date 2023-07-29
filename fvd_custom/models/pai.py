from odoo import models, fields

class SocialReport(models.Model):
    _name = "fvd_custom.pai"

    partner_id = fields.Many2one("res.partner","USUARIX")

    valoracion_dependencia = fields.Boolean("VALORACIÓN DE DEPENDENCIA")
    grado = fields.Char("GRADO")
    centro_de_salud = fields.Char("CENTRO DE SALUD ADSCRIPCIÓN")
    hospital_ref = fields.Char("HOSPITAL DE REFERENCIA")

    sanitario_obj = fields.Text("Objetivos")
    sanitario_act = fields.Text("Actuaciones")

    familiar_obj = fields.Text("Objetivos")
    familiar_act = fields.Text("Actuaciones")

    eco_obj = fields.Text("Objetivos")
    eco_act = fields.Text("Actuaciones")

    vivienda_obj = fields.Text("Objetivos")
    vivienda_act = fields.Text("Actuaciones")

    ocio_obj = fields.Text("Objetivos")
    ocio_act = fields.Text("Actuaciones")

    fecha = fields.Date("Fecha")
    prox_rev = fields.Date("Próxima revisión")

