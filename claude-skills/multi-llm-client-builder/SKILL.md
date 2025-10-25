---
name: multi-llm-client-builder
description: Generate Go client library for AI topic extraction supporting multiple LLM providers (Claude, OpenAI, Gemini, Grok, Groq). Use when building topic classification systems with unified interface, A/B testing capabilities, rate limiting, retries, and provider comparison. Works with ai-topic-extraction-prompts skill.
---

# Multi-LLM Client Builder

## Overview

Generate production-ready Go client library for topic extraction using multiple LLM providers. Provides unified interface, automatic retries, rate limiting, cost estimation, and A/B testing infrastructure.

## When to Use This Skill

Use when:
- Building Go-based topic extraction systems
- Need to support multiple LLM providers with single interface
- Want to A/B test different providers for cost/accuracy/speed
- Require rate limiting and retry logic for API calls
- Building processor service for content analysis

Works best with:
- **ai-topic-extraction-prompts** skill (provides the prompts this client uses)

Do not use when:
- Using languages other than Go
- Only need one LLM provider (use their SDK directly)
- Don't need topic extraction (different use case)

## Quick Start

The skill generates complete Go package in `internal/llm/`:

1. **Core Interface** (`topic_extractor.go`) - Unified interface for all providers
2. **Providers** (`claude_provider.go`, etc.) - Implementation for each LLM
3. **Factory** (`factory.go`) - Easy provider creation
4. **Utilities** (`ratelimiter.go`) - Rate limiting, retries
5. **Testing** - Unit test patterns and A/B testing helpers

## Generated Package Structure

```
internal/llm/
├── topic_extractor.go      # Interface + types
├── claude_provider.go      # Claude implementation
├── openai_provider.go      # OpenAI implementation
├── gemini_provider.go      # Gemini implementation
├── grok_provider.go        # Grok implementation
├── groq_provider.go        # Groq implementation
├── factory.go              # Provider factory
└── ratelimiter.go          # Rate limiting
```

## Core Interface

### TopicExtractor Interface

```go
type TopicExtractor interface {
    // Extract topics from content
    ExtractTopics(ctx context.Context, content Content) ([]Topic, error)

    // Extract with metadata (latency, cost, etc.)
    ExtractTopicsWithMetadata(ctx context.Context, content Content) (*ExtractionResult, error)

    // Provider name
    Provider() string

    // Estimate cost in USD
    EstimateCost(content Content) float64
}
```

### Topic Structure

```go
type Topic struct {
    Name        string  // "machine-learning"
    DisplayName string  // "Machine Learning"
    Confidence  float64 // 0.0-1.0
    Reasoning   string  // Why extracted
}
```

### Content Structure

```go
type Content struct {
    Title       string
    URL         string
    Description string
    Body        string
}
```

## Using the Generated Code

### Step 1: Create Extractor

```go
import "yourproject/internal/llm"

config := llm.DefaultConfig()
config.ClaudeAPIKey = os.Getenv("CLAUDE_API_KEY")
config.Temperature = 0.3
config.MinConfidence = 0.6

extractor, err := llm.NewExtractor(llm.ProviderClaude, config)
if err != nil {
    log.Fatal(err)
}
```

### Step 2: Extract Topics

```go
content := llm.Content{
    Title: article.Title,
    URL:   article.URL,
    Body:  article.Body,
}

ctx := context.Background()
topics, err := extractor.ExtractTopics(ctx, content)
if err != nil {
    log.Printf("Extraction failed: %v", err)
    return
}

for _, topic := range topics {
    fmt.Printf("%s (%.2f): %s\n",
        topic.DisplayName,
        topic.Confidence,
        topic.Reasoning)
}
```

### Step 3: Store in Database

```go
for _, topic := range topics {
    err := db.InsertTopic(ctx, &domain.Topic{
        Name:        topic.Name,
        DisplayName: topic.DisplayName,
        ContentID:   content.ID,
        Confidence:  topic.Confidence,
    })
}
```

## Provider Implementations

Each provider follows the same pattern but with provider-specific optimizations.

### Claude Provider

**Best for**: Highest accuracy, good JSON compliance
**Model**: claude-3-5-sonnet-20241022
**Cost**: ~$3-15 per 1M input tokens
**Speed**: Moderate

Uses XML-tagged prompts and thinking process for better results.

### OpenAI Provider

**Best for**: Balance of accuracy/cost/speed
**Model**: gpt-4-turbo
**Cost**: ~$10-30 per 1M input tokens
**Speed**: Fast

Uses JSON mode for guaranteed valid JSON responses.

