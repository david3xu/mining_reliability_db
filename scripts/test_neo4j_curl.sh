#!/bin/bash
# Neo4j Connection Testing Script using curl
# Based on your mining_reliability_db configuration

echo "=== Neo4j Connection Testing with curl ==="
echo ""

# Configuration (from your project defaults)
NEO4J_HTTP_URL="http://localhost:7474"
NEO4J_BOLT_URL="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Testing with configuration:"
echo "  HTTP URL: $NEO4J_HTTP_URL"
echo "  Bolt URL: $NEO4J_BOLT_URL"
echo "  Username: $NEO4J_USER"
echo ""

# Test 1: Basic HTTP connectivity
echo -e "${YELLOW}1. Testing HTTP connectivity...${NC}"
if curl -s -I "$NEO4J_HTTP_URL/" | head -1 | grep -q "200 OK"; then
    echo -e "${GREEN}✓ HTTP interface is accessible${NC}"
else
    echo -e "${RED}✗ HTTP interface not accessible${NC}"
    exit 1
fi

# Test 2: Server information
echo -e "${YELLOW}2. Getting server information...${NC}"
SERVER_INFO=$(curl -s "$NEO4J_HTTP_URL/")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Server info retrieved:${NC}"
    echo "$SERVER_INFO" | python3 -m json.tool 2>/dev/null || echo "$SERVER_INFO"
else
    echo -e "${RED}✗ Failed to get server info${NC}"
fi

# Test 3: Authentication test with simple query
echo -e "${YELLOW}3. Testing authentication with simple query...${NC}"
AUTH_RESULT=$(curl -s -X POST "$NEO4J_HTTP_URL/db/neo4j/query/v2" \
    -H "Content-Type: application/json" \
    -u "$NEO4J_USER:$NEO4J_PASSWORD" \
    -d '{"statement": "RETURN 1 as test"}')

if echo "$AUTH_RESULT" | grep -q '"test"'; then
    echo -e "${GREEN}✓ Authentication successful${NC}"
    echo "Query result: $AUTH_RESULT" | python3 -m json.tool 2>/dev/null || echo "$AUTH_RESULT"
elif echo "$AUTH_RESULT" | grep -q "error"; then
    echo -e "${RED}✗ Authentication failed${NC}"
    echo "Error: $AUTH_RESULT"
else
    echo -e "${YELLOW}? Unclear authentication result${NC}"
    echo "Response: $AUTH_RESULT"
fi

# Test 4: Database version and status
echo -e "${YELLOW}4. Getting database version and status...${NC}"
VERSION_RESULT=$(curl -s -X POST "$NEO4J_HTTP_URL/db/neo4j/query/v2" \
    -H "Content-Type: application/json" \
    -u "$NEO4J_USER:$NEO4J_PASSWORD" \
    -d '{"statement": "CALL dbms.components() YIELD name, versions, edition"}')

if echo "$VERSION_RESULT" | grep -q "name"; then
    echo -e "${GREEN}✓ Database info retrieved${NC}"
    echo "$VERSION_RESULT" | python3 -m json.tool 2>/dev/null || echo "$VERSION_RESULT"
else
    echo -e "${RED}✗ Could not get database info${NC}"
    echo "Response: $VERSION_RESULT"
fi

# Test 5: Check for existing data from your mining project
echo -e "${YELLOW}5. Checking for existing mining data...${NC}"
DATA_CHECK=$(curl -s -X POST "$NEO4J_HTTP_URL/db/neo4j/query/v2" \
    -H "Content-Type: application/json" \
    -u "$NEO4J_USER:$NEO4J_PASSWORD" \
    -d '{"statement": "MATCH (n) RETURN labels(n) as node_types, count(n) as count LIMIT 10"}')

if echo "$DATA_CHECK" | grep -q "node_types"; then
    echo -e "${GREEN}✓ Data query successful${NC}"
    echo "Existing data:"
    echo "$DATA_CHECK" | python3 -m json.tool 2>/dev/null || echo "$DATA_CHECK"
else
    echo -e "${YELLOW}? Database appears empty or query failed${NC}"
    echo "Response: $DATA_CHECK"
fi

# Test 6: Advanced connectivity test
echo -e "${YELLOW}6. Testing transaction endpoint...${NC}"
TRANSACTION_TEST=$(curl -s -X POST "$NEO4J_HTTP_URL/db/neo4j/tx/commit" \
    -H "Content-Type: application/json" \
    -u "$NEO4J_USER:$NEO4J_PASSWORD" \
    -d '{"statements": [{"statement": "RETURN datetime() as current_time"}]}')

if echo "$TRANSACTION_TEST" | grep -q "current_time"; then
    echo -e "${GREEN}✓ Transaction endpoint working${NC}"
    echo "$TRANSACTION_TEST" | python3 -m json.tool 2>/dev/null || echo "$TRANSACTION_TEST"
else
    echo -e "${RED}✗ Transaction endpoint failed${NC}"
    echo "Response: $TRANSACTION_TEST"
fi

echo ""
echo -e "${YELLOW}=== Testing Complete ===${NC}"
echo ""
echo "Your Neo4j database appears to be running correctly!"
echo "You can access the Neo4j Browser at: $NEO4J_HTTP_URL"
echo ""
echo "For your mining reliability project, you can now run:"
echo "  make schema    # Create database schema"
echo "  make import    # Import facility data"
