# Infrastructure Context

**Topic:** projekt.lab Infrastructure Overview  
**Last Updated:** 2025-11-05  
**Status:** Production  
**Relevance:** Foundation for all services

---

## Network Topology

### Domain
- **Primary Domain:** projekt.lab
- **DNS:** Managed by FreeIPA (alpha.projekt.lab)
- **IP Range:** 10.10.201.0/24

### Hosts

#### Hypervisor
**whiskey.projekt.lab**
- Role: Proxmox VE Host
- IP: 10.10.201.103
- Hardware: Physical server
- Certificate: Serial 13 (FreeIPA)
- Status: ✅ Production

#### VMs

**alpha.projekt.lab**
- Role: FreeIPA Server (Identity Management)
- IP: 10.10.201.101
- OS: Rocky Linux
- Certificate: Multiple (serial 9+)
- Status: ✅ Production

**tango.projekt.lab**
- Role: TrueNAS Scale (Network Storage)
- IP: 10.10.201.102
- Certificate: Serial 14 (FreeIPA)
- Services: NFS, SMB, iSCSI
- Status: ✅ Production

**echo.projekt.lab**
- Role: Rocky Linux VM (General Purpose)
- IP: 10.10.201.104
- Certificate: Serial 15 (FreeIPA)
- Services: Cockpit
- Status: ✅ Production

**lima.projekt.lab**
- Role: LibreNMS Monitoring Server
- IP: 10.10.201.112
- OS: Rocky Linux
- Certificate: Serial 16 (FreeIPA)
- Version: LibreNMS 25.11.0-dev.80
- Status: ✅ Production, actively monitored

**golf.projekt.lab** (Planned)
- Role: Graylog Logging Server
- IP: 10.10.201.107
- Status: 📋 Planned (Week 2+)

---

## Services Overview

### Identity & Authentication
- **FreeIPA** on alpha.projekt.lab
- Centralized user authentication
- Certificate management
- DNS server
- Status: ✅ Operational

### Storage
- **TrueNAS Scale** on tango.projekt.lab
- NFS exports for various services
- LibreNMS RRD storage
- Backup storage
- Status: ✅ Operational

### Monitoring
- **LibreNMS** on lima.projekt.lab
- SNMP v3 monitoring
- Device discovery
- Alert management
- Status: ✅ Operational, 1 device monitored

### Logging (Planned)
- **Graylog** on golf.projekt.lab
- Centralized log aggregation
- Status: 📋 Not yet deployed

---

## Certificate Management

### FreeIPA Integration
All projekt.lab hosts use FreeIPA-issued certificates.

**Issued Certificates:**
- Serial 9+: alpha.projekt.lab (multiple services)
- Serial 13: whiskey.projekt.lab (Proxmox)
- Serial 14: tango.projekt.lab (TrueNAS)
- Serial 15: echo.projekt.lab (Cockpit)
- Serial 16: lima.projekt.lab (LibreNMS)

**Process:**
1. Request certificate from FreeIPA
2. Install on target service
3. Configure service to use certificate
4. Verify HTTPS access
5. Auto-renewal enabled

**Scripts:**
- `bin/manage_certificates.sh` - Certificate request automation

**Status:** ✅ 100% Complete (12/12 tasks)

---

## Monitoring Setup

### LibreNMS
- **Installation:** Complete
- **Version:** 25.11.0-dev.80
- **Database:** MySQL (local)
- **Storage:** NFS-backed RRD data
- **Authentication:** MySQL
- **Certificate:** FreeIPA (HTTPS)
- **SNMPv3:** Configured

**Monitored Devices:**
- lima.projekt.lab (self)

**Pending Devices:**
- whiskey.projekt.lab (Proxmox)
- tango.projekt.lab (TrueNAS)
- echo.projekt.lab (Rocky Linux)
- alpha.projekt.lab (FreeIPA)

**Documentation:**
- LIBRENMS_INSTALLATION_COMPLETE.md
- LIBRENMS_QUICK_REFERENCE.md
- LIBRENMS_INSTALLATION_LESSONS.md

**Status:** 🟡 65% Complete (18/28 tasks)

---

## Storage Architecture

### NFS Exports
TrueNAS provides NFS storage for:
- LibreNMS RRD data
- Graylog log storage (planned)
- General shared storage

### Backend Storage
- TrueNAS manages ZFS pools
- Automated snapshots
- Replication configured

---

## Quick Reference

### SSH Access
```bash
# Hypervisor
ssh root@whiskey.projekt.lab

# VMs
ssh admin@alpha.projekt.lab    # FreeIPA
ssh admin@tango.projekt.lab    # TrueNAS
ssh admin@echo.projekt.lab     # Rocky Linux
ssh admin@lima.projekt.lab     # LibreNMS
```

### Web Interfaces
```
Proxmox:  https://whiskey.projekt.lab:8006
FreeIPA:  https://alpha.projekt.lab
TrueNAS:  https://tango.projekt.lab
Cockpit:  https://echo.projekt.lab:9090
LibreNMS: https://lima.projekt.lab
```

### Key Files
- `data/templates/certificate_hosts.conf` - Certificate host list
- `bin/manage_certificates.sh` - Certificate automation
- `docs/infrastructure/` - Infrastructure documentation
- `docs/monitoring/` - Monitoring documentation

---

**Last Validated:** 2025-11-05  
**Next Review:** When new services added
