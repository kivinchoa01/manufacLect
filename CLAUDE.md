# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive HTML slide-based textbook for **工程材料与机械制造基础** (Engineering Materials and Mechanical Manufacturing Fundamentals), 3rd Edition, edited by 齐乐华 (Qi Lehua) — Higher Education Press. All text and UI are in Chinese.

## Architecture

Pure static HTML/CSS/JS slides — no build tools, frameworks, or server-side processing. Every chapter is a single self-contained `.html` file with **inline CSS**. Open any file in a browser to view it.

### Directory Layout

```
index.html                         — Course catalog / table of contents (grid of chapter cards)
第1章_材料的种类与性能.html          ─┐
第2章_材料的组织结构.html           │
...                                ├─ Chapter slides (1920×1080 fixed-size slides)
第9章_焊接.html                    │
第13章_切削加工基础知识.html        ┘
第7章_铸造_blue.html               — Themed variant of Ch7 (blue color scheme)
images/                            — ~350 JPG figures, referenced as images/***.jpg
README.md
```

### Chapter Index Behavior

`index.html` lists all 17 planned chapters. Some entries link to existing `.html` files (`href="第N章_...html"`); others are disabled placeholders (`href="#"`, `opacity:.5`, `style="opacity:.5"`) with status "待生成" (to be generated). Enabled chapters are marked "已完成" (completed). To add a new chapter, create its HTML file and update the corresponding `<a>` in `index.html`.

### Slide System

Each chapter file contains a series of `<section class="slide">` elements inside a fixed `1920×1080` stage:

```html
<div class="vp">
  <div class="stage" id="stg">
    <section class="slide a ts">...</section>    <!-- Title slide (active) -->
    <section class="slide ss">...</section>       <!-- Section divider -->
    <section class="slide cs">...</section>       <!-- Content slide -->
  </div>
  <div class="ctrl">...</div>                     <!-- Navigation bar -->
</div>
```

**Slide types:**
- `.ts` — Title slide with red accent bar, chapter number, title
- `.ss` — Section divider (large centered text, section number overlay)
- `.cs` — Content slide with slide number (`<p class="sn">`), heading, body text/images

**CSS utility classes:**
- `.sn` — slide number watermark (top of content slides)
- `.hl` — highlight text (red, for key terms)
- `.iw` — image wrapper (centered, with shadow and optional `.cap` caption)
- `.fb` — full-width block (centered, gray background)
- `.g2` / `.g3` — 2-column / 3-column grid layout
- `.sm` — small/supplementary text

**KaTeX:** Mathematical formulas use CDN-loaded KaTeX with `defer` + `auto-render`.

### Navigation

A fixed bottom-center control bar (`.ctrl`) provides prev/next buttons and a page indicator. JavaScript toggles opacity/pointer-events via the `.a` (active) class. The stage auto-scales to fit the viewport. Print media queries render slides as separate pages.

### Edit Mode

Each chapter includes an edit toggle: clicking the top-left corner (`.ez`, 80×80px invisible click zone) reveals an "编辑" button (`.eb`) that toggles `contenteditable` on all slides — useful for light editing in-browser.

### Theming Variants

`第7章_铸造_blue.html` is a color-scheme variant of the standard chapter. The standard accent color is `#e03020` (red). Variants replace it globally with an alternative (e.g., `#1e2bfa` blue). To create a variant, copy the chapter file and do a global find-and-replace of the accent color.

### Image Convention

All images are JPG files in `images/` named as `<index>_<Chinese_description>.jpg`. Referenced in slides via `<img src="images/...">` inside `.iw` wrappers.

### Content Patterns

- **Chapter structure:** Theoretical basis → Process methods → Process design → Applications → Exercises
- **Exercises** are the last slides (numbered "题" style), referencing figures from the textbook
- Each section typically begins with a `.ss` divider slide before `.cs` content slides

## Creating a New Chapter

1. Copy an existing chapter file as a template
2. Update `<title>`, slide content (keeping the slide structure pattern), and image references
3. Use `images/` for any new figures
4. Add a card entry in `index.html` (matching the existing card pattern) and update its link/href

## Commands

No build, test, or lint commands needed. The project is pure static HTML:
- **View:** Open any `.html` file in a browser
- **Edit:** Directly edit the HTML files, or use the built-in edit mode (click top-left corner, then "编辑")
