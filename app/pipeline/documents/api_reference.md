# Mindria LLM Security Platform: API Reference

## Introduction
The Mindria LLM Security Platform provides a robust, secure, and extensible API for integrating large language model (LLM) auditing and security features into enterprise applications. This document serves as a comprehensive reference for developers, system integrators, and security professionals who wish to leverage Mindria’s API for secure LLM operations, compliance, and monitoring.

---

## Table of Contents
1. Authentication and Authorization
2. API Endpoints
3. Request and Response Formats
4. Error Handling
5. Rate Limiting and Throttling
6. Webhooks and Event Notifications
7. Security Considerations
8. Versioning and Deprecation Policy
9. Example Workflows
10. FAQ and Troubleshooting

---

## 1. Authentication and Authorization
All API requests to Mindria must be authenticated using an API key or OAuth 2.0 token. API keys are managed via the Admin Dashboard and can be scoped to specific roles and permissions. For enterprise deployments, SSO integration is available via SAML and OAuth providers.

### Example: API Key Authentication
```http
GET /v1/audit/logs HTTP/1.1
Host: api.mindria.com
Authorization: Bearer <API_KEY>
```

---

## 2. API Endpoints
### LLM Query Endpoint
- **POST /v1/llm/query**
  - **Description:** Submit a prompt to the LLM for processing.
  - **Request Body:**
    - `prompt` (string): The user’s prompt.
    - `user_id` (string): The user identifier.
    - `context` (object, optional): Additional context for the LLM.
  - **Response:**
    - `response` (string): The LLM’s output.
    - `audit_id` (string): Reference for audit logs.
    - `security_flags` (array): Any security or compliance issues detected.

### Audit Log Retrieval
- **GET /v1/audit/logs**
  - **Description:** Retrieve audit logs for a user, time period, or incident.
  - **Parameters:**
    - `user_id` (optional)
    - `start_time`, `end_time` (optional)
    - `incident_id` (optional)
  - **Response:**
    - `logs` (array): List of audit log entries.

### Policy Management
- **POST /v1/policy/update**
  - **Description:** Update security and compliance policies.
  - **Request Body:**
    - `policy_id` (string)
    - `rules` (object)
  - **Response:**
    - `status` (string)

---

## 3. Request and Response Formats
All requests and responses use JSON. Timestamps are in ISO 8601 format. Large responses are paginated.

### Example Request
```json
{
  "prompt": "Summarize the following document...",
  "user_id": "user-1234",
  "context": {"department": "finance"}
}
```

### Example Response
```json
{
  "response": "The document discusses...",
  "audit_id": "audit-5678",
  "security_flags": ["PII_DETECTED"]
}
```

---

## 4. Error Handling
Mindria uses standard HTTP status codes and provides detailed error messages for troubleshooting.

- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid or missing API key)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error

### Example Error Response
```json
{
  "error": {
    "code": 401,
    "message": "Invalid API key."
  }
}
```

---

## 5. Rate Limiting and Throttling
To ensure fair usage and platform stability, Mindria enforces rate limits on all API endpoints. Rate limits are configurable per customer and can be monitored via the Admin Dashboard. Exceeding the limit results in a 429 error.

---

## 6. Webhooks and Event Notifications
Mindria supports webhooks for real-time event notifications, such as security incidents, policy violations, and audit completions. Webhooks can be configured in the Admin Dashboard.

### Example Webhook Payload
```json
{
  "event": "SECURITY_INCIDENT",
  "timestamp": "2025-06-13T12:34:56Z",
  "details": {
    "user_id": "user-1234",
    "incident_type": "PII_DETECTED",
    "prompt": "..."
  }
}
```

---

## 7. Security Considerations
- All API traffic is encrypted with TLS 1.3.
- Sensitive data is redacted in logs and responses.
- API keys should be rotated regularly.
- Use least-privilege principles when assigning roles.

---

## 8. Versioning and Deprecation Policy
Mindria follows semantic versioning for its API. Deprecated endpoints are supported for at least 12 months before removal. Version information is included in the URL (e.g., `/v1/`).

---

## 9. Example Workflows
### Submitting a Prompt and Retrieving Audit Logs
1. Submit a prompt via `/v1/llm/query`.
2. Receive the LLM response and `audit_id`.
3. Retrieve the audit log for the interaction using `/v1/audit/logs?audit_id=...`.

### Updating a Security Policy
1. Fetch current policies via `/v1/policy/list`.
2. Update a policy with `/v1/policy/update`.
3. Monitor for policy enforcement events via webhooks.

---

## 10. FAQ and Troubleshooting
- **Q:** How do I obtain an API key?
  **A:** API keys are managed in the Admin Dashboard under the “API Keys” section.
- **Q:** What happens if my API key is compromised?
  **A:** Revoke the key immediately in the dashboard and generate a new one.
- **Q:** How do I report a bug or request support?
  **A:** Contact support@mindria.com or use the in-dashboard support chat.

---

## Appendix: OpenAPI Specification
A full OpenAPI (Swagger) specification is available at [https://api.mindria.com/docs](https://api.mindria.com/docs).

For further assistance, contact api-support@mindria.com.

---
