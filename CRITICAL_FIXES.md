# Critical Fixes - Quick Reference

This document provides step-by-step instructions to fix the critical issues identified in the codebase analysis.

---

## Fix 1: ESLint Errors (3 errors)

### Error 1 & 2: Empty Interfaces

**Files to fix**:
- `src/components/ui/command.tsx` (line 24)
- `src/components/ui/textarea.tsx` (line 5)

**Current code** in `command.tsx`:
```typescript
interface CommandDialogProps extends DialogProps {}
```

**Fixed code**:
```typescript
type CommandDialogProps = DialogProps;
```

**Current code** in `textarea.tsx`:
```typescript
export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}
```

**Fixed code**:
```typescript
export type TextareaProps = React.TextareaHTMLAttributes<HTMLTextAreaElement>;
```

---

### Error 3: CommonJS require() in ESM

**File**: `tailwind.config.ts` (line 143)

**Current code**:
```typescript
export default {
  // ... config
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
```

**Fixed code**:
```typescript
import tailwindcssAnimate from "tailwindcss-animate";

export default {
  // ... config
  plugins: [tailwindcssAnimate],
} satisfies Config;
```

**Full change**:
- Add import at top of file
- Replace require() with variable reference

---

## Fix 2: Security Vulnerabilities

### Step 1: Fix Auto-fixable Issues

```bash
npm audit fix
```

This will update `esbuild` and related packages.

### Step 2: Test After Fix

```bash
npm run build
npm run lint
```

### Step 3: Document Remaining Issues

The `markdown` package vulnerability has no fix. Add to README:

```markdown
## Known Issues

- **markdown package**: Contains a ReDoS vulnerability (GHSA-wx77-rp39-c6vg) with no fix available. 
  This package is used for [specify usage]. Risk is minimal because [explain mitigation].
  Tracking: [link to issue if created]
```

### Step 4: Address Peer Dependency Issue

**Option A**: Try updating @toast-ui packages
```bash
npm update @toast-ui/react-editor @toast-ui/editor
```

**Option B**: Document the workaround in README.md

Add to "Prerequisites" or "Installation" section:
```markdown
**Note**: This project requires `--legacy-peer-deps` due to React 18 compatibility:

\`\`\`bash
npm install --legacy-peer-deps
\`\`\`

This is necessary because `@toast-ui/react-editor` currently requires React 17.
```

---

## Fix 3: Bundle Size Optimization

### Implementation

**File**: `vite.config.ts`

Add manual chunks configuration:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // React core
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          
          // UI components
          'vendor-radix': [
            '@radix-ui/react-dialog',
            '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-tabs',
            '@radix-ui/react-tooltip',
          ],
          
          // Heavy dependencies
          'vendor-markdown': ['react-markdown', 'markdown'],
          'vendor-charts': ['recharts'],
          'vendor-forms': ['react-hook-form', '@hookform/resolvers', 'zod'],
        },
      },
    },
    chunkSizeWarningLimit: 1000, // Temporarily increase to monitor progress
  },
});
```

### Test the Changes

```bash
npm run build

# Check output - should see multiple vendor-*.js files
# Total gzipped size should be lower per chunk
```

---

## Fix 4: Remove Build Artifact from Git

### Step 1: Update .gitignore

Add to `.gitignore`:
```gitignore
# Downloaded packages
*.deb
*.deb.*
```

This line already exists at line 50-51, so verify it's there.

### Step 2: Remove from Git

```bash
# Remove from git but keep local file
git rm --cached pandoc-3.1.9-1-amd64.deb

# Commit the change
git commit -m "Remove Pandoc .deb file from repository - should be downloaded during setup"
```

### Step 3: Update Documentation

In README.md, ensure installation instructions say to DOWNLOAD Pandoc, not expect it in repo:

```markdown
### Prerequisites

**For PDF Generation:**
\`\`\`bash
# Download and install Pandoc (3.1.9 or later)
wget https://github.com/jgm/pandoc/releases/download/3.1.9/pandoc-3.1.9-1-amd64.deb
sudo dpkg -i pandoc-3.1.9-1-amd64.deb
\`\`\`
```

---

## Fix 5: Documentation Language Consistency

### Decision Required

**Choose One**:

1. **Option A: Full English** (Recommended for OSS)
2. **Option B: Hybrid with Documentation** (Document the language split)

### If Choosing Option A (Full English):

Create a tracking issue and systematic approach:

1. **Phase 1**: Fix documentation files
   - Translate bot.md to English
   - Translate CICD_SETUP.md to English
   - Update any Swedish comments to English

2. **Phase 2**: Update code
   - Update Python script strings to English
   - Update print statements to English
   - Update function comments to English

3. **Phase 3**: Verify
   - Search for remaining Swedish: `grep -r "Skapar\|Genererar\|Filer" --include="*.py" .`
   - Update as needed

### If Choosing Option B (Hybrid):

Update README.md with explicit language policy:

```markdown
## Language Policy

This repository uses a hybrid language approach:

- **Book Content**: English (`docs/*.md`)
- **User Documentation**: English (README.md, WORKFLOWS.md, etc.)
- **Internal Tooling**: Swedish (Python scripts, some workflow docs)
- **Code Comments**: Mixed (being standardized to English)

This reflects the Swedish origin of the project while making content accessible internationally.
```

---

## Verification Checklist

After applying fixes, verify:

- [ ] `npm run lint` passes with 0 errors (warnings acceptable)
- [ ] `npm run build` succeeds
- [ ] Bundle size reduced (check dist/ folder sizes)
- [ ] `git status` shows no uncommitted build artifacts
- [ ] Documentation updated to reflect changes
- [ ] All changes committed with clear messages

---

## Testing Commands

Run these after each fix to ensure nothing broke:

```bash
# 1. Install (if you changed dependencies)
npm install --legacy-peer-deps

# 2. Lint check
npm run lint

# 3. Build check
npm run build

# 4. Python check
python3 generate_book.py

# 5. Git status
git status

# 6. View bundle sizes
ls -lh dist/assets/
```

---

## Estimated Time

- **Fix 1** (ESLint errors): 15 minutes
- **Fix 2** (Security): 30 minutes (includes testing)
- **Fix 3** (Bundle size): 20 minutes
- **Fix 4** (Git cleanup): 10 minutes
- **Fix 5** (Language): 2+ hours (depends on scope chosen)

**Total for Fixes 1-4**: ~1.5 hours  
**Total including Fix 5**: 3.5+ hours

---

## Order of Execution

**Recommended order**:

1. Fix 1 (ESLint) - Quick wins, immediate improvement
2. Fix 3 (Bundle size) - Improves user experience
3. Fix 2 (Security) - May update dependencies
4. Fix 4 (Git cleanup) - Housekeeping
5. Fix 5 (Language) - Longer term, requires decision

This order minimizes dependency conflicts and provides incremental improvements.
