#!/bin/bash

# tinycode installation test script
# Version: 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}tinycode - Installation Test${NC}"
echo -e "${BLUE}==========================${NC}"
echo

# Test 1: Check if tinycode is in PATH
echo -e "${YELLOW}Test 1: Checking if tinycode is in PATH...${NC}"
if command -v tinycode &> /dev/null; then
    TINYCODE_PATH=$(which tinycode)
    echo -e "${GREEN}✓ tinycode found at: $TINYCODE_PATH${NC}"
else
    echo -e "${RED}✗ tinycode not found in PATH${NC}"
    echo "This means the installation failed or tinycode is not in your PATH"
    exit 1
fi

# Test 2: Check if tinycode is executable
echo -e "${YELLOW}Test 2: Checking if tinycode is executable...${NC}"
if [[ -x "$TINYCODE_PATH" ]]; then
    echo -e "${GREEN}✓ tinycode is executable${NC}"
else
    echo -e "${RED}✗ tinycode is not executable${NC}"
    exit 1
fi

# Test 3: Check version
echo -e "${YELLOW}Test 3: Checking tinycode version...${NC}"
if tinycode --version &> /dev/null; then
    echo -e "${GREEN}✓ tinycode version command works${NC}"
    tinycode --version
else
    echo -e "${RED}✗ tinycode version command failed${NC}"
    exit 1
fi

# Test 4: Check help
echo -e "${YELLOW}Test 4: Checking tinycode help...${NC}"
if tinycode --help &> /dev/null; then
    echo -e "${GREEN}✓ tinycode help command works${NC}"
else
    echo -e "${RED}✗ tinycode help command failed${NC}"
    exit 1
fi

# Test 5: Check API status
echo -e "${YELLOW}Test 5: Checking API status...${NC}"
if tinycode --check-apis &> /dev/null; then
    echo -e "${GREEN}✓ tinycode API check command works${NC}"
    echo "API Status:"
    tinycode --check-apis
else
    echo -e "${RED}✗ tinycode API check command failed${NC}"
    exit 1
fi

# Test 6: Check configuration
echo -e "${YELLOW}Test 6: Checking configuration...${NC}"
if tinycode --config &> /dev/null; then
    echo -e "${GREEN}✓ tinycode config command works${NC}"
else
    echo -e "${RED}✗ tinycode config command failed${NC}"
    exit 1
fi

# Test 7: Test from different directory
echo -e "${YELLOW}Test 7: Testing from different directory...${NC}"
cd /tmp
if tinycode --version &> /dev/null; then
    echo -e "${GREEN}✓ tinycode works from different directory${NC}"
else
    echo -e "${RED}✗ tinycode failed from different directory${NC}"
    exit 1
fi

# Return to original directory
cd - > /dev/null

echo
echo -e "${GREEN}All tests passed! tinycode is properly installed and working.${NC}"
echo
echo -e "${BLUE}Next steps:${NC}"
echo "1. Configure your API keys:"
echo "   tinycode --set-api-key openai YOUR_OPENAI_KEY"
echo "   tinycode --set-api-key claude YOUR_CLAUDE_KEY"
echo
echo "2. Try it out:"
echo "   tinycode \"list all files in current directory\""
echo
echo -e "${BLUE}Enjoy using tinycode!${NC}" 