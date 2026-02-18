# Security Policy

## Responsible Disclosure Program

At Smallest.AI, the security of our AI models, data pipelines, and infrastructure is a top priority. We appreciate the work of security researchers in making the digital world safer. This policy outlines our process for reporting vulnerabilities and what you can expect from us in return.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

If you believe you have found a security vulnerability in our models, API, or platform, please submit a report to:

- **Email:** [security@smallest.ai]

### What to include in your report:

- A detailed description of the vulnerability.
- Steps to reproduce the issue (PoC scripts, specific prompts used, or API request logs).
- The potential impact (e.g., data leak, model bypass, RCE).
- Any screenshots or videos if applicable.

## Scope

This policy covers:

1.  **Model Security:** Prompt injection, training data poisoning, or membership inference attacks.
2.  **Infrastructure:** Our API endpoints, web dashboard, and cloud environments.
3.  **Library/SDK:** Vulnerabilities within our official client libraries.

### Out of Scope:

- Hallucinations or "incorrect" model outputs that do not bypass safety filters.
- Spam or social engineering.
- Denial of Service (DoS) attacks.

## Our Commitment

If you follow this policy, we commit to:

- **Acknowledgment:** We will acknowledge receipt of your report within [e.g., 48 hours].
- **Investigation:** We will provide a timeline for triage and keep you updated on our progress.
- **Non-Retaliation:** We will not pursue legal action against researchers who act in good faith and follow these guidelines.
- **Credit:** With your permission, we will provide public credit for your discovery once the issue is resolved.

## Security Practices for Users

To keep your integration secure, we recommend:

- **API Key Management:** Never hard-code API keys in client-side code. Use environment variables.
- **Input Sanitization:** Treat AI outputs as untrusted data before rendering them in your application's UI.
- **Least Privilege:** Ensure your service accounts have the minimum permissions necessary to function.

---

_Last Updated: February 18, 2026_
