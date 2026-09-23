# Vulnerability Template: SQL Injection (SQLi)

## Raw HTTP Request
POST /login.php HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

username=admin'%20OR%201=1--&password=password

## Analyst Context
This log captures a classic SQL Injection authentication bypass attempt. The characters `' OR 1=1--` are designed to always evaluate as true and comment out the rest of the query, potentially letting the attacker log in without valid credentials. An analyst should flag single quotes, `OR`/`UNION` keywords, and comment markers (`--`, `#`, `/*`) appearing in fields that expect plain text, and check the corresponding response for a successful login, a SQL error message, or an unusually long response time (a sign of blind/time-based SQLi).

---

# Vulnerability Template: Cross-Site Scripting (XSS)

## Raw HTTP Request
GET /search.php?q=<script>alert(document.cookie)</script> HTTP/1.1
Host: target.local

## Analyst Context
This log shows a Reflected Cross-Site Scripting vector targeting the query parameter of a search page. The `<script>` tag attempting to access `document.cookie` indicates an attempt at session hijacking. An analyst should look for HTML/JS special characters (`<`, `>`, `"`, `'`) that are not URL-encoded in request parameters, then check whether the response reflects that input back unescaped into the page body, which confirms the payload wasn't sanitized.

---

# Vulnerability Template: OS Command Injection

## Raw HTTP Request
GET /ping.php?host=127.0.0.1;cat%20/etc/passwd HTTP/1.1
Host: target.local

## Analyst Context
This log shows an attempt to chain a second, unauthorized shell command onto a legitimate network utility call using a command separator (`;`, `|`, `&&`, or backticks). The presence of filesystem paths like `/etc/passwd` or Windows equivalents (`C:\Windows\System32`) in a parameter meant to hold a hostname is a strong indicator. An analyst should check the response for command output that wouldn't normally be returned by a ping utility, such as file contents or system information.

---

# Vulnerability Template: Path Traversal

## Raw HTTP Request
GET /download.php?file=../../../../etc/passwd HTTP/1.1
Host: target.local

## Analyst Context
This log shows a directory traversal attempt using repeated `../` sequences to escape the intended download directory and reach sensitive system files. Analysts should watch for encoded variants as well (`%2e%2e%2f`, `..%252f`, or backslash traversal on Windows systems) since attackers often obfuscate the payload to bypass naive filters. A 200 OK response containing file contents outside the expected directory confirms exploitation.

---

# Vulnerability Template: Server-Side Request Forgery (SSRF)

## Raw HTTP Request
POST /fetch-avatar.php HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

url=http://169.254.169.254/latest/meta-data/iam/security-credentials/

## Analyst Context
This log shows an application-side fetch feature being redirected toward the cloud metadata service endpoint (`169.254.169.254`), a common SSRF target used to steal cloud IAM credentials. Analysts should flag any user-supplied URL parameter pointing to internal IP ranges (`127.0.0.1`, `10.x.x.x`, `192.168.x.x`, `169.254.x.x`) or to `file://`, `gopher://`, or `dict://` schemes, and review the response for internal data that shouldn't be reachable from the public internet.

---

# Vulnerability Template: XML External Entity Injection (XXE)

## Raw HTTP Request
POST /import.php HTTP/1.1
Host: target.local
Content-Type: application/xml

<?xml version="1.0"?>
<!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<data>&xxe;</data>

## Analyst Context
This log shows an XML payload defining an external entity that points to a local file path. When the parser resolves `&xxe;`, it can leak file contents back into the application's response. Analysts should treat any `<!DOCTYPE` declaration containing `SYSTEM` or `PUBLIC` keywords in incoming XML as suspicious, especially when paired with `file://`, `http://`, or `expect://` URIs, and check whether the response echoes back file contents or internal data.

---

# Vulnerability Template: Cross-Site Request Forgery (CSRF)

## Raw HTTP Request
POST /account/update-email HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded
Cookie: session=abc123def456
Referer: http://evil-attacker-site.com/exploit.html

new_email=attacker@evil.com

## Analyst Context
This log shows a state-changing request originating from a third-party domain (`evil-attacker-site.com`) via the Referer header, but still carrying a valid session cookie. This pattern is typical of CSRF, where a victim is tricked into submitting a forged form while authenticated. Analysts should check whether the request included an anti-CSRF token; its absence, combined with a suspicious or mismatched Origin/Referer header, is a strong indicator.

---

# Vulnerability Template: Insecure Direct Object Reference (IDOR)

## Raw HTTP Request
GET /api/invoices/1042 HTTP/1.1
Host: target.local
Cookie: session=abc123def456

