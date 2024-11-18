from odoo import fields, models, api


class ExcelReport(models.TransientModel):
    _name = 'excel.report'

    file_name = fields.Char(
        'Excel File',
        size=64,
        readonly=True,
    )

    excel_file = fields.Binary(
        'Download Report',
        readonly=True,
    )