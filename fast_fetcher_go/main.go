package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

type Result struct {
	URL        string `json:"url"`
	StatusCode int    `json:"status_code"`
	DurationMs int64  `json:"duration_ms"`
}

func main() {
	urls := []string{
		"https://httpbin.org/get?item=asus_laptop",
		"https://httpbin.org/get?item=macbook_air",
		"https://httpbin.org/get?item=samsung_s24",
	}

	var wg sync.WaitGroup
	var results []Result
	var mu sync.Mutex
	client := &http.Client{Timeout: 5 * time.Second}

	fmt.Println("🚀 High-Concurrency Go Fetcher running...")
	for _, u := range urls {
		wg.Add(1)
		go func(target string) {
			defer wg.Done()
			start := time.Now()
			resp, err := client.Get(target)
			dur := time.Since(start).Milliseconds()
			status := 0
			if err == nil {
				status = resp.StatusCode
				resp.Body.Close()
			}
			mu.Lock()
			results = append(results, Result{URL: target, StatusCode: status, DurationMs: dur})
			mu.Unlock()
			fmt.Printf("Fetched %s in %d ms\n", target, dur)
		}(u)
	}
	wg.Wait()

	data, _ := json.MarshalIndent(results, "", "  ")
	os.WriteFile("fetch_summary.json", data, 0644)
	fmt.Println("✅ Go fetcher completed. Saved to fetch_summary.json")
}
