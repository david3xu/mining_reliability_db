# SharePoint Retrieval-Only Agent Implementation Guide

## Implementation Roadmap Table

| Phase | Step | Task | Execution Details | Time | Citation Source |
|-------|------|------|------------------|------|----------------|
| **1. Foundation** | 1.1 | Create Base Agent | Navigate to Copilot Studio → Create → New Agent<br/>Name: "SharePoint File Retrieval Agent"<br/>Disable generative responses in Overview settings | 5 min | microsoft-copilot-studio (2)_part_23.md |
| | 1.2 | Configure Authentication | Settings → Security → Authentication<br/>Select "Authenticate with Microsoft"<br/>Required Scopes: `Sites.Read.All`, `Files.Read.All` | 5 min | microsoft-copilot-studio (2)_part_24.md |
| **2. Topic Setup** | 2.1 | Build Search Topic | Topics → Create Topic → "Entity-Based File Search"<br/>Add Trigger Phrases: "find files", "search documents", "locate content" | 8 min | microsoft-copilot-studio (2)_part_38.md |
| | 2.2 | Add Question Node | Add Question Node: "What files are you looking for?"<br/>Save response as: `UserQuery` (Text) | 7 min | microsoft-copilot-studio (2)_part_48.md |
| **3. Entity Extraction** | 3.1 | Create Search Query Action | Add Node → Add Action → Create Search Query<br/>Input: `UserQuery` variable<br/>Output Variable: `EnhancedQuery` (Text) | 10 min | microsoft-copilot-studio (2)_part_51.md |
| | 3.2 | Configure Enhancement | Context Settings: Include conversation history (last 3 turns)<br/>Enhancement Mode: Entity extraction + context enrichment | 5 min | microsoft-copilot-studio (2)_part_51.md |
| **4. Power Automate** | 4.1 | Create Search Flow | Power Automate → Create Flow → "SharePoint File Search"<br/>Trigger: "When Copilot Studio calls this flow"<br/>Input Parameter: `SearchQuery` (String) | 8 min | microsoft-copilot-studio (2)_part_48.md |
| | 4.2 | SharePoint Search Action | SharePoint → Search Rows<br/>Site Address: [Your SharePoint Site URL]<br/>Search Query: @{triggerBody()['SearchQuery']}<br/>Top Count: 5 | 7 min | microsoft-copilot-studio (2)_part_48.md |
| | 4.3 | Parse JSON Results | Data Operation → Parse JSON<br/>Content: List of rows<br/>Schema: See JSON Schema below | 5 min | microsoft-copilot-studio (2)_part_48.md |
| **5. Integration** | 5.1 | Connect Flow to Topic | Add Action → Call Flow → Select "SharePoint File Search"<br/>Input Mapping: `SearchQuery` = `EnhancedQuery`<br/>Output Variable: `FileResults` (Text) | 8 min | microsoft-copilot-studio (2)_part_48.md |
| | 5.2 | Display Results | Add Message Node: "Found these relevant files:"<br/>Insert Variable: `FileResults`<br/>Add Message Node: "Need different files? Try rephrasing your search." | 5 min | microsoft-copilot-studio (2)_part_48.md |
| **6. Error Handling** | 6.1 | Handle Empty Results | Add Condition: `FileResults` is empty<br/>True Branch: "No files found. Try different keywords."<br/>False Branch: Display results | 5 min | microsoft-copilot-studio (2)_part_101.md |
| | 6.2 | Permission Validation | Add Message: "Ensure you have read access to SharePoint sites"<br/>Log failed searches for admin review | 2 min | microsoft-copilot-studio (2)_part_101.md |

## JSON Schema for Parse JSON Action

```json
{
    "type": "array",
    "items": {
        "type": "object", 
        "properties": {
            "@@search.score": {"type": "number"},
            "name": {"type": "string"},
            "ServerRedirectedURL": {"type": "string"},
            "LastModifiedTime": {"type": "string"},
            "FileType": {"type": "string"}
        }
    }
}
```

## Power Automate Flow Response Format

```
Apply to Each → List of Rows
Append to Variable: ResultsList
Value: "📄 @{items('Apply_to_each')['name']} 
       🔗 @{items('Apply_to_each')['ServerRedirectedURL']}
       📅 @{items('Apply_to_each')['LastModifiedTime']}"
```

## Implementation Summary

| **Total Time** | **70 minutes** |
|----------------|----------------|
| **Foundation** | 10 minutes |
| **Topic Setup** | 15 minutes |
| **Entity Extraction** | 15 minutes |
| **Power Automate** | 20 minutes |
| **Integration** | 13 minutes |
| **Error Handling** | 7 minutes |

## Key Platform Constraints

| Constraint | Limitation | Source |
|------------|------------|--------|
| **File Size** | 7MB (without M365 Copilot license) / 200MB (with license) | microsoft-copilot-studio (2)_part_24.md |
| **Search Results** | Top 3 results processed by platform | microsoft-copilot-studio (2)_part_101.md |
| **Authentication** | Microsoft Entra ID delegated permissions required | microsoft-copilot-studio (2)_part_101.md |
| **URL Limits** | 4 URLs per generative answers topic node (Classic mode) | microsoft-copilot-studio (2)_part_38.md |

## Quick-Start Validation Checklist

- [ ] Agent created with Microsoft authentication
- [ ] SharePoint scopes configured (`Sites.Read.All`, `Files.Read.All`)
- [ ] Custom topic with entity extraction action
- [ ] Power Automate flow with SharePoint connector
- [ ] JSON parsing implemented with provided schema
- [ ] Variables mapped correctly between topic and flow
- [ ] Error handling for empty results and permissions
- [ ] Test queries return top-5 file links without generative content

**Result:** Pure retrieval agent that extracts entities from user queries and returns relevant SharePoint file links without generative AI overhead.