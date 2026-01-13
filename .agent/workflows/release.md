---
description: Release checklist for SC GlobalIni Extractor
---
# SC GlobalIni Extractor Release Workflow

## Pre-Release Checklist

Before creating a new release tag, verify the following:

### Version Consistency
- [ ] **Sidebar version** in `extract_tool.py` line ~92 (`text="vX.X.X\n© BeltaKoda"`) matches release version
- [ ] **version_info.template** will be auto-populated from Git tag (no manual update needed)

### Code Quality
- [ ] Remove any hardcoded version strings that should be dynamic
- [ ] Remove placeholder text like "Unknown Version" - prefer blank/hidden or just show available info
- [ ] Test the GUI before releasing

## Release Process

1. Update sidebar version in `extract_tool.py`:
   ```python
   text="v1.2.0\n© BeltaKoda"  # Update this line
   ```

2. Commit changes:
   ```bash
   git add .
   git commit -m "Bump version to v1.2.0"
   git push origin main
   ```

3. Create and push tag:
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

4. GitHub Actions will automatically:
   - Generate `version_info.txt` from the tag
   - Build the EXE with embedded version metadata
   - Create a GitHub Release

## Post-Release

- Verify EXE Details tab shows correct version
- Verify sidebar in running app shows correct version
- Download and test extraction functionality
