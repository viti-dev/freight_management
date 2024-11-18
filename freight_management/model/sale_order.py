from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    freight_type = fields.Selection([
        ('air', 'Air'),
        ('sea', 'Sea'),
        ('land', 'Land'),
    ], string='Freight Type')

    cargo_weight = fields.Float(string='Cargo Weight (tons)', default=0.0)

    high_value = fields.Boolean(
        string='High Value',
        compute='_compute_high_value',
        store=True
    )

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
