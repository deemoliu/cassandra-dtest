## Design a Distributed Power Grid Control System

When demand on the grid spikes, utilities can either fire up expensive peaker plants or ask flexible loads to use less. A demand-response control system is the second option: a dispatch center sends control commands to millions of smart devices (air conditioners (ACs), water heaters, electric vehicle (EV) chargers, thermostats) asking them to shed load for a window of time. The devices live in homes and buildings on ordinary consumer internet, and their owners always keep the final say.

A demand-response event starts with a number the grid operator already chose, such as "cut 20% for 60 minutes," and ends with a number someone will be paid on. In between, 5M owner-controlled devices on flaky home networks may never hear the command, refuse it, or quietly undo it, so the system has to act on a fast estimate during the event and still defend its final answer weeks later.

Clarifying Questions
You
"Where does the 20% target come from? Are we expected to watch grid load and decide when to curtail, or does someone hand us the target?"

Interviewer
"The grid operator gives you the target, the cohort, the start time, and the duration. Forecasting and the decision to curtail are not yours."

Takeaway
This rules out the monitoring-pipeline framing. The core of the design is a control loop that turns a given target into per-device commands, then verifies and corrects, with telemetry serving only as feedback.

You
"Is the final reduction number just for the operator's dashboard, or does it feed settlement, where program participants or the utility get paid on it?"

Interviewer
"It feeds settlement. Participants and regulators can dispute it, and you need to be able to show how you got it."

Takeaway
The final number must be reproducible from raw evidence and versioned. That forces an append-only telemetry lake and a restatement policy, separate from the fast live estimate.

You
"Do we need to hit the target accurately per device, or is the cohort total what matters?"

Interviewer
"The cohort total. Per-device records only matter as evidence when someone audits the result."

Takeaway
Measurement can be statistical at cohort level, which makes a counterfactual baseline and a holdout group workable. Per-device state is kept for audit and correction targeting, not for per-device accuracy.

You
"How late can device telemetry arrive? Minutes, or could a device that was offline all event upload its readings hours later?"

Interviewer
"Usually a few minutes. Devices offline through the whole event can upload their buffered readings hours later, and duplicates happen."

Takeaway
Aggregation must run on event time with watermarks and deduplicate on device sequence numbers. Results published during the event are estimates that may be restated until a settlement cutoff.

You
"How many devices does one event target, and how quickly do they all need to get the command?"

Interviewer
"About 5M devices per event out of roughly 50M enrolled. Every reachable device should have the command within a minute of the start."

Takeaway
A 60-second window for 5M devices behind home NAT (network address translation) rules out polling and inbound HTTP. It points to push over persistent outbound device sessions with sharded dispatch.

You
"If a device loses its connection in the middle of an event, or we send something wrong, what should the device do on its own?"

Interviewer
"It must go back to the owner's normal control when the event window ends. Owners can also override at any time, and that always wins."

Takeaway
Every command needs an absolute expiry enforced on the device, so a lost connection or a bad command fails safe to owner control. Owner override is a legitimate outcome that the lifecycle has to record, not an error.

Functional requirements
Operators can create a demand-response event with a cohort, a reduction target, a start time, and a duration.
Operators can cancel an active event, and the cancel reaches every reachable device.
The system sends a per-device command to every targeted device, about 5M per event.
Devices that reconnect mid-event still receive the current, unexpired instruction.
The system tracks each device's outcome: delivered, applied, refused, overridden, unreachable, or expired.
The system ingests device acks and telemetry idempotently, even when data is late, duplicated, or out of order.
The system measures the cohort's reduction against a counterfactual baseline while the event runs.
The system issues corrective rounds during the event to close any shortfall against the target.
The system produces an auditable per-event result for settlement that can be restated when late telemetry arrives.
Non-functional requirements
Deliver the command to all reachable targeted devices within 60s of event start.
Refresh the cohort reduction estimate every 1-2min so the controller can act inside a 60min event.
Keep dispatch and tracking available during partial regional outages, and never let telemetry ingest block dispatch.
Keep event records and each device's command version strongly consistent, and let cohort metrics be eventually consistent and versioned.
Support 50M enrolled devices, about 10M per region, and about 5M per event.
Ingest about 170k telemetry events/s at a 5min cadence, up to 830k/s at 1min, with 3-5x reconnect bursts.
Retain commands, acks, and raw telemetry so the final result can be reproduced from raw evidence.
Push a cancel to every reachable device within about 60s, and let unreachable devices revert on their own at expiry.
Limit the blast radius of any command with staged rollout and per-device depth and duration caps.
Sign every command and authenticate every device, so a device only obeys commands from the control plane.
Keep raw telemetry in cheap storage and only the cohort aggregates in hot storage.

## Design Payment System

A payment processor is a service that sits between merchants (shops, restaurants, retailers) and downstream credit card networks (Visa, Mastercard, American Express). When a customer swipes or taps their card, the payment processor receives the transaction request, forwards it to the appropriate network for authorization, and later settles the actual funds in a nightly batch.

We are designing the core payment processor that sits between merchants and downstream credit card networks. The hard part is bridging fast, synchronous authorization with slower, deferred settlement without losing track of which charges actually settled.

Clarifying Questions
You
"Are both the real-time hold authorization path and the deferred batch settlement path in scope, or are we designing only one of them?"

Interviewer
"Both are in scope. Hold authorization is synchronous and merchant-blocking: the merchant needs an approve or deny before the customer leaves the counter. Charge settlement is deferred to a nightly batch run."

Takeaway
The system has two distinct modes with different expectations: an immediate merchant-facing authorization path and a deferred settlement path.

You
"What latency does the merchant expect when a hold request is submitted, and does the system have to wait for the downstream processor's response before returning?"

Interviewer
"Sub-second p95, and yes, the hold path must be synchronous all the way through to the downstream processor. The merchant needs a definitive approve or deny before the transaction completes at the point of sale."

Takeaway
The authorization step is on the critical merchant path, so the design has to treat latency there as a first-class requirement.

You
"If a merchant retries a hold or charge request after a network timeout, does each retry create a new authorization, or must repeated requests resolve safely to the same business effect?"

Interviewer
"Retries must be safe. A retried hold must not produce two separate holds. A retried charge must not appear in the nightly batch twice."

Takeaway
Retries are a normal part of payment traffic, so the system needs a reliable way to make repeated requests land on the same business outcome.

You
"If the downstream processor acknowledges only part of a nightly batch, is a batch-level acknowledgment enough, or does the system need to track settlement status for each individual charge?"

Interviewer
"Per-charge tracking is required. A batch that partially succeeds cannot be treated as fully settled. Each charge needs its own settlement outcome."

Takeaway
Settlement truth has to be tracked per charge, not just per file, because partial batch success is part of the normal failure model.

You
"How long does a hold stay valid, and what should happen to a charge request that references a hold that has already expired?"

Interviewer
"Holds expire after 7 days. A charge referencing an expired hold must be rejected. Expired holds must be automatically released so the cardholder's available funds or credit are no longer tied up."

Takeaway
Hold expiry is part of the core payment lifecycle, not just a cleanup detail. The system needs a clear answer for expired holds and late charge attempts.

Functional requirements
Accept hold requests from merchants (account number, amount, merchant identifier), forward synchronously to the downstream processor, and return approval or denial.
Accept charge requests referencing an approved hold, store durably before acknowledging, and queue for batch settlement.
At a nightly cutoff, gather all pending charges, group them by downstream processor, build batch files, and transmit them for settlement.
Automatically release held funds if no charge request arrives within the hold expiration window.
Non-functional requirements
Hold authorization p95 latency under 500 ms end-to-end, including the synchronous downstream round trip.
No charge request may be lost between merchant submission and batch settlement. Durable write before acknowledgment.
The nightly batch pipeline must complete within a bounded window, targeting under 2 hours for all downstream processors.
Support 10 million hold and charge requests per day from tens of thousands of merchants.
Idempotent hold and charge processing so that merchant retries and network failures do not create duplicate authorizations or double settlements.
Reconciliation must detect and surface mismatches between what was authorized, what was charged, and what downstream actually settled.

## Design AI Chatbot App

An AI chatbot app is a web application that lets users have real-time conversations with a large language model (LLM). The user types a message, the system sends it to an AI model, and the response streams back token-by-token so the user sees the answer being "typed out" progressively. Products like ChatGPT, Claude, and Gemini are well-known examples of this pattern.

We are designing the backend and streaming infrastructure for an ephemeral AI chatbot application. A user logs in, sends a text prompt, and receives the AI model's response streamed token-by-token via Server-Sent Events (SSE). There is no backend message persistence: the conversation lives entirely in the browser, and a page refresh resets everything. The core design tension is delivering a fast, progressive token stream through a stateless proxy while handling streaming failures, upstream model unpredictability, and auth-guarded long-running connections.

