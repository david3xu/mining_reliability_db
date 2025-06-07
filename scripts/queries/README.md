```bash
# Create simple query runner

echo '#!/bin/bash
docker exec -it neo4j-container cypher-shell -u neo4j -p password "$1"' > run_query.sh
chmod +x run_query.sh

# Execute specific excavator queries

./run_query.sh "MATCH (ar:ActionRequest) WHERE toLower(ar.categories) CONTAINS 'excavator' RETURN count(\*)"
```
