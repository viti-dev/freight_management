from odoo import models, fields

class FreightAuditLog(models.Model):
    _name = 'freight.audit.log'
    _description = 'Freight Audit Log'
    _order = 'create_date desc'

    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, readonly=True)
    action = fields.Char(string="Action")
    model_name = fields.Char(string="Model", required=True)
    record_id = fields.Integer(string="Record ID", required=True)
    change_details = fields.Text(string="Change Details")
    create_date = fields.Datetime(string="Date/Time", readonly=True)
