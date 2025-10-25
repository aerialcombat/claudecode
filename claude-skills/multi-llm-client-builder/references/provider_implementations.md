# Provider Implementations Guide

This document explains how to implement providers for each LLM service following the Claude example pattern.

## Implementation Pattern

All providers follow the same structure:

```go
type ProviderExtractor struct {
	apiKey      string
	config      *Config
	httpClient  *http.Client
	rateLimiter *RateLimiter
}

// Constructor
func NewProviderExtractor(apiKey string, config *Config) (*ProviderExtractor, error)

// Interface methods
func (p *ProviderExtractor) Provider() string
func (p *ProviderExtractor) ExtractTopics(ctx context.Context, content Content) ([]Topic, error)
func (p *ProviderExtractor) ExtractTopicsWithMetadata(ctx context.Context, content Content) (*ExtractionResult, error)
func (p *ProviderExtractor) EstimateCost(content Content) float64

// Internal methods
func (p *ProviderExtractor) callAPI(ctx context.Context, prompt string) ([]Topic, error)
func (p *ProviderExtractor) parseTopics(text string) ([]Topic, error)
func (p *ProviderExtractor) buildPrompt(content Content) string
```

## Provider-Specific Details

### OpenAI (GPT)

**Endpoint**: `https://api.openai.com/v1/chat/completions`

**Key differences from Claude**:
1. Use JSON mode: `response_format: {"type": "json_object"}`
2. System + user messages structure
3. Different auth header: `Authorization: Bearer {api_key}`

**Request structure**:
```json
{
  "model": "gpt-4-turbo",
  "response_format": {"type": "json_object"},
  "temperature": 0.3,
  "max_tokens": 1000,
  "messages": [
    {"role": "system", "content": "You are a topic extraction specialist."},
    {"role": "user", "content": "..."}
  ]
}
```

**Cost estimation** (GPT-4-turbo):
- Input: $10 per 1M tokens
- Output: $30 per 1M tokens

### Google Gemini

**Endpoint**: `https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent`

**Key differences**:
1. API key in URL query parameter
2. Use `response_mime_type: "application/json"`
3. Different response structure

**Request structure**:
```json
{
  "contents": [{"parts": [{"text": "..."}]}],
  "generation_config": {
    "response_mime_type": "application/json",
    "temperature": 0.3,
    "max_output_tokens": 1000
  }
}
```

**Cost estimation** (Gemini Pro):
- Input: $0.50-$3.50 per 1M tokens
- Output: $1.50-$7 per 1M tokens

### Grok (xAI)

**Endpoint**: `https://api.x.ai/v1/chat/completions`

**Key differences**:
1. OpenAI-compatible API
2. Different models: `grok-beta`
3. Auth header: `Authorization: Bearer {api_key}`

**Request structure**: Same as OpenAI

**Cost estimation**: Check xAI pricing (competitive with GPT)

### Groq

**Endpoint**: `https://api.groq.com/openai/v1/chat/completions`

**Key differences**:
1. OpenAI-compatible API
2. Different models: `llama3-70b-8192`, `mixtral-8x7b-32768`
3. Very fast inference
4. Auth header: `Authorization: Bearer {api_key}`

**Request structure**: Same as OpenAI

**Cost estimation** (very cheap):
- Input: ~$0.05-0.10 per 1M tokens
- Output: ~$0.05-0.10 per 1M tokens

## Common Implementation Challenges

### 1. JSON Parsing

Different providers wrap JSON differently:

**Claude**: May wrap in markdown code blocks
```
```json
[{"name": "react", ...}]
```
```

