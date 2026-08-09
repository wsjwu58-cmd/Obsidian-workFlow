August 4, 2026

[Guadalupe Aliseda-Canton](https://blog.duolingo.com/author/guadalupe/)

# Making production-ready agents the default: building Duolingo’s agent platform

See how we made AI agents easy to build, run, and improve in production.

August 4, 2026

[Guadalupe Aliseda-Canton](https://blog.duolingo.com/author/guadalupe/)

![Lin on a motorcycle and Vikram on foot, traversing two Duolingo paths on cell phones.](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/08/cover_Production-ready-agent-AI.png)

## TL;DR

At Duolingo, teams were repeatedly rebuilding the same infrastructure around AI agents. We solved this by creating a shared platform where developers define an agent once, while the platform handles execution, observability, orchestration, and evaluation. As a result, teams can build, reuse, and improve agents more easily and quickly at scale.

* * *

## Every team was rebuilding the same infrastructure

AI agents are easy to build and prototype locally. You write a prompt, give the model access to the tools and files it needs, run it, and then iterate with the prompt until you are happy with the output.

The hard part starts after that.

Once you want to run it in the cloud, the work shifts from prompting to productionizing. Every useful agent needs a surprising amount of surrounding infrastructure: setting up MCP servers, preparing credentials, cloning repositories, and loading project context.

At Duolingo, this was becoming a real pain point because we were recreating all of this infrastructure across every project that needed agents. The infrastructure one team built for one system couldn’t easily be reused by another team working on a different system or platform, so teams kept rebuilding the same foundation from scratch.

There was also a distribution problem. Once an agent had been made, we often wanted it to be available in different places. This requires the agent to be invokable across many surfaces like Slack, internal sites, a CLI, or another Temporal workflow. Without a shared execution layer, you would need to rebuild agents across those systems.

Lastly, we wanted to provide all agents with the orchestration, evaluation, and observability they need to truly be production-ready.

## Defining an agent

To address these pain points, we built a system that allows developers to easily spin up agents by simply defining what the agent should do (the system prompt), what tools it should have (which MCPs should be enabled), and what it should have access to (which repos should be cloned to its workspace). Everything else is abstracted away.

Agents are defined in a registry, making them reusable from different entry points. A simplified definition looks like this:

```python
AgentDefinition(
    name="incident_summary",
    description="Summarize incident context from prior investigation steps.",
    owner="Incident Team",
    system_prompt="Use the provided evidence to write a concise summary.",
    model="gpt-5.5",
    mcp_servers=("github", "sentry"),
    output_type=IncidentSummaryOutput,
)
```

This gives us a consistent way to describe what an agent is, who owns it, which provider it uses, what tools it needs, and what the output structure should be.

We then have a Temporal workflow called `AgentWorkflow` that handles the rest.

The goal of `AgentWorkflow` is not to be the agent itself; instead, it serves as a wrapper that abstracts away the shared infrastructure and setup requirements.

At a high level, it does four things:

1. Loads an agent’s definition
2. Prepares the execution environment
3. Runs the agent using an LLM provider SDK
4. Returns the output of the agent

Once an agent is defined in the registry, triggering it is simple from the caller’s perspective. They only need to trigger the workflow with the agent name and user prompt as inputs.

```python
AgentWorkflow(
    agent_name="incident_summary",
    prompt="Summarize the investigation findings for this incident.",
)
```

## Why Temporal?

Temporal is a durable workflow engine. It persists state, retries safely, and coordinates long-running work across systems.

That maps really well to agents because they can:

- Take several minutes to run
- Call external tools
- Wait for human input
- Fail in ways that need retry or debugging

Instead of treating an agent run as a one-off process, we can treat it as a workflow. The workflow owns the durable state and orchestration. Activities handle side effects—like preparing a workspace, cloning a repo, or saving results—while queries expose status while the workflow is running.

We had also already built enough infrastructure around Temporal that we could trigger workflows from any entry point; since agents are run in a workflow, we already supported running agents from anywhere. You can hear more on that from Staff Software Engineer Zhihao Wang [here](https://temporal.io/resources/case-studies/duolingo-temporal-nexus?ref=blog.duolingo.com) if you’re curious.

## Decoupling definition from execution

Before building this platform, the prompt, the model, the SDK, the tooling, and the execution environment were all tightly coupled.

AgentWorkflow changed that. We can create an agent by defining what it does, what tools it needs, and what it returns. The workflow manages everything about how that agent runs.

This distinction is crucial for building an agent platform that can scale. Once execution becomes independent from behavior, we can evolve runtimes, models, tooling, and evaluation independently without changing the interface consumers use.

That separation is what made the next iteration of the platform possible: support for the OpenAI Agents SDK.

### A new runtime

AgentWorkflow already supported a few runtimes, including the Claude Agents SDK and Codex CLI. Adding support for another runtime did not require changing how agents were defined or invoked; it simply became another implementation behind the same workflow abstraction.

Adding this new runtime was very impactful. The OpenAI Agents SDK significantly improved the operational characteristics of the platform, specifically in two ways:

1. With Temporal’s plugin, MCP tool calls become Temporal activities. This makes the system more durable because tool failures can use the same retry policies, state management, and failure handling as any other workflow activity. It also makes the system more observable because every tool call—including inputs, outputs, failures, and retries—is visible in the Temporal UI.
2. The OpenAI Agents SDK also supports routing requests through a proxy. This allowed us to use our internal LLM Gateway, which provides cost tracking, usage tracking, and provider abstraction. Rather than supporting separate SDK integrations for each model provider, we can route requests through the gateway and switch providers behind a consistent interface.

## Evaluating agents

Once agents are reusable, the next challenge is knowing whether they are getting better or worse.

This is especially important for agents that change code. It is not enough to ask whether the agent’s output sounds reasonable; we need to know whether it made the right change.

That’s why we built agent eval infrastructure.

Agent evals run the real agent against authored scenarios. They capture the agent’s output, change files, and git diff before grading the result.

A simplified eval case looks like this:

```python
agent_name: fix_ci
cases:
  - id: missing_requests_import
    description: Fixes a deterministic NameError by importing requests.
    input:
      repo_fixture: fixtures/missing_requests_repo
      prompt_file: prompts/fix_ci_eval_prompt.md
    graders:
      - type: structured_output
        expect:
          no_op: false
      - type: diff_assertions
        include:
          - "import requests"
        exclude:
          - "pytest.mark.skip"
        max_changed_files: 1
      - type: no_op_consistency
```

This lets us test both the agent’s output and what it actually changes.

### How grading works

We use several types of graders.

`structured_output` checks fields in the agent’s structured response.

`diff_assertions` checks the actual repo diff. It can require specific changes, catch risky changes, limit the number of changed files, or restrict edits to certain paths.

`no_op_consistency` checks that the reported outcome matches the repo state. If the output indicates that no change was needed but files changed, the eval fails. If the output indicates that a fix was made but the diff is empty, the eval also fails.

For cases where exact diff assertions are too brittle, we also support an optional LLM-as-judge. However, deterministic graders are the foundation. The LLM-as-judge is useful, but we do not want our only signal to be one model judging another model’s work.

For agent evals to be useful, they need to inspect artifacts, not just prose.

### Running evals as workflows

The eval system itself also runs on Temporal.

The suite workflow loads eval cases, starts a child workflow for each case and repetition, aggregates results, renders a report, and optionally saves the run for a dashboard.

This gives evals the same durability properties as production agent runs. A long-running eval case can keep running. A failed case is captured explicitly. Repetitions can run in parallel. Results can be persisted and reviewed later.

This also makes evals feel less like a local script and more like part of the platform.

## From weeks to minutes

Before this platform, creating a production-ready agent was a complex multi-step project. Teams had to choose an SDK, learn its nuances, set up repository cloning, configure MCP servers, and wire up credentials. Depending on the use case, this setup could take several weeks.

Now, creating an agent takes about 10 minutes. A developer can use an internal site to select MCPs, choose a model, and define a system prompt to immediately create an agent. From there, they can invoke it from anywhere without worrying about underlying details.

That speedup is only part of the impact. Every agent created through the platform automatically gets durability, observability, orchestration, evaluation, and multi-entry-point invocation. Agents are also more useful because they can be used outside of the systems that created them. Once defined, they can be used by other teams, other workflows, and eventually other agents.

Agents currently power workflows that fix CI failures, address code review comments, and support internal tools like our Slack bot for release managers. This bot uses specialized agents composed together to investigate crashes, identify relevant changes, and summarize findings.

## What’s next?

So far, this infrastructure provides a foundation for running and evaluating reusable agents.

The main things we are focusing on now are:

- Automating eval creation from engineer feedback on agent results to enable a continuous, low-effort improvement loop.
- Enabling agent orchestration. Because agents run as workflows, they can also be exposed as tools for other agents. This opens the door to larger autonomous systems where agents can trigger one another while Temporal manages durability for the entire system.

## Conclusion

Good abstractions have always been how developers move fast. When a complex problem is solved once and wrapped in a clean interface, everyone who follows inherits that work and writes better code without additional overhead.

This idea is more important now than ever. AI generates code rapidly, but not necessarily high-quality code. It is trivial to have tools like Claude Code or Codex build an agent, but those tools do not automatically consider durability, observability, or evaluation. Left alone, every new agent becomes its own infrastructure problem. The more code we generate, the more valuable an abstraction that guarantees quality becomes.

The platform we built is that abstraction. It does more than speed up creation; it changes the nature of the agents created. By moving infrastructure concerns into the platform, every new agent inherits them automatically, allowing developers to focus on behavior rather than durability or observability.

Moving fast is usually framed as a tradeoff against building production-ready systems. This platform collapses that tradeoff: the same tools that allow developers and AI to move quickly also ensure what they build is ready for production.

If working on practical, production-grade AI systems that make a real impact across the company interests you, we’re hiring!

[SEE OUR OPEN ROLES HERE](https://careers.duolingo.com/?department=Engineering&utm_source=blog.duolingo.com&utm_medium=blog&utm_campaign=prodready_blog_080426#careers)

TAGS

[Life at Duolingo](https://blog.duolingo.com/tag/life-at-duolingo)

[Engineering](https://blog.duolingo.com/tag/engineering)

SHARE ARTICLE

[LinkedIn](https://www.linkedin.com/shareArticle?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&title=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&summary=See%20how%20we%20made%20AI%20agents%20easy%20to%20build%2C%20run%2C%20and%20improve%20in%20production.&source=%5Bobject%20Object%5D "LinkedIn")[Facebook](https://www.facebook.com/sharer/sharer.php?u=https://blog.duolingo.com/production-ready-ai-agent-platform/ "Facebook")[Twitter](https://twitter.com/intent/tweet?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&text=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&media=https%3A%2F%2Fstorage.ghost.io%2Fc%2F7a%2F33%2F7a33d0f4-927d-4fe8-a6bf-96131b5e76d4%2Fcontent%2Fimages%2F2026%2F08%2Fcover_Production-ready-agent-AI.png "Twitter")[Share on KakaoTalk](https://story.kakao.com/share?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&title=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&media=https%3A%2F%2Fstorage.ghost.io%2Fc%2F7a%2F33%2F7a33d0f4-927d-4fe8-a6bf-96131b5e76d4%2Fcontent%2Fimages%2F2026%2F08%2Fcover_Production-ready-agent-AI.png "Share on KakaoTalk")[WhatsApp](whatsapp://send?text=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform%20https://blog.duolingo.com/production-ready-ai-agent-platform/ "WhatsApp")[Email](mailto:?subject=Check%20out%20this%20post%20from%20Duolingo&body=Hi!%20I%20thought%20you%20might%20enjoy%20this%20post:%20Making%20production-ready%20agents%20the%20default:%20building%20Duolingo%E2%80%99s%20agent%20platform%0D%0A%0D%0Ahttps://blog.duolingo.com/production-ready-ai-agent-platform/ "Email")

### RELATED ARTICLES

[![](https://blog.duolingo.com/production-ready-ai-agent-platform/)](about:blank#)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_AI-iOS-unit-test-generation-pipeline.png)](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

Jun 24[Kush Agrawal](https://blog.duolingo.com/author/kush/)

[**How we built an automated unit test generation pipeline for iOS**](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_How-a-simple-code-change-reduced-CPU-usage-by-97_.png)](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

Jun 22[Fabien Loudet](https://blog.duolingo.com/author/fabien/)

[**How a simple code change reduced CPU usage by 97%**](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/05/cover_How-I-Used-Duolingo-to-Find-My-Family-in-Poland.png)](https://blog.duolingo.com/learning-polish-family-reunion/)

Jun 1[David Sawicki](https://blog.duolingo.com/author/david-sawicki/)

[**How I used Duolingo to find my family in Poland**](https://blog.duolingo.com/learning-polish-family-reunion/)

### RELATED ARTICLES

[![](https://blog.duolingo.com/production-ready-ai-agent-platform/)](about:blank#)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_AI-iOS-unit-test-generation-pipeline.png)](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

Jun 24[Kush Agrawal](https://blog.duolingo.com/author/kush/)

[**How we built an automated unit test generation pipeline for iOS**](https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_How-a-simple-code-change-reduced-CPU-usage-by-97_.png)](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

Jun 22[Fabien Loudet](https://blog.duolingo.com/author/fabien/)

[**How a simple code change reduced CPU usage by 97%**](https://blog.duolingo.com/reduce-cpu-usage-97-percent/)

[![](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/05/cover_How-I-Used-Duolingo-to-Find-My-Family-in-Poland.png)](https://blog.duolingo.com/learning-polish-family-reunion/)

Jun 1[David Sawicki](https://blog.duolingo.com/author/david-sawicki/)

[**How I used Duolingo to find my family in Poland**](https://blog.duolingo.com/learning-polish-family-reunion/)