CREATE INDEX analytic_account_line_move_line_index on analytic_account_line(move_line);
CREATE INDEX account_bank_reconciliation_index ON account_bank_reconciliation(move_line);
CREATE INDEX account_asset_line_move ON account_asset_line(move);
CREATE INDEX account_asset_move ON account_asset(move);
CREATE INDEX account_payment_processing_move_index ON account_payment(processing_move);
CREATE INDEX account_payment_clearing_move_index ON account_payment(clearing_move);
CREATE INDEX account_invoice_cancel_move_index ON account_invoice(cancel_move);
CREATE INDEX account_invoice_move_index ON account_invoice(move);
CREATE INDEX account_bank_statement_move_line_move_index ON account_bank_statement_move_line(move);

