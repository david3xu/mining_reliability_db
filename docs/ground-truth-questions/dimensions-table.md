# Dimensions Table for Ground Truth Question Generation
## Extracted from 47 Fields in Mining Reliability Database - Stakeholder Intelligence Focus

| Dimension Name | Source Field(s) | Data Type | Extraction Method | Question Potential | Complexity Level | Stakeholder-Focused Template |
|----------------|-----------------|-----------|-------------------|-------------------|------------------|------------------|
| **Operating Centre** | Operating Centre | Categorical | Direct | Very High | Simple | "What [EQUIPMENT_TYPE] issues have we seen at [FACILITY] before?" |
| **Facility Name** | _facility_name | Categorical | Direct | High | Simple | "Which facility has the best track record with [EQUIPMENT_TYPE] repairs?" |
| **Year** | Initiation Date | Temporal | Date parsing | Very High | Simple | "What immediate actions worked for [EQUIPMENT_TYPE] failures in [YEAR]?" |
| **Month** | Initiation Date | Temporal | Date parsing | High | Intermediate | "Do [EQUIPMENT_TYPE] problems follow seasonal patterns at [FACILITY]?" |
| **Equipment Type** | Title, What happened? | Text Mining | NLP extraction | Very High | Intermediate | "What root causes should I investigate first for [EQUIPMENT_TYPE] failures?" |
| **Equipment Component** | Title, What happened? | Text Mining | NLP extraction | High | Intermediate | "What early warning signs indicate [EQUIPMENT_TYPE] problems are escalating?" |
| **Failure Mode** | Title, What happened? | Text Mining | Pattern matching | High | Intermediate | "How critical are [FAILURE_MODE] issues at [FACILITY] based on history?" |
| **Asset Number** | Asset Number(s) | Categorical | Direct | Medium | Simple | "Should I repair or replace this [EQUIPMENT_TYPE] based on asset history?" |
| **Root Cause Category** | Root Cause | Text Mining | Classification | Very High | Hard | "Which solutions actually worked for [ROOT_CAUSE_TYPE] problems?" |
| **Root Cause Primary** | Root Cause | Text Mining | First item extraction | High | Intermediate | "What are the most common root causes for [EQUIPMENT_TYPE] at [FACILITY]?" |
| **Root Cause Secondary** | Root Cause Tail Extraction | Text Mining | Secondary extraction | High | Hard | "What secondary factors contributed to [EQUIPMENT_TYPE] failures?" |
| **Action Plan Type** | Action Plan | Text Mining | Verb extraction | High | Hard | "What are the most effective action plan types for [EQUIPMENT_TYPE]?" |
| **Immediate Action** | Immd. Contain. Action | Text Mining | Classification | Medium | Intermediate | "What immediate containment actions work best for [FAILURE_MODE]?" |
| **Department Init** | Init. Dept. | Categorical | Direct | Medium | Simple | "Which department should I contact for [EQUIPMENT_TYPE] expertise?" |
| **Department Receiving** | Rec. Dept. | Categorical | Direct | Medium | Simple | "What unique challenges should I expect at [FACILITY] for [EQUIPMENT_TYPE]?" |
| **Stage** | Stage | Categorical | Direct | High | Simple | "What resources and timeline should I plan for [EQUIPMENT_TYPE] repairs?" |
| **Complete Status** | Complete | Categorical | Direct | High | Simple | "What makes [EQUIPMENT_TYPE] repairs successful vs incomplete?" |
| **Effectiveness** | IsActionPlanEffective | Boolean | Direct | Very High | Simple | "Which solutions have proven most effective for [EQUIPMENT_TYPE]?" |
| **Recurring Problem** | Recurring Problem(s) | Boolean | Direct | High | Simple | "How can I prevent recurrence of this [EQUIPMENT_TYPE] problem?" |
| **Past Due Status** | Past Due Status | Categorical | Direct | Medium | Simple | "When should I escalate [EQUIPMENT_TYPE] issues before they become overdue?" |
| **Days Past Due** | Days Past Due | Numerical | Direct | Medium | Intermediate | "What timeline should I plan for [EQUIPMENT_TYPE] to avoid delays?" |
| **Response Time Required** | Requested Response Time | Numerical | Direct | Medium | Intermediate | "How urgently should I treat this [EQUIPMENT_TYPE] failure?" |
| **Amount of Loss** | Amount of Loss | Numerical | Direct | High | Intermediate | "What's the business impact of delaying [EQUIPMENT_TYPE] repairs?" |
| **Action Types** | Action Types | Categorical | Direct | Low | Simple | "What type of action is most appropriate for [EQUIPMENT_TYPE]?" |
| **Categories** | Categories | Categorical | Direct | Medium | Simple | "What category of response does this [EQUIPMENT_TYPE] issue require?" |
| **Strategy Change Required** | Did this action plan require... | Boolean | Direct | Medium | Intermediate | "Will this [EQUIPMENT_TYPE] repair require strategy changes?" |
| **Review Satisfaction** | Is Resp Satisfactory? | Boolean | Direct | Medium | Intermediate | "What makes [EQUIPMENT_TYPE] solutions satisfactory to stakeholders?" |
| **Evidence Present** | Obj. Evidence | Boolean | Null check | Medium | Simple | "What evidence do I need to validate [EQUIPMENT_TYPE] root causes?" |
| **APSS Document** | If yes, APSS Doc # | Categorical | Direct | Low | Simple | "Does this [EQUIPMENT_TYPE] repair require APSS documentation?" |
| **Season** | Initiation Date | Temporal | Date calculation | Medium | Intermediate | "What seasonal factors affect [EQUIPMENT_TYPE] performance at [FACILITY]?" |
| **Day of Week** | Initiation Date | Temporal | Date calculation | Medium | Intermediate | "Do [EQUIPMENT_TYPE] failures happen more on weekends or weekdays?" |
| **Response Duration** | Response Date - Initiation Date | Calculated | Date arithmetic | High | Hard | "What [EQUIPMENT_TYPE] solutions had fastest resolution at [FACILITY]?" |
| **Completion Duration** | Completion Date - Due Date | Calculated | Date arithmetic | High | Hard | "How can I ensure on-time completion for [EQUIPMENT_TYPE] repairs?" |
| **Verification Timeline** | Various verification dates | Calculated | Date arithmetic | Medium | Hard | "What verification process works best for [EQUIPMENT_TYPE] solutions?" |
| **Equipment + Facility** | Equipment Type + Operating Centre | Combined | Cross-dimensional | Very High | Intermediate | "What unique [EQUIPMENT_TYPE] challenges exist at [FACILITY]?" |
| **Equipment + Year** | Equipment Type + Year | Combined | Cross-dimensional | Very High | Intermediate | "How have [EQUIPMENT_TYPE] solutions evolved at [FACILITY] since [YEAR]?" |
| **Facility + Year** | Operating Centre + Year | Combined | Cross-dimensional | High | Intermediate | "What maintenance improvements has [FACILITY] made since [YEAR]?" |
| **Success Rate by Equipment** | Effectiveness + Equipment Type | Calculated | Analytics | Very High | Hard | "What's the most effective long-term approach for [EQUIPMENT_TYPE]?" |
| **Success Rate by Facility** | Effectiveness + Operating Centre | Calculated | Analytics | Very High | Hard | "What successful techniques can I learn from [TOP_PERFORMING_FACILITY]?" |
| **Root Cause + Equipment** | Root Cause + Equipment Type | Combined | Complex analysis | Very High | Hard | "What root cause patterns should I investigate for [EQUIPMENT_TYPE]?" |
| **Action Effectiveness** | Action Plan Type + Effectiveness | Combined | Complex analysis | Very High | Hard | "How can I optimize my [EQUIPMENT_TYPE] repair for best results?" |
| **Cross-Facility Patterns** | Multiple facilities + Equipment | Combined | Pattern analysis | High | Hard | "What innovative [EQUIPMENT_TYPE] solutions have other facilities used?" |
| **Recurrence Prevention** | Recurring + Effectiveness | Combined | Success analysis | High | Hard | "What makes [EQUIPMENT_TYPE] repairs last long-term vs short-term?" |
| **Department Efficiency** | Department + Duration metrics | Combined | Performance analysis | Medium | Hard | "Which department provides fastest [EQUIPMENT_TYPE] expertise?" |
| **Temporal Trends** | Year + Success metrics | Combined | Trend analysis | High | Hard | "How has [EQUIPMENT_TYPE] reliability improved and what's next?" |

