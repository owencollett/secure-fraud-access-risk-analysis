# Security Log Analysis Findings

## Purpose

This phase uses synthetic authentication and network-style
security logs to demonstrate basic security-event monitoring
and rule-based alert detection.

No real customer data, employee data, credentials, or private
network logs are used.

## Detection Rules

### Repeated Failed Logins

The system flags five or more failed login attempts from the
same user and source IP within ten minutes.

This can indicate password guessing or attempted unauthorized
access, but it does not prove that an attack occurred.

### Unusual Access Time

Successful access between 10:00 PM and 6:00 AM is flagged for
review.

Off-hours access may be legitimate, so the alert requires
human investigation.

### Privilege Mismatch

The system flags activity when a user's assigned access level
is lower than the access level required for the attempted
action.

This helps identify possible authorization or least-privilege
issues.

### Unusual Network Context

The synthetic environment normally uses TCP port 443.

Connections using another port or protocol are flagged for
review.

## False Positives and Benign Explanations

A repeated failed-login alert could occur because a user forgot
their password or has an old password saved on a device.

An unusual-time alert could occur because an employee is
working late, traveling, or performing approved maintenance.

An unusual network connection could be caused by an approved
administrative or troubleshooting tool rather than malicious
activity.

A privilege mismatch could also be caused by an incorrectly
configured account or application rather than an attacker.

## Limitations

The data is synthetic and does not represent a real enterprise
environment.

The thresholds are student-project assumptions rather than
American Express security policies.

Rule-based detection can produce both false positives and false
negatives.

An alert represents suspicious activity that should be
investigated. It does not confirm that a security incident
occurred.

## Human Analyst Next Steps

A human analyst could review account history, verify the user
and device, investigate the source IP, check recent permission
changes, review related events, and determine whether the
activity was expected before taking action.

## Privacy and Security

Real passwords, API keys, customer information, employee
identifiers, private network logs, and other sensitive
information should never be committed to this public project.