### Gemini Provider

**Best for**: Cost-effectiveness
**Model**: gemini-1.5-pro or gemini-1.5-flash
**Cost**: ~$0.50-7 per 1M input tokens
**Speed**: Fast

Uses `response_mime_type` for JSON output.

### Groq Provider

**Best for**: Speed and cost
**Models**: llama3-70b-8192, mixtral-8x7b-32768
**Cost**: ~$0.05-0.10 per 1M tokens (very cheap!)
**Speed**: Very fast (200-500+ tokens/sec)

OpenAI-compatible API with extremely fast inference.

See `references/provider_implementations.md` for complete implementation details.

## Configuration

### Default Configuration

```go
config := llm.DefaultConfig()
// Returns:
// Temperature: 0.3
// MaxTokens: 1000
// Timeout: 30s
// MinConfidence: 0.6
// MaxTopics: 5
// RetryAttempts: 3
// RetryBackoff: 2s
// EnableRateLimit: true
// RequestsPerMin: 60
```

### Custom Configuration

```go
config := &llm.Config{
    ClaudeAPIKey:    os.Getenv("CLAUDE_API_KEY"),
    OpenAIAPIKey:    os.Getenv("OPENAI_API_KEY"),
    Temperature:     0.2,           // Lower for more consistency
    MaxTokens:       500,            // Less tokens = cheaper
    MinConfidence:   0.7,            // Higher quality threshold
    MaxTopics:       3,              // Fewer topics
    RetryAttempts:   5,              // More retries
    RequestsPerMin:  100,            // Higher rate limit
}
```

## A/B Testing Multiple Providers

### Parallel Comparison

```go
// Compare Claude vs OpenAI vs Gemini
providers := []llm.Provider{
    llm.ProviderClaude,
    llm.ProviderOpenAI,
    llm.ProviderGemini,
}

config.ClaudeAPIKey = os.Getenv("CLAUDE_API_KEY")
config.OpenAIAPIKey = os.Getenv("OPENAI_API_KEY")
config.GeminiAPIKey = os.Getenv("GEMINI_API_KEY")

extractors, err := llm.NewMultiExtractors(providers, config)
if err != nil {
    log.Fatal(err)
}

// Run all in parallel
var wg sync.WaitGroup
results := make(map[llm.Provider]*llm.ExtractionResult)

for provider, extractor := range extractors {
    wg.Add(1)
    go func(p llm.Provider, ext llm.TopicExtractor) {
        defer wg.Done()
        result, _ := ext.ExtractTopicsWithMetadata(ctx, content)
        results[p] = result
    }(provider, extractor)
}

wg.Wait()

// Compare results
for provider, result := range results {
    fmt.Printf("%s: %d topics, %.2fs, $%.4f\n",
        provider,
        len(result.Topics),
        result.Latency.Seconds(),
        result.Cost)
}
```

See `references/ab_testing.md` for complete A/B testing patterns, batch testing, and provider selection strategies.

## Advanced Patterns

### Cascading Strategy

Try fast/cheap provider first, fall back to accurate one:

```go
func ExtractWithFallback(ctx context.Context, content llm.Content, config *llm.Config) ([]llm.Topic, error) {
    // Try Groq first (fast + cheap)
    groq, _ := llm.NewExtractor(llm.ProviderGroq, config)
    result, err := groq.ExtractTopicsWithMetadata(ctx, content)

    if err == nil && avgConfidence(result.Topics) >= 0.8 {
        return result.Topics, nil  // High confidence - use it!
    }

    // Fall back to Claude (accurate but slower/pricier)
    claude, _ := llm.NewExtractor(llm.ProviderClaude, config)
    return claude.ExtractTopics(ctx, content)
}
```

### Batch Processing

Process multiple articles efficiently:

```go
func BatchExtract(ctx context.Context, articles []Article, extractor llm.TopicExtractor) error {
    semaphore := make(chan struct{}, 10) // Max 10 concurrent

    var wg sync.WaitGroup
    for _, article := range articles {
        wg.Add(1)
        semaphore <- struct{}{} // Acquire

        go func(a Article) {
            defer wg.Done()
            defer func() { <-semaphore }() // Release

            content := llm.Content{
                Title: a.Title,
                URL:   a.URL,
                Body:  a.Body,
            }

            topics, err := extractor.ExtractTopics(ctx, content)
            if err != nil {
                log.Printf("Failed for %s: %v", a.URL, err)
                return
            }

            // Store topics
            storeTopics(a.ID, topics)
        }(article)
    }

    wg.Wait()
    return nil
}
```