## Dimension Categories Summary

| Category | Count | Complexity | Implementation Priority |
|----------|-------|------------|----------------------|
| **Clean Categorical** | 12 | Simple | Phase 1 (Immediate) |
| **Text Mining Required** | 8 | Intermediate-Hard | Phase 2 (2-3 weeks) |
| **Temporal Derived** | 6 | Simple-Intermediate | Phase 1-2 |
| **Numerical Analysis** | 4 | Intermediate | Phase 2 |
| **Boolean/Status** | 5 | Simple | Phase 1 |
| **Cross-Dimensional** | 4 | Intermediate | Phase 2 |
| **Complex Analytics** | 8 | Hard | Phase 3 (1-2 months) |
| **TOTAL** | **47** | **Mixed** | **3 Phases** |

## Ground Truth Question Templates by Dimension Type

| Template Level | Dimensions Used | Templates | Stakeholder Focus |
|----------------|----------------|-----------|-------------------|
| **Simple (5/30)** | Single categorical/boolean | 5 | "What [EQUIPMENT_TYPE] issues have we seen at [FACILITY] before?" |
| **Intermediate (7/30)** | Cross-dimensional + some text mining | 7 | "What root causes should I investigate first for [EQUIPMENT_TYPE] at [FACILITY]?" |
| **Hard (18/30)** | Complex analytics + multi-dimensional | 18 | "What's the most effective long-term approach for [EQUIPMENT_TYPE] [FAILURE_MODE]?" |

## Implementation Notes - Stakeholder Intelligence Focus

- **Phase 1**: Start with actionable templates using categorical dimensions (Operating Centre, Year, Stage, Effectiveness)
  - Focus on immediate problem recognition and expert identification
  - Enable "What should I do?" style questions
- **Phase 2**: Add text mining for equipment-specific intelligence
  - Root cause investigation guidance
  - Solution effectiveness validation  
- **Phase 3**: Implement strategic decision support analytics
  - Cross-facility best practice transfer
  - Long-term optimization strategies
- **Total Available**: 47+ distinct dimensions from 47 fields
- **Template Potential**: Enables generation of 100+ stakeholder-focused question templates
- **Key Insight**: Each dimension now supports actionable intelligence rather than statistical counting

## Stakeholder Value Framework

| Dimension Category | Engineer Need | Template Focus | Business Impact |
|-------------------|---------------|----------------|-----------------|
| **Equipment + Facility** | "Is this normal here?" | Problem recognition | Faster diagnosis |
| **Root Cause + Equipment** | "What should I investigate?" | Diagnostic guidance | Targeted solutions |
| **Effectiveness + Equipment** | "Will this approach work?" | Solution validation | Avoid wasted effort |
| **Cross-Facility** | "Who has solved this?" | Best practice transfer | Knowledge sharing |
| **Temporal + Equipment** | "How has this evolved?" | Strategic planning | Continuous improvement | 