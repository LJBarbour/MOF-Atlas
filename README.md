# MOF Atlas

A single-page, offline-first reference and catalogue for 107 metal–organic frameworks. Open `mof-atlas.html` directly in any modern browser — no server, no network, no dependencies.

## What's in this folder

- **`mof-atlas.html`** — the app, ~1.1 MB. Embeds the database, SmilesDrawer (for 2D ligand structures), 3Dmol.js (for the 3D crystal viewer) and all app code in one file.
- **`mofs.json`** — the database in editable form. The app reads this if it sits next to the HTML; otherwise it uses the copy embedded in the HTML as a fallback.
- **`fetch_cifs.py`** — helper that downloads CIFs from the Crystallography Open Database for entries with a recorded `cod_id`, into a sibling `cif/` folder.
- **`README.md`** — this file.

## Browsing

The toolbar gives you Cards / Table / Plot / Compare views, full-text search, and a filter rail (metal, topology, application, year, BET surface area). Pin entries to the Compare view to see side-by-side property tables. Export the current filtered set as CSV or BibTeX.

## Editing existing records

Open any record (click a card or row), then **Edit** in the drawer header. The editor covers every field — name, aliases, formula, year, group, crystal system, space group, a/b/c, topology, SBU, BET, pore size, pore volume, density, metals, ligands (with SMILES that drive the 2D structure drawer), `cod_id`, applications with status, sorption table, description, references. Click **Save** to apply changes locally and the toolbar shows an *Unsaved* indicator; click **Save DB** in the toolbar when you're ready to download the updated `mofs.json`. Replace the file next to the HTML, reload, and your edits are in.

Adding a new entry: **Add MOF** in the toolbar, or **Duplicate** from any existing record (handy for series like the M-MOF-74 isostructural set).

## Supplying CIFs for the 3D viewer

The 3D viewer in each drawer looks for a crystal structure in three places, in order:

1. **Sibling file** at `cif/<entry-id>.cif` next to `mof-atlas.html` — the canonical, shareable location.
2. **Locally-cached CIF** in the browser's IndexedDB — convenient for ad-hoc work and survives reloads.
3. If neither exists, a clear placeholder explains how to add one and (where a `cod_id` is recorded) links straight to the COD page.

### Three ways to supply a CIF

**1. Drag-and-drop** (easiest, single record):
Open the entry, drag the CIF onto the 3D viewer panel. The structure renders immediately and is cached in your browser. A *Save as cif/<id>.cif* button appears so one click downloads the file with the correct name — drop the download into a `cif/` folder next to the HTML for permanence and sharing.

**2. Bulk import** (best for many at once):
Click **Import CIFs** in the toolbar. Drop in any number of `.cif` files. Each filename is matched against entry IDs and aliases — punctuation, case, and spaces are ignored, so `MOF-5.cif`, `mof5.cif`, and `MOF 5.cif` all match the same record. You get a report of matches and skipped files, and matched CIFs are cached locally. The 3D viewer auto-loads them.

**3. CIF cache manager** (review and curate):
**Cached CIFs** in the toolbar opens a panel listing every locally-cached CIF, with options to view, download, or forget each one — plus a *Download all* button to save the whole set to disk in one go (useful for migrating to a `cif/` folder or sharing).

A small `◇ CIF` badge appears on cards and table rows for any entry with a cached structure available.

### Bootstrapping with COD

Five entries ship with verified COD IDs (MOF-5, HKUST-1, ZIF-8, UiO-66, MOF-74). To download those CIFs:

```
python3 fetch_cifs.py
```

This populates a `cif/` folder next to the HTML. The `cod_id` field is also editable in the in-app editor — add IDs as you confirm them, save the DB, and run `fetch_cifs.py` again to fill the rest.

## Hosting

Drop `mof-atlas.html`, `mofs.json`, and (optionally) the `cif/` folder into a GitHub Pages repo. No build step. The IndexedDB cache is per-browser, so what visitors see is whatever is in `cif/`.

## Caveats

- The 3D viewer needs WebGL (every browser from the last decade has it).
- The IndexedDB cache is bound to the browser/profile and origin — clearing site data wipes it. The *Download all* button in the Cached CIFs panel is the migration path.
- 2D ligand structures are rendered live from SMILES via SmilesDrawer — all 122 ligand entries across the 107 MOFs render successfully.
- Only the five seed COD IDs are pre-recorded; the rest you'll need to add as you collect CIFs. The placeholder in the 3D viewer offers a direct COD search link for entries without an ID.
