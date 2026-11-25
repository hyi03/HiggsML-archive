# Draft-v2 manuscript: draft001 results

[main.tex](main.tex) is the current manuscript in REVTeX 4.2 APS/PRD reprint
format. It reports the completed controlled-MC run `h4l-draft-v2-draft001`, with
60/20/20 training/validation/final allocation and five representations trained
separately for seeds 42–44. All fifteen model intervals and the shared inclusive
reference have valid numerical status. Results remain exploratory,
non-independent and coverage-unvalidated.

## English project report

[project-report.tex](project-report.tex) is the English basic report synchronized
on 8 November 2026. It uses the verified local rerun, fifteen models, twelve
deletion-contrast rows and three figures in `figures/basic-20261108/`. Its seven main sections
cover purpose, samples, feature groups and the MLP, metrics and a worked example,
complete results, mass spectra, and conclusions. The three-hidden-layer model,
training and frozen thresholds are explained at senior-undergraduate level.
Historical interval studies appear only as a short source-linked supplement.

Compile this standalone report with LuaLaTeX:

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=.build/project-report project-report.tex
cp .build/project-report/project-report.pdf project-report.pdf
```

The convenience [English PDF](project-report.pdf) and build directory are ignored.
The PDF is synchronized with the source; compilation uses publication assets and
does not require local runs or external downloads. Select `project-report.tex`
explicitly in an editor; `main.tex` remains the separate REVTeX manuscript.
The English build now uses LuaLaTeX instead of the older pdfLaTeX command.

The synchronized English PDF is 19 A4 pages. It was built on macOS 27.2 arm64 with
TeX Live 2026, LuaHBTeX 1.24.0 and latexmk 4.88, without warnings, missing glyphs,
undefined references or overfull/underfull boxes. The six numerical table bodies,
formulas, labels, citation keys, source URLs and three figure hashes agree with
the Chinese report. All fifteen metric rows and twelve contrast rows were
recomputed from the hash-verified existing aggregate. Page rendering was checked
for clipping, overlap and table/figure readability. These checks establish
translation and document consistency, not independent scientific validation.
No training, scoring, fitting, pseudoexperiments or raw-event access was needed.

### Completed basic comparison — 8 November 2026

The English basic report uses the local `runs/h4l-draft-v2-draft001/report/`
with report identity `a7e610a163e5d155705014201b7ee330323e3bf69309e0e89b2496edba5d4317`.
See [BASIC-20261108-EVIDENCE.md](BASIC-20261108-EVIDENCE.md) for bindings, checks,
full-precision-derived values and asset hashes. The reused run name does not
identify the old manuscript's artifacts. The historical interval appendix and REVTeX manuscript retain their original sources.

All fifteen model results and the inclusive reference are numerically valid.
The report/evaluation aggregate copies, protocol, frozen model identities,
thresholds and access receipt were checked. Each model's high+low signed yields
agree with the shared baseline. Baseline and high-category spectrum totals agree
with the templates. Model metadata confirms the displayed seed-42 epochs and
thresholds; template counts and spectrum fractions confirm the displayed values.
Training/validation counts were not present in consumed aggregates and are no
longer imported from historical tables. No event payload or raw ROOT data was
read or hashed, and no scientific stage was rerun.

The table uses all five representations at seeds 42–44. Ratios are computed from
unrounded template yields, then reduced-minus-ABCD differences are computed
within each seed before taking medians and minimum–maximum ranges. Plot points
show each seed, diamonds their medians and segments their ranges, not confidence
intervals. Removing C worsens all three basic metrics in each of these three
seeds; other deletions have mixed effects. This is descriptive, not a significance
claim or a universal feature ranking. Exploratory qualification is unchanged.

The source-independent build uses three publication PDFs in
`figures/basic-20261108/`. Two are verified copies of this rerun's spectra; the
third is the derived deletion plot. Historical `figures/draft001/` assets remain
unchanged. Use the corresponding LuaLaTeX build command above; no local run is needed to compile.
The local tools are in `/Users/xulei/Library/TinyTeX/bin/universal-darwin`, already
configured for login terminals. Aggregate calculations use Python 3.12.13 in
`pytorch`, NumPy and Matplotlib; builds use TeX Live 2026 and latexmk 4.88.

### Reading order and editorial verification

The report now has seven chapters: research purpose; samples and selection;
feature groups and the neural network; metrics and the ABCD/BCD worked example;
all five representations and deletion results; mass spectra; conclusions and
limitations. The complete comparison follows the worked example, and the deletion
plot is followed immediately by a group-by-group interpretation. The main text
retains the MLP structure and layer explanations, with a compact feature overview.
Implementation APIs and reproduction details are in the appendices.

The report explains signed group-level MC standard errors and the identity
`S/B = (S0/B0) * (RS/RB)`. An appendix gives the covariance-aware retention-error
formula and spectrum support flags. Spectrum captions now correctly describe
standard-error bars and circular markers. Historical interval details remain in
[DRAFT001-EVIDENCE.md](DRAFT001-EVIDENCE.md) and its references, with only a short
historical summary in this report. Source metadata is recorded once in the source
appendix and in [BASIC-20261108-EVIDENCE.md](BASIC-20261108-EVIDENCE.md).

The six current-result table bodies (population, group counts, yields/errors,
all fifteen models, twelve contrasts and mass-region fractions) and all three
figure hashes were checked unchanged. The retention-error formula agrees with
all four existing spectrum aggregates. This is an editorial and aggregate
consistency check; it does not rerun or requalify the scientific analysis.

## Current files

- [project-report-en-concise.tex](project-report-en-concise.tex) is the concise English progress report.
- [project-report-en-revised.tex](project-report-en-revised.tex) is the detailed revised English report.
- [main.tex](main.tex): manuscript, abstract, methods, results and references.
- [workflow.tex](workflow.tex): executed workflow diagram.
- [draft001-tables.tex](draft001-tables.tex): fifteen widths and twelve paired contrasts.
- [draft001-spectra.tex](draft001-spectra.tex): signed-yield table and spectrum discussion.
- [DRAFT001-EVIDENCE.md](DRAFT001-EVIDENCE.md): report identities, hashes and checks.
- `figures/draft001/`: two verified PDF figures copied from the immutable report.

The two figure PDFs are tracked publication assets and are included in a clean
checkout. They were copied byte-for-byte from the historical `runs/h4l-draft-v2-draft001/report/`
after checking their sizes and SHA-256 hashes against the bound manifest and
the evidence index. Ordinary compilation uses the tracked copies and does not
require `runs/`. Other generated figures and build outputs remain ignored.

## Compile

Keep this directory open in the Codex LaTeX editor for compilation and PDF preview.
A separate terminal build is also available, from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=.build main.tex
```

This requires REVTeX 4.2 and the AMS, graphicx, booktabs, TikZ,
microtype, xurl and hyperref packages. References are embedded; no external
bibliography is needed. Terminal output goes to `.build/main.pdf`. Build outputs
and the REVTeX-generated `mainNotes.bib` remain ignored. Compilation does not
require event access, scoring, training or interval fitting.

## Removed historical material

The historical illustration, tables, spectra, export helpers and their diagnostic
outputs are no longer part of this directory. They are archived in
[paper/draft-v2-history](../draft-v2-history/README.md), together with the earlier
manuscript snapshot. The bilingual historical explanation links the archived
sources. The historical selected manuscript, source runs and access ledgers retain
their identities. Current-source numerical values are not taken from that archive.

The tables use native `tabular` columns, following the reference manuscript.
This avoids the REVTeX/array/tabularx compatibility error observed with the local
TeX Live 2026 installation. Both the desktop compiler and the local LaTeX Workshop
`latexmk` command were checked after this change.
