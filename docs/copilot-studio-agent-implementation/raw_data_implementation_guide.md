# Copilot Studio Complete Implementation Guide

## From Agent Creation to Production Deployment

---

## 5. Complete Implementation Guide

### 5.1 Agent Type Selection & Initial Configuration

<details>
<summary><strong>Click to expand: Agent Type Selection & Configuration</strong></summary>

**Decision Matrix**:

```bash
# Custom Agent
USE_CASE = "Multi-channel deployment + full control"
CHANNELS = ["Teams", "Web", "Mobile", "Facebook", "Azure Bot Service"]

# Copilot Agent
USE_CASE = "Microsoft 365 Copilot extension only"
CHANNELS = ["Microsoft 365 Copilot", "Teams"]
```

**Microsoft's Agent Type Definitions**:

> _"A custom agent is an agent a maker builds from scratch. A custom agent can include a wide range of capabilities, including knowledge, actions, and starter prompts. Custom agents can be published to the Microsoft 365 Copilot and Teams channel, but can also be used with other channels."_
>
> **Source**: `microsoft-copilot-studio (2)_part_68.md`

</details>

### 5.2 Description Configuration

<details>
<summary><strong>Click to expand: Description Configuration</strong></summary>

**Microsoft's Constraints**:

> _"The description can have up to 1,000 characters."_
>
> **Source**: `microsoft-copilot-studio (2)_part_12.md`

**Implementation Template**:

```bash
# Description Structure (1,000 char max)
DESCRIPTION_TEMPLATE = "
[CAPABILITY_STATEMENT] + [DATA_SOURCES] + [USER_BENEFIT] + [SCOPE_BOUNDARIES]
"

# Example Implementation - Raw Data Scenario
RAW_DATA_AGENT_DESCRIPTION = "
Historical maintenance record analyzer that searches incident data with basic fields like Incident ID, problem descriptions, solutions applied, completion status, equipment types, and facility information. Helps stakeholders respond to new incidents by finding similar past problems and their solutions through pattern matching and basic filtering for improved decision-making and faster problem resolution.
"

# Example Implementation - Advanced Mining Reliability Database
MINING_AGENT_DESCRIPTION = "
Mining reliability database analyzer that queries historical maintenance records containing 43+ data fields including Action Types, Root Cause analysis, Asset Numbers, Action Plans, and Effectiveness Verification. Uses proven solutions and lessons learned from actual mining operations to support stakeholders during new incidents by providing pattern recognition, solution effectiveness tracking, and resource planning insights for accelerated incident response and improved decision-making quality.
"
```

**Configuration Steps**:

1. Navigate to agent Overview page
2. Select Edit in Details section
3. Enter description following template structure
4. Save and test with representative queries

</details>

### 5.3 General Instructions Configuration

<details>
<summary><strong>Click to expand: General Instructions Configuration</strong></summary>

**Microsoft's Instructions Framework**:

> _"Instructions are the central directions and parameters an agent follows. Agents depend on instructions to: Decide what tool or knowledge might need to be called to address a user query or autonomous trigger. Fill inputs for any tool based on the available context. Generate a response to the end user."_
>
> **Source**: `microsoft-copilot-studio (2)_part_12.md`

**Constraints**:

> _"The instructions can have up to 8,000 characters."_
>
> **Source**: `microsoft-copilot-studio (2)_part_12.md`

**Instructions Template**:

```bash
# Instructions Structure (8,000 char max)
INSTRUCTIONS_TEMPLATE = "
## Primary Goal
[Specific objective and success criteria]

## Conversation Style
[Tone, formality level, response format]

## Tool & Knowledge Selection Logic
- For [scenario type]: Use /[SpecificTool]
- For [data queries]: Access /[DataverseConnection]
- For [document analysis]: Search /[SharePointKnowledge]

## Response Guidelines
- Always include [required elements]
- Format responses as [structure preference]
- Escalate to [fallback method] when [condition]

## Boundaries & Limitations
- Cannot perform [specific exclusions]
- Alternative approach: [redirect strategy]
"
```

**Example Implementation**:

