# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        """ Used for action button that do not accept arguments. """
        print("self.env.context", self.env.context)
        proforma_from_context = self.env.context.get("proforma", False)
        if proforma_from_context:
            id_from_params = self.env.context.get("active_id", False)
            if id_from_params:
                sale_order = self.env["sale.order"].browse(id_from_params)
                if sale_order.opportunity_id:
                    sale_order.opportunity_id.write({
                        'stage_id': self.env.ref("renovation_demo.stage_lead5").id
                    })
        return super().action_send_mail()