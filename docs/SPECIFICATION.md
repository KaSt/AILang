# AILANG - AI Communication Language

> **Write less. Mean more. Get exactly what you want.**

## Two Ways to Talk to AI

AILANG provides two complementary interfaces:

### 1. Output Contracts (Recommended for most users)

Speak naturally, get structured data back:

```python
result = ai.ask(
    "explain how git rebase works",
    returns={
        "tldr": str_(max=50),
        "steps": list_(str_()),
        "warning": optional(str_()),
    }
)
print(result.tldr)   # Guaranteed ≤50 chars
print(result.steps)  # Guaranteed list of strings
```

### 2. AILANG Syntax (Power users & automation)

Terse, composable commands:

```
img "penguin drinking cola" !photo ^cinematic
code "sort" [python] !typed ^fast
analyze {code} > fix !all > test[unit]
```

---

## Why AILANG?

Prompting is hard. You write paragraphs, add "please", explain what you don't want, and still get the wrong output. AILANG fixes this:

```
Human way:  "Can you please generate an image of a penguin drinking cola? 
            Make it photorealistic, high quality, maybe cinematic lighting?"

AILANG:     img "penguin drinking cola" !photo ^cinematic
```

That's it. Shorter, clearer, better results.

---

## Quick Start (Learn in 2 Minutes)

### The Basics

Every AILANG command follows this pattern:

```
ACTION "subject" modifiers
```

**Actions** = what you want (write, img, code, fix, explain...)
**Subject** = what it's about
**Modifiers** = how you want it

### Essential Modifiers

| Symbol | Meaning | Example |
|--------|---------|---------|
| `!` | must have | `!short` = must be short |
| `~` | nice to have | `~funny` = be funny if possible |
| `^` | prioritize this | `^speed` = prioritize speed |
| `_` | avoid this | `_emoji` = no emojis |
| `>` | then do | `write > translate[fr]` |
| `&` | and also | `title & summary` |
| `[x]` | specify | `[python]` `[formal]` `[3]` |

### Your First Commands

```ailang
write "birthday message for mom" !warm ~funny

img "sunset over mountains" !photo ^golden_hour

explain "quantum computing" [simple] !examples

code "sort algorithm" [python] !fast ^readable
```

---

## Complete Dictionary

### 📝 TEXT & WRITING

| Command | What it does |
|---------|--------------|
| `write` | Create any text |
| `rewrite` | Improve existing text |
| `summarize` | Make shorter |
| `expand` | Make longer/detailed |
| `translate` | Change language |
| `explain` | Break down concept |
| `list` | Generate bullet points |
| `compare` | Show differences |
| `reply` | Respond to something |
| `title` | Generate headlines |

**Examples:**

```ailang
// Write a professional email
write "job application for Google" [email] !professional ^concise

// Human equivalent: "Write me a professional and concise email 
// for a job application at Google. Keep it short but impactful."

// Summarize for a 5-year-old  
summarize {article} [eli5] !simple

// Human equivalent: "Can you summarize this article in a way 
// that a 5-year-old would understand? Use simple words."

// Translate and keep the tone
translate "Let's grab coffee!" [spanish] !keep_tone

// Human equivalent: "Translate 'Let's grab coffee!' to Spanish 
// but make sure it sounds natural and keeps the casual tone."

// Rewrite for Twitter
rewrite {paragraph} [tweet] !under_280 ^punchy

// Human equivalent: "Rewrite this paragraph as a tweet. 
// It must be under 280 characters and make it punchy/engaging."

// Compare two things
compare "React" "Vue" [table] !pros_cons

// Human equivalent: "Compare React and Vue. Show me a table 
// with the pros and cons of each."
```

---

### 🎨 IMAGES & VISUALS

| Command | What it does |
|---------|--------------|
| `img` | Generate image |
| `edit_img` | Modify image |
| `describe_img` | Explain what's in image |
| `style` | Apply artistic style |
| `logo` | Create logo |
| `icon` | Create icon |
| `diagram` | Create diagram |
| `mockup` | Create UI mockup |

**Style Modifiers:**

| Modifier | Style |
|----------|-------|
| `!photo` | Photorealistic |
| `!art` | Artistic/painted |
| `!3d` | 3D rendered |
| `!pixel` | Pixel art |
| `!sketch` | Hand-drawn |
| `!minimal` | Minimalist |
| `!anime` | Anime style |
| `!vintage` | Retro/vintage |