```bash
# Raw Data Instructions Template
RAW_DATA_INSTRUCTIONS = "
## Primary Goal
Analyze historical maintenance records to help stakeholders respond to new incidents by finding similar past problems and their solutions from your knowledge base containing incident records with fields like [LIST_YOUR_KEY_FIELDS].

## Conversation Style
Professional maintenance-focused responses. Provide clear sections for Similar Incidents, Solutions Used, and Success Indicators based on the available historical data.

## Knowledge Source Logic
- For incident queries: Search incident description and problem detail fields
- For solution validation: Look for records marked as 'Complete', 'Effective', or 'Successful'
- For equipment issues: Filter by equipment type, facility, or department fields
- For pattern analysis: Group by similar problem descriptions and solution approaches

## Response Guidelines
- Always include Incident ID, Date, and Facility for reference when available
- Format responses with clear headers: Similar Incidents | Solutions Applied | Success Status
- Include any available completion status, effectiveness indicators, or outcome data
- Reference specific equipment types and facilities for location-relevant insights
- Recommend contacting facility experts when multiple similar incidents found at same location

## Boundaries & Limitations
- Cannot access real-time equipment data (refer to current monitoring systems)
- Cannot determine solution effectiveness without completion/success status fields
- Cannot provide detailed technical analysis without comprehensive root cause data
"

# Advanced Mining Reliability Database Agent Instructions
MINING_INSTRUCTIONS = "
## Primary Goal
Provide stakeholder intelligence by analyzing mining reliability database containing 43+ historical maintenance fields including Action Types, Root Cause analysis, Asset Numbers, Action Plans, and Effectiveness Verification to support decision-making during new incidents with proven solutions and lessons learned from actual mining operations.

## Conversation Style
Professional and data-driven tone suitable for maintenance managers, operations teams, and reliability engineers. Provide structured responses with clear sections for Pattern Recognition, Solution Effectiveness, and Implementation Guidance based on historical evidence.

## Tool & Knowledge Selection Logic
- For incident queries: Use /ReliabilityDatabase filtering by 'Action Types' and 'Categories'
- For solution validation: Access /EffectivenessRecords filtering 'IsActionPlanEffective' = 'Yes'
- For pattern analysis: Search /RootCauseData using 'Root Cause' and 'Recurring Problem(s)' fields
- For asset management: Query /AssetRecords using 'Asset Number(s)' and equipment strategy fields
- For timeline planning: Analyze /ResponseData comparing 'Response Date' vs 'Due Date' patterns

## Response Guidelines
- Always include Action Request Number, Title, and Initiation Date for reference
- Format responses with clear headers: Problem Pattern, Historical Solutions, Implementation Timeline
- Include 'Amount of Loss' and 'Effectiveness Verification' data for business impact context
- Reference specific 'Operating Centre' and 'Stage' for location-relevant insights
- Escalate to maintenance manager when 'Recurring Problem(s)' = 'Yes' and no effective solutions found

## Boundaries & Limitations
- Cannot access real-time equipment sensors (use current monitoring systems)
- Cannot approve action plans (redirect to responsible department per 'Init. Dept.' and 'Rec. Dept.')
- Cannot override equipment management strategy (escalate per APSS documentation requirements)
"
```

**Microsoft's Reference Syntax**:

> _"At any point within the instructions, you can type / to add a reference to a specific object, such as a tool, topic, variable, or Power Fx expression."_
>
> **Source**: `microsoft-copilot-studio (2)_part_12.md`

</details>

### 5.4 Knowledge Sources Integration

<details>
<summary><strong>Click to expand: Knowledge Sources Integration</strong></summary>

**Microsoft's Knowledge Framework**:

> _"After you add one of the following knowledge source types, you're required to provide a name and description. The knowledge name for each source should be unique. The description should be as detailed as possible, especially if generative AI is enabled, as the description aids generative orchestration."_
>
> **Source**: `microsoft-copilot-studio (2)_part_24.md`

**Knowledge Source Search Methods & Priorities**:

**Microsoft's Search Mode Differences**:

> _"How knowledge sources are searched depends on which orchestration mode the agent uses: classic or generative."_
>
> **Source**: `microsoft-copilot-studio (2)_part_24.md`

**Generative Orchestration Search Logic**:

> _"When an agent is configured to use generative orchestration, the following applies: Copilot Studio filters the knowledge sources using an internal GPT based on the description given to the knowledge source. All files uploaded to the agent are searched. For all other knowledge sources, Copilot Studio selects the top four knowledge sources, regardless of type. Those four knowledge sources are searched, in addition to all of the uploaded files."_
>
> **Source**: `microsoft-copilot-studio (2)_part_24.md`

**Classic Orchestration Limits**:

> _"When an agent is configured to use classic orchestration, the following applies: In the Conversational boosting system topic, the number of knowledge sources the agent can search is limited, and depends on the type of knowledge source."_

| Knowledge Source Type    | Classic Mode Limit         | Generative Mode Priority               |
| ------------------------ | -------------------------- | -------------------------------------- |
| **Uploaded Files**       | Unlimited                  | **Always searched** (highest priority) |
| **SharePoint URLs**      | 4 maximum                  | Selected from top 4 sources            |
| **Dataverse Tables**     | 2 sources (15 tables each) | Selected from top 4 sources            |
| **Website URLs**         | 4 maximum                  | Selected from top 4 sources            |
| **Azure OpenAI Service** | 5 maximum                  | Selected from top 4 sources            |
| **Real-time Connectors** | Varies by connector        | Selected from top 4 sources            |

**Source**: `microsoft-copilot-studio (2)_part_24.md`

**6 Knowledge Source Types - Implementation Guide**:

**1. SharePoint (Organizational Documents)**

```bash
# Search Method
SHAREPOINT_SEARCH = {
  "method": "Content indexing in Dataverse",
  "file_types": ["Word", "PowerPoint", "PDF", "Excel"],
  "max_file_size": "32 MB (7 MB without M365 Copilot license)",
  "authentication": "User credentials with permission validation"
}

# Implementation Benefits
SHAREPOINT_BENEFITS = [
  "Live permission checking → Security compliance",
  "Automatic indexing → Fast search response",
  "Native M365 integration → Seamless authentication",
  "Version control support → Current document access"
]
```

**Configuration Example**:

