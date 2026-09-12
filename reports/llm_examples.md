# Sample LLM Alert Explanations

These examples show the format produced by the LLM analyst component. They are intentionally short because the LLM is meant to support an analyst, not replace an investigation.

## Example 1 — Repeated Failed Logins

**Alert:** `alert_001`  
**Severity:** high  
**Evidence:** Five failed logins for `user_003` from `203.0.113.50` within ten minutes.

### Summary
Repeated login failures from one user and source IP triggered the failed-login rule.

### Evidence
- User: `user_003`
- Source IP: `203.0.113.50`
- Five failed attempts within ten minutes

### Possible Explanations
- The user repeatedly entered the wrong password.
- An old password may be saved on a device or application.
- The attempts may be automated or unauthorized.

### Recommended Analyst Checks
- Review authentication activity immediately before and after the alert.
- Check whether the same IP attempted other accounts.
- Confirm whether the user recognizes the activity.

### Uncertainty / Limitations
The failed attempts alone do not establish malicious intent. Additional authentication and device context would be needed.

---

## Example 2 — Unusual Access Time

**Alert:** `alert_002`  
**Severity:** medium  
**Evidence:** `user_002` successfully accessed the system at 2:15 AM.

### Summary
A successful login occurred outside the project's assumed normal working hours.

### Evidence
- User: `user_002`
- Successful access at 2:15 AM

### Possible Explanations
- Legitimate off-hours work or maintenance
- A scheduled or automated process
- Unauthorized use of the account

### Recommended Analyst Checks
- Confirm whether the login was expected.
- Review the source IP, device, and authentication method if available.
- Look for related activity around the same time.

### Uncertainty / Limitations
The alert contains very little context, so the login cannot be classified as legitimate or malicious from this event alone.

---

## Example 3 — Privilege Mismatch

**Alert:** `alert_003`  
**Severity:** high  
**Evidence:** `user_001` has standard access but attempted an action requiring admin access.

### Summary
The user's assigned access level did not meet the level required for the attempted action.

### Evidence
- User access: standard
- Required access: admin

### Possible Explanations
- The user selected an admin-only action by mistake.
- Permissions or role mappings may be configured incorrectly.
- The account may have been used for an unauthorized privileged action.

### Recommended Analyst Checks
- Identify the exact action and whether it succeeded.
- Review the user's assigned roles and recent permission changes.
- Correlate the event with authentication and session activity.

### Uncertainty / Limitations
The alert does not include the attempted action, source device, or surrounding activity, so intent cannot be determined from the alert alone.

---

## Example 4 — Unusual Network Context

**Alert:** `alert_004`  
**Severity:** medium  
**Evidence:** A connection used TCP port 23 instead of the project's expected TCP port 443.

### Summary
The connection differed from the normal network pattern defined for the synthetic environment.

### Evidence
- Protocol: TCP
- Destination port: 23
- Expected port in this project: 443

### Possible Explanations
- An approved legacy or administrative service
- A configuration issue
- Scanning or unauthorized network activity

### Recommended Analyst Checks
- Identify the source and destination systems.
- Confirm whether port 23 is expected for either system.
- Review related firewall, host, and authentication events.

### Uncertainty / Limitations
A port number by itself does not identify intent or confirm the application using the connection.

---

## Example 5 — Benign Off-Hours Scenario

**Alert:** `alert_benign_example`  
**Severity:** low  
**Evidence:** `admin_001` logged in at 5:30 AM, outside the project's assumed working hours. The synthetic scenario notes that scheduled maintenance is possible.

### Summary
The login triggered the off-hours rule, but the supplied context already provides a plausible benign explanation.

### Evidence
- User: `admin_001`
- Login time: 5:30 AM
- Possible scheduled maintenance noted in the scenario

### Possible Explanations
- Scheduled maintenance
- Legitimate early administrative work
- Automated activity using the account
- Unauthorized access

### Recommended Analyst Checks
- Check the maintenance or change schedule.
- Confirm whether the administrator expected the login.
- Review the source device and session activity if available.

### Uncertainty / Limitations
The rule identifies unusual timing, not malicious behavior. The event would need more context before any conclusion could be made.
