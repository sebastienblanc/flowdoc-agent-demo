package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/firebase/genkit/go/ai"
	"github.com/firebase/genkit/go/genkit"
	"github.com/firebase/genkit/go/plugins/compat_oai/openai"
	"github.com/openai/openai-go/option"
)

func main() {
	ctx := context.Background()

	engineURL := os.Getenv("MODEL_RUNNER_BASE_URL")
	chatModelId := "openai/" + os.Getenv("CHAT_MODEL_ID")

	fmt.Println("🌍 LLM URL:", engineURL)
	fmt.Println("🤖 Chat Model:", chatModelId)

	// Initialize OpenAI plugin with custom endpoint
	oaiPlugin := &openai.OpenAI{
		APIKey: "DockerAIDocumenter",
		Opts: []option.RequestOption{
			option.WithBaseURL(engineURL),
		},
	}
	g := genkit.Init(ctx, genkit.WithPlugins(oaiPlugin))

	// Get the workflows directory
	workflowsDir := "/workspace/.github/workflows"
	docsDir := "/workspace/docs/workflows"

	// Create docs directory if it doesn't exist
	if err := os.MkdirAll(docsDir, 0755); err != nil {
		log.Fatalf("Failed to create docs directory: %v", err)
	}

	// Find all workflow files
	files, err := filepath.Glob(filepath.Join(workflowsDir, "*.yml"))
	if err != nil {
		log.Fatalf("Failed to find workflow files: %v", err)
	}
	yamlFiles, _ := filepath.Glob(filepath.Join(workflowsDir, "*.yaml"))
	files = append(files, yamlFiles...)

	if len(files) == 0 {
		fmt.Println("No workflow files found in .github/workflows/")
		return
	}

	fmt.Printf("Found %d workflow(s) to document\n", len(files))

	var workflowDocs []string

	// Process each workflow file
	for _, file := range files {
		fmt.Printf("Processing: %s\n", filepath.Base(file))

		// Read the workflow file
		workflowContent, err := os.ReadFile(file)
		if err != nil {
			log.Printf("Failed to read %s: %v", file, err)
			continue
		}

		// Generate documentation using AI
		response, err := genkit.Generate(ctx, g,
			ai.WithModelName(chatModelId),
			ai.WithSystem(os.Getenv("SYSTEM_INSTRUCTIONS")),
			ai.WithMessages(
				ai.NewSystemTextMessage(string(workflowContent)),
			),
			ai.WithPrompt(os.Getenv("USER_MESSAGE")),
			
			ai.WithStreaming(func(ctx context.Context, chunk *ai.ModelResponseChunk) error {
				fmt.Print(chunk.Text())
				return nil
			}),
		)
		if err != nil {
			log.Printf("😡 Error during generation for %s: %v", file, err)
			continue
		}

		// Save documentation to file
		baseName := strings.TrimSuffix(filepath.Base(file), filepath.Ext(file))
		outputFile := filepath.Join(docsDir, baseName+".md")
		err = os.WriteFile(outputFile, []byte(response.Text()), 0644)
		if err != nil {
			log.Printf("😡 Error writing output file %s: %v", outputFile, err)
			continue
		}

		fmt.Printf("\n✅ Generated: docs/workflows/%s.md\n\n", baseName)
		workflowDocs = append(workflowDocs, baseName)
	}

	// Create index file
	indexContent := fmt.Sprintf(`# GitHub Actions Workflows Documentation

This directory contains auto-generated documentation for all GitHub Actions workflows.

**Last Updated:** %s UTC

## Workflows

`, time.Now().UTC().Format("2006-01-02 15:04:05"))

	for _, doc := range workflowDocs {
		// Capitalize first letter and replace hyphens with spaces for display name
		displayName := strings.ReplaceAll(doc, "-", " ")
		if len(displayName) > 0 {
			displayName = strings.ToUpper(displayName[:1]) + displayName[1:]
		}
		indexContent += fmt.Sprintf("- [%s](./%s.md)\n", displayName, doc)
	}

	indexPath := filepath.Join(docsDir, "README.md")
	err = os.WriteFile(indexPath, []byte(indexContent), 0644)
	if err != nil {
		log.Printf("😡 Error writing index file: %v", err)
	}

	fmt.Println("\n✅ Documentation generated successfully in docs/workflows/")
}

