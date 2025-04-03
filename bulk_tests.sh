#!/bin/bash

# Run all tests using pytest in Codebase/Tests

echo "\n Running all pfSenseManager tests (pytest)"
pytest ./Codebase/Tests/ --disable-warnings "$@"