## Integration with Dark Processor Service

### Processor Service Pattern

```go
// cmd/processor/main.go
package main

import (
    "context"
    "encoding/json"
    "yourproject/internal/llm"
    "github.com/nats-io/nats.go"
)

type ContentMessage struct {
    RequestID string
    Content   struct {
        ID          int64
        Title       string
        URL         string
        Description string
        Body        string
    }
}

func main() {
    // Setup LLM extractor
    config := llm.DefaultConfig()
    config.ClaudeAPIKey = os.Getenv("CLAUDE_API_KEY")
    extractor, _ := llm.NewExtractor(llm.ProviderClaude, config)

    // Connect to NATS
    nc, _ := nats.Connect(nats.DefaultURL)
    defer nc.Close()

    // Subscribe to content queue
    nc.Subscribe("content.scraped", func(msg *nats.Msg) {
        var cm ContentMessage
        json.Unmarshal(msg.Data, &cm)

        // Extract topics
        content := llm.Content{
            Title:       cm.Content.Title,
            URL:         cm.Content.URL,
            Description: cm.Content.Description,
            Body:        cm.Content.Body,
        }

        topics, err := extractor.ExtractTopics(context.Background(), content)
        if err != nil {
            log.Printf("Extraction failed: %v", err)
            return
        }

        // Store in database
        for _, topic := range topics {
            db.InsertTopic(cm.RequestID, cm.Content.ID, topic)
        }

        log.Printf("Extracted %d topics for content %d", len(topics), cm.Content.ID)
    })

    select {} // Block forever
}
```

## Resources

### assets/

- **topic_extractor.go.template** - Core interface, types, config
- **claude_provider.go.template** - Complete Claude implementation (reference example)
- **factory.go.template** - Provider factory pattern
- **ratelimiter.go.template** - Token bucket rate limiter

### references/

- **provider_implementations.md** - Complete guide for implementing all providers (OpenAI, Gemini, Grok, Groq)
- **ab_testing.md** - A/B testing patterns, batch testing, provider selection

## Best Practices

1. **Use rate limiting** - Prevents hitting API limits
2. **Enable retries** - Handle transient failures gracefully
3. **Filter by confidence** - Only use topics with confidence >= 0.6
4. **A/B test providers** - Find best balance for your needs
5. **Monitor costs** - Track spending with `EstimateCost()`
6. **Use cascading** - Fast/cheap first, accurate fallback
7. **Batch processing** - Limit concurrency to avoid rate limits
8. **Handle context cancellation** - Respect timeouts

## Testing

### Unit Test Example

```go
func TestClaudeExtractor(t *testing.T) {
    apiKey := os.Getenv("CLAUDE_API_KEY")
    if apiKey == "" {
        t.Skip("API key not set")
    }

    extractor, err := llm.NewClaudeExtractor(apiKey, nil)
    require.NoError(t, err)

    content := llm.Content{
        Title: "Introduction to React Hooks",
        URL:   "https://example.com",
        Body:  "React Hooks are a new feature...",
    }

    topics, err := extractor.ExtractTopics(context.Background(), content)
    require.NoError(t, err)
    assert.NotEmpty(t, topics)
    assert.LessOrEqual(t, len(topics), 5)

    for _, topic := range topics {
        assert.NotEmpty(t, topic.Name)
        assert.GreaterOrEqual(t, topic.Confidence, 0.6)
    }
}
```

## Common Issues

**Issue**: Rate limit errors
**Solution**: Lower `RequestsPerMin` or add delay between batches

**Issue**: Invalid JSON responses
**Solution**: Provider may wrap JSON in markdown - parsing handles this

**Issue**: High costs
**Solution**: Use cheaper providers (Groq/Gemini) or cascading strategy

**Issue**: Low accuracy
**Solution**: Use Claude or increase temperature slightly (0.3 → 0.4)

**Issue**: Slow processing
**Solution**: Use Groq for speed or parallel processing

## Next Steps

After generating the LLM client:

1. **Implement remaining providers** - Follow Claude example for OpenAI, Gemini, etc.
2. **Build processor service** - Use NATS consumer pattern above
3. **A/B test providers** - Find best for your needs
4. **Integrate prompts** - Use prompts from ai-topic-extraction-prompts skill
5. **Monitor and iterate** - Track costs, latency, accuracy

## Related Skills

- **ai-topic-extraction-prompts** - Prompts and evaluation framework (use together)
- **topic-portal-router** - Subdomain routing for topic portals
- **graph-scoring-builder** - Topic graph traversal (coming next)
