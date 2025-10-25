---
name: ai-topic-extraction-prompts
description: Generate optimized prompts and evaluation frameworks for extracting topics from web content using LLMs. Use when building AI-powered topic classification systems with support for multiple LLM providers (Claude, OpenAI, Gemini, Grok, Groq). Includes baseline prompts, response schemas, provider-specific optimizations, and A/B testing methodology.
---

# AI Topic Extraction Prompts

## Overview

Generate production-ready prompts for extracting topics from scraped web content using LLMs. Supports multiple providers with optimizations for each, plus comprehensive evaluation and A/B testing frameworks.

## When to Use This Skill

Use when:
- Building topic classification for web content
- Need to extract topics from articles, documentation, blogs
- Want to compare different LLM providers for accuracy/cost/speed
- Building content curation or recommendation systems
- Need consistent topic extraction across large content datasets

Do not use when:
- Simple keyword extraction is sufficient (use regex/NLP instead)
- Topics are predefined (use classification, not extraction)
- Content is not text-based (images, videos need different approaches)

## Quick Start

The skill provides everything needed for topic extraction:

1. **Baseline Prompt** (`assets/baseline_prompt.txt`) - Works across all LLM providers
2. **Response Schema** (`assets/response_schema.json`) - JSON structure for validation
3. **Provider Optimizations** (`references/provider_optimizations.md`) - Provider-specific tweaks
4. **Evaluation Framework** (`references/evaluation_framework.md`) - A/B testing methodology

## Core Concepts

### Topic Extraction Goals

Extract 3-5 topics per content piece that are:
- **Specific enough** to be meaningful (not "technology", "programming")
- **General enough** to group content (not "react-18.2.0-useeffect-bug")
- **Consistent** across similar content (always "golang", never "go-lang")

### Confidence Scoring

Each topic includes a confidence score (0.0-1.0):
- **0.9-1.0**: Topic is central to the content
- **0.7-0.9**: Topic is clearly present and important
- **0.6-0.7**: Topic is mentioned significantly
- **< 0.6**: Don't include (too tangential)

### Response Format

```json
[
  {
    "name": "machine-learning",
    "display_name": "Machine Learning",
    "confidence": 0.95,
    "reasoning": "Article extensively discusses neural networks and ML algorithms"
  }
]
```

## Using the Baseline Prompt

### Step 1: Load the Prompt Template

Read `assets/baseline_prompt.txt` which includes:
- Clear task description
- Input format (title, URL, description, body)
- Output format (JSON schema)
- Guidelines for quality topics
- Example output

### Step 2: Fill Template Variables

Replace placeholders with actual content:

```python
with open('assets/baseline_prompt.txt', 'r') as f:
    prompt_template = f.read()

prompt = prompt_template.format(
    title=article.title,
    url=article.url,
    description=article.description or "",
    body=article.body
)
```

### Step 3: Call LLM

```python
response = llm_client.complete(prompt)
topics = json.loads(response.text)
```

### Step 4: Validate Response

Use `assets/response_schema.json` to validate:

```python
import jsonschema

with open('assets/response_schema.json', 'r') as f:
    schema = json.load(f)

jsonschema.validate(topics, schema)
```

## Provider-Specific Optimizations

### Choosing a Provider

See `references/provider_optimizations.md` for detailed comparison.

**Quick Guide:**
- **Highest Accuracy**: Claude (Sonnet/Opus)
- **Best Balance**: OpenAI (GPT-4-turbo) or Gemini (Pro)
- **Fastest**: Groq (Llama3)
- **Cheapest**: Groq or Gemini (Flash)

### Claude Optimization Example

Add XML tags and thinking process:

```
<content>
Title: {title}
Body: {body}
</content>

Before providing JSON, think through:
1. What are the main topics?
2. Which are specific enough?
3. Confidence for each?

Now provide JSON response:
```

### OpenAI Optimization Example

Use JSON mode for guaranteed valid JSON:

```python
response = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a topic extraction specialist. Always respond with valid JSON."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)
```

