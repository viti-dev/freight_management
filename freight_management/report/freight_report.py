from odoo import models, fields
from odoo.tools.misc import xlwt
from xlsxwriter.workbook import Workbook
import base64
import io
import pytz

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

        sheet1.write(row_index, column_index, 'Name')
        sheet1.write(row_index, column_index + 1, 'Amount')


        sheet1.col(1).width = 4000
        sheet1.col(0).width = 10000
        row_index += 1

        for type in self.generate_report():
            sheet1.write_merge(row_index, row_index, column_index, column_index+ 1, type)
            row_index+=1
            for x in self.generate_report()[type]:
                sheet1.write(row_index, column_index, x['name'] or '')
                sheet1.write(row_index, column_index + 1, x['amount_total'] or 0)
                row_index+=1
            # row_index += 1

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
                    vals = {'name': order.name, 'amount_total': order.amount_total}
                    if order.freight_type in data_dict:
                        # Append the order details to the list of orders for this freight type
                        data_dict[order.freight_type].append(vals)
                    else:
                        # Initialize the dictionary with a list containing this order's details
                        data_dict[order.freight_type] = [vals]

                    # report_data[order.freight_type]['orders'].append(order.name)
                    # report_data[order.freight_type]['total_revenue'] += order.amount_total
            print(data_dict,'===================')
            return data_dict
