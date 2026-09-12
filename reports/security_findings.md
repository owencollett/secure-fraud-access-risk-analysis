# Security Log Analysis Findings

## Purpose

This part of the project uses synthetic authentication and network-style logs to practice basic security monitoring and rule-based alert detection. No real customer data, employee data, credentials, or private network logs are used.

## Detection rules

### Repeated failed logins

Five or more failed login attempts from the same user and source IP within ten minutes are flagged for review. This could be password guessing, but it could also be a user repeatedly entering the wrong password.

### Unusual access time

Successful access between 10:00 PM and 6:00 AM is flagged. Off-hours access can be legitimate, so this rule is only a reason to investigate further.

### Privilege mismatch

An alert is created when a user's assigned access level is lower than the access level required for the attempted action. This can point to a permissions issue, a user mistake, or potentially unauthorized activity.

### Unusual network context

The synthetic environment treats TCP port 443 as the normal connection pattern. Other ports or protocols are flagged so they can be reviewed.

## False positives

Each rule can produce benign alerts. Failed logins may come from an outdated saved password. Off-hours access may be approved maintenance. A privilege mismatch may come from a configuration problem. An unusual port may be tied to an authorized administrative tool.

For that reason, the detector does not label an event as a confirmed attack. It creates an alert with the evidence that triggered the rule.

## Limitations

- The data is synthetic and much simpler than a real enterprise environment.
- Detection thresholds are project assumptions, not production security policies.
- The rules can produce false positives and false negatives.
- The project does not include endpoint telemetry, identity-provider context, threat intelligence, or a full SIEM environment.

## Analyst follow-up

A real investigation could include checking account history, confirming the user and device, reviewing the source IP, looking at recent permission changes, correlating related events, and deciding whether the activity was expected.

## Privacy and security

Real passwords, API keys, customer information, employee identifiers, private network logs, and other sensitive information should not be committed to this public repository.
