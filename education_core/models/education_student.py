
from odoo import fields, models, api, _


class EducationStudent(models.Model):
    _name = 'education.student'
    _inherit = ['mail.thread']
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Student record'
    _rec_name = 'name'

    @api.multi
    def student_documents(self):
        """Return the documents student submitted
        along with the admission application"""
        self.ensure_one()
        if self.application_id.id:
            documents = self.env['education.documents'].search([('application_ref', '=', self.application_id.id)])
            documents_list = documents.mapped('id')
            return {
                'domain': [('id', 'in', documents_list)],
                'name': _('Documents'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'education.documents',
                'view_id': False,
                'context': {'default_application_ref': self.application_id.id},
                'type': 'ir.actions.act_window'
            }

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('ad_no', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(EducationStudent, self).name_search(name, args=args, operator=operator, limit=limit)

    @api.model
    def create(self, vals):
        """Over riding the create method to assign sequence for the newly creating the record"""
        vals['ad_no'] = self.env['ir.sequence'].next_by_code('education.student')
        res = super(EducationStudent, self).create(vals)
        return res

    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete="cascade")
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')
    application_no = fields.Char(string="Application No")
    date_of_birth = fields.Date(string="Date Of birth", requird=True)
    guardian_name = fields.Char(string="Guardian")
    father_name = fields.Char(string="Father")
    mother_name = fields.Char(string="Mother")
    class_id = fields.Many2one('education.class.division', string="Class")
    admission_class = fields.Many2one('education.class', string="Admission Class")
    ad_no = fields.Char(string="Admission Number", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender', required=True, track_visibility='onchange')
    blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'), ('o-', 'O-'),
                                    ('ab-', 'AB-'), ('ab+', 'AB+')],
                                   string='Blood Group', required=True, track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Company')
    per_street = fields.Char()
    per_street2 = fields.Char()
    per_zip = fields.Char(change_default=True)
    per_city = fields.Char()
    per_state_id = fields.Many2one("mystate.mystate", string='District Name', ondelete='restrict')
    per_mycountry_id = fields.Many2one('mycountry.mycountry', string='Country Name', ondelete='restrict')
    medium = fields.Many2one('education.medium', string="Medium",)
    
    
    religion_id = fields.Many2one('religion.religion', string="Religion")
    is_same_address = fields.Boolean(string="Is same Address?")
    nationality = fields.Many2one('country.country', string='Nationality', ondelete='restrict')
    application_id = fields.Many2one('education.application', string="Application No")
    class_history_ids = fields.One2many('education.class.history', 'student_id', string="Application No")

    _sql_constraints = [
        ('ad_no', 'unique(ad_no)', "Another Student already exists with this admission number!"),
    ]
