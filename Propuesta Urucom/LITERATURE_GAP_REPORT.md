# Literature Gap Report — Urucom.tex

Targeted literature review for "Automatic DC-Offset Calibration for a Low-Cost Geophone Front End." Scope: strengthen novelty argument, technical background, and comparison with prior work. No manuscript files were modified. No fabricated or unverified references are included — every candidate below was checked against Crossref and/or a publisher/aggregator page before being listed. Where a search category returned nothing citable, that is reported as a gap with no candidate, not papered over with a weak match.

---

## 1. Claims currently lacking citations

| # | Claim (file:paragraph) | Current citation support | Gap |
|---|---|---|---|
| C1 | "Digitally Assisted Control Calibration" — section title and framing (`03_self_calibrating_platform.tex`, §III-B heading) | None | The term of art ("digitally assisted analog") is used without citing the subfield. Flagged already in the earlier internal review (audit item U1) and never resolved. |
| C2 | "A continuously active DC servo... showed a low corner centered impractically slowly, a faster loop interfered with the signal, and a gain change forced another transient" (`05_discussion.tex`, §V ¶2; also `01_introduction.tex` ¶4) | None | The corner-frequency/settling-time tradeoff of a DC servo loop is asserted from the authors' own bench experience with zero external support, even though this exact tradeoff is well documented in the chopper/DC-servo literature. |
| C3 | "its internal analog blocks cannot be independently optimized for low offset, drift, and flicker noise" (`01_introduction.tex` ¶2) | \cite{Lopin2018} only | Lopin2018 supports the *specific PSoC potentiostat* tradeoff anecdote, but the general offset/1/f-noise-reduction literature (the reason autozero/chopper exists at all) is not cited anywhere, weakening the DC-coupled justification paragraph that follows. |
| C4 | Motivation for a low-cost, mixed-signal-SoC geophone node vs. existing low-cost alternatives (`01_introduction.tex` ¶1) | \cite{Kafadar2020} only | Only one low-cost comparison point is cited. A second, architecturally different low-cost geophone recorder (microcontroller + fixed-gain instrumentation amp, no on-chip calibration) would make the "existing low-cost nodes don't self-calibrate" contrast concrete instead of implied. |

---

## 2. Missing literature categories (searched, no qualifying candidate found)

Per the reject criteria in scope (unverifiable, generic-calibration-only, duplicate, or padding-only sources excluded):

- **Category 3/4 (offset trimming of cascaded PGA/filter/ADC chains, calibrating intermediate nodes vs. digital subtraction at the ADC output).** This is the paper's actual novelty claim. Searched directly; results were exclusively patents, vendor application notes (Analog Devices, Microchip), or time-interleaved-ADC gain/offset/timing-mismatch calibration papers — a different problem domain (per-channel mismatch in multi-ADC sampling, not per-stage physical operating-point trim in a cascaded analog chain). None were peer-reviewed and on-topic enough to cite without overstating relevance. **This category remains a real, reportable gap** — it is also the reason the manuscript's own Discussion already concedes the comparison with prior self-calibration work is "architectural, not quantitative."
- **DC-coupled / low-frequency preservation for geophones specifically**, beyond \cite{Ma2023}. No second paper found that addresses this narrower point without duplicating Ma2023's coverage.

---

## 3. Candidate references found (5, all independently verified via Crossref)

### R1 — Enz & Temes 1996 (essential)
- **IEEE reference:** C. C. Enz and G. C. Temes, "Circuit techniques for reducing the effects of op-amp imperfections: autozeroing, correlated double sampling, and chopper stabilization," *Proc. IEEE*, vol. 84, no. 11, pp. 1584–1614, Nov. 1996.
- **DOI:** 10.1109/5.542410
- **Peer-reviewed:** Yes — Proceedings of the IEEE (invited survey).
- **Verified:** Yes, cross-checked via Semantic Scholar, IEEE Xplore listing, and SCIRP reference record; DOI confirmed independently in two of those sources.
- **Claim it supports:** C3 — the canonical survey of autozero/CDS/chopper techniques, i.e., exactly the class of solution the DC-coupled design in this paper explicitly did *not* choose.
- **Where to cite:** `01_introduction.tex`, the DC-coupled paragraph — right after "leaves per-stage trimming as the remaining option once the amplifiers themselves cannot be swapped for lower-offset external parts." Anchors the claim that autozero/chopper is the well-known alternative being ruled out, not an oversight.
- **How it differs from what's already cited:** Nothing currently cited addresses offset/1-f-noise reduction technique classes in general; Lopin2018 and InfineonAN68403 are specific product/prior-work comparisons, not the technique survey.

