[Skip to content](https://vercel.com/i/agent-orchestration-patterns#geist-skip-nav)

Once an AI feature grows past a single prompt, the decision becomes how to connect large language model (LLM) calls into a system that stays reliable under production load. The right orchestration pattern should match task decomposability, latency tolerance, token budget, and human-in-the-loop requirements. Start with the least complex pattern that solves the problem, then escalate only when the workload demands it. Six patterns map to those tradeoffs across reliability, cost, and coordination.

**Key takeaways:**

- Multi-agent systems can use up to 15× the token volume of standard chats, so task value has to justify the added complexity.

- Under equal compute budgets, single-agent loops match or exceed multi-agent accuracy on multi-hop reasoning tasks across Qwen3, DeepSeek-R1, and Gemini 2.5.

- Prompt chaining is the lowest-risk upgrade from a single LLM call, but chained accuracy compounds step by step.

- Orchestrator-worker is the pattern designed for cases where subtask count and nature are unknown at authoring time, which makes it the entry point for multi-agent work rather than the default.

- Vercel Workflows checkpoints each step and handles failure retries plus pauses for external events, so any of the six patterns can run durably.

- FLORA's creative agent fans a single session across more than 50 image models, with each step persisting and retrying on failure.


## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#agent-orchestration-patterns-at-a-glance) Agent orchestration patterns at a glance

Start with the lowest-complexity pattern before adding agents. The six patterns form a complexity ladder. The premature fan-out anti-pattern appears when a team adds agents before the workload has independent subtasks, compounding cost and failure surface at the same time.

Multi-agent systems use approximately [15× more tokens](https://www.anthropic.com/engineering/multi-agent-research-system) than chat interactions, so task value has to justify the added agents. Pattern choice depends on the workload rather than the team's ambition.

The six patterns differ by fit, token cost, and failure conditions. Use this table as a planning range before choosing a pattern:

| Pattern | Best for | Token cost relative to single call | When to avoid |
| --- | --- | --- | --- |
| Single-agent loop | Tasks that fit one context window with tool access | Baseline | Independent subtasks that benefit from parallel exploration |
| Prompt chaining | Fixed subtasks known at authoring time | Moderate, fixed by chain length | Unknown subtask boundaries |
| Routing | Distinct input categories handled separately | Low to moderate | Inputs that need identical handling |
| Parallelization | Predefined independent subtasks | High, varies with fan-out | Sequential dependencies or shared context |
| Orchestrator-worker | Subtasks unpredictable until runtime | High, varies with worker count | Predictable subtasks |
| Evaluator-optimizer | Clear rubric plus measurable gains from iteration | Moderate, varies with critique cycles | Real-time responses or no rubric |

Those ranges are relative estimates anchored to measured agent and multi-agent token figures. The July 2026 AI Gateway Production Index puts Anthropic at [61% of AI Gateway spend](https://vercel.com/blog/ai-gateway-production-index-july-2026) on 32% of tokens, so the most consequential agentic work concentrates cost. Choosing among [agentic workflow patterns](https://vercel.com/i/what-are-agentic-workflows) comes before any infrastructure decision.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#1.-start-agent-orchestration-with-a-single-agent-loop) 1\. Start agent orchestration with a single-agent loop

Under equal token budgets, [single-agent baselines](https://arxiv.org/html/2604.02460v1) match or exceed multi-agent accuracy on multi-hop reasoning, with reported multi-agent advantages better explained by unaccounted computation than by architecture.

The same constraint appears in production. The less complex architecture will get you far, while parallel writing still runs into coordination and context-sharing constraints. Escalation should follow a capability gap, such as context-window pressure or independent subtasks that can actually run in parallel.

A single-agent loop is an LLM that calls tools, receives results, adds them to context, and repeats until a stopping condition is met. In AI SDK 7, [`ToolLoopAgent`](https://ai-sdk.dev/docs/reference/ai-sdk-core/tool-loop-agent) runs this loop and stops after 20 steps by default through `stopWhen: stepCountIs(20)`. The `prepareStep` callback can adjust the model, tools, messages, and runtime context between steps. AI SDK 7 also adds typed `runtimeContext`, agent-level tool approvals, and total, per-step, per-chunk, and per-tool timeouts. State management problems, including repeated account numbers and re-run searches, push teams off this pattern. A `WorkflowAgent` turns the loop into separate invocations, so completed steps never re-run.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#2.-use-prompt-chaining-for-fixed-agent-orchestration-steps) 2\. Use prompt chaining for fixed agent orchestration steps

Prompt chaining runs a fixed sequence of LLM calls where each call processes the previous output. Prompt chaining fits tasks with fixed decomposition. It trades latency for accuracy by narrowing each call's scope. Accuracy compounds across steps. At 95% per-step accuracy across ten steps, end-to-end accuracy is about 60%, and at 90% it is about 35%.

That compounding is why programmatic gates between steps are not optional. Gates can check schema validity, required fields, policy thresholds, or human approval before the next call inherits a bad intermediate result. Vercel's internal data agent d0 runs durable multi-step orchestration in production.

The AI SDK handles its model calls, while [Vercel Workflows](https://vercel.com/docs/workflows) adds retry and state recovery when Snowflake times out or a model call fails, and pauses a run that has to wait on a person or a webhook. Skip chaining when subtask boundaries are unknown at authoring time, or when independent subtasks could run at the same time.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#3.-route-agent-orchestration-by-input-type) 3\. Route agent orchestration by input type

Routing adds an initial classification step, LLM-based or deterministic, that assigns each input to a specialized downstream handler. It separates concerns and works when distinct categories are better handled separately. Router accuracy sets a ceiling on the whole system, because a misclassified input sends the wrong work to a specialist handler.

Wherever the input space allows it, prefer deterministic classifiers (regex, keyword match, rule-based routing), since they remove one model failure surface entirely. Routing also needs a validation set that reflects production inputs, since a clean taxonomy on paper does not guarantee reliable classification at the boundary.

At the model level, [AI Gateway](https://vercel.com/docs/ai-gateway) routes across hundreds of models through a single endpoint. It handles automatic failover and load balancing, with per-provider fallback. Okara runs chief marketing officer (CMO) agents for [120,000+ businesses](https://vercel.com/customers/how-okara-runs-cmo-agents-for-120000-companies-on-vercel) on this layer, and with retry and fallback handling moved into the gateway it now processes 4 billion tokens daily. Skip routing when every input needs identical handling or classification accuracy can't be validated.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#4.-run-parallel-agent-orchestration-for-independent-subtasks) 4\. Run parallel agent orchestration for independent subtasks

Parallelization runs independent subtasks simultaneously and aggregates their outputs programmatically. It uses predefined subtasks, while orchestrator-worker determines them at runtime. The pattern fits when subtasks can run at the same time for speed, or when multiple perspectives on one task raise confidence in the result. The aggregation step should be defined before fan-out starts, because inconsistent worker outputs can erase the latency benefit at merge time.

AI SDK represents a [subagent](https://ai-sdk.dev/docs/agents/subagents) as an agent invoked through a parent agent's tool. Each subagent receives its own context window and returns a focused result to the parent, which keeps context-heavy or parallel work out of the main agent's history. Subagents add latency and coordination cost, so use them only when context isolation or parallel execution provides a measurable benefit.

In wide fan-out, billing matters as much as code, since each concurrent invocation spends most of its life waiting on a model call. FLORA's creative agent fans out across more than 50 image models from one session. [Fluid compute](https://vercel.com/docs/fluid-compute) prices on active central processing unit (CPU), so waiting on a model call does not add to that meter. Skip parallelization when subtasks must build on one another in sequence or need one shared context.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#5.-choose-orchestrator-worker-agent-orchestration-for-dynamic-decomposition) 5\. Choose orchestrator-worker agent orchestration for dynamic decomposition

In orchestrator-worker, a central LLM determines at runtime which subtasks a request needs, assigns them to worker agents, and synthesizes the results. With the AI SDK, each worker can be implemented as a subagent exposed to a parent `ToolLoopAgent` through a tool. The worker runs with an isolated context and returns a summarized result for synthesis. The fit is a complex task where the subtasks can't be predicted, like coding, where the number of files to change depends on the request. It is over-engineered for anything else. Each worker holds its own context window, which means coordination adds cost as well as capability.

General Intelligence's Cofounder gives founders a full team of agents covering engineering, marketing, search engine optimization (SEO), finance, sales, customer support, and operations, a shape consistent with orchestrator-worker. Its engineers ship [10 pull requests](https://vercel.com/customers/how-general-intelligence-used-agents-to-build-an-agent-platform-on-vercel) (PRs) and 70+ commits per engineer per day across 4,000+ preview branches, and 90% of site reliability engineering (SRE) work is automated. Worker code runs isolated in [Vercel Sandbox](https://vercel.com/docs/sandbox) microVMs with a separate filesystem and network. Skip the pattern when subtasks are predictable, or coordination overhead outweighs the value of dynamic decomposition.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#6.-apply-evaluator-optimizer-agent-orchestration-when-quality-can-be-measured) 6\. Apply evaluator-optimizer agent orchestration when quality can be measured

Evaluator-optimizer pairs two LLM calls in a loop. One generates a response, the other evaluates it and provides feedback, and the cycle continues until a quality threshold or step ceiling is reached. The pattern needs a clear evaluation rubric and measurable gains from iterative refinement, so it earns its cost only when responses improve under critique.

Two signs make the fit stronger: responses improve when a human can articulate useful feedback, and the LLM can provide useful feedback itself. The runaway critique loop anti-pattern appears when ambiguous criteria keep requesting revisions without a measurable endpoint. Avoid the pattern when first-attempt quality already meets requirements, and enforce a hard revision ceiling in application code. For agent-based implementations, the AI SDK exposes `stopWhen` conditions and AI SDK 7 timeout budgets for bounding total and per-step execution.

[Vercel's Turborepo](https://vercel.com/solutions/turborepo) performance work is the human-in-the-loop version of that critique cycle. AI agents, Vercel Sandboxes, and human review over eight days produced up to a [96% speed improvement](https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans), and the same effort found that unattended state-of-the-art agents without context engineering fall short.

Vercel's Next.js agent evals found `AGENTS.md` outperformed skills on Next.js 16 APIs. Vercel Sandbox caps each isolated run at 45 minutes on Hobby and 24 hours on Pro and Enterprise, which bounds how long a critique loop can execute.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#how-vercel-runs-agent-orchestration-patterns-in-production) How Vercel runs agent orchestration patterns in production

The six patterns are architecture decisions, but four platform behaviors remove failure modes that compound across them. In practice, they address the same runtime concerns across different shapes of work, including state recovery, model selection, fan-out cost, and isolated execution.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#fluid-compute-reduces-active-cpu-cost-in-fan-out-steps) Fluid compute reduces active-CPU cost in fan-out steps

Parallelization and orchestrator-worker fan out into many concurrent invocations dominated by I/O wait. A team has to reject any billing model that charges for that wait, since it makes wide fan-out impractical. Fluid compute meters active CPU separately at a [$0.128/hour base rate](https://vercel.com/docs/functions/usage-and-pricing), with regional rates and other metered resources still applicable.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#vercel-workflows-makes-each-pattern-durable) Vercel Workflows makes each pattern durable

Chaining, orchestrator-worker, and evaluator-optimizer all fail expensively when state disappears mid-run. The `use workflow` directive turns async TypeScript functions into durable workflows with checkpointing and retries. Runs can also pause and resume, so a failed run continues from the last good step. Workflow steps on Pro and Enterprise support execution durations up to 1,800 seconds.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#ai-gateway-centralizes-model-routing-across-patterns) AI Gateway centralizes model routing across patterns

Routing and orchestrator-worker select models by task requirements and provider health, while cost constraints shape the fallback policy. Per-provider integration work slows product work. AI Gateway consolidates that into one unified endpoint with retries and load balancing, plus configurable fallbacks and zero markup on tokens. Provider integration lives in the gateway rather than application code, so teams can adopt newly available models without rebuilding each provider path.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#vercel-sandbox-isolates-worker-and-evaluator-execution) Vercel Sandbox isolates worker and evaluator execution

Orchestrator-worker and evaluator-optimizer patterns run generated or untrusted code in coding-agent workloads. Coding agents need that isolation before they are safe to point at a real repository. Each Vercel Sandbox is a Firecracker microVM with its own filesystem and network, and `Sandbox.fork()` creates isolated branches from a shared snapshot. Each agent can also run as its own Linux user with a private home directory, while groups allow selected files to be shared between agents. When traces span orchestrators and workers, session correlation links them into a single connected view.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#match-your-orchestration-pattern-to-your-workload,-then-ship) Match your orchestration pattern to your workload, then ship

Choosing a pattern whose token cost or operational complexity exceeds the task's value creates the main risk. Escalate for a concrete capability gap, such as a task that no longer fits one context window. Vercel supports all six patterns on a single infrastructure stack:

- **Durable orchestration:** Vercel Workflows checkpoints every step so no pattern restarts from zero on failure.

- **Active-CPU billing:** Fluid compute excludes model-call I/O wait from active-CPU metering, which makes fan-out patterns more practical while other metered resources still apply.

- **Unified model routing:** AI Gateway handles automatic failover across the same routing layer, removing per-provider integration from application code.

- **Isolated code execution:** Vercel Sandbox runs worker and evaluator code in a Firecracker microVMs with bounded execution windows.

- **End-to-end observability:** [OpenTelemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry) session correlation links traces across orchestrator and worker agents in one view.


Deploy a [new project](https://vercel.com/new) to start with a single-agent loop, or begin from [Vercel templates](https://vercel.com/templates) and escalate patterns only when the workload demands it. Keep the first version as small as the task allows, then add coordination when the workload proves the need.

## [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#frequently-asked-questions-about-agent-orchestration) Frequently asked questions about agent orchestration

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#what-is-the-difference-between-orchestrator-worker-and-hierarchical-multi-agent-patterns) What is the difference between orchestrator-worker and hierarchical multi-agent patterns?

A supervisor routes among a predefined roster of specialists and controls the communication flow. An orchestrator derives the subtasks themselves at runtime and delegates them to worker agents.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#when-should-i-use-a-single-agent-loop-instead-of-multi-agent-orchestration) When should I use a single-agent loop instead of multi-agent orchestration?

Use a single-agent loop when the task fits one context window, when subtasks cannot be split to run in parallel, and when latency or token budgets are tight. Escalate only when a concrete capability gap makes multi-agent orchestration necessary.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#how-does-token-cost-scale-across-agent-orchestration-patterns) How does token cost scale across agent orchestration patterns?

Token cost scales as you add model calls, workers, critique cycles, and separate context windows. Use the relative multipliers in the table as a planning range rather than treating any pattern as a fixed price.

### [Copy link to heading](https://vercel.com/i/agent-orchestration-patterns\#what-makes-a-workflow-durable-in-an-agent-orchestration-context) What makes a workflow durable in an agent orchestration context?

Durable execution checkpoints state after each step, so a failure mid-chain resumes from the last successful step. Vercel Workflows implements durability with the `use workflow` directive, so a run can pause for a webhook or a human approval without holding compute and resume from the last checkpoint.

## More Build with AI articles

- [**How to choose an embedding model for production retrieval** \\
Embedding models set retrieval quality and lock your schema. Learn six selection criteria, four eval practices, and how to keep model swaps cheap.](https://vercel.com/i/embedding-model-selection-guide)
- [**5 AI agent guardrails that hold in production** \\
Learn five runtime guardrail patterns for AI agents: input validation, tool scoping, approval gates, loop limits, and output checks on Vercel.](https://vercel.com/i/five-ai-agent-guardrails-production)

* * *

## Ready to deploy?

[Start deploying](https://vercel.com/new) [Talk to an expert](https://vercel.com/contact/sales)