Clarifying Questions
You
"Should conversations be persisted server-side so users can resume a session later, or is the conversation history owned entirely by the client?"

Interviewer
"Entirely client-owned. No server-side message storage. A page refresh resets everything. That is acceptable for this product."

Takeaway
This removes server-side chat history from scope. The backend only needs durable state for identity and usage, not for conversation storage or replay.

You
"What is the acceptable latency from prompt submission to the first streamed token appearing in the UI?"

Interviewer
"Under 500 milliseconds at p95. Once the stream starts, token delivery should feel continuous, with no perceptible gaps between tokens."

Takeaway
The synchronous work before the first token has to stay very small. Anything heavy or optional cannot sit on the critical path ahead of stream start.

You
"Does the client send the full conversation history with each new prompt, or does the backend maintain session state and assemble the context itself?"

Interviewer
"The client sends it all. The backend is stateless and does not track session context between requests."

Takeaway
Client-owned context means request size grows with conversation length. Token-budget enforcement and truncation start as a client-side product concern rather than a backend persistence problem.

You
"How many concurrent streaming connections should the system be able to support at peak?"

Interviewer
"About 50,000 concurrent SSE connections at peak. Assume bursty spikes when many users prompt at the same time."

Takeaway
The service has to support a large fleet of long-lived streaming connections, so connection management becomes a first-class scaling concern.

You
"If the upstream AI model stalls or times out while a response is being streamed, what should the user experience be?"

Interviewer
"Surface whatever partial text arrived and clearly signal the error. Users should be able to retry the prompt manually. Do not hang silently."

Takeaway
The product needs a clear partial-result and retry contract when upstream generation fails. Silent hangs are not acceptable behavior for the streaming path.

You
"What should happen if a user's authentication token expires while an active SSE stream is still delivering tokens?"

Interviewer
"Let the current stream finish. Require fresh authentication before the next prompt. Don't abort mid-sentence."

Takeaway
Auth is a request-start concern, not a per-token concern during an already active stream. Mid-stream expiry should affect the next prompt, not the response already in flight.

