# AI-Powered Network Diagnostics & IT Risk Assessment Agent

A University of Houston Computer Information Systems project by Nikhil Varghese.

This project uses an AI agent to investigate why a web service is unavailable and explain what the disruption could mean for the business. The test environment represents a fictional order-entry service. It lets the agent gather real networking evidence and distinguish a DNS lookup failure, a TCP connection failure, and an HTTP error.

## How the agent works

1. **Check DNS.** Query the lab resolver and compare the returned IP address with the expected address.
2. **Test the connection.** Use `curl` to check whether the client can connect to the service and receive an HTTP response.
3. **Verify the diagnosis.** Check the listening socket with `ss` and compare the result with fixture logs or a controlled retest.
4. **Explain the impact.** Report what the evidence supports, what remains uncertain, and what an operator should check next. For the order-entry scenario, describe which business activity could be interrupted and what would confirm the impact.

The agent follows a reusable workflow defined in `SKILL.md`. Each conclusion is tied to a tool result. A successful DNS lookup confirms name resolution at the queried resolver. Service availability requires a separate check.

## Tools and environment

| Tool | Role |
| --- | --- |
| Codex | Follows the diagnostic workflow and interprets results |
| Python | Runs the controlled DNS and HTTP services |
| Node.js | Sends DNS queries directly to the lab resolver |
| `curl` and `ss` | Test the HTTP endpoint and inspect TCP listeners |

The lab runs on IPv4 loopback in Linux. Its findings apply to the test environment and the endpoint under investigation. Any impact on actual order processing would need separate verification.
