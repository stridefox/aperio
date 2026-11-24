# database/researchinfo/query_executor.py
# Helper for running SQL queries against the research catalog database (mysql-connector).
# Audit integration: call the capture helpers in features/audit/services.py
# (log_query / log_data_change) inside the same transaction as each executed query.
# Status: placeholder - not implemented yet.
