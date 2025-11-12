---
name: Monitoring Alert
about: Issue triggered by monitoring systems (LibreNMS, Graylog, etc.)
title: '[ALERT] '
labels: ['monitoring', 'infrastructure']
assignees: ''
---

## Alert Information

### Source System
- [ ] LibreNMS
- [ ] Graylog
- [ ] System logs
- [ ] Manual observation
- [ ] Other: _______

### Severity
- [ ] Critical - Service down/major impact
- [ ] High - Significant degradation
- [ ] Medium - Minor impact
- [ ] Low - Informational

### Affected System
**Hostname:** [e.g., lima.projekt.lab, whiskey.projekt.lab]  
**IP Address:** [e.g., 10.10.201.112]  
**Service/Component:** [e.g., LibreNMS, SNMP, HTTP]

## Alert Details

### Alert Name/Rule
What triggered this alert?

### Alert Message
```
Paste the full alert message/output here
```

### Timestamp
**First Detected:** YYYY-MM-DD HH:MM:SS  
**Last Occurrence:** YYYY-MM-DD HH:MM:SS  
**Frequency:** [How often is this occurring?]

## Symptoms

### What's Happening?
Describe the observed behavior:
- 
- 
- 

### Impact
Who/what is affected?
- [ ] Users cannot access service
- [ ] Performance degraded
- [ ] Monitoring only (no user impact)
- [ ] Potential future impact

### Current State
```bash
# Output of relevant commands
systemctl status service-name
# or
lnms device:poll hostname
# or
journalctl -u service-name -n 50
```

## Investigation

### Initial Checks Performed
- [ ] Verified service is running
- [ ] Checked system resources (CPU, memory, disk)
- [ ] Reviewed recent changes
- [ ] Checked logs
- [ ] Tested connectivity
- [ ] Verified configuration

### Findings
What did you discover?
- 

### Suspected Cause
What might be causing this?
- 

## Metrics/Graphs
If available, include relevant monitoring data:
- CPU usage:
- Memory usage:
- Network traffic:
- Disk I/O:
- Custom metrics:

## Recent Changes
Were there any recent changes that might be related?
- [ ] Code deployed
- [ ] Configuration changed
- [ ] System updated
- [ ] Network changes
- [ ] No recent changes

**Details:**
- When:
- What:
- By whom:

## Remediation Steps

### Immediate Actions Needed
What needs to be done right now?
1. 
2. 
3. 

### Temporary Workaround
Is there a temporary fix?
```bash
# Commands for workaround
```

### Permanent Fix
What's needed long-term?
- 

## Root Cause Analysis
Once resolved, document the root cause:
- **Root Cause:**
- **Why it occurred:**
- **How to prevent:**

## Resolution
- [ ] Issue resolved
- [ ] Monitoring confirms normal operation
- [ ] Alert acknowledged/silenced
- [ ] Post-mortem created (if needed)

## Related Issues
- Duplicate of #XX
- Related to #XX
- Caused by #XX

## Additional Context
Logs, screenshots, graphs, or other relevant information.
