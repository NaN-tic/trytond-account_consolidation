from sql import Cast, Literal
from trytond.model import ModelView #, fields
from trytond.wizard import Wizard, StateView, StateTransition, \
    Button
from trytond.transaction import Transaction
from trytond.pool import Pool


class ConsolidationStart(ModelView):
    'Consolidation'
    __name__ = 'account.consolidation.start'


class ConsolidationWizard(Wizard):
    'Consolidation'
    __name__ = 'account.consolidation'
    start = StateView('account.consolidation.start',
        'account_consolidation.account_consolidation_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Execute', 'do', 'tryton-ok', default=True),
            ])
    do = StateTransition()

    def transition_do(self):
        pool = Pool()
        Move = pool.get('account.move')
        Line = pool.get('account.move.line')
        Account = pool.get('account.account')
        AccountTemplate = pool.get('account.account.template')
        Period = pool.get('account.period')

        cursor = Transaction().cursor

        destination = Move.__table__()
        move = Move.__table__()
        line = Line.__table__()
        period = Period.__table__()
        account = Account.__table__()
        template = AccountTemplate.__table__()

        company_id = 1
        company = Literal(company_id)

        query = line.delete(where=(line.move==move.id) &
            (move.company==company), using=[move])
        query = ('DELETE FROM account_move_line USING account_move WHERE '
            'account_move_line.move=account_move.id AND '
            'account_move.company=%d' % company_id)
        cursor.execute(query)
        query = move.delete(where=move.company == company)
        cursor.execute(*query)

        query = move.join(period,
            condition=((move.date >= period.start_date)
                & (move.date <= period.end_date)
                & (period.type == 'standard')
                ))
        query = query.select(company, move.create_date, move.create_uid,
            move.write_date, move.write_uid, move.id, move.number, move.date,
            move.post_number, move.post_date, move.state, move.journal,
            move.description, period.id, where=(move.company != company))
        destination = destination.insert([
                destination.company, destination.create_date,
                destination.create_uid, destination.write_date,
                destination.write_uid, destination.origin, destination.number,
                destination.date, destination.post_number,
                destination.post_date, destination.state, destination.journal,
                destination.description, destination.period
                ], values=query)
        cursor.execute(*destination)


        line = Line.__table__()
        destination = Line.__table__()

        account2 = Account.__table__()

        query = account.join(template,
            condition=(account.template == template.id))
        query = query.join(account2,
            condition=((account2.template == template.id)
                & (account2.company == company)))
        query = query.join(line,
            condition=(account.id == line.account))
        query = query.join(move,
            condition=(Cast(line.move, Move.origin.sql_type().base) ==
                move.origin))
        query = query.select(move.id, line.debit, line.credit, line.party,
            line.description, line.maturity_date, account2.id, line.state,
            line.second_currency, line.amount_second_currency)
        query = destination.insert([
                destination.move,
                destination.debit, destination.credit, destination.party,
                destination.description, destination.maturity_date,
                destination.account, destination.state,
                destination.second_currency,
                destination.amount_second_currency,
                ], values=query)
        cursor.execute(*query)
        return 'end'
