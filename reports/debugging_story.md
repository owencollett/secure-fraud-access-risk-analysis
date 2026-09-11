# Phase 7 Debugging Story

## Problem

During final testing, I identified that the LLM analyst module
accepted any non-empty response from the language model.

This meant a response could be accepted even if it failed to
include the required analyst sections.

## Root Cause

The original validation only checked whether the LLM response
was empty.

It did not verify whether the required structured sections were
present.

## Fix

I added an LLM output validation function that requires:

- Summary
- Evidence
- Possible Explanations
- Recommended Analyst Checks
- Uncertainty / Limitations

If any required section is missing, the program raises a clear
error instead of accepting the response.

## Regression Test

I added automated pytest coverage that supplies a deliberately
malformed LLM response.

The test verifies that the malformed response raises an error.

This prevents the same issue from silently returning in future
changes.

