# Topic Extraction Evaluation Framework

## Quality Metrics

### 1. Relevance (Most Important)
**Definition**: How well do extracted topics match the actual content?

**Measurement**:
- Manual review: Do extracted topics accurately represent the content?
- Score: 0-10 (10 = perfect match, 0 = completely irrelevant)

**Examples**:
- ✅ Good: Article about React hooks → extracts "react", "hooks", "javascript"
- ❌ Bad: Article about React hooks → extracts "programming", "web", "software"

### 2. Specificity
**Definition**: Are topics at the right level of granularity?

**Measurement**:
- Too broad: "technology", "programming", "science"
- Too narrow: "react-18.2.0-useeffect-cleanup-bug"
- Just right: "react", "hooks", "frontend"

**Guidelines**:
- Prefer specific over generic (good: "machine-learning", bad: "ai")
- But not too specific (good: "react", bad: "react-18-hooks")
- Think: "Would I want to browse a portal for this topic?"

### 3. Consistency
**Definition**: Are topic names consistent across similar content?

**Measurement**:
- Same topic, same name: "golang" not "go-lang" or "go-programming"
- Use established terminology: "machine-learning" not "ml" or "ai-learning"
- Plural vs singular: Be consistent (prefer singular: "algorithm" not "algorithms")

**Common Inconsistencies to Avoid**:
- Language names: "golang" vs "go" vs "go-lang" → Pick one!
- Framework names: "react-js" vs "reactjs" vs "react" → "react"
- Abbreviations: "ml" vs "machine-learning" → Spell it out

### 4. Coverage
**Definition**: Did we extract all important topics without missing key ones?

**Measurement**:
- Are major topics from the content represented?
- No more than 5 topics (focus on most important)
- Confidence >= 0.6 for all extracted topics

### 5. Precision
**Definition**: Are all extracted topics actually relevant (no false positives)?

**Measurement**:
- Review each topic: Is this truly a main topic of the content?
- Avoid tangential topics (mentioned once in passing)
- Avoid generic topics that apply to everything

## A/B Testing Methodology

### Setup
Compare two prompts/providers on the same content set:

```
Content → Prompt A → Topics A
Content → Prompt B → Topics B
       ↓
    Human Review → Which is better?
```

### Test Dataset
Create a diverse set of 20-50 articles covering:
- Different domains (tech, sports, finance, etc.)
- Different content types (news, tutorials, documentation)
- Different lengths (short vs long articles)
- Known topics (you manually tagged them)

### Comparison Metrics

**Quantitative**:
- Precision: % of extracted topics that are correct
- Recall: % of actual topics that were extracted
- F1 Score: Harmonic mean of precision and recall
- Average confidence scores

**Qualitative**:
- Topic quality (specific enough? too broad?)
- Consistency (same topic names for similar content?)
- Usefulness (would you use these topics in your portal?)

### Testing Procedure

1. **Run extraction** on test dataset with both configurations
2. **Manual review**: For each article, mark topics as:
   - ✅ Correct and useful
   - ⚠️ Correct but too broad/narrow
   - ❌ Incorrect or irrelevant
3. **Calculate metrics**: Precision, recall, F1
4. **Compare**: Which configuration performed better?
5. **Iterate**: Adjust prompts and re-test

### Provider Comparison

When comparing Claude vs OpenAI vs Gemini:

**Track**:
- Accuracy (F1 score)
- Cost per 1000 requests
- Latency (p50, p95, p99)
- Consistency (same input → same output?)
- Error rate

**Example Results Table**:
| Provider | F1 Score | Cost/1K | p95 Latency | Errors |
|----------|----------|---------|-------------|--------|
| Claude   | 0.92     | $1.50   | 800ms       | 0.1%   |
| OpenAI   | 0.89     | $1.20   | 600ms       | 0.3%   |
| Gemini   | 0.87     | $0.80   | 1200ms      | 0.5%   |

**Decision Criteria**:
- If accuracy is critical → Choose highest F1
- If cost matters → Balance F1 with cost
- If latency matters → Balance F1 with latency
- Consider using fastest for real-time, most accurate for batch

## Example Test Cases

### Test Case 1: React Tutorial
**Content**: "Learn React Hooks: useEffect, useState, and Custom Hooks"

**Expected Topics**:
- react (confidence: 0.95)
- hooks (confidence: 0.90)
- javascript (confidence: 0.75)

**Good Extraction**:
```json
[
  {"name": "react", "confidence": 0.95, "reasoning": "Tutorial specifically about React framework"},
  {"name": "hooks", "confidence": 0.92, "reasoning": "All examples focus on React Hooks API"},
  {"name": "javascript", "confidence": 0.80, "reasoning": "Code examples in JavaScript"}
]
```

**Bad Extraction**:
```json
[
  {"name": "programming", "confidence": 0.90, "reasoning": "Article about programming"},
  {"name": "web-development", "confidence": 0.85, "reasoning": "Web development tutorial"},
  {"name": "frontend", "confidence": 0.80, "reasoning": "Frontend framework"}
]
```
*Too generic - doesn't capture the specific React/Hooks focus*

### Test Case 2: Machine Learning Research
**Content**: "Deep Learning for Computer Vision: CNNs and Transfer Learning in PyTorch"

**Expected Topics**:
- machine-learning (confidence: 0.95)
- computer-vision (confidence: 0.95)
- pytorch (confidence: 0.90)
- deep-learning (confidence: 0.85)

**Edge Case**: Should we extract both "machine-learning" and "deep-learning"?
- Yes, if deep learning is specifically discussed (not just mentioned)
- No, if article is general ML (pick the more specific one)

### Test Case 3: Business Article
**Content**: "How Startups Use Agile Methodology to Build Products Faster"

**Expected Topics**:
- startups (confidence: 0.90)
- agile (confidence: 0.90)
- product-management (confidence: 0.75)

**Common Mistakes**:
- Extracting "software" (too generic)
- Extracting "scrum" if not specifically discussed (agile is better)
- Extracting "business" (too generic, everything is business)

## Continuous Improvement

### Feedback Loop
1. **Deploy** topic extraction in production
2. **Collect** edge cases where extraction failed
3. **Analyze** patterns in failures
4. **Update** prompts to handle new patterns
5. **Re-test** on test dataset to ensure no regression
6. **Deploy** improved version

### Common Failure Patterns

**Pattern 1**: Content in non-English
- Solution: Add language detection, use multilingual models

**Pattern 2**: Very short content (tweets, headlines)
- Solution: Adjust confidence thresholds, require minimum content length

**Pattern 3**: Multi-topic content (tutorial covering 5 technologies)
- Solution: Allow more topics, but prioritize by content emphasis

**Pattern 4**: Niche/specialized topics not well-known
- Solution: Add domain-specific topic dictionaries, or allow custom topics

### Version Control

Track prompt versions:
```
v1.0 (2025-01-15): Baseline prompt
v1.1 (2025-01-20): Added specificity guidelines, improved examples
v1.2 (2025-01-25): Provider-specific optimizations for Claude
v2.0 (2025-02-01): Restructured for better JSON compliance
```

For each version, track:
- F1 score on test dataset
- Common failure modes
- Changes made
- Why those changes improved (or didn't improve) results
