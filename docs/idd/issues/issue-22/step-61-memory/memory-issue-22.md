# Step 61: Memory

## Critical Flame Python Constraints

### Deployment Context
**Source Directory (Development):**
```
cfg/site-cfg/flame-cfg/flame-python/logik_projekt/
```

**Destination Directory (Production):**
```
/var/opt/Autodesk/flame/projects/<MyLOGIK-PROJEKT-flame-project>/setups/python/logik_projekt/
```

### Flame Python Restrictions

> [!CAUTION]
> **NO `__init__.py` FILES ALLOWED**
> 
> Autodesk Flame only loads Python scripts with **unique filenames**. This prevents the use of conventional Python packaging:
> - ❌ No `__init__.py` files
> - ❌ No package-style imports
> - ❌ No relative imports using package structure
> 
> All modules must have globally unique filenames and use absolute or direct imports.

> [!WARNING]
> **HARDCODED PATHS WILL BREAK**
> 
> Any hardcoded paths in the development repository will break once scripts are copied to a Flame project's Python directory:
> - Development paths: `cfg/site-cfg/flame-cfg/flame-python/logik_projekt/...`
> - Production paths: `/var/opt/Autodesk/.../setups/python/logik_projekt/...`
> 
> **Solution:** All paths must be dynamically determined at runtime using:
> - `os.path.dirname(__file__)` for script-relative paths
> - Environment variables or Flame API calls for project-specific paths
> - Configuration files that adapt to deployment context

### Import Strategy

Due to Flame's unique filename requirement, imports are highly restrictive:

1. **Direct imports only:** `import module_name` (no package.module)
2. **Aggregator pattern:** Use aggregator scripts (e.g., `pyside6_qt_flame_modules.py`) to centralize imports
3. **No nested packages:** Flat directory structure required

### Testing Workflow

1. **Development:** Edit scripts in `cfg/site-cfg/flame-cfg/flame-python/logik_projekt/`
2. **Deployment:** Copy entire `logik_projekt/` directory to Flame project's `setups/python/` directory
3. **Validation:** Test in actual Flame environment (paths and imports must work in both contexts)

---

## Key Decisions

- **Session Date:** 2025-11-22
- **Primary Focus:** Scripts in `cfg/site-cfg/flame-cfg/flame-python/logik_projekt/`
- **Constraint Documentation:** Added to memory and insight files
- **Next Steps:** Ensure all scripts follow Flame Python restrictions before testing
