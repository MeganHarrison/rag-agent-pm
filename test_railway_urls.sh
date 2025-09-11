#!/bin/bash

# Test your Railway URLs after deployment
# Replace these with your actual Railway URLs

echo "🧪 Testing Railway Deployment URLs"
echo "=================================="

# Replace these with your actual Railway URLs from the dashboard
CHAT_API_URL="https://your-rag-agent-api.up.railway.app"
VECTORIZATION_API_URL="https://your-rag-vectorization-api.up.railway.app"

echo "Chat API URL: $CHAT_API_URL"
echo "Vectorization API URL: $VECTORIZATION_API_URL"
echo ""

echo "Testing Chat API health..."
curl -s "$CHAT_API_URL/health" | python -m json.tool

echo ""
echo "Testing Vectorization API health..."
curl -s "$VECTORIZATION_API_URL/health" | python -m json.tool

echo ""
echo "If both return {\"status\":\"healthy\"}, your APIs are working!"
echo "Use these URLs in your Next.js app environment variables."