## Analyst Context
This log shows a request for a resource identified by a simple, sequential numeric ID. IDOR is suspected when a low-privileged, authenticated user successfully retrieves a record (like an invoice, order, or profile) that does not belong to them, simply by incrementing or guessing the ID. Analysts should correlate the session/account making the request against the ownership of the record in the response, and watch for rapid sequential requests (1041, 1042, 1043...) which suggest automated enumeration.

---

# Vulnerability Template: Open Redirect

## Raw HTTP Request
GET /logout?redirect=https://evil-attacker-site.com/phishing-page HTTP/1.1
Host: target.local

## Analyst Context
This log shows a redirect parameter pointing to an external, untrusted domain instead of a relative path within the application. Attackers abuse this to make phishing links appear to originate from a trusted domain before bouncing the victim elsewhere. Analysts should flag any `redirect`, `url`, `next`, or `return` parameter containing a full external URL, and check the response for a 3xx status with a `Location` header pointing off-domain.

---

# Vulnerability Template: LDAP Injection

## Raw HTTP Request
POST /directory-search.php HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

username=*)(uid=*))(|(uid=*

## Analyst Context
This log shows LDAP filter metacharacters (`*`, `)`, `(`, `|`) injected into a directory search field to alter the logic of the underlying LDAP query, potentially returning all directory entries or bypassing authentication. Analysts should flag unescaped LDAP special characters in fields tied to user lookups, and check whether the response returns an unexpectedly large or unfiltered result set.

---

# Vulnerability Template: Server-Side Template Injection (SSTI)

## Raw HTTP Request
GET /greet?name={{7*7}} HTTP/1.1
Host: target.local

## Analyst Context
This log shows a template expression (`{{7*7}}`) submitted in a field that is normally just displayed as text. If the response contains `49` instead of the literal string `{{7*7}}`, it confirms the input is being evaluated by the server-side template engine, which can often be escalated to remote code execution. Analysts should watch for template syntax across engines (`{{ }}`, `${ }`, `<%= %>`) in any user-controlled field.

---

# Vulnerability Template: Insecure Deserialization

## Raw HTTP Request
POST /api/session HTTP/1.1
Host: target.local
Content-Type: application/x-java-serialized-object

rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3Rvcko

## Analyst Context
This log shows a raw serialized Java object (recognizable by the `rO0AB` base64/binary signature) submitted as request data. If the receiving endpoint deserializes this without validation, a crafted object graph can trigger remote code execution during deserialization. Analysts should flag serialized object signatures in unexpected contexts (Java `rO0`, PHP `O:`, Python pickle opcodes) and treat any endpoint accepting such formats from untrusted clients as high-risk.

---

# Vulnerability Template: NoSQL Injection

## Raw HTTP Request
POST /login HTTP/1.1
Host: target.local
Content-Type: application/json

{"username": "admin", "password": {"$ne": null}}

## Analyst Context
This log shows a JSON body using a MongoDB query operator (`$ne`) instead of a plain string value for the password field, attempting to bypass authentication by matching any password that is "not equal to null." Analysts should flag request bodies where fields expected to be simple strings instead contain operator objects (`$ne`, `$gt`, `$regex`, `$where`), and check whether the response indicates a successful login despite no valid credentials being supplied.

---

# Vulnerability Template: HTTP Host Header Injection

## Raw HTTP Request
POST /password-reset HTTP/1.1
Host: evil-attacker-site.com
Content-Type: application/x-www-form-urlencoded

email=victim@example.com

## Analyst Context
This log shows a password-reset request where the Host header has been altered to an attacker-controlled domain. If the application uses this header to build the reset link sent by email, the victim receives a link pointing to the attacker's server, leaking the reset token. Analysts should compare the Host header against the application's expected domain list and flag any mismatch, especially on endpoints that generate absolute URLs or emails.

---

# Vulnerability Template: Broken Authentication (Credential Stuffing)

## Raw HTTP Request
POST /login.php HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded
X-Forwarded-For: 203.0.113.45

username=jsmith@example.com&password=Winter2025!

## Analyst Context
This log on its own looks like a normal login attempt, so credential stuffing is identified through volume and pattern rather than a single request: many login attempts in a short window, from a small set of IPs or rotating proxies, cycling through large username lists paired with either the same password or breach-list variants (e.g., `Winter2025!`, `Winter2026!`). Analysts should correlate failed-login rate, source IP reputation, and username enumeration patterns across the log rather than judging any single request in isolation.

---

# Vulnerability Template: Security Misconfiguration (Verbose Error Disclosure)

## Raw HTTP Request
GET /product.php?id=abc HTTP/1.1
Host: target.local

## Analyst Context
This log shows a deliberately malformed parameter (a string where an integer ID is expected) used to trigger an unhandled error. The request itself is unremarkable; the finding is in the response, which may return a full stack trace, database connection string, or internal file path instead of a generic error page. Analysts should treat any 500-series response that leaks framework names, file paths, or query fragments as a misconfiguration that also aids further attacks like SQL injection.

---

# Vulnerability Template: Session Fixation

## Raw HTTP Request
GET /login.php?PHPSESSID=attackerfixedsession123 HTTP/1.1
Host: target.local

## Analyst Context
This log shows an attacker pre-setting a known session identifier before the victim authenticates. If the application accepts the attacker-supplied session ID and does not regenerate it after login, the attacker can reuse `attackerfixedsession123` afterward to ride the victim's authenticated session. Analysts should check whether the session identifier changes between the pre-login and post-login response, and flag applications where it remains constant across the authentication boundary.

---

# Vulnerability Template: HTTP Request Smuggling

## Raw HTTP Request
POST / HTTP/1.1
Host: target.local
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED

## Analyst Context
This log shows conflicting length-specification headers (`Content-Length` and `Transfer-Encoding: chunked` both present), which front-end and back-end servers may parse differently, allowing a second, hidden request to be smuggled through and interpreted separately by the back-end. Analysts should flag any request containing both headers simultaneously, and review downstream logs for requests that appear to have been split or misrouted to the wrong handler.

---

# Vulnerability Template: XPath Injection

## Raw HTTP Request
POST /user-lookup.php HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

username=' or '1'='1&password=' or '1'='1

## Analyst Context
This log shows classic boolean-based injection syntax (`' or '1'='1`) submitted to a field backed by an XPath query against an XML data store rather than a SQL database. The always-true condition can bypass authentication checks or return unintended nodes from the XML document. Analysts should flag quote-and-boolean patterns in fields backed by XML/XPath data sources and confirm exploitation by checking whether the response returns data for a user that shouldn't match the supplied credentials.

---

# Vulnerability Template: Unrestricted File Upload

## Raw HTTP Request
POST /upload.php HTTP/1.1
Host: target.local
Content-Type: multipart/form-data; boundary=----WebKitBoundary

------WebKitBoundary
Content-Disposition: form-data; name="file"; filename="shell.php.jpg"
Content-Type: image/jpeg

<?php system($_GET['cmd']); ?>
------WebKitBoundary--

## Analyst Context
This log shows a file upload disguising a server-side script (PHP code) behind an image-like filename and a spoofed `Content-Type` of `image/jpeg`. If the server trusts the extension or MIME type without validating actual file content, the uploaded file can be executed later for remote code execution. Analysts should flag uploads where the declared Content-Type doesn't match the file's actual signature/magic bytes, and treat double extensions (`.php.jpg`) or script tags inside "image" uploads as high-severity findings.

---

# Vulnerability Template: CRLF Injection / HTTP Response Splitting

## Raw HTTP Request
GET /redirect?url=/home%0d%0aSet-Cookie:%20admin=true HTTP/1.1
Host: target.local

## Analyst Context
This log shows encoded carriage-return/line-feed sequences (`%0d%0a`) injected into a parameter that gets reflected into a response header, allowing the attacker to inject an arbitrary additional header (here, a forged cookie) or split the response into two. Analysts should flag `%0d%0a`, `\r\n`, or raw newline characters in any parameter that influences redirects or headers, and inspect the raw response for unexpected extra headers.

---

# Vulnerability Template: Clickjacking

## Raw HTTP Request
GET /account/transfer-funds HTTP/1.1
Host: target.local
Cookie: session=abc123def456

## Analyst Context
Clickjacking isn't identified from the request but from the response: this sensitive page is loaded without an `X-Frame-Options` or `Content-Security-Policy: frame-ancestors` header, meaning it can be embedded in an invisible iframe on an attacker's site and tricked into accepting clicks. Analysts should check response headers on any state-changing page for the presence and value of these headers, and flag their absence as a finding even though the underlying request itself looks completely legitimate.

---

# Vulnerability Template: Business Logic Abuse (Race Condition)

## Raw HTTP Request
POST /api/redeem-coupon HTTP/1.1
Host: target.local
Content-Type: application/json
Cookie: session=abc123def456

{"coupon_code": "SAVE50"}

## Analyst Context
This log shows a single, unremarkable coupon redemption request; the vulnerability surfaces when many identical requests appear with near-identical timestamps (millisecond-level clustering) from the same session, indicating an attacker fired concurrent parallel requests to redeem a single-use coupon multiple times before the balance/usage check could commit. Analysts should look at request timing clusters and correlate them against the account's resulting balance or redemption count to confirm whether the logic was bypassed.

---

# Vulnerability Template: JWT "alg:none" Signature Bypass

## Raw HTTP Request
GET /api/admin/users HTTP/1.1
Host: target.local
Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.

## Analyst Context
This log shows a JWT whose base64-decoded header reads `{"alg":"none","typ":"JWT"}` and whose signature segment after the final period is empty. Some poorly configured verification libraries accept this and trust the claims (here, `role: admin`) without checking any signature at all. Analysts should decode the header segment of bearer tokens seen in logs and flag `"alg":"none"`, algorithm-confusion cases where a token is signed with a symmetric algorithm the server expected to be asymmetric, or unusually short/blank signature segments, then check whether the corresponding response reflects privileged access that shouldn't be granted to an unverified token.

---

# Vulnerability Template: Mass Assignment

## Raw HTTP Request
PATCH /api/users/482 HTTP/1.1
Host: target.local
Cookie: session=abc123def456
Content-Type: application/json

{"display_name": "Jane", "isAdmin": true}

## Analyst Context
This log shows a profile-update request that includes an `isAdmin` field the client-facing form was never meant to expose, alongside a legitimate field like `display_name`. If the backend binds the entire JSON body directly to an internal object/model without an explicit allow-list of editable fields, the extra property can silently grant elevated privileges. Analysts should compare submitted JSON keys against the documented/expected fields for that endpoint, and flag any request containing privileged-sounding properties (`isAdmin`, `role`, `balance`, `verified`) that a normal UI form wouldn't generate, then confirm impact by checking whether the field's value actually changed in a follow-up request.

---

# Vulnerability Template: GraphQL Introspection & Batching Abuse

## Raw HTTP Request
POST /graphql HTTP/1.1
Host: target.local
Content-Type: application/json

{"query": "query { __schema { types { name fields { name } } } }"}

## Raw HTTP Response
HTTP/1.1 200 OK
Content-Type: application/json

{"data":{"__schema":{"types":[{"name":"User","fields":[{"name":"id"},{"name":"email"},{"name":"passwordHash"}]}]}}}

## Analyst Context
This log shows an introspection query being used to enumerate the entire GraphQL schema, including field names that hint at sensitive internal data (`passwordHash`) that likely shouldn't be queryable at all, let alone discoverable. Analysts should flag `__schema` or `__type` introspection queries reaching production endpoints, since introspection is normally disabled outside development. A related pattern to watch for is query batching or deeply nested queries sent in a single request, often used to brute-force login mutations or cause resource-exhaustion denial of service by bypassing simple rate limits that only count HTTP requests rather than the number of operations inside them.

---

# Vulnerability Template: Prototype Pollution

## Raw HTTP Request
POST /api/settings/update HTTP/1.1
Host: target.local
Content-Type: application/json

{"__proto__": {"isAdmin": true}}

## Analyst Context
This log shows a JSON body targeting the `__proto__` key, an attempt to pollute the base JavaScript Object prototype so that every object in the application inherits the injected property (`isAdmin: true`) afterward. This is especially dangerous in Node.js backends that recursively merge user input into configuration or settings objects without checking for these reserved keys. Analysts should flag `__proto__`, `constructor`, or `prototype` appearing as JSON keys in any request body, since legitimate clients never need to submit them, and check whether unrelated, unauthenticated requests afterward start behaving as if privileged (a sign the pollution affected shared application state).

---

# Vulnerability Template: Subdomain Takeover

## Raw HTTP Request
GET / HTTP/1.1
Host: old-campaign.target.local

## Raw HTTP Response
HTTP/1.1 404 Not Found
Content-Type: text/html

<h1>NXDOMAIN</h1><p>This domain is not configured. Sign up at cloudservice.example to claim it.</p>

## Analyst Context
This log shows a request to a subdomain that still has an active DNS CNAME record pointing at a third-party cloud service, but the corresponding resource on that service was deleted or never claimed, evidenced by a "not configured, sign up to claim" style response. An attacker who registers the same resource name on the cloud provider can then serve arbitrary content, including phishing pages, under the trusted subdomain. Analysts reviewing DNS/CDN logs should flag any CNAME pointing to a third-party service alongside a response indicating the target resource is unclaimed, and treat it as an urgent finding since it requires no interaction with the main application to exploit.