```bash
# SharePoint Knowledge Source Setup
SHAREPOINT_CONFIG = {
  "name": "HR_Policies_SharePoint",
  "description": "Employee handbook, policy documents, and procedure guides from HR SharePoint site including onboarding, benefits, compliance, and safety procedures",
  "url": "contoso.sharepoint.com/sites/HR-Policies",
  "scope": "Site and all subfolders",
  "authentication": "User credentials"
}
```

**2. Dataverse (Structured Business Data)**

```bash
# Search Method
DATAVERSE_SEARCH = {
  "method": "Structured query with synonyms and glossary",
  "data_types": ["Tables", "Multiline text", "File attachments"],
  "max_tables": "15 per knowledge source",
  "reasoning": "Unstructured reasoning over structured data"
}

# Implementation Benefits
DATAVERSE_BENEFITS = [
  "Structured data queries → Precise results",
  "Glossary enhancement → Natural language mapping",
  "Real-time data access → Current information",
  "Power Platform integration → Workflow automation"
]
```

**Configuration Example**:

```bash
# Basic Raw Data Knowledge Source Setup
BASIC_KNOWLEDGE_SOURCES = [
  {
    "name": "Historical_Incident_Records",
    "type": "Dataverse" | "SharePoint" | "File Upload",
    "description": "Historical maintenance incident records containing problem descriptions, solutions applied, completion status, equipment types, and facility information for pattern recognition and solution guidance",
    "key_searchable_fields": ["problem_description", "solution_applied", "equipment_type", "facility_location"],
    "access_method": "Basic text search and filtering"
  },

  {
    "name": "Equipment_Reference_Docs",
    "type": "File Upload",
    "description": "Equipment manuals, maintenance procedures, and troubleshooting guides for [YOUR_EQUIPMENT_TYPES] to supplement historical incident analysis",
    "optimization": "Upload key troubleshooting documents as PDFs for guaranteed search"
  }
]

# Advanced Dataverse Knowledge Source Setup - Mining Reliability Database
DATAVERSE_CONFIG = {
  "name": "Mining_Reliability_Database",
  "description": "Historical mining maintenance records with 43+ data fields including Action Request Numbers, Root Cause analysis, Asset management data, Action Plans, and Effectiveness Verification for stakeholder intelligence and incident response decision-making",
  "tables": ["ReliabilityActions", "RootCauseAnalysis", "AssetManagement", "EffectivenessTracking"],
  "key_fields": ["Action Request Number", "Action Types", "Categories", "Root Cause", "Asset Number(s)", "IsActionPlanEffective", "Amount of Loss"],
  "glossary_terms": [
    "recurring_problem: Equipment or process issue that has occurred multiple times as tracked in 'Recurring Problem(s)' field",
    "action_effectiveness: Success measurement tracked in 'IsActionPlanEffective' field with verification dates",
    "root_cause_tail: Specific failure mode identification from 'Root Cause Tail Extraction' analysis",
    "equipment_management_strategy: Systematic approach changes tracked in APSS, eAM, ASM and BOM systems"
  ]
}
```

**3. File Upload (Specialized Content)**

```bash
# Search Method
FILE_UPLOAD_SEARCH = {
  "method": "Direct content indexing with highest priority",
  "file_types": ["PDF", "Word", "PowerPoint", "Text", "Excel"],
  "processing": "Always searched in both orchestration modes",
  "storage": "Dataverse with full-text indexing"
}

# Implementation Benefits
FILE_UPLOAD_BENEFITS = [
  "Guaranteed search priority → Always included",
  "Specialized content control → Curated knowledge",
  "No external dependencies → Reliable access",
  "Custom document optimization → Tailored responses"
]
```

**Configuration Example**:

```bash
# File Upload Knowledge Source Setup
FILE_UPLOAD_CONFIG = {
  "name": "Safety_Procedures_Manual",
  "description": "Emergency response procedures, equipment operation manuals, safety protocols, and incident response checklists for mining operations",
  "files": ["Emergency_Response_2024.pdf", "Equipment_Manual_Excavators.docx", "Safety_Checklist_Daily.pdf"],
  "optimization": "Pre-processed for mining terminology and safety keywords"
}
```

**4. Public Website (External Reference)**

```bash
# Search Method
WEBSITE_SEARCH = {
  "method": "Web crawling with depth limitations",
  "depth_limit": "2 levels maximum (/subpath/subpath)",
  "content_types": ["HTML pages", "Linked documents"],
  "indexing": "Periodic content refresh"
}

# Implementation Benefits
WEBSITE_BENEFITS = [
  "External expertise access → Industry best practices",
  "Real-time public information → Current regulations",
  "No maintenance overhead → Automatic updates",
  "Broad knowledge coverage → Comprehensive responses"
]
```

**Configuration Example**:

```bash
# Public Website Knowledge Source Setup
WEBSITE_CONFIG = {
  "name": "Mining_Safety_Regulations",
  "description": "Official mining safety regulations, industry standards, and best practice guidelines from government and industry association websites",
  "url": "https://msha.gov/regulations/mining-safety",
  "scope": "Regulations section and safety standards",
  "refresh_frequency": "Weekly content indexing"
}
```

**5. Azure AI Search (Indexed Content)**

