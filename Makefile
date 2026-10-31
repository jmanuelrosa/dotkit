# dotkit

PYTEST := uv run --offline --with pytest pytest

.PHONY: test vendor check

test:
	$(PYTEST) -q

vendor:
	bin/dotkit-vendor $(CONSUMERS)

check:
	bin/dotkit-vendor --check $(CONSUMERS)
