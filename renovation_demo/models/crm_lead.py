# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'


    interest = fields.Text(
        string='Interest'
    )

    appointment_date = fields.Date(
        string="Appointment date"
    )

    def write(self, values):
        if values.get('stage_id', False) == self.env.ref('crm.stage_lead2').id:
            self.activity_schedule(
                act_type_xmlid='mail.mail_activity_data_todo',
                date_deadline=None,
                summary='Analyze opportunity, contact the client',
                note='if the appeal has sales potential - schedule an appointment, otherwise transfer opportunity to the partners and move opportunity to the “Closed” status'
            )
        if (self.stage_id.id == self.env.ref('crm.stage_lead2').id):
            check_interest = self.interest or values.get('interest', False)
            check_appointment_date = self.appointment_date or values.get('appointment_date', False)
            if check_interest and check_appointment_date:
                activity = self.activity_search(
                    act_type_xmlids=['mail.mail_activity_data_todo'],
                    additional_domain=[('summary', '=', 'Analyze opportunity, contact the client')]
                )
                if activity:
                    appointment_date = self.appointment_date or values.get('appointment_date', False)
                    activity.action_feedback(feedback=f"Appointment date - {appointment_date}".format(appointment_date=appointment_date))
                values.update({
                    'stage_id': self.env.ref('crm.stage_lead3').id
                })
        return super().write(values)