**Examples:**

```ailang
// Penguin drinking cola - photorealistic
img "penguin drinking cola" !photo ^cinematic _text

// Human equivalent: "Generate a photorealistic image of a penguin 
// drinking cola with cinematic lighting. Don't include any text in the image."

// Logo for a coffee shop
logo "mountain coffee shop" !minimal [earth_tones] ^memorable

// Human equivalent: "Design a minimal, memorable logo for a coffee 
// shop called Mountain Coffee. Use earth tones."

// Album cover art
img "astronaut playing guitar on moon" !art [synthwave] ^vibrant

// Human equivalent: "Create an artistic image of an astronaut 
// playing guitar on the moon. Synthwave style, vibrant colors."

// App icon
icon "meditation app" !minimal [purple,white] !rounded

// Human equivalent: "Create a minimal app icon for a meditation app. 
// Use purple and white colors. Make it rounded/iOS style."

// Architecture diagram
diagram "microservices e-commerce" [flowchart] !clear ^labeled

// Human equivalent: "Create a flowchart diagram showing microservices 
// architecture for an e-commerce system. Make it clear with labels."
```

---

### 💻 CODE & DEVELOPMENT

| Command | What it does |
|---------|--------------|
| `code` | Write code |
| `fix` | Debug/repair code |
| `refactor` | Improve code structure |
| `test` | Generate tests |
| `review` | Analyze code quality |
| `convert` | Change language |
| `api` | Design API |
| `query` | Write database query |
| `regex` | Create regex pattern |
| `docs` | Generate documentation |

**Quality Modifiers:**

| Modifier | Meaning |
|----------|---------|
| `!typed` | Include types |
| `!tested` | Include tests |
| `!commented` | Add comments |
| `!dry` | No repetition |
| `^fast` | Optimize for speed |
| `^readable` | Optimize for clarity |
| `^memory` | Optimize for memory |
| `_deps` | No external dependencies |

**Examples:**

```ailang
// Function to validate email
code "email validator" [typescript] !typed !tested ^readable

// Human equivalent: "Write a TypeScript function to validate email 
// addresses. Include type annotations, unit tests, and prioritize 
// code readability."

// Fix buggy code
fix {broken_code} !explain

// Human equivalent: "This code has a bug. Fix it and explain 
// what was wrong."

// Convert Python to Rust
convert {py_code} [rust] ^performance !safe

// Human equivalent: "Convert this Python code to Rust. 
// Optimize for performance and make it memory-safe."

// API design
api "todo app" [rest] !crud [openapi]

// Human equivalent: "Design a REST API for a todo app with all 
// CRUD operations. Give me the OpenAPI specification."

// SQL query
query "users who bought > 3 items last month" [postgres] ^optimized

// Human equivalent: "Write an optimized PostgreSQL query to find 
// all users who bought more than 3 items in the last month."

// Generate regex
regex "valid phone number" [us] !explained

// Human equivalent: "Give me a regex pattern for valid US phone 
// numbers and explain how it works."
```

---

### 🔍 ANALYSIS & REASONING

| Command | What it does |
|---------|--------------|
| `analyze` | Deep examination |
| `evaluate` | Judge quality |
| `predict` | Forecast outcome |
| `diagnose` | Find problems |
| `recommend` | Suggest options |
| `rank` | Order by criteria |
| `verify` | Check accuracy |
| `extract` | Pull out info |
| `classify` | Categorize |
| `sentiment` | Detect emotion |

**Examples:**

```ailang
// Analyze a business idea
analyze "subscription socks startup" [market] !swot ^honest

// Human equivalent: "Analyze this business idea: a subscription 
// service for socks. Do a SWOT analysis focused on market viability. 
// Be honest, don't sugarcoat it."

// Recommend a tech stack
recommend "social media app" [tech_stack] !2024 ^scalable

// Human equivalent: "Recommend a tech stack for building a 
// social media app in 2024. Focus on scalability."

// Extract action items from meeting notes
extract {meeting_notes} [action_items] > assign[person] !deadlines

// Human equivalent: "Go through these meeting notes, extract all 
// action items, assign them to the relevant people mentioned, 
// and include deadlines."

// Sentiment analysis
sentiment {reviews} > summarize [trends]

// Human equivalent: "Analyze the sentiment of these reviews, 
// then summarize the main trends you see."
```

---

