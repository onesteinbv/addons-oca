from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    is_start = fields.Boolean(default=False, string="Start Stage")
