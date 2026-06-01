.PHONY: validate validate-professional-intelligence-context-query validate-wallguard-query-context

validate: validate-professional-intelligence-context-query validate-wallguard-query-context

validate-professional-intelligence-context-query:
	python3 scripts/validate_professional_intelligence_context_query.py

validate-wallguard-query-context:
	python3 scripts/validate_wallguard_query_context.py
