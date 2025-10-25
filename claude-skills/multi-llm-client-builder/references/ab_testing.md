# A/B Testing Multiple Providers

Guide for comparing multiple LLM providers for topic extraction accuracy, cost, and performance.

## Parallel Comparison Pattern

```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// CompareProviders runs topic extraction with multiple providers in parallel
func CompareProviders(content llm.Content, providers []llm.Provider, config *llm.Config) (*ComparisonResult, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()

	extractors, err := llm.NewMultiExtractors(providers, config)
	if err != nil {
		return nil, err
	}

	results := make(chan *llm.ExtractionResult, len(providers))
	var wg sync.WaitGroup

	// Run all providers in parallel
	for provider, extractor := range extractors {
		wg.Add(1)
		go func(p llm.Provider, ext llm.TopicExtractor) {
			defer wg.Done()

			result, err := ext.ExtractTopicsWithMetadata(ctx, content)
			if err != nil {
				result = &llm.ExtractionResult{
					Provider: string(p),
					Error:    err,
				}
			}
			results <- result
		}(provider, extractor)
	}

	wg.Wait()
	close(results)

	// Collect results
	comparison := &ComparisonResult{
		ContentID: content.URL,
		Results:   make(map[string]*llm.ExtractionResult),
	}

	for result := range results {
		comparison.Results[result.Provider] = result
	}

	return comparison, nil
}

type ComparisonResult struct {
	ContentID string
	Results   map[string]*llm.ExtractionResult
}

// Metrics calculates performance metrics for comparison
func (cr *ComparisonResult) Metrics() *Metrics {
	m := &Metrics{
		ByProvider: make(map[string]ProviderMetrics),
	}

	for provider, result := range cr.Results {
		pm := ProviderMetrics{
			TopicCount: len(result.Topics),
			Latency:    result.Latency,
			Cost:       result.Cost,
			Success:    result.Error == nil,
		}

		if result.Error == nil && len(result.Topics) > 0 {
			pm.AvgConfidence = avgConfidence(result.Topics)
		}

		m.ByProvider[provider] = pm
	}

	return m
}

type Metrics struct {
	ByProvider map[string]ProviderMetrics
}

type ProviderMetrics struct {
	TopicCount    int
	AvgConfidence float64
	Latency       time.Duration
	Cost          float64
	Success       bool
}

func avgConfidence(topics []llm.Topic) float64 {
	if len(topics) == 0 {
		return 0
	}
	sum := 0.0
	for _, t := range topics {
		sum += t.Confidence
	}
	return sum / float64(len(topics))
}
```

## Batch Testing

Test multiple articles across all providers:

```go
func BatchCompare(articles []llm.Content, providers []llm.Provider, config *llm.Config) (*BatchMetrics, error) {
	results := make([]*ComparisonResult, 0, len(articles))

	for _, article := range articles {
		result, err := CompareProviders(article, providers, config)
		if err != nil {
			return nil, err
		}
		results = append(results, result)
	}

	// Aggregate metrics
	return AggregateMetrics(results), nil
}

type BatchMetrics struct {
	TotalArticles int
	ByProvider    map[string]AggregateMetrics
}

type AggregateMetrics struct {
	SuccessRate    float64
	AvgLatency     time.Duration
	AvgCost        float64
	AvgTopicCount  float64
	AvgConfidence  float64
	TotalCost      float64
}
```

## Evaluating Accuracy

Compare against ground truth (manually tagged topics):

```go
func EvaluateAccuracy(extracted []llm.Topic, groundTruth []string) AccuracyMetrics {
	extractedNames := make(map[string]bool)
	for _, t := range extracted {
		extractedNames[t.Name] = true
	}

	gtSet := make(map[string]bool)
	for _, name := range groundTruth {
		gtSet[name] = true
	}

	// Calculate precision and recall
	truePositives := 0
	for name := range extractedNames {
		if gtSet[name] {
			truePositives++
		}
	}

	precision := float64(truePositives) / float64(len(extracted))
	recall := float64(truePositives) / float64(len(groundTruth))

	var f1 float64
	if precision+recall > 0 {
		f1 = 2 * (precision * recall) / (precision + recall)
	}

	return AccuracyMetrics{
		Precision: precision,
		Recall:    recall,
		F1Score:   f1,
	}
}

type AccuracyMetrics struct {
	Precision float64
	Recall    float64
	F1Score   float64
}
```

## Decision Framework

After running A/B tests, choose provider based on priorities:

```go
func SelectBestProvider(metrics *BatchMetrics, priorities Priorities) string {
	var bestProvider string
	var bestScore float64

	for provider, m := range metrics.ByProvider {
		score := calculateScore(m, priorities)
		if score > bestScore {
			bestScore = score
			bestProvider = provider
		}
	}

	return bestProvider
}

type Priorities struct {
	AccuracyWeight float64 // 0-1
	CostWeight     float64 // 0-1
	SpeedWeight    float64 // 0-1
}

func calculateScore(m AggregateMetrics, p Priorities) float64 {
	// Normalize metrics to 0-1 scale
	accuracyScore := m.AvgConfidence // Already 0-1
	costScore := 1.0 / (1.0 + m.AvgCost*100) // Inverse cost
	speedScore := 1.0 / (1.0 + float64(m.AvgLatency.Milliseconds())/1000) // Inverse latency

	// Weighted sum
	return (accuracyScore * p.AccuracyWeight) +
		(costScore * p.CostWeight) +
		(speedScore * p.SpeedWeight)
}
```

## Example Usage

```go
func main() {
	// Test dataset
	articles := []llm.Content{
		{Title: "React Hooks Guide", URL: "...", Body: "..."},
		{Title: "Python ML Tutorial", URL: "...", Body: "..."},
		// ... 20-50 articles
	}

	// Providers to compare
	providers := []llm.Provider{
		llm.ProviderClaude,
		llm.ProviderOpenAI,
		llm.ProviderGemini,
	}

	// Run batch comparison
	config := llm.DefaultConfig()
	metrics, err := BatchCompare(articles, providers, config)
	if err != nil {
		panic(err)
	}

	// Print results
	for provider, m := range metrics.ByProvider {
		fmt.Printf("%s: F1=%.2f, Cost=$%.4f, Latency=%dms\n",
			provider, m.AvgConfidence, m.TotalCost, m.AvgLatency.Milliseconds())
	}

	// Select best based on priorities
	priorities := Priorities{
		AccuracyWeight: 0.5,
		CostWeight:     0.3,
		SpeedWeight:    0.2,
	}

	best := SelectBestProvider(metrics, priorities)
	fmt.Printf("\nBest provider for your priorities: %s\n", best)
}
```

## Cascading Strategy

Use fast/cheap provider first, fall back to accurate one:

```go
func CascadingExtraction(content llm.Content, config *llm.Config) ([]llm.Topic, error) {
	ctx := context.Background()

	// Try Groq first (fast + cheap)
	groq, _ := llm.NewExtractor(llm.ProviderGroq, config)
	result, err := groq.ExtractTopicsWithMetadata(ctx, content)

	if err == nil && avgConfidence(result.Topics) >= 0.8 {
		// High confidence - use Groq result
		return result.Topics, nil
	}

	// Low confidence or error - fall back to Claude (accurate)
	claude, _ := llm.NewExtractor(llm.ProviderClaude, config)
	topics, err := claude.ExtractTopics(ctx, content)

	return topics, err
}
```

This saves cost while maintaining quality!
