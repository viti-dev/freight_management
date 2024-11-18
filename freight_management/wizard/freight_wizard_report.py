from odoo import models, fields
from odoo.tools.misc import xlwt
import base64
import io

class FreightReport(models.TransientModel):
    _name = 'freight.report'
    _description = 'Freight Report'

    freight_type = fields.Selection([
        ('air', 'Air'),
        ('sea', 'Sea'),
        ('land', 'Land')
    ], string="Freight Type")
    high_value = fields.Boolean()

    def action_print_pdf(self):
        return self.env.ref('freight_management.report_freight').report_action(self)

    def action_print_excel(self):
        workbook = xlwt.Workbook(encoding="UTF-8")

        filename = 'Freight_Report'
        filename = filename + '.xls'

        sheet1 = workbook.add_sheet('Report')

        row_index = 0
        column_index = 0
        style_title_value = xlwt.easyxf('font:height 200; align: horiz center; font: color black; font:bold True;borders: top_color black, bottom_color black, right_color black, left_color black,\
                        left thin, right thin, top thin, bottom thin;')
        sheet1.write(row_index, column_index, 'Sale Order', style_title_value)
        sheet1.write(row_index, column_index + 1, 'High Value Orders', style_title_value)
        sheet1.write(row_index, column_index + 2, 'Total Revenue', style_title_value)


        sheet1.col(1).width = 4000
        sheet1.col(0).width = 10000
        row_index += 1

        bold_center_style = xlwt.easyxf('font: bold 1; alignment: horizontal center')
        right_align_style = xlwt.easyxf('alignment: horizontal right')
        report_data = self.generate_report()
        for report_type, data in report_data.items():
            sheet1.write_merge(row_index, row_index, column_index, column_index + 1, report_type, bold_center_style)
            row_index += 1
            for x in data:
                sheet1.write(row_index, column_index, x['name'] or '')
                sheet1.write(row_index, column_index + 1, x['high_value'] or 0, right_align_style)
                sheet1.write(row_index, column_index + 2, x['amount_total'] or 0, right_align_style)
                row_index += 1

        fp = io.BytesIO()
        workbook.save(fp)

        report_id = self.env['excel.report'].create(
            {'excel_file': base64.encodebytes(fp.getvalue()), 'file_name': filename})
        fp.close()
        return {'view_mode': 'form',
                'res_id': report_id.id,
                'res_model': 'excel.report',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
                }

    def generate_report(self):
        domain = [('state', '=', 'sale')]
        if self.freight_type:
            domain.append(('freight_type','=',self.freight_type))

        orders = self.env['sale.order'].search(domain)
        if self.high_value:
            orders = orders.filtered(lambda x: x.high_value)
        else:
            orders = orders
        data_dict = {}
        for order in orders:
            if order.freight_type:
                vals = {'name': order.name, 'high_value': order.high_value if order.high_value else 'False', 'amount_total': order.amount_total}
                if order.freight_type in data_dict:
                    data_dict[order.freight_type].append(vals)
                else:
                    data_dict[order.freight_type] = [vals]
        return data_dict
