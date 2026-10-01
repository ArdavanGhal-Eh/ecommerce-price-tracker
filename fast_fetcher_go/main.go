package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"
)

type FetchResult struct {
	URL        string `json:"url"`
	StatusCode int    `json:"status_code"`
	DurationMs int64  `json:"duration_ms"`
	Success    bool   `json:"success"`
	Size       int    `json:"size_bytes"`
}

func fetchWorker(id int, urls <-chan string, results chan<- FetchResult, client *http.Client, wg *sync.WaitGroup) {
	defer wg.Done()
	for targetURL := range urls {
		start := time.Now()
		req, err := http.NewRequest("GET", targetURL, nil)
		if err != nil {
			results <- FetchResult{URL: targetURL, Success: false}
			continue
		}
		req.Header.Set("User-Agent", "Mozilla/5.0 (Fast-Go-Crawler-Engine/1.0)")

		resp, err := client.Do(req)
		duration := time.Since(start).Milliseconds()

		if err != nil {
			results <- FetchResult{URL: targetURL, DurationMs: duration, Success: false}
			continue
		}

		body, _ := io.ReadAll(resp.Body)
		resp.Body.Close()

		results <- FetchResult{
			URL:        targetURL,
			StatusCode: resp.StatusCode,
			DurationMs: duration,
			Success:    resp.StatusCode == 200,
			Size:       len(body),
		}
		fmt.Printf("[Go Worker %d] Fetched: %s (Status: %d | Time: %d ms)\n", id, targetURL, resp.StatusCode, duration)
	}
}

func main() {
	concurrency := flag.Int("concurrency", 10, "Number of concurrent worker goroutines")
	outputFile := flag.String("output", "fetch_summary.json", "Output JSON report file")
	flag.Parse()

	targetURLs := []string{
		"https://httpbin.org/get?item=asus_laptop",
		"https://httpbin.org/get?item=macbook_air",
		"https://httpbin.org/get?item=samsung_s24",
		"https://httpbin.org/get?item=xiaomi_monitor",
		"https://httpbin.org/get?item=sony_headphone",
	}

	urlChan := make(chan string, len(targetURLs))
	resultChan := make(chan FetchResult, len(targetURLs))
	client := &http.Client{Timeout: 10 * time.Second}
	var wg sync.WaitGroup

	fmt.Printf("🚀 Starting High-Concurrency Go Fetcher (%d workers)...\n", *concurrency)
	for i := 1; i <= *concurrency; i++ {
		wg.Add(1)
		go fetchWorker(i, urlChan, resultChan, client, &wg)
	}
	for _, u := range targetURLs { urlChan <- u }
	close(urlChan)

	wg.Wait()
	close(resultChan)

	var allResults []FetchResult
	for res := range resultChan { allResults = append(allResults, res) }

	data, _ := json.MarshalIndent(allResults, "", "  ")
	os.WriteFile(*outputFile, data, 0644)
	fmt.Printf("✅ Completed batch fetch of %d URLs. Summary written to %s\n", len(allResults), *outputFile)
}