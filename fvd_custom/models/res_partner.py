from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    passport = fields.Char(string="Nº Pasaporte")
    birthdate = fields.Date(string="Fecha de Nacimiento")
    age = fields.Integer(string="Edad", compute="_compute_age")
    title = fields.Many2one(string="Id. Genero")
    nationality_one = fields.Many2one(string="Nacionalidad 1", comodel_name="res.country")
    nationality_two = fields.Many2one(string="Nacionalidad 2", comodel_name="res.country")
    nationality_three = fields.Many2one(string="Nacionalidad 3", comodel_name="res.country")
    nationality_ids = fields.Many2many(
        "res.partner.nationality", "partner_ids", string="Nacionalidad"
    )
    pai_ids = fields.One2many("fvd_custom.pai", "partner_id", "PAI")
    incidencia_ids = fields.One2many("fvd_custom.incidence_data", "user", "Incidencias")
    informe_social_ids = fields.One2many(
        "fvd_custom.social_report", "partner_id", "Informes Sociales"
    )

    dafo_ids = fields.One2many("fvd_custom.dafo", "employee_id", "DAFO")

    tipo_via = fields.Selection(
        [
            ("avenida", "Avenida"),
            ("Bulevar", "Bulevar"),
            ("Calle", "Calle"),
            ("Callejon", "Callejon"),
            ("Camino", "Camino"),
            ("Plaza", "Plaza"),
            ("Ronda", "Ronda"),
        ]
    )
    nombre_via = fields.Char("Nombre via")
    n_calle = fields.Char("Nº Calle")
    portal = fields.Char("Portal")
    escalera = fields.Char("Escalera")
    plant = fields.Char("Planta")
    puerta = fields.Char("Puerta")

    n_cuenta = fields.Char("Nº Cuenta bancaria")

    calidad_de = fields.Selection(
        [
            ("alumprac", "Alumnx en Practicas"),
            ("colab", "Personas Colaboradoras"),
            ("tbc", "TBC"),
            ("vol","Voluntariadx"),
        ],
        default=False,
    )
    coste_serv = fields.Float("Coste del servicio")

    file_cesion_de_datos = fields.Binary("Cesion de datos")
    date_cesion_de_datos = fields.Date()

    file_suspencion_de_datos = fields.Binary("Suspencion de datos")
    date_suspencion_de_datos = fields.Date()

    file_cesion_de_imagen = fields.Binary("Cesion de imagen")
    date_cesion_de_imagen = fields.Date()

    file_compromiso_de_confidencialidad = fields.Binary("Compromiso de confidencialidad")
    date_compromiso_de_confidencialidad = fields.Date()

    file_instrucciones_previas = fields.Binary("Instrucciones previas")
    date_instrucciones_previas = fields.Date()

    file_expediente = fields.Binary("Expediente")
    date_expediente = fields.Date()

    n_exp = fields.Char("Nº EXPEDIENTE")
    pa = fields.Char("PA")
    ts = fields.Char("TS")
    profesional = fields.Many2one("hr.employee", "Profesional")
    accion_cabo = fields.Text("ACCIÓN LLEVADA A CABO")
    cause_just = fields.Text("CAUSA QUE LO JUSTIFICA")
    inf_rel = fields.Text("INFORMACIÓN RELEVANTE")

    marital = fields.Selection(
        [
            ("married", "CASADX"),
            ("divorced", "DIVORCIADX"),
            ("cohabitant", "PAREJA DE HECHO"),
            ("single", "SOLTERX"),
            ("widower", "VIUDX"),
            ("separated", "SEPARADX"),
        ],
        default="single",
        string="Estado Civil"
    )

    file_expediente_c = fields.Binary("Expediente")
    date_expediente_c = fields.Date()

    file_contrato_vinculante_a_servicio_a = fields.Binary("Contrato vinculante a servicio")
    date_contrato_vinculante_a_servicio_a = fields.Date()

    file_contrato_vinculante_a_servicio = fields.Binary("Contrato vinculante a servicio")
    date_contrato_vinculante_a_servicio = fields.Date()

    file_contrato_vinculante_a_servicio_f = fields.Binary("Contrato vinculante a servicio")
    date_contrato_vinculante_a_servicio_f = fields.Date()

    def write(self, vals):
        if vals.get("file_cesion_de_datos", False):
            self.date_cesion_de_datos = fields.Date.today()
        if vals.get("file_suspencion_de_datos", False):
            self.date_suspencion_de_datos = fields.Date.today()
        if vals.get("file_cesion_de_imagen", False):
            self.date_cesion_de_imagen = fields.Date.today()
        if vals.get("file_compromiso_de_confidencialidad", False):
            self.date_compromiso_de_confidencialidad = fields.Date.today()
        if vals.get("file_instrucciones_previas", False):
            self.date_instrucciones_previas = fields.Date.today()
        if vals.get("file_expediente", False):
            self.date_expediente = fields.Date.today()
        if vals.get("file_expetiente_c", False):
            self.date_expediente_c = fields.Date.today()
        if vals.get("file_contrato_vinculante_a_servicio", False):
            self.date_contrato_vinculante_a_servicio = fields.Date.today()
        if vals.get("file_contrato_vinculante_a_servicio_a", False):
            self.date_contrato_vinculante_a_servicio_a = fields.Date.today()
        if vals.get("file_contrato_vinculante_a_servicio_f", False):
            self.date_contrato_vinculante_a_servicio_f = fields.Date.today()
        return super().write(vals)

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
            if record.birthdate and record.birthdate > datetime.today().date():
                raise ValidationError("La fecha de nacimiento no puede superar la fecha actual")
