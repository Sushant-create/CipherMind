# Tech Industry Resume Writing Framework

This framework is designed for software engineers, product managers, designers, and other tech professionals looking to build a resume that passes both applicant tracking systems (ATS) and human recruiter review. It emphasizes clarity, quantifiable impact, and scannability.

## Structural Layout and Formatting

**Length and Density**
- One page for candidates with fewer than 10 years of experience; two pages maximum for senior/staff+ candidates or those with extensive publications/patents.
- Aim for 5-7 bullet points per role for recent/relevant positions, tapering to 2-3 bullets for older or less relevant roles.

**Section Order**
1. Contact Information (name, phone, email, LinkedIn, GitHub/portfolio, city/state — no full street address needed)
2. Professional Summary (optional, 2-3 lines, only if it adds context an ATS keyword scan wouldn't catch)
3. Technical Skills (grouped by category: Languages, Frameworks, Cloud/Infra, Tools)
4. Professional Experience (reverse chronological)
5. Projects (especially valuable for early-career candidates or career changers)
6. Education
7. Certifications/Publications (if applicable)

**Formatting Mechanics**
- Use a single, ATS-friendly font (Calibri, Arial, Georgia) at 10.5-11.5pt body size; avoid tables, text boxes, or multi-column layouts that many ATS parsers mangle.
- Maintain consistent date formatting throughout (e.g., "Jan 2023 – Present," not a mix of "01/2023" and "January 2023").
- Use standard section headers ("Experience," "Education," "Skills") rather than creative labels ("My Journey," "Toolbox") since ATS keyword mapping relies on conventional naming.
- Save and submit as a **PDF** unless the application explicitly requests a .docx (some ATS platforms parse Word files more reliably — check the posting).

**Good vs. Bad Example**
- ✅ Good: Clean single-column layout, bolded job titles, consistent bullet indentation, 0.75" margins.
- ❌ Bad: Two-column layout with a skills sidebar, decorative icons instead of text labels, 9pt font to cram in more content.

## The XYZ Bullet Point Formula (Accomplished X, as measured by Y, by doing Z)

The XYZ formula — popularized by Google's own resume guidance — forces every bullet to answer three questions: **What did you accomplish? How was it measured? What did you actually do to achieve it?**

**Formula:** *"Accomplished [X], as measured by [Y], by doing [Z]."*

You don't need to use this exact sentence structure in the final bullet, but every strong bullet should contain all three components.

**Bad bullet (missing Y and Z — just a responsibility):**
> Responsible for improving backend API performance.

**Better bullet (has X and Z, but no measurable Y):**
> Improved backend API performance by refactoring database query logic and adding caching layers.

**Strong XYZ bullet (X, Y, and Z all present):**
> Reduced API p95 latency by 62% (from 800ms to 305ms) by refactoring N+1 database queries and introducing a Redis caching layer for high-traffic endpoints.

**More examples across roles:**

- ❌ Weak: "Worked on the onboarding flow redesign."
- ✅ Strong: "Increased new-user activation rate by 18% by redesigning the onboarding flow based on funnel drop-off analysis and A/B testing three variants."

- ❌ Weak: "Managed a team of engineers."
- ✅ Strong: "Delivered 4 major product launches on schedule by leading a cross-functional team of 6 engineers and establishing a bi-weekly sprint review process that cut scope creep by 30%."

- ❌ Weak: "Helped reduce customer churn."
- ✅ Strong: "Reduced monthly customer churn from 4.2% to 2.9% by building a predictive churn-risk model and triggering proactive outreach for at-risk accounts."

**When you don't have a hard number:** Use scope, scale, or frequency as a proxy metric — team size, number of users affected, systems touched, or time saved — rather than omitting the "Y" entirely.

## High-Impact Action Verbs

Lead every bullet with a strong, specific verb in past tense (or present tense only for your current role). Avoid generic, passive, or vague openers.

**By Category:**

| Category | Strong Verbs |
|---|---|
| Building/Creating | Architected, Engineered, Developed, Designed, Launched, Built |
| Improving/Optimizing | Optimized, Streamlined, Accelerated, Reduced, Refactored, Enhanced |
| Leading/Influencing | Spearheaded, Directed, Mentored, Championed, Orchestrated, Drove |
| Analyzing/Solving | Diagnosed, Resolved, Investigated, Identified, Evaluated, Modeled |
| Growing/Scaling | Scaled, Expanded, Grew, Increased, Amplified |
| Saving/Cutting | Reduced, Eliminated, Cut, Consolidated, Automated |

**Good vs. Bad:**
- ❌ Bad: "Was responsible for the migration of the legacy monolith to microservices."
- ✅ Good: "Architected the migration of a legacy monolith to a microservices architecture, reducing deployment time from 45 minutes to 4 minutes."

- ❌ Bad: "Helped with the design of a new caching system."
- ✅ Good: "Designed a distributed caching system that cut database load by 40% during peak traffic."

**Verb Variety Tip:** Avoid starting more than two bullets with the same verb across your entire resume. If you find yourself using "Managed" five times, differentiate: "Directed," "Coordinated," "Oversaw," "Supervised" all convey similar meaning with more precision depending on context.

## Common Mistakes to Avoid

**1. Listing duties instead of accomplishments**
- ❌ "Duties included writing unit tests and attending sprint planning."
- ✅ "Increased test coverage from 54% to 91%, reducing production incidents by 35% over two quarters."

**2. Vague, unquantified impact**
- ❌ "Helped improve team efficiency."
- ✅ "Cut average code review turnaround time from 2 days to 4 hours by introducing automated linting and a review-rotation schedule."

**3. Objective statements instead of summaries**
- ❌ "Seeking a challenging position where I can grow my skills."
- This tells the reader nothing about value delivered. Replace with a professional summary focused on your track record, or omit entirely if your experience section speaks for itself.

**4. Keyword stuffing without context**
- ❌ "Skilled in Python, Java, AWS, Docker, Kubernetes, React, Node.js, GraphQL, Terraform, CI/CD."
- Listing 15+ tools with no indication of depth signals breadth without substance. Group skills logically and reserve bullet points to show how key tools were actually applied.

**5. Inconsistent tense and formatting**
- Mixing "Managed team" (past) with "Manages team" (present) for the same still-current role, or switching bullet punctuation/capitalization style between sections. Pick one tense per role (present for current, past for prior) and one punctuation style, and apply it uniformly.

**6. Burying the most relevant experience**
- Don't let a 6-month internship from 8 years ago take equal visual weight to your current senior role. Allocate bullet count and space proportional to relevance and recency.

**7. Typos and unexplained gaps**
- A single typo in a technical resume can signal carelessness to an engineering hiring manager. Proofread with a tool (Grammarly, Hemingway) and have a second person review it. For employment gaps longer than 6 months, a brief one-line explanation (e.g., "Career break for caregiving," "Independent consulting") prevents recruiters from guessing.

**8. Including irrelevant personal information**
- ❌ Photos, age, marital status, or a full home address — these add legal risk for employers and no value, and are often flagged or stripped by ATS systems anyway.

**9. Over-designed templates**
- Heavy graphics, icons, or unusual fonts may look creative but frequently break ATS parsing, causing qualified candidates to be auto-rejected before a human ever sees the resume. When in doubt, prioritize parseability over visual flair.
