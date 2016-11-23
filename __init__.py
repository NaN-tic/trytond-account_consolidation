# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
import account

def register():
    Pool.register(
        account.ConsolidationStart,
        module='account_consolidation', type_='model')
    Pool.register(
        account.ConsolidationWizard,
        module='account_consolidation', type_='wizard')
