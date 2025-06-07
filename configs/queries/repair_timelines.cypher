// Calculate excavator motor repair timelines
MATCH (ar:ActionRequest)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
WHERE {filter_clause}
  AND ap.due_date IS NOT NULL
  AND ap.completion_date IS NOT NULL
WITH ap.action_plan AS repair_type,
     duration.between(
       datetime(head(split(ap.due_date, ' | '))),
       datetime(head(split(ap.completion_date, ' | ')))
     ).days AS repair_duration,
     toFloat(ar.requested_response_time) AS planned_timeline,
     ap.complete AS completion_status
WHERE repair_duration >= 0 AND repair_duration <= 30
RETURN repair_type,
       avg(repair_duration) AS average_days,
       min(repair_duration) AS fastest_completion,
       max(repair_duration) AS longest_completion,
       count(*) AS repair_instances,
       avg(planned_timeline) AS average_planned_days
ORDER BY average_days ASC
