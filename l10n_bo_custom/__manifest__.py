{
    "name": "Odoo Custom BO",
    "version": "1.1",
    "license": "LGPL-3",
    "description": """""",
    "website": "andersonarmeya.com",
    "depends": ["base","account"],
    "data": [
        "security/ir.model.access.csv",
        "report/voucher.xml",
        "wizard/accounting_reports_views.xml",
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
        "views/l10n_bo_custom_voucher.xml"
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "author": "Anderson Armeya (andyenfiverr)",
}