### Gemini Optimization Example

Use response_mime_type:

```python
generation_config = {
    "response_mime_type": "application/json",
    "temperature": 0.3
}

response = model.generate_content(
    prompt,
    generation_config=generation_config
)
```

## A/B Testing Different Providers

### Test Setup

1. **Create Test Dataset** (20-50 diverse articles):
   - Different domains (tech, sports, business)
   - Different lengths (short, medium, long)
   - Known topics (manually tagged ground truth)

2. **Run Extraction** with each provider:
```python
for article in test_dataset:
    topics_claude = extract_with_claude(article)
    topics_openai = extract_with_openai(article)
    topics_gemini = extract_with_gemini(article)

    results.append({
        'article': article,
        'claude': topics_claude,
        'openai': topics_openai,
        'gemini': topics_gemini,
        'ground_truth': article.known_topics
    })
```

3. **Calculate Metrics** (see `references/evaluation_framework.md`):
   - Precision: % of extracted topics that are correct
   - Recall: % of actual topics that were extracted
   - F1 Score: Harmonic mean of precision and recall

4. **Compare**:
```
| Provider | F1 Score | Cost/1K | p95 Latency |
|----------|----------|---------|-------------|
| Claude   | 0.92     | $1.50   | 800ms       |
| OpenAI   | 0.89     | $1.20   | 600ms       |
| Gemini   | 0.87     | $0.80   | 1200ms      |
```

### Decision Matrix

Based on your priorities:

**Accuracy Priority**: Use Claude (highest F1)
**Cost Priority**: Use Groq or Gemini Flash
**Speed Priority**: Use Groq
**Balance**: Use OpenAI GPT-4-turbo or Gemini Pro

Can also use **cascading approach**:
1. Try Groq (fast, cheap)
2. If confidence < 0.7, fall back to Claude (accuracy)
3. Use OpenAI for spot-checking quality

## Evaluation and Iteration

### Quality Metrics

From `references/evaluation_framework.md`:

1. **Relevance** (0-10): Do topics match content?
2. **Specificity**: Not too broad, not too narrow
3. **Consistency**: Same topics = same names
4. **Coverage**: All important topics extracted
5. **Precision**: No false positives

### Common Failure Patterns

**Pattern**: Too generic topics
**Example**: "programming", "technology", "software"
**Fix**: Add specificity guidelines to prompt, show examples

**Pattern**: Inconsistent naming
**Example**: "golang" vs "go" vs "go-language"
**Fix**: Add consistency rules, maintain topic dictionary

**Pattern**: Missing important topics
**Example**: Article about "React Hooks" only extracts "react"
**Fix**: Emphasize extracting subtopics, increase max topics to 5

### Continuous Improvement Loop

1. Deploy extraction in production
2. Collect edge cases where it failed
3. Add to test dataset
4. Update prompts to handle new patterns
5. Re-test on full dataset (ensure no regression)
6. Deploy improved version

## Integration Example

### Complete Workflow

```python
import json
import jsonschema

# Load resources
with open('assets/baseline_prompt.txt') as f:
    prompt_template = f.read()

with open('assets/response_schema.json') as f:
    schema = json.load(f)

def extract_topics(content, provider='claude'):
    """Extract topics from content using specified provider"""

    # Fill prompt
    prompt = prompt_template.format(
        title=content.title,
        url=content.url,
        description=content.description or "",
        body=content.body
    )

    # Call LLM (provider-specific)
    if provider == 'claude':
        response = claude_client.complete(prompt, temperature=0.3)
    elif provider == 'openai':
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
    # ... other providers

    # Parse response
    topics = json.loads(response.text)

    # Validate
    jsonschema.validate(topics, schema)

    # Filter by confidence
    topics = [t for t in topics if t['confidence'] >= 0.6]

    return topics

# Use it
content = fetch_scraped_content()
topics = extract_topics(content, provider='claude')

# Store in database
for topic in topics:
    store_topic(
        name=topic['name'],
        display_name=topic['display_name'],
        content_id=content.id,
        confidence=topic['confidence']
    )
```