```bash
# Search Method
AI_SEARCH_METHOD = {
  "method": "Advanced semantic search with AI ranking",
  "index_types": ["Custom indexes", "Cognitive search results"],
  "search_features": ["Semantic ranking", "Vector search", "Hybrid search"],
  "integration": "Direct Azure AI Search service connection"
}

# Implementation Benefits
AI_SEARCH_BENEFITS = [
  "Advanced search capabilities → Precise relevance",
  "Custom indexing control → Optimized content",
  "Semantic understanding → Context-aware results",
  "Azure ecosystem integration → Unified management"
]
```

**6. Real-time Connectors (Live Data)**

```bash
# Search Method
REALTIME_SEARCH = {
  "method": "Live API calls with authentication",
  "connector_types": ["Salesforce", "ServiceNow", "Confluence", "Zendesk"],
  "data_scope": "Collection level (knowledge bases, not individual articles)",
  "security": "User permission validation per query"
}

# Implementation Benefits
REALTIME_BENEFITS = [
  "Live data access → Current information",
  "Permission inheritance → Security compliance",
  "Multiple system integration → Unified knowledge",
  "Automatic content updates → No manual refresh"
]
```

**Knowledge Source Priority Strategy**:

**Microsoft's Priority Logic**:

> _"Knowledge sources defined in generative answers nodes take priority over knowledge sources at the agent level. Agent level sources function as a fallback."_
>
> **Source**: `microsoft-copilot-studio (2)_part_40.md`

**Optimal Selection Strategy**:

```bash
# Priority Implementation Framework
KNOWLEDGE_PRIORITY = {
  "tier_1_guaranteed": "Uploaded files (always searched)",
  "tier_2_selected": "Top 4 from SharePoint/Dataverse/Websites/AI Search",
  "tier_3_fallback": "Agent-level sources when topic-level unavailable",
  "selection_criteria": "Description quality determines GPT-based filtering"
}

# Strategic Implementation Order
IMPLEMENTATION_SEQUENCE = [
  "1. Upload critical specialized documents (guaranteed search)",
  "2. Connect primary Dataverse tables (structured data priority)",
  "3. Add SharePoint sites (organizational knowledge)",
  "4. Configure external websites (industry references)",
  "5. Integrate real-time connectors (live system data)",
  "6. Add Azure AI Search (advanced semantic capabilities)"
]
```

**Configuration Steps**:

1. Navigate to Knowledge page
2. Select Add knowledge source
3. Choose source type based on data location
4. Provide unique name and detailed description
5. Configure authentication if required
6. Test knowledge source accessibility

**Knowledge Source Suggestions**:

> _"To access a list of the top ten suggested knowledge sources for your agent, select See suggestions on the Add knowledge dialog. From here, you can discover, search, and add sources: Used in one of your previous agents, Used in agents shared with you, Used previously while working with Office products"_
>
> **Source**: `microsoft-copilot-studio (2)_part_24.md`

</details>

### 5.5 Tools Integration

<details>
<summary><strong>Click to expand: Tools Integration</strong></summary>

**Microsoft's Tools Definition**:

> _"Tools are the building blocks that enable your agent to interact with external systems. Tools expand the functionality of your agent, allowing it to perform various actions in response to user requests or autonomous triggers."_
>
> **Source**: `microsoft-copilot-studio (2)_part_44.md`

**7 Tool Types Implementation**:

```bash
# Tool Selection Matrix
TOOL_TYPES = {
  "Prebuilt Connector": "Fastest → Office 365, Dataverse, Teams",
  "Custom Connector": "Power Platform → Proprietary APIs",
  "Agent Flow": "Multi-step → Complex business logic",
  "Prompt": "AI-powered → Text generation/analysis",
  "REST API": "Direct → Web service integration",
  "MCP Tool": "Protocol → External tool servers",
  "Computer Use": "GUI → Legacy system automation"
}
```

**Tool Configuration Process**:

> _"1. Open your agent by choosing Agents in the left hand navigation pane and selecting your agent from the list. 2. Go to the Tools page for the agent. 3. Select Add a tool. 4. In the Add tool pane, select New tool. 5. Select the type of tool you want to add from the list"_
>
> **Source**: `microsoft-copilot-studio (2)_part_44.md`

**Tool Description Critical Factor**:

> _"Generative orchestration relies on this description to determine when your agent should use the tool. Write clear, specific descriptions including what the tool does and when it should be used."_
>
> **Source**: `microsoft-copilot-studio (2)_part_44.md`

**Tool Configuration Template**:

```bash
# Tool Description Structure
TOOL_DESCRIPTION_TEMPLATE = "
[ACTION_CAPABILITY] + [DATA_SOURCE] + [USE_CASES] + [INPUT_REQUIREMENTS] + [OUTPUT_FORMAT]
"
```

**Example Implementations by Tool Type**:

