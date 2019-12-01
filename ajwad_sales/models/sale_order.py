from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class Team(models.Model):
    _inherit = 'crm.team'

    discount_limit = fields.Float('Discount Limit')



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('display_type', self.default_get(['display_type'])['display_type']):
                values.update(product_id=False, price_unit=0, product_uom_qty=0, product_uom=False, customer_lead=0)

            values.update(self._prepare_add_missing_fields(values))

        lines = super().create(vals_list)
        for line in lines:
        	ginv = line.order_id
        	discount_limit = ginv.team_id.discount_limit
        	if line.discount <= discount_limit:
	            if line.product_id and line.order_id.state == 'sale':
	                msg = _("Extra line with %s ") % (line.product_id.display_name,)
	                line.order_id.message_post(body=msg)
	                # create an analytic account if at least an expense product
	                if line.product_id.expense_policy not in [False, 'no'] and not line.order_id.analytic_account_id:
	                    line.order_id._create_analytic_account()
	        else:
	            raise ValidationError('Discount Value Greater Than Discount Limit' + ' ' + str(discount_limit))
        return lines
