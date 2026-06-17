"""infinilab harness: fixed infrastructure for the RH autoresearch loop.

This package is the trusted spine. The autonomous loop writes experiments in
`experiments/`; it does not modify `harness/`. Changing the harness is a
deliberate human-level act, because the harness is what makes results
trustworthy.
"""
