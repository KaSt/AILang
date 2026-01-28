"""
AILANG Examples - Real-world use cases.
"""

from ailang import transpile

# =============================================================================
# CONTENT CREATION
# =============================================================================

print("=== Content Creation ===\n")

content_examples = [
    # Blog post
    ('write "remote work productivity tips" [blog][2000words] !headers !actionable ^seo', 
     "SEO-optimized blog post"),
    
    # Social media
    ('write "product launch announcement" [tweet_thread][5] !engaging ^hooks _sales_pitch',
     "Twitter thread"),
    
    # Video script
    ('script "how to make sourdough" [youtube][10min] !hook ^retention !timestamps',
     "YouTube script"),
    
    # Newsletter
    ('write "weekly tech digest" [newsletter] !scannable ^value _fluff',
     "Newsletter"),
]

for cmd, desc in content_examples:
    print(f"{desc}:")
    print(f"  AILANG: {cmd}")
    print(f"  Prompt: {transpile(cmd)[:100]}...")
    print()

# =============================================================================
# SOFTWARE DEVELOPMENT
# =============================================================================

print("=== Software Development ===\n")

dev_examples = [
    # Code generation
    ('code "REST API for user management" [fastapi] !typed !validated ^security',
     "API code"),
    
    # Code review
    ('@as "senior engineer" { review {pull_request} !security !performance ^bugs _style }',
     "Code review"),
    
    # Documentation
    ('docs {codebase} [readme] !quickstart !examples ^installation',
     "README generation"),
    
    # Testing
    ('test {function} [pytest] !edge_cases !mocks ^coverage',
     "Test generation"),
    
    # Debugging
    ('diagnose {error_log} > fix !root_cause ^explained',
     "Debug assistance"),
]

for cmd, desc in dev_examples:
    print(f"{desc}:")
    print(f"  AILANG: {cmd}")
    print(f"  Prompt: {transpile(cmd)[:100]}...")
    print()

# =============================================================================
# BUSINESS & MARKETING
# =============================================================================

print("=== Business & Marketing ===\n")

business_examples = [
    # Competitive analysis
    ('compare {our_product} {competitor} [table] !features !pricing ^honest _biased',
     "Competitive analysis"),
    
    # Email campaigns
    ('write "abandoned cart recovery" [email] !personalized ^urgency _spam',
     "Marketing email"),
    
    # Pitch deck
    ('pitch {startup_idea} [investor][5slides] !problem_solution ^traction !metrics',
     "Investor pitch"),
    
    # Customer support
    ('reply {angry_customer_email} !empathetic ^solution !professional _defensive',
     "Support response"),
]

for cmd, desc in business_examples:
    print(f"{desc}:")
    print(f"  AILANG: {cmd}")
    print(f"  Prompt: {transpile(cmd)[:100]}...")
    print()

# =============================================================================
# CREATIVE & DESIGN
# =============================================================================

print("=== Creative & Design ===\n")

creative_examples = [
    # Image generation
    ('img "cyberpunk tokyo street at night" !photo [neon] ^detailed _people',
     "Image prompt"),
    
    # Logo design
    ('logo "sustainable fashion brand" !minimal [earth_tones] ^memorable _complex',
     "Logo brief"),
    
    # Naming
    ('name "AI writing assistant" [5] !available ^memorable _generic _techy',
     "Product naming"),
    
    # Story
    ('story "robot learns to love" [short][2000words] !twist ^emotional',
     "Short story"),
]

for cmd, desc in creative_examples:
    print(f"{desc}:")
    print(f"  AILANG: {cmd}")
    print(f"  Prompt: {transpile(cmd)[:100]}...")
    print()

# =============================================================================
# DATA & ANALYSIS
# =============================================================================

print("=== Data & Analysis ===\n")

data_examples = [
    # Data transformation
    ('parse {csv_data} [json] !typed > validate !schema',
     "Data transformation"),
    
    # Summarization
    ('summarize {meeting_transcript} > extract[action_items] > format[email]',
     "Meeting summary"),
    
    # Research
    ('research "AI trends 2024" > summarize[key_points] > write[report]',
     "Research report"),
    
    # Sentiment analysis
    ('sentiment {customer_reviews} > classify[positive,negative,neutral] > summarize[trends]',
     "Sentiment analysis"),
]

for cmd, desc in data_examples:
    print(f"{desc}:")
    print(f"  AILANG: {cmd}")
    print(f"  Prompt: {transpile(cmd)[:100]}...")
    print()

# =============================================================================
# PERSONAL PRODUCTIVITY
# =============================================================================

print("=== Personal Productivity ===\n")

personal_examples = [
    # Trip planning
    ('plan "weekend in Paris" [itinerary] !budget_friendly ^local_gems _tourist_traps',
     "Trip itinerary"),
    
    # Learning
    ('explain "machine learning" [levels: eli5 > beginner > advanced] !examples',
     "Progressive learning"),
    
    # Decision making
    ('compare "buy vs rent apartment" [pros_cons] !financial ^long_term',
     "Decision analysis"),
    
    # Health
    ('recipe "high protein breakfast" !under_15min [vegetarian] ^meal_prep',
     "Recipe creation"),
]

for cmd, desc in personal_examples:
    print(f"{desc}:")
    print(f"  AILANG: {cmd}")
    print(f"  Prompt: {transpile(cmd)[:100]}...")
    print()