Functional requirements
Authenticated users can send a text prompt and receive a streamed AI response rendered token-by-token in real time.
The system relays the prompt to an upstream AI model and streams the response back to the client via SSE, with a typing indicator during delivery.
Conversation context (prior turns) is maintained in the frontend and sent with each new prompt so the model can produce multi-turn responses.
The backend is stateless with respect to chat history. No messages or conversations are persisted server-side.
Users can log in, receive a JSON Web Token (JWT), and use it to authenticate all requests including streaming connections.
Non-functional requirements
TTFT (time-to-first-token) under 500 ms at p95. Token-to-render latency should feel instantaneous once the stream begins.
The streaming endpoint should target 99.9% availability, with graceful degradation when the upstream AI model is slow or fully unavailable.
Support 50K concurrent streaming connections at peak, with bursty load when many users prompt simultaneously.
JWT-based authentication for all endpoints, including long-running SSE connections.
Per-user rate limits on prompts and cumulative token budget enforcement to control upstream API cost.
Minimize wasted AI model invocations. A stream that the user abandons mid-response should be terminated promptly to avoid unnecessary cost.
Assumptions
The AI model is an external LLM provider (such as OpenAI's API) with a streaming-capable endpoint.
The backend acts as a stateless streaming proxy. It does not store messages or conversation state.
The frontend sends the full conversation history with each new prompt for multi-turn context.
Only text-based chat is in scope. Single AI model provider, no model routing.

## Design TinyURL

A URL shortening service takes long URLs and returns compact aliases (short codes) that redirect browsers and API clients to the original destination. For example, a long URL like https://www.example.com/products/spring-sale?utm_source=newsletter&utm_campaign=april_launch might become https://s.example.com/aZ9k2Qx. It is read-heavy: the dominant workload is issuing HTTP redirects for lookups by short code, while new mappings are created far less often.

A URL shortener sounds like a single table and a redirect, but its read and write paths have different challenges. Redirects require a small key lookup at very high read QPS and low tail latency. Meanwhile, every new short code must be globally unique and durably stored.

Clarifying Questions
You
"If a user submits the exact same long URL twice, should we always return the exact same short code? And are custom aliases in scope?"

Interviewer
"For this system, yes. We want duplicate submissions of the same long URL to come back with the same short code. Custom aliases are in scope too, and if someone asks for one that is already taken, we should return a conflict error instead of overwriting it."

Takeaway
Stable deduplication requires a way to map long URLs to existing short codes before creating new ones. Custom aliases require an atomic check against the namespace on creation.

You
"If a user deletes or updates a link, does that change need to take effect globally in real time, or can the redirection path tolerate some delay?"

Interviewer
"We can tolerate eventual consistency. Redirection speed is critical, so we do not mind if there is a short delay for deletion or update updates to propagate globally."

Takeaway
Eventual consistency allows us to serve redirects entirely from cache, decoupling read latency and query load from our authoritative storage database.

You
"Can a single short link end up getting massive traffic if it goes viral, and does the system need to survive that kind of skew?"

Interviewer
"Absolutely. Viral links are a core part of the product. The system must be able to handle extreme traffic spikes for a single hot link without degrading redirection for other links."

Takeaway
Single-key hotspots cannot be solved by database partitioning alone. We must rely on highly localized caching close to the user to handle extreme, single-key traffic spikes.

You
"If our primary storage systems go down, is it better to fail the redirect and return an error, or continue serving existing links even if they might be slightly out of date?"

Interviewer
"For this system, keeping redirects available matters more than reflecting the newest change immediately. During an outage, we should keep redirecting users even if a recently updated or deleted link behaves like the older version for a while."

Takeaway
A fail-open stance means the read path should serve cached redirects during storage outages, prioritizing availability over immediate consistency.

Functional requirements
Users can submit a long HTTP or HTTPS URL and receive a unique short URL on the public short-link host when creation succeeds.
Browsers and clients can resolve a short code through the short-link host and receive an HTTP redirect to the stored long URL when a mapping exists.
Repeated creates for the same long URL may return the same mapping when the product enables stable deduplication, and the design must say how retries avoid duplicates.
Unknown short codes return a clear 404 response with no durable side effects.
Optional custom aliases may be supported, with namespace conflicts returned as explicit errors rather than silent overwrite.
Non-functional requirements
Redirect path targets server-side p95 under 50 ms excluding client network under normal load, with bounded synchronous work on the hot path.
Create path targets interactive latency with server-side p95 under 200 ms under normal conditions.
Assume on the order of 500M redirects per day and about 10M new mappings per day at peak planning, with a working read-to-write ratio near 100:1.
Favor high availability for redirects. Read caches may be eventually consistent if staleness stays bounded and authority remains in storage.
After the API acknowledges a created mapping, that mapping must not be silently lost. Durability is single-region strong for the core tutorial path.
Basic create-side rate limits and abuse controls are required. Short codes should resist casual guessing without turning the design into a security paper.
Favor cache-heavy redirect paths and bounded storage growth. Avoid per-redirect fan-out that grows without limit.

## Design Youtube
## Design ChatGPT

ChatGPT is an AI-powered conversational assistant where users type text prompts and receive AI-generated responses in real time. The system maintains multi-turn conversations, streaming each response token by token so the user sees output appearing progressively rather than waiting for a complete answer.

We are designing the backend for a ChatGPT-like conversational AI service. Users send text prompts within multi-turn conversations. The system assembles the conversation context, dispatches inference to a GPU cluster, and streams generated tokens back in real time via Server-Sent Events (SSE). Users expect sub-second responsiveness, but GPU inference takes seconds and is expensive. The architecture bridges that gap with streaming delivery, intelligent scheduling, and a lean pre-inference pipeline.

Clarifying Questions
You
"Should the system persist conversation history durably, so users can resume a conversation across sessions?"

Interviewer
"Yes, conversations must be durable. Users expect to return to a thread days later and continue from where they left off."

Takeaway
Durable conversation history is part of the core product contract, not an optional extra. The design therefore needs a clear boundary between persisted conversation state and the live streaming path.

You
"What latency targets apply to the streaming response? Specifically the time before the first token appears and the token delivery rate once the stream is running?"

Interviewer
"Time-to-first-token at or below 500 milliseconds at p50 and 2 seconds at p95. Once streaming begins, the delivery rate should be 30 to 60 tokens per second per stream."

Takeaway
The synchronous path before the first token has a tight latency budget. Context loading, safety checks, and scheduling overhead all have to fit within that budget instead of growing unchecked.

You
"When a conversation grows longer than the model's token limit, what should the system do with the excess history?"

Interviewer
"Truncate the oldest turns. Users understand that very long conversations lose early context. We do not need to summarize. Just drop from the beginning."

Takeaway
This makes truncation the required behavior when history exceeds the model limit. The system needs a predictable way to assemble recent context without pretending the full conversation always fits.

You
"How many simultaneous inference requests should the system be able to serve at peak?"

Interviewer
"Around 50,000 concurrent inference requests at peak. GPU compute is the dominant cost, so utilization efficiency matters."

Takeaway
At this scale, the core problem is no longer just request handling. The system needs an explicit policy for who gets scarce GPU capacity first when demand exceeds supply.

You
"What should happen if the SSE connection drops before the AI has finished generating the response?"

Interviewer
"The partial response should be recoverable. If the user refreshes or reconnects, they should be able to see what was generated before the disconnect."

Takeaway
Recovery must include already generated assistant text, not just fully completed prior turns. The persistence contract therefore has to support reconnecting users seeing what the system had already produced before the stream broke.

You
"When the GPU cluster reaches capacity and cannot immediately serve all incoming requests, what is the priority policy, and is it acceptable to reject some requests?"

Interviewer
"Paid subscribers must be served within SLO. Free-tier users can be queued or rejected with a clear error. Do not drop paid requests under any normal operating condition."

Takeaway
This makes service tier part of the scheduling contract. Under overload, the system must protect paid-user latency even if free-tier traffic waits longer or gets rejected.

Functional requirements
Users can send a text message within a conversation and receive an AI-generated response streamed token by token.
Users can create new conversations, list existing ones, and resume a previous conversation with full history context.
The system assembles relevant conversation history into a context payload for each inference request, respecting the model's token limit.
The system enforces safety guardrails on both user input (prompt filtering) and model output (response filtering) before delivery.
The system applies per-user rate limits and token-budget caps based on subscription tier.
Non-functional requirements
Time-to-first-token (TTFT) at or below 500 ms at p50 and 2 s at p95 under normal load.
Sustained token throughput of 30 to 60 tokens per second per active stream.
99.9% availability for the chat completion API.
Support 100M registered users, 10M daily active users, and peak 50K concurrent inference requests.
Completed conversation turns must survive service restarts. In-flight partial responses can be regenerated on failure.
GPU compute dominates operational cost. The design must address utilization efficiency and tier-based throttling.

## Design Distributed Web Crawler

A web crawler (or spider) is a program that systematically traverses the web by downloading pages and following hyperlinks from one page to the next. Web crawlers power search engine indexing, dataset collection for Large Language Model (LLM) training, content monitoring, and archival projects. The core challenge is doing this at internet scale, across billions of pages, while being polite to site operators and resilient to the messy, failure-prone nature of the open web.

We are designing a distributed web crawler that starts from a set of seed URLs, fetches web pages, extracts text content and outbound links, deduplicates work, and stores the extracted text for downstream use such as LLM training. The core challenge is crawling billions of pages within a bounded time window while being polite to site operators and avoiding redundant work.

Clarifying Questions
You
"Should the crawler follow links freely to any new domain it discovers on the public internet, or should it stay within a predefined set of domains from the seed list?"

Interviewer
"Follow outbound links freely across the public internet, starting from a seed set but expanding to any new domains discovered, subject to robots.txt rules and per-domain politeness limits."

Takeaway
Unbounded domain traversal means the URL frontier must scale to billions of unique URLs, making URL-level deduplication before enqueuing a correctness requirement rather than an optimization. Domain-level rate limiting must also coordinate across the entire fleet rather than being enforced locally per worker.

You
"Should the crawler also preserve the raw HTML of each fetched page in case downstream consumers need it, or should it only store the extracted text content?"

Interviewer
"Only store the extracted text content. Downstream consumers do not need the raw HTML, and storing raw HTML at our scale would create unnecessary storage overhead. Storing or serving raw HTML is out of scope."

Takeaway
Storing only the extracted text simplifies our storage footprint and means the content-level deduplication index operates on the extracted text body rather than the raw HTML markup.

You
"If two different URLs return identical HTML content, should the system store that content twice or detect the duplicate and skip the second storage?"

Interviewer
"Duplicate content should be detected and storage should be skipped after the first occurrence. Two URLs pointing to identical content produce one stored object, not two."

Takeaway
Two distinct deduplication layers are needed: URL-hash deduplication before enqueuing to filter redundant fetches, and content-hash deduplication after fetching to filter redundant storage. The content-hash index must handle concurrent writes from a distributed fleet without creating duplicate storage windows.

You
"If two crawler workers are both trying to fetch pages from the same domain, can they each make one request per second independently, or does the 1 req/s limit apply to the entire fleet combined?"

Interviewer
"The 1 req/s limit applies to the entire fleet combined. All workers together must send at most one request per second to any single domain. A worker that cannot crawl a domain right now should move on to other URLs rather than waiting."

Takeaway
Per-domain rate limiting across a distributed fleet requires shared coordination state rather than local per-worker enforcement. Workers that encounter a rate-limited domain must yield the URL back to the frontier or defer it rather than blocking, to keep their threads fully utilized on other domains.

You
"If a worker crashes while fetching a URL it already dequeued from the frontier, should that URL be treated as done, retried by another worker, or left stuck?"

Interviewer
"A URL that a worker was fetching when it crashed should be automatically retried by another worker. No in-progress URLs should be permanently lost when a worker fails."

Takeaway
The frontier queue's visibility timeout provides the crash-recovery contract without requiring a separate heartbeat or lease store: a worker acknowledges its message only after writing to storage and updating the URL metadata row, so crashes before the acknowledgment make the URL reappear automatically.

Functional requirements
Crawl the web starting from a set of seed URLs, discovering new pages via breadth-first search (BFS) link traversal.

Extract text content from each crawled HTML page and store it for downstream consumers.

Discover outbound URLs from each page and feed them back into the crawl frontier for future processing.

Deduplicate at both the URL level (before fetching) and the content level (after fetching) to avoid redundant crawling and storage.

Respect robots.txt directives and per-domain crawl rate limits (politeness).

Non-functional requirements
Crawl approximately 10B pages on the reachable web.
Complete the full crawl within a 5-day window.
Resume crawling without losing progress when individual workers crash.
Honor robots.txt and Crawl-delay directives, limiting to at most 1 req/s per domain.
Maximize per-machine throughput by keeping crawler threads busy instead of blocked waiting for HTTP responses.

## Design Slack-like Chat System
Slack is a workplace messaging platform that lets users communicate through direct messages and group channels. Users can create channels around topics or teams, share text and media, and receive notifications in real time across multiple devices.

We are designing the core messaging layer for a Slack-like platform: direct messages between two users and group channels with membership lists that range from a handful of people to tens of thousands. The central tension is that small conversations want eager push delivery for an instant feel, while large channels make per-message push prohibitively expensive and demand a fundamentally different delivery model.

Clarifying Questions
You
"Are we designing only for small conversations like DMs and team channels, or do we also need to handle large announcement-style channels with potentially tens of thousands of members?"

Interviewer
"Both are in scope. A channel can be a two-person DM or a company-wide announcement channel with up to 100K members. Delivery behavior can differ by channel size, but both types must be supported."

Takeaway
The system cannot use a single delivery model for all channels. Channel membership count becomes a first-class input to the delivery strategy, and the architecture must handle both extremes.

You
"What is the delivery latency expectation for small conversations versus large channels, and does the product treat them differently?"

Interviewer
"Yes, the product distinguishes. Small conversations should deliver within 200 ms. Large channels have a 500 ms budget. The difference is intentional because larger channels take longer to reach all members."

Takeaway
The latency gap between small and large channels is a product requirement, not just an engineering convenience. It justifies using a different delivery path for each channel size rather than one uniform approach.

You
"Should the sender receive a delivery confirmation only after the message is durably stored on the server, or is it acceptable to show a sent indicator right away and persist in the background?"

Interviewer
"The server must persist the message before returning the send confirmation. Showing a pending indicator on the client before that is fine as a UX touch, but the server must not acknowledge until it has durably saved the message."

Takeaway
The write path is synchronous through the persistence layer before any delivery fan-out begins. This rules out fire-and-forget publish-first designs for the send acknowledgment.

You
"Roughly how many users are online at once? I also want to sanity-check whether large announcement channels create a special burst case for us."

Interviewer
"About 20% of daily active users are online at any given time, which works out to roughly 10M concurrent connections. A large announcement channel can have up to 100K active members, and a single message to that channel is the peak fan-out scenario we must support."

Takeaway
The connection fleet must handle tens of millions of persistent connections distributed across many servers, and a single large-channel message can fan out to 100K connections in a burst. A routing layer between servers is not optional at this scale.

You
"When a client reconnects after a network outage, how should it recover the messages it missed while offline? Does the server hold those messages in reserve, or does the client fetch them from the conversation history?"

Interviewer
"The server does not hold messages in reserve for disconnected clients. On reconnect, the client should fetch any missed messages from the durable message history using its last-seen position in the conversation."

Takeaway
The real-time delivery stream is a best-effort channel, not a durable buffer. Reconnect recovery must go through the message history endpoint with a cursor, keeping the server stateless for per-client delivery tracking.

Functional requirements
Users can send direct messages (DMs) to another individual user.
Users can create a group channel and add or remove members.
Users can send text messages with optional image attachments to a channel, delivered to all members.
Online users receive new messages in real time through persistent connections.
Users can delete their own messages (soft delete visible to other participants).
Non-functional requirements
Messages reach online recipients within 200ms for DMs and small channels, within 500ms for large channels.
Target 99.9% uptime for the message send path. Sends always succeed even if some delivery paths degrade.
Once the server accepts a message, it must never be lost. Persist before acknowledging the send.
Support 50M daily active users, approximately 1B messages per day, with channels ranging from 2 members (DM) to 100K+ members.
Messages within a single channel appear in consistent order across all clients.
Users logged in on multiple devices receive messages on all active sessions.
Assumptions
A DM is modeled internally as a two-member channel.
Channel membership is invite-only. No public channel discovery.
Rich media means image uploads only. Videos and files are out of scope.
Deletion is soft: the message body is replaced with a "deleted" marker.
Single-region deployment for this design.
User authentication and profiles are assumed to exist.


## Design CICD System

A multi-tenant CI/CD platform listens to source-control events, decides whether a workflow should run, executes build or test or deploy steps in isolated environments, and shows users a truthful progress page. Unlike a single-team Jenkins box, it has to survive bursty Git pushes, keep tenants isolated, and recover cleanly when runners or browsers disconnect.

A naive design says, "A Git push arrives, read the YAML, start some containers, and show a spinner." The hard part is that the push is untrusted input, the workflow config must be pinned to the pushed commit, the scheduler may release only one step at a time, and the browser still has to tell the truth after reconnect. The goal is one repo-pinned, tenant-safe, strictly ordered workflow timeline that the scheduler and the UI can both trust.

Clarifying Questions
You
"Should the system support only linear sequential workflows where each step runs after the previous one finishes, or does the scope include parallel stages running at the same time or conditional branching based on a step's outcome?"

Interviewer
"Linear sequential only. Each workflow is a flat ordered list of steps. No parallel fan-out between steps, no matrix builds, no conditional skip logic. One step finishes, then the next one starts."

Takeaway
Strictly linear execution reduces the scheduler to a single invariant: at most one step in a run may be dispatched or running at any time. This lets the scheduler advance the run by finding the first non-terminal step rather than evaluating a dependency graph.

You
"Can a single push event trigger multiple parallel workflows with different event triggers and conditions, or is there exactly one scheduled workflow run triggered per code push?"

Interviewer
"One scheduled workflow run per push. If a push is received, we trigger a single workflow execution. Complex event-based workflow routing or multi-workflow selection are out of scope."

Takeaway
One scheduled run per push simplifies our scheduling path, letting us use the repository code push as the definitive, unambiguous trigger for a single workflow run.

You
"Do tenants need fully dedicated execution infrastructure, or is shared compute acceptable as long as each tenant's execution, secrets, logs, and identity stay isolated?"

Interviewer
"Shared compute is acceptable for most tenants as long as execution, secrets, logs, and identities are strictly isolated per tenant. Dedicated infrastructure could exist later for premium customers, but it is not required in this scope."

Takeaway
Tenant isolation has to be enforced at the execution boundary, not by giving every customer their own infrastructure. The design should preserve strict per-tenant separation for runtime identity, secrets, and logs while still allowing shared capacity underneath.

You
"What is the expected peak push rate and the maximum number of concurrently running workflow steps we need to support across all tenants? Steps that run for 20 to 30 minutes will create a sustained concurrency level higher than the push rate alone suggests."

Interviewer
"Plan for 2,000 pushes per minute at peak and up to 10,000 concurrently running steps. Most steps finish in under 5 minutes, but long build jobs can run for 30 minutes. We need enough capacity to handle the peak without one tenant starving others."

Takeaway
10,000 concurrent steps with a tail duration of 30 minutes means cluster capacity must be sized for sustained holding, not just arrival rate. Per-tenant fairness limits and step timeout policies become structural requirements rather than optional optimizations.

You
"When the browser disconnects mid-run, does it need every missed state transition replayed after reconnect, or is it enough to reload the current run state and continue the log view from where it left off?"

Interviewer
"Reload the current run state and continue the log view from where it left off. Replaying every missed transition since the beginning would be too expensive for long-running workflows. The UI just needs to become correct again after reconnect."

Takeaway
The current run state is the source of truth for reconnects, while the live stream only keeps the page fresh between reloads. The design should make the UI correct again after a disconnect without depending on a perfect replay of every missed transition.

Functional requirements
Accept a GitHub push webhook, analyze branch, ref, commit SHA, and delivery metadata, and decide whether a workflow should start.
Resolve the canonical GitHub repository identity and the tenant-scoped internal repository record through an internal API before reading workflow config.
Read the workflow configuration from the GitHub repository at the pushed commit SHA and validate that it defines a linear sequence of jobs or steps.
Create one workflow run and its ordered step records in the control plane before any Kubernetes runner starts.
Execute steps sequentially on Kubernetes in isolated Docker-based environments, advancing only after the current step reaches a terminal state.
Provide a browser UI that shows workflow status, ordered steps, the current running step, failures, and near-real-time progress after the workflow starts.
Let the UI recover to a correct workflow snapshot after reconnect and continue log viewing from a resume cursor.
Store enough run history, pinned config metadata, and audit detail to explain later why a workflow ran, or why planning failed before execution.
Non-functional requirements
Acknowledge the Git push webhook within about 2 seconds after durable dedupe and enqueue.
Reflect workflow and step status changes in the UI within about 2 seconds under normal load.
Start the next eligible step within about 10 seconds of the previous step finishing when cluster capacity exists.
Target 99.9% availability for webhook ingest, run reads, and progress updates while individual runner failures do not lose workflow truth.
Preserve one authoritative workflow timeline even if webhook handlers, schedulers, runner pods, or browser connections fail.
Enforce tenant isolation for repository bindings, secrets, logs, artifacts, and execution identities.
Scale to roughly 50,000 repositories, 2,000 pushes per minute peak, and 200,000 workflow runs per day.
Retain workflow state, pinned config version, and audit history for at least 90 days.
Keep cluster cost controlled through ephemeral runners, bounded retention, and fairness limits for noisy tenants.

## Design Online Chess Game

An online chess platform such as chess.com lets two players get paired quickly, join a shared game room, see the same board in real time, and finish the game under a strict time control. To the user it feels like a lightweight realtime app, but the system still needs three non-negotiable truths: match outcome, legal move order, and clock ownership.

Two humans want the game to feel like a single shared board, yet only the server can decide who got paired, which move legally happened next, and whose clock actually ran. If those three truths drift, the product stops being chess and becomes two disconnected animations.

NOTE

In the interview, I would pin down the time control early. Increment vs no-increment changes both pool boundaries and how you apply the clock at each committed move.

Clarifying Questions
You
"Are we supporting a single time control, or do we need to handle multiple formats like bullet, blitz, and classical? And does any time control use a per-move increment?"

Interviewer
"Support multiple formats, at minimum the popular ones like 3+2, 5+0, and 10+0. Yes, increment must be supported."

Takeaway
Multiple time controls require separate matchmaking queues partitioned by time control label so players only wait against compatible opponents. Increment support means the clock model must apply a configurable bonus to the moving player's remaining time after each committed ply, not just decrement a countdown.

You
"Are we handling both rated and casual games? And are spectators, tournaments, and puzzle modes in scope?"

Interviewer
"Rated and casual head-to-head matches are in scope. Tournaments, spectators, and puzzle features are out of scope for this design."

Takeaway
Rated games introduce a rating update step that must happen after the game result is durable, but not during the live move path. Rating updates should be decoupled from move acknowledgement to avoid adding latency to the player-facing game loop.

You
"If a player's move request is retried due to a dropped connection, can the server end up committing the same ply twice, or does the protocol guarantee at-most-one commit per ply?"

Interviewer
"At most one commit per ply, always. A duplicate or stale move submission must be detected and rejected, not applied again."

Takeaway
Move submissions must carry a ply number or version identifier so the server can reject any request that does not match the expected next ply. This single check is the invariant that prevents two different committed states from existing for the same position in a live game.

You
"Can clients send their locally measured remaining time as part of a move submission, or does the server own that calculation entirely?"

Interviewer
"The server owns remaining time completely. Client-submitted clock values are ignored for legal purposes."

Takeaway
This means remaining time per player must be stored durably at each committed move boundary and derived from server timestamps, not accumulated from client reports. A client that disconnects and reconnects cannot inflate its own clock by withholding or replaying move submissions.

You
"If no opponent at a matching rating is available, does the system widen the acceptable rating range over time, and is there a maximum wait before the player is notified?"

Interviewer
"Yes, widen the rating window gradually. After a few minutes without a match, a broader range is acceptable. Players should not wait more than a few minutes in normal conditions."

Takeaway
Matchmaking queue entries must carry a timestamp so the pairing worker can apply a widening policy based on elapsed wait time. The queue is partitioned by time control, and each partition runs its own widening logic independently, which keeps the pairing logic local to one pool rather than scanning across all modes.

You
"If a player disconnects near the end of their remaining time and the connection is not restored, should the server adjudicate a timeout loss based on server time, or should it wait for the player to come back?"

Interviewer
"Adjudicate a timeout loss based on server time. Do not wait indefinitely for a disconnected player."

Takeaway
Timeout must be computed from the last committed clock boundary plus server-wall-clock elapsed time, independent of whether any client is connected. This means the game server must be able to schedule a timeout check at the expected expiry time and fire a terminal result without needing a live socket event from either player.

Functional requirements
Players can choose a supported time control and enter or leave a matchmaking queue for that mode.
The system can pair two compatible players, create a game, assign colors, and place both players in the same live game session.
Players can submit moves, and the server validates turn order and move legality before accepting the next ply.
Each game tracks authoritative per-player remaining time, applies increment when configured, and ends the game on timeout when a player runs out of time.
Players can reconnect to an active game, recover canonical board and clock state, and finish with a durable result that can feed downstream rating updates.
Non-functional requirements
The server is authoritative for match outcome, move order, legal board state, and clock accounting.
No game can commit two different next moves for the same ply.
Target 99.95% availability for matchmaking, move submission, and canonical game-state reads within a healthy region.
Target p95 < 250 ms for normal matchmaking in a healthy pool.
Target p95 < 150 ms for move acknowledgement within a region.
Target p95 < 1 s for opponent-visible updates after a committed move.
Assume about 3M daily active players and 150k concurrent live games at peak.
Plan for 5k/s peak queue entries and 20k/s peak move submissions during busy windows.
Once a move or terminal result is acknowledged, move order, remaining clocks at that boundary, and the final result must survive crash or failover.
Client-side countdown display is cosmetic only.
Server-owned remaining time must not increase because of retries or reconnects.
Timeout decisions use server time.
Only the two participants may submit moves or join private game channels, with authentication and rate limiting assumed at a high level.

## Design Webhook Delivery System

A webhook delivery system lets one product notify another product by making an outbound HTTP callback when a business event happens. On the surface this looks like a simple POST to a stored URL. The real design problem is that the callback target lives on the public internet, can be slow or malicious, and should never block the product that generated the event.

Triggering a webhook should feel like a small durable write to the product that owns the event. The hard part is everything that happens after that write.

Clarifying Questions
You
"When a tenant registers a webhook for a specific event type, can they point multiple callback URLs at the same event type, or is it always one URL per event type per tenant?"

Interviewer
"One active callback URL per event type per tenant. Fanout to multiple URLs for the same event is out of scope."

Takeaway
One-to-one routing means the trigger path resolves a single registration row per trigger and produces one delivery record, keeping the routing and delivery state machine straightforward without a fan-out join on the hot trigger path.

You
"If a tenant updates their callback URL while a delivery is already being retried, should that retry go to the new URL or the URL that was registered when the trigger was originally accepted?"

Interviewer
"Use the URL that was active when the trigger was originally accepted. An in-flight delivery should not be rerouted to a new URL registered after acceptance."

Takeaway
Each delivery record must store a snapshot of the destination at accept time rather than a live reference to the registration row, making retry behavior deterministic and preventing a URL change from silently redirecting deliveries already mid-lifecycle.

You
"Is the system expected to guarantee that each triggered event is delivered to the callback endpoint exactly once, even across retries and worker crashes?"

Interviewer
"Exactly-once delivery to arbitrary external HTTP endpoints is not achievable. The system guarantees at-least-once delivery. Receivers must tolerate duplicate deliveries using the stable delivery identifier included in every outbound request."

Takeaway
The delivery contract is at-least-once. The system provides a stable delivery ID in every outbound request so idempotent receivers can deduplicate. The tutorial must not claim exactly-once delivery in requirements or design.

You
"If a tenant's callback URL is returning server errors for several hours, should its retries be isolated from other tenants, or does a failing endpoint slow down deliveries for everyone sharing the same retry infrastructure?"

Interviewer
"A failing tenant endpoint must not block or degrade delivery for unrelated tenants. Isolation is a firm requirement at the scale we are operating."

Takeaway
Retry scheduling and worker dispatch need per-tenant or per-destination partitioning so one noisy endpoint does not monopolize worker connections or queue head-of-line bandwidth.

You
"How many times should the system retry a delivery that keeps failing before giving up, and once it ends up in the dead-letter queue, who is responsible for replaying it?"

Interviewer
"Retries are bounded, around 8 to 10 attempts with exponential backoff. After exhausting the retry budget, the delivery moves to a dead-letter queue with a reason code. Replay after that point is a manual or operator-triggered action, not automatic."

Takeaway
A finite retry budget with explicit dead-letter graduation keeps the retry backlog bounded and prevents infinite attempt accumulation on permanently failing endpoints. The dead-letter state must store enough context for operators to replay or triage without re-triggering the original producer.

You
"Should the system verify that a newly registered callback URL actually belongs to the tenant before routing real production events to it, and what happens to triggers that arrive before validation completes?"

Interviewer
"Yes, endpoint validation is required before a registration becomes active. Triggers that arrive for an unvalidated or inactive registration should be rejected or queued rather than routed to an unverified URL."

Takeaway
Validation gates activation, which means the registration state machine must include a pending-validation state before any live trigger traffic is routed to the URL.

Functional requirements
A user can register or update a webhook by providing a callback URL and an eventId, and each eventId maps to exactly one active callback URL for that tenant.
When a producer triggers an eventId, the system durably accepts the event payload and asynchronously delivers an HTTP webhook to the registered callback URL.
The outbound webhook body includes everything the receiver needs to process the event without extra hot-path lookups in this platform.
Failed or timed-out deliveries are retried with a bounded policy such as exponential backoff, then moved to a dead-letter queue (DLQ) after the retry limit is exhausted.
The system validates callback endpoints and sends signed or authenticated requests so delivery targets the correct registered user and the receiver can verify authenticity.
Non-functional requirements
Target 99.99% availability for trigger acceptance and 99.9% for delivery processing within a healthy region.
Target p95 < 100 ms to accept and durably enqueue a triggered event, with first delivery attempts usually starting within a few seconds under normal load.
Support up to 1B events per day, around 11.6k/s average ingress, peak bursts in the low 100k/s range, and hundreds of thousands of concurrent in-flight deliveries and retries.
Webhook delivery is asynchronous, non-blocking, and at-least-once, and receivers must tolerate duplicate deliveries.
Accepted events, resolved endpoint snapshots, delivery state, attempt results, and dead-letter outcomes must survive worker or node failure.
Slow or failing callback endpoints must not block unrelated tenants or healthy destinations.
Only authenticated owners can manage a mapping, callback URLs must be validated before activation, outbound requests must be signed, and the system must defend against SSRF-style or abusive endpoints.
The hot ingest path should stay small, and worker concurrency, broker batching, and retry spacing should keep throughput high without turning retries into a thundering herd.

## Design Job Scheduler

A distributed job scheduler accepts instructions such as "run this task every day at 02:00 UTC" and makes sure the task runs at the right time. Doing that on one machine is straightforward. The interesting part begins when many schedulers and workers share the job: the system must recover from failures without losing a scheduled run or recording the same run twice.


We will design a scheduler for immediate, one-time, and recurring jobs. As we work through it, keep one question in mind: when several machines notice that the same job is due, how do we create one durable record for that scheduled run and recover it safely after a failure?

Clarifying Questions
You
"Are we designing for recurring cron-style jobs only, or does the scheduler also need to handle one-shot jobs scheduled for a specific future time and jobs that should run immediately on demand?"

Interviewer
"All three. Most jobs use recurring cadences, but engineers also need to schedule one-off maintenance tasks for a specific time and trigger immediate runs through an API. All three types need the same reliability guarantees."

Takeaway
All three kinds of schedule should create the same kind of durable run record. Later, we will call that record an execution slot. Using one model gives immediate, one-time, and recurring jobs the same retry and recovery behavior.

You
"When the same scheduled occurrence could be dispatched twice after a crash, does the platform guarantee at most one committed success for that occurrence, or is deduplication left entirely to the job handler?"

Interviewer
"The platform must prevent two workers from both reporting committed success for the same fire time. What the job does externally, like sending an email or calling a payment API, is the handler's problem. We are not in a position to guarantee idempotency for arbitrary external calls."

Takeaway
The scheduler can guarantee one committed result for each run record, but it cannot control side effects in another system. We will use a generation number to reject results from an old worker, while handlers use their own idempotency keys for external calls.

You
"If the scheduler has been down for several hours, should every missed occurrence fire when it comes back, or is there an age limit after which we discard missed occurrences?"

Interviewer
"All missed occurrences must be backfilled from durable state once the control plane recovers. No occurrences are to be skipped, dropped, or ignored regardless of how long the outage lasted."

Takeaway
The system needs a durable checkpoint from which it can recreate every missed run after recovery. An in-memory timer or queue alone cannot meet this requirement.

You
"Are jobs' schedules spread evenly across the clock, or do many of them cluster at common marks like the top of every 5 minutes or every hour? That would create a sharp spike rather than a smooth load curve."

Interviewer
"Very clustered. Most engineers write cron expressions like every 5 minutes or midnight daily, so the top of every 5-minute window can bring a burst 10 times higher than average. It is a real operational headache already on the current system."

Takeaway
The schedule must be divided across scheduler nodes so one node does not process the entire burst. We should also place only work that will run soon into the ready queue, rather than filling it with the distant future.

You
"If a scheduler node that owns a shard crashes, is it acceptable for that shard's occurrences to experience a brief scheduling gap of a few minutes until a new owner picks up and catches up, or do we need near-instant handoff with no visible gap?"

Interviewer
"A gap of a few minutes is fine as long as the missed fires are backfilled when the new owner takes over. We do not need zero-downtime handoff. Sub-minute failover would be a nice-to-have, not a hard requirement."

Takeaway
Brief scheduling gaps are acceptable because the new owner can recreate missed runs from durable state. That lets us use leased shard ownership without designing an active-active handoff protocol.

Functional requirements
Users can create immediate, one-time, or recurring UTC jobs with parameters, timeouts, and retry policies.
The platform creates one durable slot for each due run and recreates missed slots after downtime.
Each slot records claims, attempts, timeouts, and its final outcome.
The system detects failed workers, reclaims their work, and applies cancellation or retry policy to long-running jobs.
Users and operators can inspect job definitions, execution history, lag, and final outcomes.
Non-functional requirements
Under nominal load, work for a due occurrence should start within about 2 seconds of the scheduled fire time.
After outages or restarts, missed occurrences are backfilled from durable state rather than dropped.
Each (job_id, scheduled_fire_time) has one durable slot and at most one committed success.
End-to-end exactly-once external side effects still require idempotent handlers or transactional integration outside this core.
Plan for about 10k execution starts per second sustained, with 5-10x burst skew at minute or hour boundaries.
Scheduler nodes and worker nodes scale out independently with coordinated shard ownership and lag-driven concurrency limits.
Loss of schedulers, workers, queues, or single hosts must not lose accepted schedule intent or leave work permanently stuck without escalation.
Queue lag, missed-fire backlog, retry counts, lease timeouts, and dead-letter volume must be visible for correctness and capacity debugging.

## Design Google Calendar

Google Calendar is a shared calendaring product where people manage multiple calendars, create recurring events, invite attendees, and keep their schedule consistent across phones, web clients, and email-driven reminders. Although the interface resembles familiar CRUD, the design must keep one authoritative event record while recurrence, attendee state, permissions, reminders, and device sync all derive different views from it.

Google Calendar is a shared scheduling product where correctness is critical: a duplicate reminder, a lost RSVP, or a stale device view breaks user trust. The design must keep event identity, recurrence, attendee state, and sync recovery coherent under a bounded resource footprint.

Clarifying Questions
You
"Are AI scheduling, conference room booking, and CalDAV federation in scope, or are we focusing on core shared calendaring: recurring events, attendee RSVPs, and cross-device sync?"

Interviewer
"Core shared calendaring is in scope, including recurring events with exception handling and attendee RSVP. AI scheduling, resource calendars, and CalDAV federation are out."

Takeaway
Focusing on core scheduling keeps the design centered on event truth and attendee consistency rather than complex recommendation logic or cross-protocol federation.

You
"For recurring events, should I think of the series as one recurring event with occasional exceptions, or do we expect every future occurrence to behave like its own independent event? And is pre-expanding the whole future acceptable?"

Interviewer
"Infinite future expansion is not acceptable. We must support editing one occurrence without affecting the rest of the series."

Takeaway
We must avoid materializing an infinite future of events. Instead, the design should compute occurrences dynamically from a set of rules and bounded exception overrides.

You
"What is the write acknowledgement latency target for event mutations, and does cross-device freshness need to be synchronous or is eventual consistency acceptable?"

Interviewer
"Target p95 < 200 ms for event writes. Cross-device freshness within a few seconds is fine; it does not need to be synchronous."

Takeaway
A sub-200 ms write SLA implies we must acknowledge updates as soon as the core event is saved, moving reminder evaluations and fan-out notifications to background tasks.

You
"When an organizer edits a shared event, should that update one shared event for everyone, or can different attendees end up with their own version of the event? And does an RSVP ever change the actual event details?"

Interviewer
"There should be one organizer-owned event definition that attendees see. An RSVP changes the attendee's response, but it does not change the event's title, time, or recurrence."

Takeaway
Keeping a single source of truth for the event means we must decouple shared details from individual attendee RSVPs to prevent organizer edits from causing write conflicts.

You
"If a client reconnects after being offline or missing push notifications, what is the canonical way for it to catch up on missed changes without relying on push delivery or re-downloading full calendar state?"

Interviewer
"Push notifications are freshness hints only. Clients must be able to catch up on all missed changes after a disconnect using a reliable sync path, without depending on push delivery or pulling full state."

Takeaway
This requires a reliable, stateful delta-sync path. Reconnecting clients must be able to pull and replay missed updates from a specific token rather than reloading full calendars.

You
"How accurate does reminder delivery need to be, and what should happen when a recurring series is edited while reminders for upcoming occurrences are already scheduled?"

Interviewer
"About ~1 minute accuracy is the target. Duplicate reminder sends are not acceptable, even when a series edit reschedules or cancels affected occurrences."

Takeaway
To guarantee no duplicate or missed alerts, reminder triggers must be evaluated asynchronously downstream from event writes, ensuring edits automatically invalidate scheduled jobs.

Functional requirements
Users should be able to create multiple calendars and manage which calendars appear in their account.
Users should be able to share a calendar with view or edit permissions, including private-event visibility rules.
Users should be able to create, update, view, and delete one-time, all-day, multi-day, and timezone-aware events.
Users should be able to create recurring events and edit or cancel a single occurrence without corrupting the rest of the series.
Organizers should be able to invite attendees, and attendees should be able to RSVP without taking ownership of the event definition.
Organizer updates and cancellations should propagate to attendees without creating divergent event copies.
Users should receive reminders for upcoming events and attendee-facing update notifications for important changes.
Clients should be able to sync calendar changes across devices and recover after disconnects or missed freshness signals by using a canonical sync path.
Non-functional requirements
Target 99.95% availability for calendar reads, writes, and sync recovery.
Acknowledge event create, edit, delete, and RSVP writes in p95 < 200 ms.
Serve common day or week calendar windows in about p95 < 500 ms.
Make cross-device freshness visible within a few seconds under normal conditions.
Deliver reminders within roughly 1 minute of the requested reminder time in normal operation.
Preserve accepted writes, recurrence rules, access control list (ACL) changes, and attendee responses without silent loss.
Prevent recurring edits and exceptions from producing duplicate reminders or contradictory attendee state.
Enforce calendar sharing rules and private-event visibility on every read path.
Keep storage and compute bounded by avoiding infinite future materialization of recurring events.


## Design GPU Scheduling Platform

A GPU scheduling platform manages a shared pool of GPU nodes and allows multiple users or teams to submit compute jobs, typically ML training runs, fine-tuning tasks, or batch inference, that require GPU resources. The platform queues jobs by priority, assigns them to nodes with available capacity, runs them inside containers, and handles failures automatically. It provides the shared scheduling and execution layer used by an ML platform team.

We are designing the scheduling and execution layer for a shared GPU cluster. Users submit containerized batch jobs with resource requirements and priority levels. The platform queues, schedules, runs, and monitors those jobs across a pool of GPU nodes. The scheduler must make fast priority-driven placement decisions while keeping the scheduler, database, and remote node agent consistent, even when one of them fails mid-assignment.

Clarifying Questions
You
"Before I design the scheduler, I want to understand the placement model. Do any jobs require GPUs across multiple nodes simultaneously, meaning all nodes must start at once and failing to acquire one means releasing all the others?"

Interviewer
"No, assume each job fits on a single node. Gang scheduling for distributed training is a follow-up. The core tutorial covers single-job, single-node placement."

Takeaway
This keeps the core placement problem to one job on one node. Distributed multi-node coordination is out of scope for the main design.

You
"If the platform decides a job should run on a specific node but that node becomes unreachable before the job actually starts, should those GPU resources be released automatically after a short time?"

Interviewer
"Release it automatically after a short timeout. GPU slots must never stay locked by a ghost claim. We cannot hold a GPU slot hostage to an unresponsive node."

Takeaway
Reservation state cannot be allowed to stick forever after a partial failure. The design needs an automatic expiry or recovery mechanism for in-flight placements.

You
"When a high-priority job arrives and all GPUs are occupied, should the scheduler preempt any running job with lower priority, or only jobs that are at least one full priority band lower than the arriving job?"

Interviewer
"Only preempt jobs that are of strictly lower priority than the incoming one. Never preempt a job of equal priority, as that would create endless evictions."

Takeaway
Preemption is allowed, but only across distinct priority boundaries. Jobs of equal priority should not displace each other.

You
"When a long-running job is preempted after hours of GPU compute, is the platform responsible for preserving the job's progress, or is that entirely the application's responsibility?"

Interviewer
"The platform is not responsible for workload data. We send a graceful stop signal to the container, then re-queue the task. The job itself is responsible for saving its internal state during preemption."

Takeaway
The scheduler is responsible only for container orchestrating and resource slot assignment, not managing checkpoint storage or application-level state.

You
"If the scheduler crashes in the middle of making placement decisions, should the system recover automatically from persistent state, or is some manual cleanup acceptable after restart?"

Interviewer
"A crash or restart should not result in lost state or require manual recovery. All active and pending placements should remain consistent and recoverable from our persistent database."

Takeaway
Placement and queue state must be backed by durable storage rather than living purely in-memory, ensuring that scheduler restarts are completely seamless and automated.

You
"A single missed heartbeat could just be a transient network blip. Should the platform declare a node dead immediately, or only after multiple consecutive misses?"

Interviewer
"Require at least two or three consecutive missed heartbeats before declaring failure. A single missed heartbeat could be a transient delay. We would rather wait a few extra seconds than preempt a healthy job."

Takeaway
Failure detection should resist transient network blips instead of reacting to a single missed heartbeat. The timeout policy has to balance fast recovery against false positives.

Functional requirements
Users can submit a GPU job specifying a container image, GPU count, memory requirement, and priority level.
The scheduler assigns pending jobs to available GPU nodes based on priority, resource fit, and fairness.
Jobs run inside containers pulled from a container registry, with GPU and memory isolation on the target node.
Users can query job status and retrieve logs or output artifacts after completion.
The platform preempts lower-priority running jobs when a higher-priority job arrives and no resources are free.
Non-functional requirements
Prefer strong consistency for scheduling decisions so a GPU slot is never double-assigned. Job-status reads can tolerate eventual consistency.
High-priority jobs should begin executing within 5 seconds of submission when resources are available. Normal-priority jobs within 2 minutes.
Support up to 1,000 GPU nodes, 10,000 concurrent queued jobs, and 100 concurrent running jobs.
Detect node failures within 30 seconds via heartbeats and auto-retry failed jobs up to a configurable limit.
Target >80% GPU utilization cluster-wide while respecting priority and per-team fairness.
Jobs from different users must be resource-isolated (GPU, memory, network) to prevent noisy-neighbor effects.


## Design A Nearby POI Service

A nearby POI (Point of Interest) service lets users search for restaurants, gas stations, parks, hospitals, and other places near a given location. Products like Yelp, Foursquare, Google Maps, and Uber's place-picker all rely on a POI backend that indexes millions of places and answers "what is near me?" queries in milliseconds. Behind the simple search box is a geospatial indexing problem: the service must narrow a huge global dataset to a small set of nearby candidates without scanning every record.

Serving nearby queries over 200 million Point of Interest (POI) records requires balancing massive read volumes with consistent, durable updates. The core product tension is returning highly accurate, sorted location results to users in under 200 milliseconds, even under concentrated peak traffic in major metropolitan centers.

Clarifying Questions
You
"Who writes POI data here? Is it mostly business owners and admins, or do we also need to handle crowd-sourced edits from end users at large scale?"

Interviewer
"Business owners and platform admins only, at a few hundred writes per second at peak. No crowd-sourced real-time contribution flow."

Takeaway
A low peak write volume allows us to focus our database design on optimizing heavy read and search propagation latency, rather than raw ingest throughput.

You
"For nearby search, do we return everything within a radius, the nearest k results, or do we need both?"

Interviewer
"The client can specify either: a radius for proximity filtering, or a k count for nearest-k results. Both modes need to work."

Takeaway
Supporting both radius cutoffs and nearest-K searches forces us to design a search-traversal logic that can stop expanding once target counts or distance limits are met.

You
"After a new POI is created or an existing one is updated, how quickly must the change be visible to users doing nearby searches? Is 30 to 60 seconds of lag acceptable, or does the business need near-instant search freshness?"

Interviewer
"30 to 60 seconds is acceptable. Near-instant is not required. Users can tolerate a short delay before a newly added coffee shop appears."

Takeaway
A 30 to 60 second propagation target lets us decouple our search indexing path from the transactional write path, allowing asynchronous, eventual consistency.

You
"If the primary nearby search cache for a specific geographic region becomes temporarily unavailable or lags, should the system return an error for that region, or is is it acceptable to fall back to a slightly stale copy of the data?"

Interviewer
"Serve the stale data from the last known state. A slightly stale nearby list of restaurants is far better than throwing an error and returning nothing to the user."

Takeaway
Prioritizing read availability means our read path should gracefully tolerate cache replication lag or stale local replicas during peak surges or regional cache drops.

Functional requirements
Given a user's location and an optional radius, return the nearest k POIs ranked by distance, with optional category and keyword filters.
Serve a POI detail page with name, address, coordinates, category, hours, and a rating snapshot.
Support creating and updating POI records (owner or admin writes) so that new or changed POI data eventually appears in search results.
Support paginated browsing of search results beyond the initial nearest set.
Non-functional requirements
Target 99.95% availability for search and detail reads.
Nearby search at p95 < 200 ms, POI detail at p95 < 100 ms, POI create/update acknowledgement at p95 < 300 ms.
Scale for ~200M POIs globally, ~50k search queries per second at peak, ~500 POI writes per second at peak.
Traffic is heavily read-dominant (~100:1 read-to-write ratio) with strong skew toward popular metro areas.
POI records must survive crashes. Geo indexes and caches are rebuildable helpers, not the source of truth.
Tolerate bounded staleness between authoritative POI writes and geo-index freshness, typically 30-60 s propagation.

## Design a Sandboxed Cloud IDE

A cloud IDE (Integrated Development Environment) such as Replit, GitHub Codespaces, Google Colab, or an internal "devbox" lets a user write code, manage files, and run commands entirely from the browser. The code does not run on the user's laptop. It runs on the provider's machines inside a sandbox, which means the provider is executing untrusted programs from thousands of strangers on shared hardware. The product feels like a personal laptop that is always on. The backend is a fleet of short-lived, isolated machines that exist only while someone is working.

We will design the core loop: a user opens a workspace, the platform finds or starts a sandbox for it, the user edits files and types into a terminal, clicks Run and watches logs stream back live, then walks away while the platform suspends the sandbox and keeps the files.

Users expect a laptop that is always on and instant, but the provider can only afford to run their untrusted code on isolated machines that exist while someone is actually typing. Every requirement below pulls on one of three tensions: start latency vs. idle cost, live streaming vs. durable replay, and isolation vs. density.

Clarifying Questions
You
"Is this closer to Colab, where people mostly run things, or Codespaces, where a workspace is a long-lived devbox they come back to every day?"

Interviewer
"Treat it as a devbox. People come back to the same project, but the thing I care about most is what happens when they click Run or Build."

Takeaway
The workspace must outlive any machine, and run/build becomes a tracked job with its own state and log, not just bytes in a terminal.

You
"Whose code is running in there? Only employees, or anyone who signs up?"

Interviewer
"Anyone. Assume some users are actively hostile."

Takeaway
A plain container sharing the host kernel is not a strong enough boundary. We need VM (virtual machine)-grade isolation, which pushes us toward microVMs and egress control.

You
"If a host dies, how much of a user's work can we lose? Zero, or the last minute or so?"

Interviewer
"Losing about a minute is acceptable. Losing the project is not."

Takeaway
Files can live on fast local disk as long as we snapshot them to object storage periodically. We do not need a write-through network filesystem.

You
"If my browser drops in the middle of a long build, should I see the whole log when I reconnect, or just whatever is printing now?"

Interviewer
"The whole build log. And they should be able to open an old run later."

Takeaway
Run logs need offsets and a durable store so the client can resume from where it stopped. The interactive terminal can stay ephemeral and simply redraw.

You
"How many workspaces are active at peak, and is it fine to stop someone's machine after they walk away?"

Interviewer
"About 50k active at peak. Stopping idle machines is expected, but reopening should feel fast."

Takeaway
Idle suspension is required for cost, so resume latency becomes the problem. That leads to warm pools and snapshot restore.

Functional requirements
Users can create a workspace from a runtime template and reopen it later with their files intact.
Users can create, edit, rename, and delete files in the browser, and saves persist across sessions.
Users can open an interactive terminal in the browser and see output in near real time.
Users can click Run or Build to execute their project inside their sandbox and watch the logs stream live.
Users can cancel a running job and later view the full log of a finished run.
Workspaces start on demand and suspend when idle, while the platform manages sandboxes across a host fleet.
Non-functional requirements
Untrusted code must not read another tenant's files, processes, or network, nor escape to the host.
Terminal keystroke echo should stay under 100ms p99 within a region.
A run's first log line should reach the browser within 1s of start.
Warm resume should take under 5s p95, and cold start under 30s p95.
Idle workspaces should release CPU and RAM after about 15min without activity.
Saved files must survive host loss with at most about 60s of lost work.
Run logs are retained for 7 days.
The control plane targets 99.9% availability, and one host failure affects only that host's workspaces.
Per-sandbox CPU, RAM, disk, and egress quotas must stop one tenant from starving its neighbours.

## Design instagram

Instagram is a feed problem with an important twist. Every photo post triggers an asynchronous media processing lifecycle that must finish before a feed can render the image. The design must keep home-feed reads cheap, wait for images to become renderable, and avoid sending a celebrity post to millions of follower feeds synchronously.

Clarifying Questions
You
"Are we handling video, Stories, and Reels as well, or keeping the scope to photo uploads, home feed reads, and follow management?"

Interviewer
"Photo-only posts for this design. Home feed reads and follow management are in scope. Video, Stories, Reels, comments, and explore are out."

Takeaway
Photo-only scope bounds media complexity to simple static resizing and CDN delivery. This avoids the heavy compute and multiple manifest variants required for video transcoding.

You
"When does the system acknowledge a successful upload to the author, and what does a follower's feed show while the photo is still being processed?"

Interviewer
"Acknowledge the upload after the metadata is durably stored, before media processing finishes. The feed can show a placeholder for photos whose renditions are still in progress."

Takeaway
We must split uploads into a fast synchronous metadata check-in and an asynchronous image processing pipeline. Followers can render placeholders while the background renditions complete.

You
"How fresh does the home feed need to be, and does a new follow relationship need to immediately surface that author's posts in the reader's feed?"

Interviewer
"Eventual consistency is fine for the home feed. A lag of a few seconds is acceptable. Follow changes may also take a short time to propagate."

Takeaway
Accepting eventual consistency lets us decouple feed generation from the hot read path. We can precompute timelines out-of-band instead of running heavy, real-time relational joins on every scroll.

You
"Do we need to support authors with very large follower counts, and is there a budget for how much write work a single post can trigger?"

Interviewer
"Yes, celebrity authors with 10M+ followers exist. Synchronous per-follower fanout on every post is too expensive and must be avoided."

Takeaway
We cannot use a single push model for all users. We must isolate celebrity posts and fetch them at query time, preventing massive write amplification under high follower counts.

You
"What should happen if media processing fails for a photo, and is it acceptable for image delivery to get slower temporarily instead of making the post unreadable?"

Interviewer
"A failed rendition is retriable and the original uploaded bytes must not be lost. If image delivery is temporarily slower, that is acceptable as long as the post remains available."

Takeaway
This mandates an immutable original storage layer as our source of truth. If background processing fails or a cache misses, we can always replay transformations from these durable original bytes.

Functional requirements
Users can follow and unfollow other accounts, and those relationship changes affect which authors appear in the reader's home feed.
An author can upload a photo with a caption, and the system durably accepts the post after persisting metadata and initiating the media processing pipeline.
A reader can fetch the newest page of their home feed and paginate older items with an opaque cursor.
The home feed shows recent photo posts from followed accounts with eventual consistency, including a scalable path for celebrity authors whose follower count makes full synchronous fanout too expensive.
Uploaded images are processed into multiple resolutions (thumbnail, standard, full) and served through a CDN for low-latency delivery.
Non-functional requirements
Target 99.9% availability for photo upload and home-feed reads in a healthy region.
Target p95 < 300 ms for upload acknowledgement (ACK) after durable metadata persist, before full processing completes.
Target p95 < 300 ms for the first home-feed page from a warm regional stack.
Assume 50M daily active users (DAU), 300k/s peak home-feed reads, 5k/s peak photo uploads, 15B+ follow edges, and celebrity accounts with 10M+ followers.
Home-feed reads may lag the latest post by a few seconds, but the author's own profile and authoritative post record stay readable immediately after upload ACK.
Accepted post metadata, follow changes, and original uploaded media must survive process or node failure. Materialized feed rows and processed image variants are rebuildable.
The hot post path avoids synchronous O(follower_count) work for large authors.

## Design Uber

Ride-hailing looks like a map and a button, but the backend must answer two fundamentally different questions at the same time. The first is fast and fuzzy: which drivers look plausibly nearby right now? The second is slow and exact: which single driver actually wins this trip under retries, timeouts, and network loss?

Clarifying Questions
You
"Should we design the full Uber platform, including surge pricing, driver onboarding, and payment processing, or focus on the real-time matching, dispatch, trip lifecycle, and location tracking core?"

Interviewer
"Focus on matching, dispatch, the trip lifecycle, and location tracking. Pricing, onboarding, and payment internals are out of scope."

Takeaway
Cutting pricing and payment keeps the design focused on the dispatch core. The main challenge is separating "who looks nearby" from "who actually wins the trip" without mixing those concerns.

You
"If a driver's acceptance arrives a few hundred milliseconds after the offer window has closed, but the trip is still unassigned, should the system accept the late response or reject it unconditionally based on the offer expiry?"

Interviewer
"Reject unconditionally if the offer window has closed. Ambiguous late-accept behavior creates problems we do not want to deal with."

Takeaway
This tells us late accepts should be treated as invalid, even if the trip still happens to be open. That keeps the dispatch state machine simpler and avoids ambiguous reassignment behavior.

You
"Do driver location heartbeats need to be durably stored so the system can replay them or audit exact driver positions, or are they ephemeral signals that only matter for the current dispatch cycle?"

Interviewer
"Ephemeral. We care about where a driver is right now, not about storing a precise record of their historical movements. Completed trip details are recorded through the trip's final state."

Takeaway
This means the location stream is a live matching signal, not part of the authoritative trip record. We should keep that high-frequency path logically separate from the transactional trip lifecycle.

You
"How strict is the one-driver-per-trip rule? If two drivers accept at almost the same time, do we need to prevent the duplicate at commit time, or can the system correct it a few seconds later?"

Interviewer
"Strictly at commit time. Two drivers heading to the same pickup is a customer-facing failure we cannot recover from gracefully."

Takeaway
This tells us single-driver assignment has to be enforced at the exact point of commit, not cleaned up afterward. The design needs a clear way to reject concurrent winners immediately.

You
"If the dispatch loop exhausts all nearby candidates because every driver declined or timed out, should the system immediately tell the rider no drivers are available, or should it queue the request and expand the search area before giving up?"

Interviewer
"Queue the request and expand the search radius before giving up. Telling a rider there are no drivers when there are available drivers a bit farther away is a poor experience."

Takeaway
This means "no drivers available" should be the last resort, not the first miss. The design should leave room for retries and controlled expansion before it gives up on a request.

Functional requirements
A rider can request a ride by providing a pickup location and destination, receive a fare estimate, and confirm the request to begin driver matching.
The system can find nearby available drivers, issue sequential time-bounded offers (each with a short time-to-live), and assign at most one driver to one trip.
Rider and driver apps observe trip lifecycle states in near real time: requested, offered, assigned, en route, in progress, completed, and cancelled.
A rider can cancel a trip before pickup, including while the driver is en route. A driver can accept or decline a ride offer within the offer window.
During an active trip, rider and driver apps exchange periodic location updates so maps and ETAs stay fresh.
When a trip ends, the system durably records the final outcome and hands off fare finalization so both sides can load a stable trip summary afterward.
Non-functional requirements
Nearby-driver lookup should target p95 < 300 ms. Slight staleness is acceptable because this path only suggests candidates, not commits assignments.
Rider request to first driver offer should target p95 < 2 s under normal city load.
Durable trip milestone fanout to both clients should target p95 < 1 s. Location streams may be latest-only with bounded loss.
At most one active trip per rider and at most one active trip per driver, enforced under retries and reordered requests.
Ride request and active-trip APIs target 99.95% availability. Accepted assignments and completed trip records target 99.99% durability.
The system should handle sustained peak bursts of ~100k requests from concentrated areas during rush hours and special events.
Heartbeats and location fanout must stay off the transactional path that commits assignments and trip completion.
