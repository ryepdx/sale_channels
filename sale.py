from openerp import SUPERUSER_ID
from openerp.osv import fields, osv, orm

class sale_order(osv.osv):
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

    def _default_input_channel(self, cr, uid, sale=None, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        group_names = [group.full_name.lower() for group in user.groups_id]

        if not sale and context.get('active_model') == 'sale.order' and context.get('active_id'):
            sale = self.browse(cr, uid, context.get('active_id'), context)

        if 'sales / see own leads' in group_names or 'sales / manager' in group_names:
            return 'service'
        elif sale and sale.reship_reason:
            return 'reship'
        elif sale and sale.amazon_order_id:
            return 'amazon'
        return 'internal'

    _defaults = {
        'input_channel': _default_input_channel,
        'payment_channel': 'check'
    }

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('payment_method') == 'cc_preauth':
            vals['payment_channel'] = 'credit_card'

        if vals.get('order_policy') == 'paypal':
            vals['payment_channel'] = 'paypal'

        return super(sale_order, self).write(cr, uid, ids, vals, context=context)

    def reship(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = {}
        kwargs['default'].update({'input_channel': 'reship'})
        return super(sale_order, self).reship(*args, **kwargs)

sale_order()


class website(orm.Model):
    _inherit = "website"

    def sale_get_order(self, cr, *args, **kwargs):
        sale_order = super(website, self).sale_get_order(*args, **kwargs)
        sale_pool = self.pool.get("sale.order")
        sale_pool.write(cr, SUPERUSER_ID, sale_order.id, {"input_channel": "web"})
        return sale_pool.browse(cr, SUPERUSER_ID, sale_order.id, context=kwargs.get("context"))

website()