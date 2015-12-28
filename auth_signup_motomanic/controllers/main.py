# -*- coding: utf-8 -*-
from openerp.addons.auth_signup.controllers.main import AuthSignupHome
from openerp.http import request


class AuthSignupHome(AuthSignupHome):

    def _signup_with_values(self, token, values):
        qcontext = request.params.copy()
        values.update(model_id=qcontext.get('model_id', False))
        values.update(year_ids=qcontext.get('year_ids', False))
        return super(AuthSignupHome, self)._signup_with_values(token, values)
