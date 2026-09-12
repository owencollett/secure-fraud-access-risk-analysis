# Debugging Note: LLM Output Validation

## Problem

While testing the LLM analyst module, I noticed that any non-empty response would be accepted. That meant the program could save an explanation even if the model ignored the requested structure.

## Cause

The first validation check only tested whether the response was empty. It did not confirm that the required sections were present.

## Fix

I added `validate_llm_output()` to require these sections:

- Summary
- Evidence
- Possible Explanations
- Recommended Analyst Checks
- Uncertainty / Limitations

If one is missing, the function raises an error instead of accepting the response.

## Regression test

I added a pytest case with a deliberately incomplete response and verified that it raises `ValueError`. This gives the output contract a simple automated check and helps prevent the same issue from being reintroduced later.
