# AILANG Command Dictionary

Complete reference of all AILANG commands organized by category.

---

## Text & Writing

| Command | Description | Example |
|---------|-------------|---------|
| `write` | Create any text content | `write "blog post about AI" !engaging` |
| `rewrite` | Improve or modify text | `rewrite {text} !professional ^clarity` |
| `summarize` | Make content shorter | `summarize {article} [3sentences]` |
| `expand` | Add detail to content | `expand {outline} !detailed` |
| `translate` | Change language | `translate "hello" [spanish] !natural` |
| `explain` | Break down a concept | `explain "blockchain" [eli5] !analogies` |
| `list` | Generate bullet points | `list "productivity tips" [10]` |
| `compare` | Show differences | `compare "React" "Vue" [table]` |
| `reply` | Respond to something | `reply {email} !professional ^helpful` |
| `title` | Generate headlines | `title {article} [5] ^clickworthy _clickbait` |

### Examples

```ailang
// Blog post with SEO
write "remote work tips" [blog][2000words] !headers ^seo !cta

// Executive summary
summarize {report} [executive] !key_metrics ^actionable

// Localization
translate {ui_strings} [japanese] !natural !consistent

// Comparison table
compare "PostgreSQL" "MongoDB" [table] !use_cases !performance
```

---

## Images & Visuals

| Command | Description | Example |
|---------|-------------|---------|
| `img` | Generate an image | `img "sunset over mountains" !photo` |
| `logo` | Create a logo | `logo "tech startup" !minimal` |
| `icon` | Create an icon | `icon "settings" [flat]` |
| `diagram` | Create diagrams | `diagram "microservices" [flowchart]` |
| `mockup` | UI/UX mockups | `mockup "mobile app login" [ios]` |
| `edit_img` | Modify an image | `edit_img {image} "add sunset"` |
| `describe_img` | Explain an image | `describe_img {image} !detailed` |
| `style` | Apply artistic style | `style {image} [van_gogh]` |

### Style Modifiers

| Modifier | Style |
|----------|-------|
| `!photo` | Photorealistic |
| `!art` | Artistic/illustrated |
| `!3d` | 3D rendered |
| `!pixel` | Pixel art |
| `!sketch` | Hand-drawn |
| `!minimal` | Minimalist |
| `!anime` | Anime style |
| `!vintage` | Retro/vintage |

### Examples

```ailang
// Product photography
img "wireless headphones on marble" !photo [studio_lighting] ^commercial

// App icon
icon "meditation app" !minimal [purple,white] [rounded] ^memorable

// Architecture diagram
diagram "AWS infrastructure" [architecture] !labeled ^clear

// UI mockup
mockup "dashboard analytics" [figma] !dark_mode ^modern
```

---

## Code & Development

| Command | Description | Example |
|---------|-------------|---------|
| `code` | Write code | `code "binary search" [rust] !typed` |
| `fix` | Debug/repair code | `fix {code} !explain` |
| `refactor` | Improve structure | `refactor {code} ^readable !dry` |
| `test` | Generate tests | `test {function} [pytest] !edge_cases` |
| `review` | Analyze code quality | `review {pr} !security ^bugs` |
| `convert` | Change language | `convert {code} [typescript]` |
| `api` | Design API | `api "user management" [rest] [openapi]` |
| `query` | Write DB queries | `query "active users" [postgres] ^optimized` |
| `regex` | Create patterns | `regex "email validation" !explained` |
| `docs` | Generate docs | `docs {code} [readme] !quickstart` |

### Quality Modifiers

| Modifier | Meaning |
|----------|---------|
| `!typed` | Include type annotations |
| `!tested` | Include unit tests |
| `!commented` | Add code comments |
| `!dry` | No repetition (DRY principle) |
| `^fast` | Optimize for speed |
| `^readable` | Optimize for clarity |
| `^memory` | Optimize for memory |
| `^secure` | Focus on security |
| `_deps` | No external dependencies |

### Examples

```ailang
// Full-featured function
code "rate limiter" [python] !typed !tested !commented ^concurrent

// Code review
@as "senior engineer" { review {pr} !security !performance ^honest _style }

// API design
api "e-commerce" [graphql] !pagination !auth ^typed

// Database query
query "top customers by revenue last quarter" [postgres] ^optimized !explained
```

---

