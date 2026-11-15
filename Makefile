.PHONY: verify-env build test audit

verify-env:
	bookengine run verify_environment

build:
	bookengine build --all-formats

test:
	bookengine test -q

audit:
	bookengine run audit_references
