from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    freight_type = fields.Selection([
        ('air', 'Air'),
        ('sea', 'Sea'),
        ('land', 'Land'),
    ], string='Freight Type', required=True)

    cargo_weight = fields.Float(string='Cargo Weight (tons)', required=True)

    high_value = fields.Boolean(
        string='High Value',
        compute='_compute_high_value',
        default=False,
    )

    approval_id = fields.Many2one('freight.approval', string='Approval')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('approval_requested', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
    ], string='Status', default='draft')

    @api.constrains('cargo_weight')
    def _check_cargo_weight(self):
        for order in self:
            if order.cargo_weight <= 0:
                raise UserError('Cargo weight must be greater than zero.')

    @api.depends('amount_total', 'cargo_weight')
    def _compute_high_value(self):
        for order in self:
            order.high_value = order.amount_total > 500000 or order.cargo_weight > 50

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        if order.high_value and not order.approval_id:
            raise UserError('High-value orders require approval before confirmation.')
        return order

    def action_confirm(self):
        for order in self:
            if order.high_value and not order.approval_id:
                raise UserError('High-value orders require approval before confirmation.')
        return super(SaleOrder, self).action_confirm()

    def action_request_approval(self):
        for order in self:
            if not order.order_line:
                raise UserError('There is no order line .')
            if order.state != 'draft' and order.state != 'sent':
                raise UserError('Approval request can only be made in draft state or Quotation Sent.')
            """Send a request for approval to admin"""
            approval_record = self.env['freight.approval'].create({
                'name': order.name,
                'freight_order_id': self.id,
                'state': 'pending',
                'requested_by': self.env.user.id,
                'approved_by': False
            })
            self.write({'state': 'approval_requested', 'approval_id': approval_record.id})
            order.approval_id = approval_record.id
            order.state = 'approval_requested'
            log_vals = {'user_id': self.env.user.id,
                        'model_name': 'sale.order',
                        'change_details': 'Order Approval Requested',
                        'record_id': order.id,
                        'create_date': datetime.now(),
                        }
            self.env['freight.audit.log'].create(log_vals)
        return True

    def write(self, vals):
        changes = []
        if 'freight_type' in vals:
            changes.append(f"Freight Type changed from {self.freight_type} to {vals['freight_type']}")
        if 'cargo_weight' in vals:
            changes.append(f"Cargo Weight changed from {self.cargo_weight} to {vals['cargo_weight']}")
        if 'high_value' in vals:
            changes.append(f"High Value status changed from {self.high_value} to {vals['high_value']}")

        res = super(SaleOrder, self).write(vals)
        if changes:
            self.env['freight.audit.log'].create({
                'action': 'Updated Freight Order',
                'model_name': 'sale.order',
                'record_id': self.id,
                'change_details': '\n'.join(changes),
            })
        return res

    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        self.env['freight.audit.log'].create({
            'action': 'Created Freight Order',
            'model_name': 'sale.order',
            'record_id': res.id,
            'change_details': 'Freight order created.',
        })
        return res