## Analysis & Reasoning

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Deep examination | `analyze {data} !patterns ^insights` |
| `evaluate` | Judge quality | `evaluate {essay} [rubric] !detailed` |
| `predict` | Forecast outcomes | `predict {trend} [6months]` |
| `diagnose` | Find problems | `diagnose {error_log} !root_cause` |
| `recommend` | Suggest options | `recommend {situation} [3options]` |
| `rank` | Order by criteria | `rank {options} ^roi` |
| `verify` | Check accuracy | `verify {claim} !sources` |
| `extract` | Pull out info | `extract {doc} [entities]` |
| `classify` | Categorize | `classify {tickets} [priority]` |
| `sentiment` | Detect emotion | `sentiment {reviews} > summarize` |

### Examples

```ailang
// Business analysis
analyze "subscription model for SaaS" [market] !swot ^honest

// Technical diagnosis
diagnose {crash_log} !root_cause > recommend[fixes] ^prioritized

// Data extraction
extract {contract} [parties,dates,obligations] [json]

// Sentiment trends
sentiment {customer_feedback} > classify[positive,negative,neutral] > summarize[trends]
```

---

## Creative & Ideas

| Command | Description | Example |
|---------|-------------|---------|
| `brainstorm` | Generate ideas | `brainstorm "app features" [20] ^innovative` |
| `name` | Create names | `name "coffee shop" [5] !available` |
| `story` | Write narrative | `story "AI awakening" [short] !twist` |
| `joke` | Create humor | `joke "programming" !clean` |
| `poem` | Write poetry | `poem "autumn" [haiku] !traditional` |
| `script` | Write dialogue | `script "sales call" [5min]` |
| `pitch` | Create pitch | `pitch {idea} [investor] !60sec` |
| `slogan` | Write tagline | `slogan "eco brand" !memorable` |
| `recipe` | Food instructions | `recipe "healthy pasta" !under_30min` |
| `playlist` | Music suggestions | `playlist "coding focus" [20songs]` |

### Examples

```ailang
// Startup naming
name "AI writing assistant" [10] ^memorable !available _generic _techy

// Children's story
story "brave little robot" [kids_5] !moral !illustrated_style ^heartwarming

// Product pitch
pitch {product} [investor][60sec] ^problem_solution !metrics !traction

// Creative brainstorm
brainstorm "viral marketing ideas" [15] ^unconventional !budget_friendly _unethical
```

---

## Data & Transformation

| Command | Description | Example |
|---------|-------------|---------|
| `format` | Change structure | `format {json} [csv]` |
| `merge` | Combine inputs | `merge {files} [single]` |
| `split` | Divide content | `split {doc} [chapters]` |
| `filter` | Select subset | `filter {data} [active_users]` |
| `sort` | Order items | `sort {list} [alphabetical]` |
| `dedupe` | Remove duplicates | `dedupe {list}` |
| `validate` | Check correctness | `validate {json} [schema]` |
| `map` | Transform items | `map {items} [uppercase]` |
| `template` | Apply pattern | `template {data} [email_template]` |
| `parse` | Extract structure | `parse {text} [json]` |

### Examples

```ailang
// Data pipeline
parse {csv} [json] > validate !schema > dedupe > format[yaml]

// Content splitting
split {book} [chapters] > summarize *

// Data cleaning
filter {users} [active] > dedupe[email] > sort[created_date] > format[csv]
```

---

## Operators Reference

| Operator | Name | Description | Example |
|----------|------|-------------|---------|
| `!` | Must | Required constraint | `!short` `!typed` |
| `~` | Maybe | Nice to have | `~funny` `~examples` |
| `^` | Priority | Focus on this | `^speed` `^quality` |
| `_` | Avoid | Don't do this | `_verbose` `_emoji` |
| `>` | Chain | Then do | `write > translate` |
| `&` | Parallel | And also | `title & summary` |
| `[x]` | Specifier | Details | `[python]` `[10]` |
| `{x}` | Variable | Placeholder | `{text}` `{code}` |
| `*` | Iterate | For each | `translate *[es,fr]` |
| `@as` | Persona | Act as | `@as "expert"` |

---

## Common Modifier Reference

### Output Style

| Modifier | Effect |
|----------|--------|
| `!short` / `!brief` / `!concise` | Keep it short |
| `!detailed` / `!comprehensive` | Include details |
| `!simple` | Easy to understand |
| `!technical` | Use technical terms |
| `!formal` | Formal tone |
| `!casual` | Conversational tone |
| `!professional` | Business appropriate |

### Format

| Modifier | Effect |
|----------|--------|
| `!bullets` | Bullet points |
| `!numbered` | Numbered list |
| `!headers` | Include sections |
| `!examples` | Include examples |
| `!bare` | Just the answer |

### Quality

| Modifier | Effect |
|----------|--------|
| `^quality` | Prioritize quality |
| `^fast` | Prioritize speed |
| `^creative` | Be creative |
| `^accurate` | Be precise |
| `^honest` | Be direct/truthful |
