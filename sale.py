from openerp import SUPERUSER_ID
from openerp.osv import fields, osv, orm

class sale_order(osv.Model):
    _inherit = 'sale.order'
    _columns = {
        'input_channel': fields.selection(
            [('internal', 'Internal'), ('web', 'Web'), ('amazon', 'Amazon'), ('mail', 'Mail'),
             ('call_center', 'Call Center'), ('service', 'Customer Service'), ('reship', 'Reship')],
            'Input Channel', required=False),
        'payment_channel': fields.selection(
            [('credit_card', 'Credit Card'), ('amazon', 'Amazon'),
             ('check', 'Check or Cash'), ('paypal', 'Paypal')], 'Payment Channel', required=False)
    }

    def _default_input_channel(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        group_names = [group.full_name.lower() for group in user.groups]
        if 'sales / see own leads' in group_names or 'sales / manager' in group_names:
            return 'service'
        return 'internal'


    _defaults = {
        'input_channel': _default_input_channel
    }

sale_order()


class website(orm.Model):
    _inherit = "website"

    def sale_get_order(self, cr, *args, **kwargs):
        sale_order = super(website, self).sale_get_order(*args, **kwargs)
        sale_pool = self.pool.get("sale.order")
        sale_pool.write(cr, SUPERUSER_ID, sale_order.id, {"input_channel": "web"})
        return sale_pool.browse(cr, SUPERUSER_ID, sale_order.id, context=kwargs.get("context"))

website()