```bash
# Basic Raw Data Tool Configuration Examples
SIMPLE_TOOLS = {
  "Historical_Pattern_Search": {
    "type": "Dataverse" | "REST API",
    "description": "Search historical incident records by problem description keywords to find similar past incidents. Returns incident ID, problem description, solution applied, and completion status. Use when stakeholders need examples of how similar problems were previously resolved.",
    "basic_query": "Filter incidents WHERE problem_description CONTAINS keywords",
    "return_fields": ["incident_id", "date", "facility", "problem_description", "solution_applied", "status"]
  },

  "Solution_Success_Filter": {
    "type": "Dataverse",
    "description": "Filter historical solutions by completion/success status to find proven approaches. Returns only incidents marked as complete, effective, or successful. Use when stakeholders need validated solutions rather than all historical attempts.",
    "basic_query": "Filter incidents WHERE status = 'Complete' OR effective = 'Yes'",
    "return_fields": ["solution_applied", "equipment_type", "facility", "completion_date"]
  },

  "Equipment_Incident_Lookup": {
    "type": "Dataverse",
    "description": "Search incidents by equipment type and facility to find location-specific patterns. Returns equipment-specific incident history for the requesting facility. Use when stakeholders need equipment and location-relevant historical context.",
    "basic_query": "Filter incidents WHERE equipment_type = input AND facility = input",
    "return_fields": ["incident_count", "common_solutions", "typical_resolution_time"]
  }
}

# Advanced Tool Examples - Mining Reliability Database
RELIABILITY_TOOL = {
  "name": "Historical_Solution_Retriever",
  "description": "Queries mining reliability database for proven solutions by filtering 'IsActionPlanEffective' = 'Yes' records. Use when stakeholders need validated action plans for similar incident types. Requires 'Action Types' or 'Categories' keywords. Returns historical Action Plans with Effectiveness Verification data and completion timelines.",
  "type": "Prebuilt Connector",
  "connector": "Dataverse",
  "query_fields": ["Action Types", "Categories", "IsActionPlanEffective", "Action Plan", "Effectiveness Verification"]
}

# REST API Example - Asset Performance Tracking
ASSET_API_TOOL = {
  "name": "Asset_History_Analyzer",
  "description": "Queries reliability database by 'Asset Number(s)' to retrieve maintenance history, recurring problems, and equipment management strategy changes. Use when stakeholders need asset-specific intelligence for decision-making. Requires asset ID or equipment type. Returns complete asset profile with Root Cause patterns and Amount of Loss data.",
  "type": "REST API",
  "endpoint": "api/reliability/asset-history",
  "response_fields": ["Asset Number(s)", "Recurring Problem(s)", "Root Cause", "Amount of Loss", "Equipment Management Strategy"]
}

# Agent Flow Example - Stakeholder Intelligence Report
INTELLIGENCE_FLOW_TOOL = {
  "name": "Stakeholder_Intelligence_Generator",
  "description": "Creates comprehensive stakeholder intelligence reports by collecting pattern recognition data from reliability database fields including Action Types, Root Cause analysis, and solution effectiveness tracking. Use when stakeholders need complete historical context for incident response planning. Requires incident category or problem type. Returns formatted intelligence report with proven solutions and resource planning insights.",
  "type": "Agent Flow",
  "workflow": "Multi-step data collection from 43+ database fields with stakeholder-focused analysis",
  "output_sections": ["Pattern Recognition", "Solution Effectiveness", "Implementation Guidance", "Resource Planning"]
}
```

</details>

### 5.6 Triggers Configuration

<details>
<summary><strong>Click to expand: Triggers Configuration</strong></summary>

**Trigger Types Available**:

```bash
# Microsoft Documented Triggers
TRIGGER_TYPES = [
  "By agent → Generative orchestration selection",
  "Phrases → Classic keyword matching",
  "Activity Received → Channel events",
  "Message → User input processing",
  "Event → External system notifications",
  "On redirect → Topic-to-topic routing",
  "Inactivity → Timeout handling"
]
```

**Example Trigger Configurations**:

```bash
# By Agent Trigger (Generative Mode) - Mining Reliability Database
BY_AGENT_TRIGGER = {
  "name": "Solution_Effectiveness_Analysis",
  "trigger_type": "By agent",
  "description": "Analyzes mining reliability database for proven solutions by filtering 'IsActionPlanEffective' field and correlating with 'Root Cause' patterns. Use when stakeholders need validated action plans, effectiveness verification data, or resource planning insights from historical maintenance records with 43+ data fields.",
  "priority": "High",
  "condition": "User query contains solution validation, proven action plans, or effectiveness verification terms"
}

# Event Trigger (Autonomous Agent) - Asset Management
EVENT_TRIGGER = {
  "name": "Recurring_Problem_Alert",
  "trigger_type": "Event",
  "description": "Automatically triggered when maintenance system detects recurring problems matching 'Recurring Problem(s)' field patterns. Initiates stakeholder intelligence gathering, historical solution retrieval, and equipment management strategy review.",
  "payload_source": "Asset management system",
  "instructions": "When recurring problem detected, query reliability database filtering by 'Asset Number(s)' and 'Root Cause', retrieve effective action plans using /Historical_Solution_Retriever, and generate stakeholder intelligence report with 'Amount of Loss' analysis"
}

# Phrase Trigger (Classic Mode) - Database Query
PHRASE_TRIGGER = {
  "name": "Pattern_Recognition_Topic",
  "trigger_type": "Phrases",
  "phrases": ["similar incidents", "historical patterns", "proven solutions", "action plan effectiveness", "root cause analysis"],
  "priority": "Medium",
  "exact_match": false,
  "database_focus": "Action Types, Categories, Root Cause fields"
}
```

**Event Triggers for Autonomous Agents**:

> _"You can use event triggers to create autonomous agents that respond to events without direct user input."_
>
> **Source**: `microsoft-copilot-studio (2)_part_104.md`

**Configuration Steps**:

