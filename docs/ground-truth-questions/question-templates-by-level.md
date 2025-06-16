# Ground Truth Question Templates by Complexity Level
## Maintenance Engineer Perspective - Actionable Intelligence from Historical Data

Based on top 6 dimensions: **Operating Centre, Year, Equipment Type, Root Cause Category, Effectiveness, Solution Intelligence**

---

## SIMPLE LEVEL (5 Templates) - Immediate Problem Context

### Template 1: Equipment Problem Recognition
**"What [EQUIPMENT_TYPE] issues have we seen at [FACILITY] before?"**
- **Purpose**: Help engineer recognize if current problem is familiar
- **Parameters**: EQUIPMENT_TYPE = {gearbox, electrical, pump, crusher, conveyor}
- **Parameters**: FACILITY = {HUN, Pinjarra, Kwinana, WDL, YRN}
- **Stakeholder Value**: "Have we dealt with this gearbox problem at Pinjarra before?"

### Template 2: Immediate Action Guidance  
**"What immediate actions worked for [EQUIPMENT_TYPE] failures in [YEAR]?"**
- **Purpose**: Provide quick action steps based on recent successful cases
- **Parameters**: EQUIPMENT_TYPE = {gearbox, electrical, pump, crusher, conveyor}
- **Parameters**: YEAR = {2023, 2022, 2021, 2020, 2019}
- **Stakeholder Value**: "What should I do right now for this electrical failure?"

### Template 3: Solution Effectiveness Check
**"Which solutions actually worked for [ROOT_CAUSE_TYPE] problems?"**
- **Purpose**: Validate repair approach before investing time/resources
- **Parameters**: ROOT_CAUSE_TYPE = {training, design, material, environmental, maintenance}
- **Stakeholder Value**: "Will replacing this part actually fix the training-related issue?"

### Template 4: Expert Identification
**"Which facility has the best track record with [EQUIPMENT_TYPE] repairs?"**
- **Purpose**: Identify who to contact for expertise and best practices
- **Parameters**: EQUIPMENT_TYPE = {gearbox, electrical, pump, crusher, conveyor}
- **Stakeholder Value**: "Who should I call for help with this gearbox problem?"

### Template 5: Problem Urgency Assessment
**"How critical are [FAILURE_MODE] issues at [FACILITY] based on history?"**
- **Purpose**: Help prioritize response and resource allocation
- **Parameters**: FAILURE_MODE = {electrical burn, vibration, leak, overheating, contamination}
- **Parameters**: FACILITY = {HUN, Pinjarra, Kwinana, WDL, YRN}
- **Stakeholder Value**: "Should I treat this electrical burn as an emergency?"

---

## INTERMEDIATE LEVEL (7 Templates) - Contextual Problem Intelligence

### Template 6: Root Cause Investigation Priority
**"What root causes should I investigate first for [EQUIPMENT_TYPE] failures at [FACILITY]?"**
- **Purpose**: Guide diagnostic efforts toward most likely causes
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "What usually causes gearbox problems specifically at Pinjarra?"

### Template 7: Time-Sensitive Solution Selection
**"What [EQUIPMENT_TYPE] solutions had fastest resolution times in [TIME_PERIOD]?"**
- **Purpose**: Choose repair approach when downtime is critical
- **Parameters**: EQUIPMENT_TYPE + TIME_PERIOD = {last 6 months, 2023, 2022}
- **Stakeholder Value**: "What's the quickest way to fix this pump based on recent successes?"

### Template 8: Location-Specific Risk Intelligence
**"What unique challenges should I expect with [EQUIPMENT_TYPE] repairs at [FACILITY]?"**
- **Purpose**: Prepare for facility-specific complications or requirements
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Are there special considerations for electrical work at HUN?"

### Template 9: Seasonal/Pattern Recognition
**"Do [EQUIPMENT_TYPE] problems follow any patterns at [FACILITY] that I should know about?"**
- **Purpose**: Understand if current problem is part of larger pattern
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Is this pump issue part of a seasonal pattern at Kwinana?"

### Template 10: Resource Planning Intelligence
**"What resources and timeline should I plan for [EQUIPMENT_TYPE] repairs based on successful cases?"**
- **Purpose**: Set realistic expectations and gather needed resources
- **Parameters**: EQUIPMENT_TYPE = {gearbox, electrical, pump, crusher, conveyor}
- **Stakeholder Value**: "How long will this gearbox repair take and what parts do I need?"

