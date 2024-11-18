from odoo import models, fields, api

class FreightApproval(models.Model):
    _name = 'freight.approval'
    _description = 'Freight Approval'

    order_id = fields.Many2one('sale.order', string='Freight Order', required=True)
    approval_status = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Approval Status', required=True)
    approved_by = fields.Many2one('res.users', string='Approved By')
    approval_date = fields.Datetime(string='Approval Date', default=fields.Datetime.now)

    def approve(self):
        self.write({'approval_status': 'approved', 'approved_by': self.env.user})
        self.order_id.approval_id = self.id
        self.order_id.state = 'approved'

    def reject(self):
        self.write({'approval_status': 'rejected'})
        self.order_id.state = 'rejected'