**Solution**:
```go
func parseTopics(text string) ([]Topic, error) {
	text = strings.TrimSpace(text)
	// Strip markdown if present
	if strings.HasPrefix(text, "```json") {
		text = strings.TrimPrefix(text, "```json")
		text = strings.TrimSuffix(text, "```")
		text = strings.TrimSpace(text)
	}

	var topics []Topic
	if err := json.Unmarshal([]byte(text), &topics); err != nil {
		return nil, err
	}
	return topics, nil
}
```

### 2. Rate Limiting

Each provider has different rate limits. Use the RateLimiter with provider-specific limits:

- Claude: 50-100 requests/min depending on tier
- OpenAI: 500-10,000 requests/min depending on tier
- Gemini: 60 requests/min (free tier)
- Groq: Very high (thousands/min)

### 3. Error Handling

Implement retry logic for transient errors:

```go
for attempt := 0; attempt <= retryAttempts; attempt++ {
	topics, err := callAPI(ctx, prompt)
	if err == nil {
		return topics, nil
	}

	// Don't retry validation errors
	if isNonRetryableError(err) {
		return nil, err
	}

	// Exponential backoff
	time.Sleep(backoff * time.Duration(1<<attempt))
}
```

### 4. Context Cancellation

Always respect context cancellation:

```go
select {
case <-time.After(backoff):
case <-ctx.Done():
	return nil, ctx.Err()
}
```

## Testing Each Provider

### Unit Test Template

```go
func TestProviderExtractor(t *testing.T) {
	apiKey := os.Getenv("PROVIDER_API_KEY")
	if apiKey == "" {
		t.Skip("API key not set")
	}

	extractor, err := NewProviderExtractor(apiKey, nil)
	require.NoError(t, err)

	content := Content{
		Title: "Introduction to React Hooks",
		URL: "https://example.com",
		Body: "React Hooks are...",
	}

	ctx := context.Background()
	topics, err := extractor.ExtractTopics(ctx, content)

	require.NoError(t, err)
	assert.NotEmpty(t, topics)
	assert.LessOrEqual(t, len(topics), 5)

	for _, topic := range topics {
		assert.NotEmpty(t, topic.Name)
		assert.GreaterOrEqual(t, topic.Confidence, 0.6)
		assert.LessOrEqual(t, topic.Confidence, 1.0)
	}
}
```

## Implementation Checklist

When implementing a new provider:

- [ ] Create `ProviderExtractor` struct
- [ ] Implement `NewProviderExtractor` constructor with validation
- [ ] Implement all `TopicExtractor` interface methods
- [ ] Add provider-specific prompt optimization
- [ ] Implement JSON parsing with error handling
- [ ] Add rate limiting
- [ ] Implement retry logic with exponential backoff
- [ ] Add cost estimation
- [ ] Write unit tests
- [ ] Document API-specific quirks
- [ ] Add to factory pattern in `factory.go`

## Example: Complete OpenAI Implementation Outline

```go
type OpenAIExtractor struct {
	apiKey      string
	config      *Config
	httpClient  *http.Client
	rateLimiter *RateLimiter
}

func NewOpenAIExtractor(apiKey string, config *Config) (*OpenAIExtractor, error) {
	// Similar to Claude implementation
}

func (o *OpenAIExtractor) callOpenAI(ctx context.Context, prompt string) ([]Topic, error) {
	reqBody := map[string]interface{}{
		"model": "gpt-4-turbo",
		"response_format": map[string]string{"type": "json_object"},
		"temperature": o.config.Temperature,
		"max_tokens": o.config.MaxTokens,
		"messages": []map[string]string{
			{"role": "system", "content": "You are a topic extraction specialist. Always respond with valid JSON."},
			{"role": "user", "content": prompt},
		},
	}

	// Make HTTP request (similar to Claude)
	req.Header.Set("Authorization", "Bearer " + o.apiKey)

	// Parse response (OpenAI has cleaner JSON than Claude)
	var apiResp struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
	}

	// Extract and parse topics
}

func (o *OpenAIExtractor) buildPrompt(content Content) string {
	// Simpler prompt for OpenAI (no XML tags needed)
	return fmt.Sprintf(`Extract topics from this content and respond with ONLY a JSON array.

Content:
Title: %s
URL: %s
Body: %s

JSON format: [{"name":"topic-slug","display_name":"Topic Name","confidence":0.95,"reasoning":"..."}]

Include 3-5 topics with confidence >= 0.6, ordered by confidence.`,
		content.Title, content.URL, content.Body)
}
```

Follow this pattern for Gemini, Grok, and Groq implementations.