### Template 11: Warning Sign Recognition
**"What early warning signs indicate [EQUIPMENT_TYPE] problems are escalating?"**
- **Purpose**: Help engineer monitor situation and prevent bigger failures
- **Parameters**: EQUIPMENT_TYPE = {gearbox, electrical, pump, crusher, conveyor}
- **Stakeholder Value**: "What should I watch for to prevent this electrical issue from getting worse?"

### Template 12: Cross-Equipment Impact Assessment
**"When [EQUIPMENT_TYPE] fails, what other systems are typically affected at [FACILITY]?"**
- **Purpose**: Understand broader operational impact and plan accordingly
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "If this gearbox fails, what else might go down at Pinjarra?"

---

## HARD LEVEL (18 Templates) - Strategic Decision Intelligence

### Template 13: Optimal Solution Strategy
**"What's the most effective long-term approach for [EQUIPMENT_TYPE] [FAILURE_MODE] at [FACILITY]?"**
- **Purpose**: Choose strategy that prevents recurrence, not just quick fix
- **Parameters**: EQUIPMENT_TYPE + FAILURE_MODE + FACILITY combinations
- **Stakeholder Value**: "What's the best way to permanently solve gearbox vibration at Pinjarra?"

### Template 14: Cross-Facility Best Practice Transfer
**"What successful [EQUIPMENT_TYPE] maintenance techniques can I learn from [TOP_PERFORMING_FACILITY]?"**
- **Purpose**: Apply proven methods from high-performing locations
- **Parameters**: EQUIPMENT_TYPE + facility performance rankings
- **Stakeholder Value**: "How does Kwinana achieve better electrical reliability than us?"

### Template 15: Failure Mode Prevention Strategy
**"What preventive actions stop [FAILURE_MODE] in [EQUIPMENT_TYPE] systems?"**
- **Purpose**: Implement prevention rather than reactive repairs
- **Parameters**: FAILURE_MODE + EQUIPMENT_TYPE combinations
- **Stakeholder Value**: "How can I prevent electrical burns in our truck fleet?"

### Template 16: Investment Decision Support
**"Should I repair or replace this [EQUIPMENT_TYPE] based on [FACILITY] historical outcomes?"**
- **Purpose**: Make cost-effective decisions using historical performance data
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Is it worth repairing this old gearbox or should we replace it?"

### Template 17: Risk Escalation Criteria
**"When should I escalate [EQUIPMENT_TYPE] issues at [FACILITY] based on past critical failures?"**
- **Purpose**: Know when to call for help before situation becomes critical
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "At what point does this electrical issue become dangerous?"

### Template 18: Solution Optimization Intelligence
**"How can I optimize my [EQUIPMENT_TYPE] repair to achieve [PERFORMANCE_GOAL] like successful cases?"**
- **Purpose**: Learn from best-performing repairs to exceed standard fixes
- **Parameters**: EQUIPMENT_TYPE + PERFORMANCE_GOAL = {longest MTBF, fastest repair, lowest cost}
- **Stakeholder Value**: "How can I make this gearbox repair last longer than usual?"

### Template 19: Recurrence Prevention Analysis
**"What makes [EQUIPMENT_TYPE] repairs at [FACILITY] successful long-term vs short-term fixes?"**
- **Purpose**: Understand what differentiates lasting solutions from temporary fixes
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Why do some pump repairs at HUN last years while others fail quickly?"

### Template 20: Innovation Opportunity Identification
**"What innovative solutions have other facilities used for chronic [EQUIPMENT_TYPE] problems?"**
- **Purpose**: Find creative approaches when standard methods aren't working
- **Parameters**: EQUIPMENT_TYPE = focus on chronic problem equipment
- **Stakeholder Value**: "Are there new approaches for our recurring conveyor issues?"

### Template 21: Environmental Impact Consideration
**"How do [ENVIRONMENTAL_FACTOR] conditions at [FACILITY] affect [EQUIPMENT_TYPE] failure patterns?"**
- **Purpose**: Understand location-specific factors affecting equipment performance
- **Parameters**: ENVIRONMENTAL_FACTOR + FACILITY + EQUIPMENT_TYPE
- **Stakeholder Value**: "Does the coastal environment at Pinjarra make electrical issues worse?"