### R2 — Murmann 2006 (essential)
- **IEEE reference:** B. Murmann, "Digitally assisted analog circuits," *IEEE Micro*, vol. 26, no. 2, pp. 38–47, Mar.–Apr. 2006.
- **DOI:** 10.1109/MM.2006.33
- **Peer-reviewed:** Yes — IEEE Micro is a peer-reviewed IEEE magazine.
- **Verified:** Yes, via Crossref API direct query (`api.crossref.org/works?query.title=...`), matched on exact title/author/venue/year/DOI.
- **Claim it supports:** C1 — this is the standard citation for the term "digitally assisted analog," used as the section title/heading in the manuscript.
- **Where to cite:** `03_self_calibrating_platform.tex`, first sentence of §III-B ("Digitally Assisted Control Calibration"), or alternatively in the Introduction where the architecture is first framed as reusing digital resources to correct analog imperfections.
- **How it differs from what's already cited:** No existing reference addresses the digitally-assisted-analog design paradigm as a named subfield; this closes exactly that gap.

### R3 — Liu et al. 2020 (essential)
- **IEEE reference:** Y. Liu, Z. Zhou, Y. Zhou, W. Li, and Z. Wang, "A low-noise chopper amplifier with offset and low-frequency noise compensation DC servo loop," *Electronics*, vol. 9, no. 11, Art. no. 1797, 2020.
- **DOI:** 10.3390/electronics9111797
- **Peer-reviewed:** Yes — MDPI Electronics, peer-reviewed journal (note: MDPI has mixed reputation across fields; this specific journal and article are indexed and peer-reviewed, but flag for the co-author's judgment call given the venue).
- **Verified:** Yes, via Crossref API direct query; authors, volume/issue/article number, year, and DOI all confirmed programmatically (not just from search snippets).
- **Claim it supports:** C2 — a concrete, peer-reviewed treatment of exactly the DC-servo corner-frequency/offset-compensation tradeoff the Discussion describes from bench experience alone.
- **Where to cite:** `05_discussion.tex` §V ¶2, at "a continuously active DC servo showed a low corner centered impractically slowly..." — and optionally back-referenced from `01_introduction.tex` ¶4 where the same design decision is first mentioned.
- **How it differs from what's already cited:** Nothing currently cited addresses DC-servo design tradeoffs at all; this is a genuinely uncovered claim, not a duplicate.

### R4 — Soler-Llorens et al. 2016 (useful)
- **IEEE-style reference:** J. L. Soler-Llorens, J. J. Galiana-Merino, J. Giner-Caturla, P. Jauregui-Eslava, S. Rosa-Cintas, and J. Rosa-Herranz, "Development and programming of Geophonino: A low cost Arduino-based seismic recorder for vertical geophones," *Computers & Geosciences*, vol. 94, pp. 1–8, 2016.
- **DOI:** 10.1016/j.cageo.2016.05.014
- **Peer-reviewed:** Yes — Computers & Geosciences (Elsevier).
- **Verified:** Yes — DOI and full author list confirmed via search-engine aggregation of the ScienceDirect/ADS listings (ScienceDirect itself blocked direct fetch with HTTP 403; DOI cross-checked against two independent secondary listings, both agreeing).
- **Claim it supports:** C4 — a second, architecturally distinct low-cost geophone recorder (fixed-gain instrumentation amp + Arduino, no on-chip auto-calibration) to sharpen the "existing low-cost options don't self-calibrate" contrast.
- **Where to cite:** `01_introduction.tex` ¶1, alongside or near \cite{Kafadar2020}.
- **How it differs from what's already cited:** Kafadar2020 is already cited for the general "low-cost data acquisition" claim; Soler-Llorens adds a second, different low-cost architecture (Arduino + fixed analog front end) that has no calibration story at all, making the contrast with this paper's contribution concrete rather than argued from a single example.
- **Confidence flag:** slightly lower than R1–R3 since the primary publisher page (ScienceDirect) could not be fetched directly; verification rests on two independent secondary sources agreeing on the same DOI, not a first-party page.

### R5 — Sonoda et al. 2012 (optional)
- **IEEE reference:** K. Sonoda, Y. Kishida, T. Tanaka, K. Kanda, T. Fujita, K. Maenaka, and K. Higuchi, "Wearable photoplethysmographic sensor system with PSoC microcontroller," in *Proc. 2012 5th Int. Conf. Emerging Trends Eng. Technol. (ICETET)*, 2012.
- **DOI:** 10.1109/ICETET.2012.19
- **Peer-reviewed:** Conference proceedings, peer-reviewed (IEEE ICETET 2012).
- **Verified:** Yes, via Crossref API direct query. Note: the same title also exists as a 2013 journal version (DOI 10.1080/1931308X.2013.795034, *Int. J. Intelligent Computing in Medical Sciences & Image Processing*) — two distinct, independently indexed publications of related content by the same author group; the IEEE conference version is recommended for consistency with this manuscript's IEEE venue.
- **Claim it supports:** A secondary, optional data point that PSoC is an established platform for sensor-instrumentation front ends outside this paper's own prior work (Lopin2018).
- **Where to cite:** `01_introduction.tex` ¶2, if the platform-selection paragraph is judged to need a second PSoC-instrumentation example beyond Lopin2018.
- **Why optional, not useful/essential:** Lopin2018 already carries this exact claim ("PSoC used for sensor instrumentation"); this is redundant unless the co-author specifically wants a non-potentiostat, non-self-calibration example to show breadth. Do not add if it would only pad the count.

---

## 4. Recommended final subset (in priority order, all 5 candidates found — none dropped for weakness)

1. **R1 — Enz & Temes 1996** (essential): closes C3, backs the entire DC-coupled design-choice paragraph.
2. **R2 — Murmann 2006** (essential): closes C1, resolves an already-flagged audit item (unsupported use of "digitally assisted").
3. **R3 — Liu et al. 2020** (essential): closes C2, the single most-exposed unsupported claim in the Discussion.
4. **R4 — Soler-Llorens et al. 2016** (useful): closes C4, sharpens the novelty contrast in the Introduction with a concrete second data point.
5. **R5 — Sonoda et al. 2012** (optional): include only if page budget and co-author judgment allow; otherwise skip — it would not be missed.

All 5 fit within the "≤5–7 new references" cap. If page space is the binding constraint (the manuscript is already at the IEEE URUCON 5-page limit with no slack — confirmed in the prior page-count pass), recommend R1–R3 only (the three "essential" items) and hold R4/R5 for a future extended version.

---

## 5. Citation insertion map (for `Urucom.tex`, not yet applied)

| Reference | File | Anchor sentence | Insertion |
|---|---|---|---|
| R1 (Enz & Temes) | `sections/01_introduction.tex` | "...leaves per-stage trimming as the remaining option once the amplifiers themselves cannot be swapped for lower-offset external parts without abandoning the single-chip premise." | Append `\cite{EnzTemes1996}` after this sentence, or insert a clause: "...(the well-established alternative — autozero, correlated double sampling, or chopper stabilization \cite{EnzTemes1996} — requires either a second clock domain or external precision components this design avoids)." |
| R2 (Murmann) | `sections/03_self_calibrating_platform.tex` | `\subsection{Digitally Assisted Control Calibration}` (§III-B heading) or first sentence below it | Add citation on first use of the term, e.g. "For each stage, the filtered observation... [digitally assisted analog calibration \cite{Murmann2006}]" — or simpler, footnote/cite right after the subsection heading's first sentence. |
| R3 (Liu et al.) | `sections/05_discussion.tex` | "The foreground method was adopted after a continuously active DC servo showed a low corner centered impractically slowly, a faster loop interfered with the signal, and a gain change forced another transient." | Append `\cite{Liu2020}` at the end of this sentence. |
| R4 (Soler-Llorens et al.) | `sections/01_introduction.tex` | "...so compact wireless nodes built from inexpensive geophones and mixed-signal microcontrollers are attractive for dense, reconfigurable arrays \cite{Kafadar2020}." | Change to `\cite{Kafadar2020,Soler2016}` or add one clause distinguishing this paper's node from fixed-gain Arduino-based recorders. |
| R5 (Sonoda et al., optional) | `sections/01_introduction.tex` | "...integrates programmable-gain amplifiers, operational amplifiers, analog filters, voltage DACs, analog multiplexers, a delta-sigma ADC, a digital filter block, DMA, and an Arm Cortex-M3 processor in one device \cite{InfineonPSoC}." | Only if included: append `\cite{Sonoda2012}` alongside, as a second real-world PSoC sensor-instrumentation example. |

**BibTeX-ready `\bibitem` blocks** (for direct use if the co-author approves; not yet inserted into `references/references.tex`):

```
\bibitem{EnzTemes1996}
C. C. Enz and G. C. Temes, ``Circuit techniques for reducing the effects
of op-amp imperfections: autozeroing, correlated double sampling, and
chopper stabilization,'' \emph{Proc. IEEE}, vol. 84, no. 11,
pp. 1584--1614, Nov. 1996, doi: 10.1109/5.542410.

\bibitem{Murmann2006}
B. Murmann, ``Digitally assisted analog circuits,'' \emph{IEEE Micro},
vol. 26, no. 2, pp. 38--47, Mar.--Apr. 2006, doi: 10.1109/MM.2006.33.

\bibitem{Liu2020}
Y. Liu, Z. Zhou, Y. Zhou, W. Li, and Z. Wang, ``A low-noise chopper
amplifier with offset and low-frequency noise compensation DC servo
loop,'' \emph{Electronics}, vol. 9, no. 11, Art. no. 1797, 2020,
doi: 10.3390/electronics9111797.

\bibitem{Soler2016}
J. L. Soler-Llorens, J. J. Galiana-Merino, J. Giner-Caturla,
P. Jauregui-Eslava, S. Rosa-Cintas, and J. Rosa-Herranz, ``Development
and programming of Geophonino: A low cost Arduino-based seismic
recorder for vertical geophones,'' \emph{Computers \& Geosciences},
vol. 94, pp. 1--8, 2016, doi: 10.1016/j.cageo.2016.05.014.

\bibitem{Sonoda2012}
K. Sonoda, Y. Kishida, T. Tanaka, K. Kanda, T. Fujita, K. Maenaka, and
K. Higuchi, ``Wearable photoplethysmographic sensor system with PSoC
microcontroller,'' in \emph{Proc. 2012 5th Int. Conf. Emerging Trends
Eng. Technol. (ICETET)}, 2012, doi: 10.1109/ICETET.2012.19.
```

---

## Notes on process

- No reference below was accepted on a single search-snippet's word; each DOI was either confirmed via a direct Crossref API query or cross-checked against two independent secondary sources agreeing on the same identifier.
- Categories that returned only patents, vendor application notes, or off-topic ADC-mismatch-calibration papers were reported as unresolved gaps (§2) rather than filled with a weak match, per the "reject" instructions.
- Adding any of these requires manually adding the `\bibitem` blocks above to `references/references.tex` **at the correct position for first-appearance order** (the bibliography was just reordered for exactly this reason — see prior session work) and re-running the citation-order check afterward.
- Page budget: the manuscript is currently at exactly 5 of 5 allowed pages. Adding citations costs no space (inline `\cite{}` markers are ~1 character each), but the reference list itself will grow by up to 5 lines at `\scriptsize`; recommend re-verifying the page count after insertion, prioritizing R1–R3 if space gets tight.