1. Navigate to Topics page
2. Select desired topic
3. Hover over Trigger node and select Change trigger
4. Choose appropriate trigger type
5. Configure trigger conditions and priority
6. Test trigger activation scenarios

</details>

### 5.7 Topics Creation & Management

<details>
<summary><strong>Click to expand: Topics Creation & Management</strong></summary>

**Topic Purpose**:
Topics define specific conversation flows and responses within your agent. Each topic represents a discrete capability or conversation path.

**Topic Configuration**:

1. Navigate to Topics page
2. Select Create new topic
3. Choose trigger type (By agent for generative mode)
4. Add topic description for orchestration selection
5. Build conversation flow with message nodes
6. Configure input/output variables
7. Test topic execution

**Microsoft's Topic Flexibility**:

> _"Since an agent configured with generative orchestration can use information from knowledge, actions, and topics to generate a response, you can make your topics more flexible by not sending their final response in a message node, but instead return it as an output variable to the agent."_
>
> **Source**: `microsoft-copilot-studio (2)_part_22.md`

</details>

### 5.8 Suggested Prompts (Starter Prompts)

<details>
<summary><strong>Click to expand: Suggested Prompts (Starter Prompts)</strong></summary>

**Microsoft's Starter Prompts Framework**:

> _"If your agent is meant to be used in Teams or Microsoft 365, you can configure up to six starter prompts to suggest ways your customers can start conversations with the agent. When you use the conversational agent creation experience, Copilot automatically generates starter prompts based on information in the description and instructions for the agent."_
>
> **Source**: `microsoft-copilot-studio (2)_part_4.md`

**Configuration Process**:

> _"To add or update starter prompts: 1. On the Overview page, select the Edit icon at the top of the Starter prompts section. 2. Revise or add titles and prompts, as desired, and select Save when you're done."_
>
> **Source**: `microsoft-copilot-studio (2)_part_4.md`

**Implementation Template**:

```bash
# Basic Raw Data Starter Prompts (adjust field names to match your data)
BASIC_STARTER_PROMPTS = [
  {
    "title": "Find Similar Problems",
    "prompt": "Search for incidents similar to [describe your problem] in historical records"
  },
  {
    "title": "Proven Solutions",
    "prompt": "Show me solutions that were marked as complete or successful for [equipment type] issues"
  },
  {
    "title": "Facility Experience",
    "prompt": "What similar incidents has [facility name] handled successfully?"
  },
  {
    "title": "Equipment History",
    "prompt": "Find maintenance history for [equipment type] showing problem patterns and solutions"
  },
  {
    "title": "Quick Reference",
    "prompt": "Generate incident summary with similar cases and recommended actions"
  }
]

# Advanced Starter Prompts Structure (Max 6)
ADVANCED_STARTER_PROMPTS = [
  "Find recent mining incidents in Q4",
  "Analyze equipment failure patterns",
  "Search safety procedure documents",
  "Get incident resolution recommendations",
  "Compare current vs historical safety data",
  "Generate incident summary report"
]
```

**Example Implementations by Use Case**:

```bash
# Mining Reliability Database Agent Starter Prompts
MINING_RELIABILITY_PROMPTS = [
  {
    "title": "Proven Solutions",
    "prompt": "Find action plans with 'IsActionPlanEffective' = Yes for similar equipment failures"
  },
  {
    "title": "Pattern Recognition",
    "prompt": "Search 'Root Cause' and 'Recurring Problem(s)' fields for failure mode patterns"
  },
  {
    "title": "Asset Intelligence",
    "prompt": "Analyze asset history using 'Asset Number(s)' for maintenance strategy insights"
  },
  {
    "title": "Solution Effectiveness",
    "prompt": "Compare 'Action Plan' completion times with 'Effectiveness Verification' results"
  },
  {
    "title": "Resource Planning",
    "prompt": "Review 'Amount of Loss' and response timeline patterns for budget planning"
  },
  {
    "title": "Stakeholder Report",
    "prompt": "Generate intelligence summary with proven solutions and implementation guidance"
  }
]

# HR Support Agent Starter Prompts
HR_SUPPORT_PROMPTS = [
  {
    "title": "Policy Information",
    "prompt": "Find employee handbook policies about remote work"
  },
  {
    "title": "Benefits Overview",
    "prompt": "Explain health insurance options and enrollment process"
  },
  {
    "title": "Leave Requests",
    "prompt": "How do I submit vacation time and check my balance?"
  },
  {
    "title": "Onboarding Guide",
    "prompt": "Show new employee onboarding checklist and timeline"
  },
  {
    "title": "Performance Review",
    "prompt": "When is my next performance review and what's the process?"
  },
  {
    "title": "Training Programs",
    "prompt": "Find available training programs for professional development"
  }
]
```

</details>

### 5.9 Agent Flows Integration

<details>
<summary><strong>Click to expand: Agent Flows Integration</strong></summary>

**Microsoft's Agent Flows Definition**:

> _"Agent flows offer a powerful way to automate repetitive tasks and integrate your apps and services. Agent flows can be triggered manually, by other automated events or agents, or based on a schedule. With Copilot Studio, you can create agent flows using either natural language or a visual editor."_
>
> **Source**: `microsoft-copilot-studio (2)_part_1.md`

**Flow Creation Methods**:

