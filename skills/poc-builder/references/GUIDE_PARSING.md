# Guide Parsing Heuristics

How to extract structured data from sfquickstarts guides and other content sources.

---

## sfquickstarts format

```markdown
author: Author Name
id: guide-slug
summary: One-line summary
categories: Category1,Category2
environments: web
status: Published
feedback link: https://github.com/...
tags: Tag1, Tag2, Tag3
<!-- -->

## Overview
Duration: 5

Guide overview text...

<!-- -->

## Step Title
Duration: 15

Step content with code blocks...

<!-- -->

## Conclusion
Duration: 5

Summary and next steps...
```

**Key parsing rules:**
- Sections separated by `<!-- -->`
- Each section starts with `## Title` followed by `Duration: N`
- First chunk = metadata (frontmatter-style key:value pairs)
- Code blocks use standard markdown fencing
- Steps are sequential

## Extracting steps from a guide

1. Split content on `<!-- -->` delimiters
2. First chunk = metadata (extract title, summary, tags)
3. Each subsequent chunk = one step
4. For each step:
   - Title = first `## ` heading
   - Duration = `Duration: N` line (minutes)
   - Code blocks = all fenced code blocks (note the language)
   - Explanatory text = everything outside code blocks
   - Sub-steps = any `### ` headings within the step

## Extracting data requirements

Look for:
1. **CREATE TABLE statements** → column names, types, shape
2. **INSERT/COPY INTO statements** → sample data, file formats
3. **SELECT statements** → which columns are actually used
4. **External stage references** → data files in S3/GCS/Azure
5. **Variable references** → parameterized values (connection strings, keys)
