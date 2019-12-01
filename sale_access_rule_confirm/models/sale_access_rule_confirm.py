from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleAccessRuleConfirm(models.Model):
    _name = 'sale.access.rule.confirm'
    _description = 'Sale Access Rule Confirm'