### Template 22: Multi-System Failure Chain Analysis
**"What failure chains start with [EQUIPMENT_TYPE] problems and how can I break them?"**
- **Purpose**: Prevent cascading failures by understanding system interdependencies
- **Parameters**: EQUIPMENT_TYPE = {critical system components}
- **Stakeholder Value**: "If this gearbox fails, what cascade failures should I prevent?"

### Template 23: Maintenance Strategy Evolution
**"How has [EQUIPMENT_TYPE] maintenance strategy evolved at [FACILITY] and what's next?"**
- **Purpose**: Understand maintenance approach trends and future direction
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Are we moving toward predictive maintenance for gearboxes?"

### Template 24: Performance Benchmarking
**"How does our [EQUIPMENT_TYPE] reliability at [FACILITY] compare to industry best practices?"**
- **Purpose**: Understand performance gaps and improvement opportunities
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Are our gearbox failure rates at Pinjarra acceptable?"

### Template 25: Training Need Identification
**"What knowledge gaps contributed to [EQUIPMENT_TYPE] failures and how can I address them?"**
- **Purpose**: Identify and address skill/knowledge issues preventing effective maintenance
- **Parameters**: EQUIPMENT_TYPE + failure analysis
- **Stakeholder Value**: "Do I need additional training to properly maintain this electrical system?"

### Template 26: Technology Integration Assessment
**"What role could new technology play in solving our [EQUIPMENT_TYPE] challenges at [FACILITY]?"**
- **Purpose**: Evaluate technology solutions for persistent equipment problems
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Would condition monitoring help with our gearbox issues at Pinjarra?"

### Template 27: Supply Chain Risk Mitigation
**"What supply chain issues affect [EQUIPMENT_TYPE] repairs at [FACILITY] and how can I prepare?"**
- **Purpose**: Anticipate and prepare for parts/service availability issues
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "Should I stock critical gearbox parts due to supply chain delays?"

### Template 28: Legacy System Transition Planning
**"How should I manage the transition from legacy [EQUIPMENT_TYPE] to modern systems?"**
- **Purpose**: Plan equipment modernization while maintaining operational reliability
- **Parameters**: EQUIPMENT_TYPE = {aging equipment types}
- **Stakeholder Value**: "How do I replace old gearboxes without disrupting production?"

### Template 29: Emergency Response Optimization
**"What emergency response protocols work best for [EQUIPMENT_TYPE] critical failures at [FACILITY]?"**
- **Purpose**: Optimize emergency response procedures based on successful crisis management
- **Parameters**: EQUIPMENT_TYPE + FACILITY combinations
- **Stakeholder Value**: "What's our fastest response plan when gearboxes fail during peak production?"

### Template 30: Knowledge Transfer and Documentation
**"How can I capture and share the lessons learned from this [EQUIPMENT_TYPE] repair for future incidents?"**
- **Purpose**: Ensure valuable experience becomes organizational knowledge
- **Parameters**: EQUIPMENT_TYPE + repair complexity
- **Stakeholder Value**: "How do I document this complex gearbox repair so others can learn from it?"

---

## Template Implementation Framework

| Template Type | Stakeholder Need | Information Goal | Action Outcome |
|---------------|------------------|------------------|----------------|
| **Recognition** | "Have I seen this before?" | Problem familiarity | Confidence in approach |
| **Action Guidance** | "What should I do now?" | Immediate steps | Execute proven solution |
| **Solution Validation** | "Will this work?" | Approach confirmation | Avoid wasted effort |
| **Expert Support** | "Who can help?" | Knowledge access | Get expert assistance |
| **Decision Intelligence** | "What's the best choice?" | Strategic guidance | Optimize outcomes |

## Template Quality Criteria

### ✅ Good Template Characteristics:
- **Actionable**: Leads to specific actions
- **Contextual**: Considers facility/equipment specifics  
- **Decision-Supporting**: Helps choose between options
- **Experience-Leveraging**: Uses historical intelligence
- **Problem-Solving Focused**: Addresses real engineer needs

### ❌ Poor Template Characteristics:
- **Statistical Only**: Just provides counts/numbers
- **Generic**: Doesn't consider context
- **Information Without Action**: Data without guidance
- **Academic**: Theoretical rather than practical

This framework provides **30 unique question templates** that generate hundreds of stakeholder-focused questions for copilot evaluation, ensuring the AI provides actionable intelligence rather than just data retrieval. 