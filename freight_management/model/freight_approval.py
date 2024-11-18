from odoo import models, fields, api

class FreightApproval(models.Model):
    _name = 'freight.approval'
    _description = 'Freight Approval'

    name = fields.Char(string="Approval Reference", required=True)
    freight_order_id = fields.Many2one('sale.order', string="Freight Order", required=True)
    approved_by = fields.Many2one('res.users', string="Approved By", readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default='pending')
    approval_date = fields.Datetime(string='Approval Date', default=fields.Datetime.now)

    def approve(self):
        self.write({'state': 'approved', 'approved_by': self.env.user})
        self.freight_order_id.approval_id = self.id
        self.freight_order_id.state = 'approved'

    def reject(self):
        self.write({'state': 'rejected'})
        self.freight_order_id.state = 'rejected'

    def write(self, vals):
        changes = []
        if 'state' in vals:
            changes.append(f"Approval state changed to {vals['state']}")

        res = super(FreightApproval, self).write(vals)
        if changes:
            self.env['freight.audit.log'].create({
                'action': 'Approval Updated',
                'model_name': 'freight.approval',
                'record_id': self.id,
                'change_details': '\n'.join(changes),
            })
        return res

