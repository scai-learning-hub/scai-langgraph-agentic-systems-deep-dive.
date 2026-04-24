# Deployment Checklist

Use this checklist before shipping the LangGraph API.

## Pre-Deployment Checks

- environment variables configured
- secrets not committed
- request timeout configured
- max iteration limit configured
- request validation enabled
- response schema defined
- retry policy reviewed
- tool failure handling defined
- checkpoint storage plan chosen
- logging enabled
- tracing plan chosen
- rate limiting planned
- cost tracking planned
- human approval points identified
- graph paths tested beyond happy path
- Docker image size reviewed
- CI/CD checks in place
- rollback plan documented

## Why This Matters

Production failures often come from missing operational basics rather than from model quality alone.