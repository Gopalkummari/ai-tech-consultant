# AI PROMPT LOG & INSIGHTS
**Project**: AI Tech Consultant Capstone Suite  
**Tools Evaluated**: Claude Code, Cursor, Anthropic API  

---

## The 5 Most Useful Prompts

### Prompt 1: Polite Resumable Sitemap Ingestion with Checkpointing
> *"Implement an asynchronous, polite XML sitemap crawler for a public help center with 1,500+ URLs. Enforce a 1.0s delay between requests, batch articles in groups of 5, and persist a disk-backed checkpoint JSON file after every batch so the scraping session can be stopped at any moment and resumed without re-fetching completed URLs."*  
*Why it was effective*: Prevented server rate-limiting and IP bans, and made long-running ingestion resilient to network hiccups.

### Prompt 2: Multimodal Screenshot Understanding for UI Navigation
> *"When extracting help center articles with `<img src=...>`, write a vision analysis synthesizer that inspects the article title, breadcrumb category, and image alt-text to generate a structured `vision_description`. Describe exactly what admin UI settings, toggle switches, and form inputs are visible in the screenshot so that RAG queries can cite visual proof."*  
*Why it was effective*: Turned visual screenshots into searchable knowledge tokens, resolving questions where the answer was in an image rather than text.

### Prompt 3: Native Setting vs. Custom Code Capability Classifier
> *"Act as a Principal Solutions Architect for Brilliant Directories. Create a capability checker that evaluates client feature requests against our knowledge base. Classify each feature into one of three buckets: NATIVE_SETTING ($0, 0.5h), STANDARD_CUSTOMIZATION (Form/Widget override, 2-4h), or COMPLEX_CUSTOM_DEV (15-40h). Calculate the exact dollar savings for the client when a feature can be solved with a built-in setting."*  
*Why it was effective*: Directly automated the core value proposition of an AI Tech Consultant—saving clients thousands of dollars by identifying native toggles.

### Prompt 4: Self-Improving Diff Learner from Human Edits
> *"When a human supervisor edits an AI-generated customer email draft, compare the original text and edited text using string delta diffing. Extract the stylistic or procedural rule (e.g. 'Always state 5-10 business days for Stripe refunds') and persist it into an active `learned_rules.json` file so subsequent drafts inherit the correction."*  
*Why it was effective*: Created an autonomous feedback loop where the agent improves with every email sent without retraining weights.

### Prompt 5: Two-Meeting Scope-Diff & Change Order Pricing
> *"Build a scope-diffing agent that compares an initial discovery meeting transcript against a follow-up revision meeting transcript. Itemize: (1) Added scope items with hours/cost, (2) Dropped scope items with hours/cost saved, and (3) Modified scope items with net deltas. Format the output as an executive change-order table."*  
*Why it was effective*: Automated the most tedious consulting task—tracking scope creep and proving financial/timeline impacts to client stakeholders.

---

## Key Insight from Using AI Coding Assistants
> **"Constrain the facts, liberate the formatting."**  
> When prompting AI to act as a technical consultant, leaving factual retrieval open-ended results in plausible-sounding hallucinations (e.g., inventing fake setting names). However, when the prompt strictly binds the model to an authoritative knowledge base (Task 1's API) and gives it freedom only over tone, formatting, and mathematical diffing, the output reaches production-grade reliability with zero hallucinations.
