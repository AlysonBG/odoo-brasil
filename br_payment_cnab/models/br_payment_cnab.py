# -*- coding: utf-8 -*-
# © 2018 Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
from ..other.cnab240 import Cnab_240
#from ..febraban.cnab import Cnab
from odoo import models, fields, api
from odoo.exceptions import UserError

#campo novo para decidir modo de pagamento deve ser adicionado ao account.voucher
class PaymentCnabInformation(models.Model):
    _name = 'l10n_br.payment_cnab'

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s" % (rec.mov_finality or '')))
        return result

    @api.multi
    def generate_cnab(self):
        pass
        #raise UserError(self.mov_finality)
        #Cnab_240.createCnab(self)
        # for order_id in self:createCnab
        #     order = self.env['l10n_br.payment_cnab'].browse(order_id.id)
        #     cnab = Cnab.get_cnab(
        #         order.payment_mode_id.bank_account_id.bank_bic, '240')()
        #     remessa = cnab.remessa(order)
        #     self.cnab_file = base64.b64encode(remessa.encode('UTF-8'))
        #     self.data_emissao_cnab = datetime.now()


    mov_finality = fields.Selection([
        ('01', u'Current Account Credit'),
        ('02', u'Rent Payment/Condominium'),
        ('03', u'Dept Security Payment'),
        ('04', u'Dividend Payment'),
        ('05', u'Tuition Payment'),
        ('07', u'Provider/Fees Payment'),
        ('08', u'Currency Exchange/Fund/Stock Exchange Payment'),
        ('09', u'Transfer of Collection / Payment of Taxes'),
        ('11', u'DOC/TED to Saving Account'),
        ('12', u'DOC/TED to Judicial Deposit'),
        ('13', u'Child Support/Alimony'),
        ('14', u'Income Tax Rebate'),
        ('99', u'Other')
        ], string=u'Movimentation Purpose')

    operation_code = fields.Selection([
        ('018', u'TED CIP'),
        ('810', u'TED STR'),
        ('700', u'DOC'),
        ('000', u'CC')
    ], string=u'Operation Code')


    entry_mode = fields.Selection([('01', u'Current Account Credit'),
        ('03', u'Transfer to Other Banks (DOC, TED CIP e TED STR)'),
        ('05', 'Saving Account Credit'),
        ('10', 'Payment Order/acquittance'),
        ('11', 'Barcode paymet'), #ajeitar
        ('16', 'regular DARF'), #traduzir daqui pra baixo - se necessário
        ('17', u'GPS - Guia de previdência Social'),
        ('18', 'Simple DARF'),
        ('20', u'"caixa" Autentication'),
        ('22', 'GARE SP ICMS'),
        ('23','GARE SP DR'),
        ('24','GARE SP ITCMD'),
        ('25','IPVA SP'),
        ('26','LICENCIAMENTO SP'),
        ('27','DPVAT SP')], string="Entry mode")

    warning_code = fields.Selection([
        ('0', u'No Warning'),
        ('2', u'Warning only for addresser'),
        ('5', u'Warning only for receiver'),
        ('6', u'Warning for both, addresser and receiver')
    ], string=u'Warning Code', default='0')

    lote_serv =  fields.Integer('Order of Service')
    reg_type = fields.Integer('Register Type') #muda de acordo com o segmento, pra A e B é 3, deve ser implementado depois como readonly
    cnab_get = fields.Binary('Get CNAB', readonly=True)

class PaymentOrderLine(models.Model):
    _inherit = 'payment.order.line'

    other_payment = fields.Many2one('l10n_br.payment_cnab', string="Other Payment Information")