### 🎯 CREATIVE & IDEAS

| Command | What it does |
|---------|--------------|
| `brainstorm` | Generate ideas |
| `name` | Create names |
| `story` | Write narrative |
| `joke` | Create humor |
| `poem` | Write poetry |
| `script` | Write dialogue |
| `pitch` | Create pitch |
| `slogan` | Write tagline |
| `recipe` | Food instructions |
| `playlist` | Music suggestions |

**Examples:**

```ailang
// Startup names
name "ai writing assistant" [5] !available ^memorable _generic

// Human equivalent: "Give me 5 memorable name ideas for an AI 
// writing assistant startup. Check if domains might be available. 
// Avoid generic names."

// Children's story
story "brave little robot" [kids_5] !moral ^illustrated_style

// Human equivalent: "Write a children's story about a brave little 
// robot for 5-year-olds. Include a moral lesson. Write it in a style 
// that would work well with illustrations."

// Product pitch
pitch {product_desc} [investor] !60sec ^problem_solution

// Human equivalent: "Create a 60-second investor pitch for this 
// product. Focus on the problem-solution narrative."

// Recipe creation
recipe "healthy pasta" !under_30min [vegetarian] ^meal_prep

// Human equivalent: "Give me a healthy vegetarian pasta recipe 
// that takes under 30 minutes and works well for meal prep."

// Dad joke
joke "programming" !clean ^groan_worthy

// Human equivalent: "Tell me a clean programming joke. 
// The more groan-worthy the better."
```

---

### 🔧 DATA & TRANSFORMATION

| Command | What it does |
|---------|--------------|
| `format` | Change structure |
| `merge` | Combine inputs |
| `split` | Divide content |
| `filter` | Select subset |
| `sort` | Order items |
| `dedupe` | Remove duplicates |
| `validate` | Check correctness |
| `map` | Transform each item |
| `template` | Apply pattern |
| `parse` | Extract structure |

**Examples:**

```ailang
// Convert JSON to CSV
format {json_data} [csv] !headers

// Human equivalent: "Convert this JSON data to CSV format. 
// Include headers."

// Clean up a messy list
dedupe {list} > sort[alpha] > format[numbered]

// Human equivalent: "Take this list, remove duplicates, sort 
// alphabetically, then number each item."

// Parse resume into structured data
parse {resume_text} [json] !{name,email,skills,experience}

// Human equivalent: "Parse this resume text and extract it 
// into JSON with name, email, skills, and experience fields."
```

---

### 🌐 PERSONAS & CONTEXT

Set a context for multiple commands:

```ailang
@as "senior python developer" {
  review {code}
  suggest "improvements"
}

// Human equivalent: "Act as a senior Python developer. 
// First review this code, then suggest improvements."

@as "5 year old" {
  explain "black holes"
}

// Human equivalent: "Explain black holes as if you were a 5 year old."

@as "harsh critic" {
  evaluate {essay} !detailed
}

// Human equivalent: "Be a harsh critic. Evaluate this essay in detail. 
// Don't hold back."
```

---

## Chaining Power

Chain commands for complex workflows:

```ailang
// Research → Summarize → Tweet thread
research "AI trends 2024" > summarize[key_points] > write[tweet_thread][5]

// Human equivalent: "Research AI trends for 2024, then summarize 
// the key points, then turn that into a Twitter thread of 5 tweets."

// Analyze → Fix → Test → Document
analyze {code} > fix !all > test[unit] > docs[readme]

// Human equivalent: "Analyze this code for issues, fix all problems, 
// generate unit tests for it, then create README documentation."

// Generate → Translate → Format for multiple languages
write "welcome message" > translate *[es,fr,de,jp] > format[json]

// Human equivalent: "Write a welcome message, translate it to 
// Spanish, French, German, and Japanese, then format all of 
// them as JSON."
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    AILANG CHEAT SHEET                       │
├─────────────────────────────────────────────────────────────┤
│  STRUCTURE:   action "subject" [spec] modifiers             │
│                                                             │
│  MODIFIERS:   !must  ~maybe  ^priority  _avoid              │
│                                                             │
│  CHAINS:      action1 > action2 > action3                   │
│                                                             │
│  PARALLEL:    output1 & output2 & output3                   │
│                                                             │
│  ITERATE:     *[item1, item2, item3]                        │
│                                                             │
│  CONTEXT:     @as "persona" { commands }                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  COMMON COMMANDS                                            │
│  write  img    code   explain  summarize  translate         │
│  fix    analyze  list   compare  recommend  convert         │
├─────────────────────────────────────────────────────────────┤
│  COMMON MODIFIERS                                           │
│  !short  !detailed  !simple  !formal  !casual  !examples    │
│  ^fast   ^quality   ^creative   _verbose   _technical       │
└─────────────────────────────────────────────────────────────┘
```