```bash
# Flow Creation Options
CREATION_METHODS = {
  "Natural Language": "Describe workflow in conversation",
  "Visual Editor": "Drag-and-drop flow designer"
}

# Integration Patterns
INTEGRATION_TYPES = [
  "Standalone automation → Independent execution",
  "Agent tool → Called by agent during conversations",
  "Triggered automation → Event-driven execution"
]
```

**Configuration Steps**:

1. Navigate to Flows page in Copilot Studio
2. Select Create new flow
3. Choose creation method (natural language or visual)
4. Define flow logic and integrations
5. Configure trigger conditions
6. Add flow as tool to agent if needed
7. Test flow execution and agent integration

</details>

### 5.10 Conversational Introduction Configuration

<details>
<summary><strong>Click to expand: Conversational Introduction Configuration</strong></summary>

**Introduction Message Setup**:

> _"Help your agent make a great first impression with a new introductory message. This message lets users know what your agent does and encourages them to interact with your agent."_
>
> **Source**: `microsoft-copilot-studio (2)_part_4.md`

**Microsoft's Configuration Process**:

> _"1. In the Test your agent chat, select your agent's introductory message. The Conversation Start topic opens, and the Message node for your introductory message is in focus. 2. In the Message box, select the text of the message. 3. Replace the default message with your own."_
>
> **Source**: `microsoft-copilot-studio (2)_part_4.md`

**Introduction Template**:

```bash
# Introduction Message Structure
INTRO_TEMPLATE = "
Hello, I'm [AGENT_NAME], your [PURPOSE] assistant.

I can help you:
- [PRIMARY_CAPABILITY_1]
- [PRIMARY_CAPABILITY_2]
- [PRIMARY_CAPABILITY_3]

Try asking: '[EXAMPLE_QUERY]' or use the suggested prompts below.
"
```

**Example Implementations by Domain**:

```bash
# Basic Introduction for Raw Data Agent
SIMPLE_INTRO = "
Hello, I'm MaintenanceBot, your historical incident analysis assistant.

I can help you by searching our maintenance records for:
- Similar problems and how they were resolved
- Solutions that were marked as successful or complete
- Equipment-specific incident patterns at your facility
- Quick reference for common maintenance issues

Try asking: 'Find similar pump problems at Building A' or 'Show successful solutions for conveyor belt issues'
"

# Mining Reliability Database Agent Introduction
MINING_RELIABILITY_INTRO = "
Hello, I'm ReliabilityBot, your mining reliability database intelligence assistant.

I can help you:
- Find proven solutions by filtering 'IsActionPlanEffective' records
- Analyze patterns using 'Root Cause' and 'Recurring Problem(s)' data
- Track asset history through 'Asset Number(s)' and management strategy changes
- Generate stakeholder intelligence reports with effectiveness verification

Try asking: 'Show me effective action plans for similar equipment failures' or use the suggested prompts below.
"

# HR Support Agent Introduction
HR_INTRO = "
Hello, I'm HRAssist, your employee support specialist.

I can help you:
- Find HR policies and employee handbook information
- Explain benefits enrollment and leave processes
- Guide you through onboarding and training programs
- Answer questions about performance reviews and career development

Try asking: 'How do I submit a vacation request?' or use the suggested prompts below.
"

# IT Helpdesk Agent Introduction
IT_INTRO = "
Hello, I'm TechSupport, your IT helpdesk assistant powered by organizational knowledge.

I can help you:
- Troubleshoot common software and hardware issues
- Guide you through system access and password resets
- Find technical documentation and setup procedures
- Connect you with specialized support for complex problems

Try asking: 'How do I connect to the VPN?' or use the suggested prompts below.
"
```

</details>

### 5.11 Testing & Validation Framework

<details>
<summary><strong>Click to expand: Testing & Validation Framework</strong></summary>

**Microsoft's Testing Philosophy**:

> _"The best way to improve your agent? Test it. Make some changes. Test it again. Repeat."_
>
> **Source**: `microsoft-copilot-studio (2)_part_4.md`

**Testing Process**:

> _"1. Start by testing how your agent currently responds in the test chat. Ask your agent a question. 2. Go to the Overview page, and update the instructions for your agent to use a different tone. 3. Test your agent's new instructions with another question. How has the response changed?"_
>
> **Source**: `microsoft-copilot-studio (2)_part_4.md`

**Validation Checklist**:

```bash
# Component Testing Sequence
TESTING_PHASES = [
  "Description accuracy → Correct agent selection",
  "Instructions compliance → Proper tone and format",
  "Knowledge source access → Data retrieval validation",
  "Tool execution → Action completion verification",
  "Topic flow → Conversation path testing",
  "Integration testing → End-to-end workflow validation"
]

# Test Query Categories
TEST_SCENARIOS = [
  "Simple information requests",
  "Multi-step complex queries",
  "Out-of-scope boundary testing",
  "Error condition handling",
  "Authentication flow validation"
]
```

</details>

### 5.12 Publication & Deployment Strategy

<details>
<summary><strong>Click to expand: Publication & Deployment Strategy</strong></summary>

**Channel Selection Matrix**:

