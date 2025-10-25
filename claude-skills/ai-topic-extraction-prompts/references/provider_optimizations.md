# Provider-Specific Optimizations

Guidelines for adapting the baseline prompt to different LLM providers for optimal topic extraction performance.

## Claude (Anthropic)

### Strengths
- Excellent at following structured instructions
- Strong JSON formatting compliance
- Good at nuanced reasoning explanations
- Respects confidence thresholds well

### Optimizations

**1. Use XML-style tags for structure** (Claude likes clear boundaries):
```
<content>
Title: {title}
URL: {url}
Body: {body}
</content>

<output_format>
JSON array with fields: name, display_name, confidence, reasoning
</output_format>
```

**2. Emphasize thinking process**:
Add before output request:
```
Before providing JSON output, think through:
1. What are the 3-5 main topics discussed?
2. Which are specific enough but not too narrow?
3. What confidence level for each?

Then provide your JSON response:
```

**3. Model Selection**:
- `claude-3-5-sonnet-20241022`: Best balance (accuracy + cost + speed)
- `claude-3-opus-20240229`: Highest accuracy, slower, more expensive
- `claude-3-haiku-20240307`: Fastest, cheapest, slightly lower accuracy

### Expected Performance
- F1 Score: 0.90-0.95
- JSON compliance: 99%+
- Cost: ~$3-15 per 1M input tokens (model dependent)

## OpenAI (GPT)

### Strengths
- Fast response times
- Good at technical content
- Strong JSON mode support
- Wide knowledge base

### Optimizations

**1. Use JSON mode** (GPT-4 and newer):
```python
response = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format={ "type": "json_object" },
    messages=[...]
)
```

**2. System message optimization**:
```
System: You are a topic extraction specialist. Always respond with valid JSON.
User: [prompt with content]
```

**3. Be explicit about JSON structure**:
```
Respond with a JSON object with this exact structure:
{
  "topics": [
    {"name": "...", "display_name": "...", "confidence": 0.0, "reasoning": "..."}
  ]
}
```

**4. Model Selection**:
- `gpt-4-turbo`: Best overall (accuracy + cost)
- `gpt-4o`: Fastest, good accuracy
- `gpt-3.5-turbo`: Cheapest, lower accuracy

### Expected Performance
- F1 Score: 0.85-0.92
- JSON compliance: 95%+ (98%+ with JSON mode)
- Cost: ~$10-30 per 1M input tokens

## Google Gemini

### Strengths
- Competitive pricing
- Good at multimodal content (if images included)
- Fast inference
- Strong on recent/current events

### Optimizations

**1. Clear instruction structure**:
Gemini responds well to numbered instructions:
```
Instructions:
1. Read the content carefully
2. Identify 3-5 main topics
3. For each topic, determine confidence (0.0-1.0)
4. Output as JSON array
5. Order by confidence (highest first)
```

**2. Use response_mime_type for JSON**:
```python
generation_config = {
    "response_mime_type": "application/json",
    "temperature": 0.3,
}
```

**3. Include schema in prompt**:
```
Output schema:
{
  "topics": [
    {
      "name": "string (lowercase-hyphenated)",
      "display_name": "string",
      "confidence": "number 0.0-1.0",
      "reasoning": "string"
    }
  ]
}
```

**4. Model Selection**:
- `gemini-1.5-pro`: Best accuracy
- `gemini-1.5-flash`: Fastest, cheaper, good enough

### Expected Performance
- F1 Score: 0.83-0.90
- JSON compliance: 90-95%
- Cost: ~$3.50-7 per 1M input tokens

## Grok (xAI)

### Strengths
- Real-time/current information
- Good at technical and scientific content
- Competitive speed

### Optimizations

**1. Direct, concise prompts**:
Grok prefers shorter, punchier instructions:
```
Task: Extract topics from content.
Format: JSON with name, display_name, confidence, reasoning.
Limit: Max 5 topics, confidence >= 0.6.
Order: By confidence, descending.
```

**2. Emphasize JSON format early**:
```
IMPORTANT: Output must be valid JSON array. No markdown, no explanations, just JSON.
```

**3. Model Selection**:
- `grok-beta`: Current main model

