# HTML Output Styling Reference

Used by the developer-voice skill when generating HTML artifacts. Apply this color scheme and typography consistently across all output files.

## Color Scheme

```
Problems / pain:   bg #fff0f0, border-left #e53935
Solutions:         bg #f0f9ff, border-left #29b5e8
Caveats:           bg #fff8e1, border-left #ffa000
Snowflake answer:  bg #e8f5fe, border-left #0d47a1
Get started:       bg #e8f5e9, border-left #2e7d32
Reddit quotes:     bg #f5f7fa, border-left #29b5e8, font-style italic
Talk notes:        color #7e57c2, border-left #ce93d8, font-style italic, font-size small
```

## Typography & Layout

```
Font: system font stack (-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif)
Max width: 860px, centered (margin: 0 auto)
Body padding: 24px
H1: 28px, H2: 22px, H3: 18px
```

## Section Callout Pattern

```html
<div style="background:#fff0f0; border-left:4px solid #e53935; padding:16px; margin:16px 0; border-radius:4px">
  <strong>Pain point header</strong>
  <p>Content here.</p>
</div>
```

## Reddit Quote Pattern

```html
<blockquote style="background:#f5f7fa; border-left:4px solid #29b5e8; padding:12px 16px; margin:16px 0; font-style:italic; border-radius:4px">
  "Quote text here."
  <footer style="margin-top:8px; font-size:0.85em; color:#666;">— r/subreddit, role/context if known</footer>
</blockquote>
```

## Talk Notes Pattern (for talk-track format)

```html
<div style="color:#7e57c2; border-left:3px solid #ce93d8; padding:8px 12px; margin:12px 0; font-style:italic; font-size:0.9em">
  💬 <strong>Talk note:</strong> Delivery hint or framing suggestion here.
</div>
```