```bash
# Custom Agent Deployment Options
CUSTOM_AGENT_CHANNELS = [
  "Microsoft Teams → Internal org deployment",
  "Web integration → Customer-facing websites",
  "Mobile apps → Native app integration",
  "Microsoft 365 Copilot → Enterprise integration",
  "Azure Bot Service → Multi-channel distribution"
]

# Copilot Agent Deployment
COPILOT_AGENT_CHANNELS = [
  "Microsoft 365 Copilot → Primary integration",
  "Microsoft Teams → Direct team access"
]
```

**Publication Process**:

1. Complete all testing phases
2. Review security and compliance settings
3. Select target deployment channels
4. Configure authentication requirements
5. Publish agent to selected channels
6. Monitor performance and user feedback
7. Iterate based on analytics data

</details>

### 5.13 Performance Monitoring & Analytics

<details>
<summary><strong>Click to expand: Performance Monitoring & Analytics</strong></summary>

**Microsoft's Analytics Framework**:

> _"The Analytics page in Copilot Studio provides an aggregated insight into the overall health of your agent with event triggers across analytics sessions."_
>
> **Source**: `microsoft-copilot-studio (2)_part_96.md`

**Key Metrics to Monitor**:

```bash
# Performance Indicators
ANALYTICS_METRICS = [
  "Knowledge source usage → Content effectiveness",
  "Action completion rates → Tool reliability",
  "User satisfaction scores → Response quality",
  "Error rates → System stability",
  "Session duration → User engagement"
]
```

</details>

---

## Quick-Start Implementation Sequence

<details>
<summary><strong>Click to expand: Raw Data Implementation Priority</strong></summary>

### 🔧 **Implementation Priority for Raw Data**

### **Phase 1: Basic Pattern Matching (Week 1)**

```bash
# Day 1-2: Core Data Fields Identification
1. ✅ Map your raw data to business value categories (Step 1)
2. ✅ Upload key incident records as **File Upload** knowledge source (guaranteed search)
3. ✅ Configure basic instructions focusing on text search capabilities (Step 2)

# Day 3-5: Basic Tool Setup
4. ✅ Create simple **Historical_Pattern_Search** tool for text matching (Step 4)
5. ✅ Configure basic knowledge sources for incident records (Step 3)
6. ✅ Test with 5-10 representative queries
```

### **Phase 2: Field-Specific Search (Week 2)**

```bash
# Day 1-3: Advanced Knowledge Sources
7. ✅ Add **Dataverse** connection if records are in structured tables
8. ✅ Create field-specific tools (equipment lookup, facility filtering)
9. ✅ Configure basic escalation logic (Step 6)

# Day 4-5: User Interface Optimization
10. ✅ Add starter prompts based on your actual field names (Step 5)
11. ✅ Set up simple introduction message (Step 7)
12. ✅ Test escalation triggers with your data patterns
```

### **Phase 3: Success Filtering & Deployment (Week 3)**

```bash
# Day 1-3: Solution Validation
13. ✅ Identify your "success indicator" fields (Complete, Effective, Status, etc.)
14. ✅ Create **Solution_Success_Filter** tool to find proven approaches
15. ✅ Add business context based on available completion/outcome data

# Day 4-5: Production Deployment
16. ✅ Deploy and gather user feedback
17. ✅ Monitor basic analytics
18. ✅ Build incrementally based on user patterns
```

</details>

<details>
<summary><strong>Click to expand: Advanced Implementation for Sophisticated Systems</strong></summary>

### **Advanced Implementation for Sophisticated Systems**

### Phase 1: Foundation (Week 1)

```bash
# Day 1-2: Agent Creation & Core Configuration
1. Select agent type (Custom vs Copilot)
2. Configure description (1,000 char)
3. Write instructions (8,000 char)
4. Set up introduction message

# Day 3-5: Data Integration
5. Add knowledge sources (priority order)
6. Configure authentication
7. Test knowledge accessibility
```

### Phase 2: Capability Building (Week 2)

```bash
# Day 1-3: Tools & Actions
8. Add priority tools (prebuilt connectors first)
9. Configure tool descriptions
10. Test tool execution

# Day 4-5: Conversation Design
11. Create essential topics
12. Configure triggers
13. Set up starter prompts
```

### Phase 3: Testing & Deployment (Week 3)

```bash
# Day 1-3: Validation
14. Execute testing checklist
15. Validate all integration points
16. Performance optimization

# Day 4-5: Production Deployment
17. Configure security settings
18. Publish to target channels
19. Enable analytics monitoring
20. User training and feedback collection
```

</details>

## 🎯 **Key Success Factors for Raw Data**

1. **Start Simple**: Focus on basic text search before advanced intelligence
2. **Know Your Fields**: Map your actual field names to business value categories
3. **Leverage File Upload**: Upload critical documents as PDFs for guaranteed search priority
4. **Use Available Status Fields**: Even basic "Complete/Incomplete" provides solution validation
5. **Build Incrementally**: Add sophistication as you understand user patterns

With raw data, you can still provide **valuable historical intelligence** - just focus on pattern matching and basic filtering rather than advanced analytics! 🚀

**Advanced System Success Criteria**:

- Agent selection accuracy >90%
- Response time <5 seconds
- User satisfaction >8/10
- Knowledge source utilization >70%
- Tool execution success rate >95%

---

_All implementation steps based on Microsoft Copilot Studio official documentation with proper citations from project knowledge sources._