---

## Transpiler: AILANG ↔ Human

### AILANG → Human Prompt

```
INPUT:  img "cat astronaut" !photo ^cinematic [4k] _text

OUTPUT: Generate a photorealistic image of a cat dressed as an 
        astronaut. Use cinematic lighting and composition. 
        Resolution should be 4K. Do not include any text or 
        words in the image.
```

### Human Prompt → AILANG

```
INPUT:  I need you to write a professional LinkedIn post about 
        my promotion to Senior Engineer. Keep it humble but 
        confident. Not too long. Maybe include some gratitude 
        for my team.

OUTPUT: write "linkedin promotion to Senior Engineer" [linkedin] 
        !professional !humble ~gratitude ^concise _bragging
```

### Conversion Rules

| AILANG | Human Phrase |
|--------|--------------|
| `!x` | "must be x" / "make sure it's x" |
| `~x` | "maybe x" / "if possible, x" |
| `^x` | "focus on x" / "prioritize x" |
| `_x` | "don't x" / "avoid x" / "no x" |
| `[x]` | "in x format" / "x style" / "use x" |
| `>` | "then" / "after that" |
| `&` | "and also" / "plus" |
| `*[a,b,c]` | "for each of: a, b, c" |
| `@as "x"` | "act as x" / "you are x" |

---

## Real-World Examples

### Job Hunting

```ailang
// Tailor resume for a job
rewrite {resume} @match {job_posting} ^keywords !honest

// Prep for interview  
list "questions for {company} {role} interview" [15] > answer *

// Follow-up email
write "interview follow-up" [email] !grateful ^specific _desperate
```

### Content Creation

```ailang
// YouTube video script
script "how to make sourdough" [youtube][10min] !hook ^retention _boring

// Blog post with SEO
write "remote work productivity" [blog][2000words] ^seo !headers !cta

// Instagram carousel
write "home workout tips" [carousel][10slides] !punchy ^visual_hooks
```

### Business

```ailang
// Meeting summary
summarize {transcript} > extract[decisions & action_items] > format[email]

// Competitive analysis
analyze {competitor} vs {our_product} [table] !strengths !weaknesses ^honest

// Customer email response
reply {angry_email} !empathetic ^solution _defensive [professional]
```

### Learning

```ailang
// Explain complex topic progressively
explain "machine learning" [levels: eli5 > beginner > intermediate > advanced]

// Create study flashcards
extract {textbook_chapter} [flashcards][20] !key_concepts ^exam_likely

// Practice problems
generate "calculus derivatives" [problems][10] !varied ^solutions_hidden
```

### Personal

```ailang
// Trip planning
plan "weekend in Tokyo" [itinerary] !budget_friendly ^local_gems _tourist_traps

// Gift ideas
brainstorm "gift for dad who likes fishing" [10] ^unique !under_100

// Difficult conversation
script "asking for a raise" [talking_points] !confident ^data_driven _apologetic
```

---

## Why People Love AILANG

| Pain Point | AILANG Solution |
|------------|-----------------|
| "AI gives me walls of text" | `!concise` or `!short` |
| "Output format is random" | `[json]` `[table]` `[bullets]` |
| "I forget to specify things" | Modifiers catch everything |
| "Complex prompts are hard" | Chain with `>` |
| "Same prompt, different results" | Structured = consistent |
| "Prompt engineering is a skill" | AILANG is just vocabulary |

---

## Philosophy

1. **Commands, not requests** - You're instructing, not asking
2. **Explicit, not implied** - Say exactly what you want
3. **Composable** - Small pieces that combine
4. **Readable** - Anyone can understand it
5. **Efficient** - Fewer tokens, same meaning

---

## What's Next

- [ ] Web-based AILANG ↔ Human translator
- [ ] Browser extension for any AI chat
- [ ] VS Code extension
- [ ] Fine-tuned models that understand AILANG natively
- [ ] Community command library

---

*AILANG v0.2 - Stop prompting. Start commanding.*