## Testing Prompts

### Unit Test Example

```python
def test_topic_extraction():
    content = {
        'title': 'Introduction to React Hooks',
        'url': 'https://example.com/react-hooks',
        'description': 'Learn about useState and useEffect',
        'body': 'React Hooks are a new feature in React 16.8...'
    }

    topics = extract_topics(content)

    # Assert we got topics
    assert len(topics) > 0
    assert len(topics) <= 5

    # Assert quality
    topic_names = [t['name'] for t in topics]
    assert 'react' in topic_names
    assert 'hooks' in topic_names or 'react-hooks' in topic_names

    # Assert confidence
    for topic in topics:
        assert topic['confidence'] >= 0.6
        assert topic['confidence'] <= 1.0

    # Assert reasoning
    for topic in topics:
        assert len(topic['reasoning']) > 10
```

### Integration Test

```python
def test_ab_comparison():
    """Compare Claude vs OpenAI on same content"""

    test_articles = load_test_dataset()

    results = []
    for article in test_articles:
        claude_topics = extract_topics(article, 'claude')
        openai_topics = extract_topics(article, 'openai')

        results.append({
            'article_id': article.id,
            'claude_count': len(claude_topics),
            'openai_count': len(openai_topics),
            'claude_f1': calculate_f1(claude_topics, article.ground_truth),
            'openai_f1': calculate_f1(openai_topics, article.ground_truth)
        })

    # Aggregate
    claude_avg_f1 = mean([r['claude_f1'] for r in results])
    openai_avg_f1 = mean([r['openai_f1'] for r in results])

    print(f"Claude F1: {claude_avg_f1:.3f}")
    print(f"OpenAI F1: {openai_avg_f1:.3f}")
```

## Resources

### assets/

- **baseline_prompt.txt** - Universal prompt template that works across all LLM providers
- **response_schema.json** - JSON schema for validating LLM responses

### references/

- **evaluation_framework.md** - Comprehensive guide to measuring topic extraction quality, A/B testing methodology, and continuous improvement
- **provider_optimizations.md** - Provider-specific optimizations for Claude, OpenAI, Gemini, Grok, and Groq with comparison matrix

## Best Practices

1. **Start with baseline prompt** - Works well across all providers
2. **Measure first** - Run A/B tests before optimizing
3. **Track metrics** - F1 score, cost, latency for each provider
4. **Iterate on prompts** - Use evaluation framework to improve
5. **Version prompts** - Track changes and their impact on F1 scores
6. **Filter by confidence** - Only use topics with confidence >= 0.6
7. **Validate JSON** - Always validate against schema
8. **Handle errors gracefully** - LLMs sometimes return malformed JSON

## Common Pitfalls

**Pitfall 1**: Using high temperature
- **Problem**: Inconsistent results, varying topic names
- **Solution**: Use temperature 0.2-0.3 for topic extraction

**Pitfall 2**: Not validating JSON
- **Problem**: Crashes when LLM returns invalid JSON
- **Solution**: Always validate with schema, have fallback parsing

**Pitfall 3**: Extracting too many topics
- **Problem**: Generic, low-confidence topics pollute dataset
- **Solution**: Limit to 5 topics, require confidence >= 0.6

**Pitfall 4**: Inconsistent topic names
- **Problem**: "golang" vs "go" causes fragmentation
- **Solution**: Maintain topic dictionary, normalize names post-extraction

**Pitfall 5**: Not measuring accuracy
- **Problem**: Don't know if prompts/providers are working well
- **Solution**: Create test dataset, calculate F1 scores, iterate

## Next Steps

After topic extraction:
1. **Deduplicate topics** - Normalize similar topic names
2. **Build topic graph** - Discover parent/child relationships
3. **Score topics** - Weight by content count, recency, engagement
4. **Cache topic collections** - For fast portal serving

These will be covered in subsequent skills (Graph Scoring Builder, Portal Cache Manager).