### Expected Performance
- F1 Score: 0.82-0.88 (varies, newer model)
- JSON compliance: 85-92%
- Cost: Check current xAI pricing (competitive)

## Groq

### Strengths
- Extremely fast inference (hosting optimized models)
- Cost-effective
- Good for high-throughput scenarios

### Optimizations

**1. Use supported models**:
Groq hosts specific models:
- `llama3-70b-8192`: Best accuracy
- `llama3-8b-8192`: Fastest
- `mixtral-8x7b-32768`: Good balance

**2. Optimize for speed**:
```python
response = client.chat.completions.create(
    model="llama3-70b-8192",
    temperature=0.1,  # Lower for more consistent JSON
    max_tokens=1000,  # Limit for topic extraction
    messages=[...]
)
```

**3. Be strict with JSON format**:
Llama models need very explicit JSON structure:
```
You must respond with ONLY a JSON array. Example:
[{"name":"react","display_name":"React","confidence":0.9,"reasoning":"..."}]

Do not include any text before or after the JSON array.
```

### Expected Performance
- F1 Score: 0.78-0.85 (model dependent)
- JSON compliance: 80-90%
- Speed: 200-500+ tokens/sec (very fast!)
- Cost: Very cheap (~$0.05-0.10 per 1M tokens)

## Comparison Matrix

| Provider | Accuracy | Speed | Cost | JSON Quality | Best For |
|----------|----------|-------|------|--------------|----------|
| Claude   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | High accuracy |
| OpenAI   | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Balance |
| Gemini   | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Cost/performance |
| Grok     | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Current events |
| Groq     | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | High throughput |

## Temperature Settings

**Recommended temperatures for topic extraction:**

| Provider | Recommended Temp | Reasoning |
|----------|-----------------|-----------|
| Claude   | 0.3-0.5 | Balance consistency and nuance |
| OpenAI   | 0.2-0.4 | Lower for better JSON compliance |
| Gemini   | 0.3-0.5 | Similar to Claude |
| Grok     | 0.2-0.3 | Lower for more consistent output |
| Groq     | 0.1-0.2 | Llama models need lower temp for JSON |

**Why low temperature?**
- Topic extraction is deterministic (same content → same topics)
- We want consistent JSON formatting
- Creativity not needed (we want accurate extraction, not novel topics)

## Error Handling Per Provider

### Common JSON Parsing Errors

**Claude**: Rare, usually wraps JSON in markdown:
```
Here are the topics:
```json
[...]
```
```
Solution: Strip markdown code blocks before parsing

**OpenAI**: With JSON mode, very clean. Without it, may add explanation text:
```
The extracted topics are:
[...]
```
Solution: Use JSON mode or extract JSON from response

**Gemini**: Sometimes returns wrapped or includes schema in output:
Solution: Use `response_mime_type` or parse more aggressively

**Grok/Groq**: May include extra text or malformed JSON:
Solution: Strict prompt + fallback parsing (extract array from text)

### Retry Strategy

```
1. First attempt: Parse response as-is
2. If fails: Strip markdown, try again
3. If fails: Extract JSON array with regex
4. If fails: Log error, try different provider or return empty
```

## A/B Testing Recommendations

### Test Scenario 1: Accuracy Priority
```
Primary: Claude (Sonnet)
Fallback: OpenAI (GPT-4-turbo)
```

### Test Scenario 2: Cost Priority
```
Primary: Groq (Llama3-70b)
Secondary: Gemini (Flash)
Fallback: OpenAI (GPT-3.5)
```

### Test Scenario 3: Speed Priority
```
Primary: Groq (Llama3)
Fallback: Gemini (Flash)
```

### Test Scenario 4: Best Balance
```
Primary: Gemini (Pro) - Good accuracy + cost
Fallback: OpenAI (GPT-4-turbo)
Validation: Claude (for spot-checking quality)
```

## Prompt Versioning by Provider

Track different prompt versions per provider:

```
prompts/
  baseline.txt          # Universal prompt
  claude/
    v1.0.txt           # Claude-optimized
    v1.1.txt
  openai/
    v1.0.txt           # GPT-optimized
  gemini/
    v1.0.txt
```

This allows provider-specific tuning while maintaining consistency.
