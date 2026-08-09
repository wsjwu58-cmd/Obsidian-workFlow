<!DOCTYPE html><html lang="en" style="user-select: auto;">
<body class="post-template tag-life-at-duolingo tag-engineering" style="user-select: text;"><div id="MathJax_Message" style="display: none;"></div>
    <div class="site-wrapper" style="user-select: auto;">
        
        <main class="page-body" style="user-select: auto;">
                
    
    

<article class="post-page has-mobile-view" style="user-select: auto;">
    <div class="wrapper post-wrapper" style="user-select: auto;">
        <div class="post-banner" style="user-select: auto;">
            <div class="post-banner--header" style="user-select: auto;">
                 <div class="caption-wrap mobile-caption bannerCaption" style="user-select: auto;">
                    <span class="caption" style="user-select: auto;">
                            <time datetime="2026-08-04" style="user-select: auto;">August 4, 2026</time>
                                                <div class="divider mobile" style="user-select: auto;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none" style="user-select: auto;">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round" style="user-select: auto;"></path>
</svg>
                        </div>
                    </span>
                    <div class="divider" style="user-select: auto;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none" style="user-select: auto;">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round" style="user-select: auto;"></path>
</svg>
                    </div>
                    <span class="caption author" style="user-select: auto;">
                                <a href="https://blog.duolingo.com/author/guadalupe/" style="user-select: auto;">Guadalupe Aliseda-Canton</a>
                                            </span>
                    
                </div>
                    <h1 class="section-title post-title" style="user-select: auto;">Making production-ready agents the default: building Duolingo’s agent platform</h1>
                                <p style="user-select: auto;">See how we made AI agents easy to build, run, and improve in production.</p>
                <div class="caption-wrap desktop-caption bannerCaption" style="user-select: auto;">
                    <span class="caption" style="user-select: auto;">
                            <time datetime="2026-08-04" style="user-select: auto;">August 4, 2026</time>
                                            </span>
                    <div class="divider" style="user-select: auto;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none" style="user-select: auto;">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round" style="user-select: auto;"></path>
</svg>
                    </div>
                    <span class="caption author" style="user-select: auto;">
                                <a href="https://blog.duolingo.com/author/guadalupe/" style="user-select: auto;">Guadalupe Aliseda-Canton</a>
                                            </span>
                    
                </div>
            </div>
            <div class="post-banner--image" style="user-select: auto;">
                    <img src="https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/08/cover_Production-ready-agent-AI.png" alt="Lin on a motorcycle and Vikram on foot, traversing two Duolingo paths on cell phones." style="user-select: auto;">
            </div>
        </div>
        <div class="section-divider" style="user-select: auto;"></div>
        <main style="user-select: auto;">
            <div class="post-content" style="user-select: auto;">
                <h2 id="tldr" style="user-select: auto;">TL;DR</h2><p style="user-select: auto;">At Duolingo, teams were repeatedly rebuilding the same infrastructure around AI agents. We solved this by creating a shared platform where developers define an agent once, while the platform handles execution, observability, orchestration, and evaluation. As a result, teams can build, reuse, and improve agents more easily and quickly at scale.</p><p style="user-select: auto;"></p><hr style="user-select: auto;"><h2 id="every-team-was-rebuilding-the-same-infrastructure" style="user-select: auto;">Every team was rebuilding the same infrastructure</h2><p style="user-select: auto;">AI agents are easy to build and prototype locally. You write a prompt, give the model access to the tools and files it needs, run it, and then iterate with the prompt until you are happy with the output.</p><p style="user-select: auto;">The hard part starts after that.</p><p style="user-select: auto;">Once you want to run it in the cloud, the work shifts from prompting to productionizing. Every useful agent needs a surprising amount of surrounding infrastructure: setting up MCP servers, preparing credentials, cloning repositories, and loading project context.</p><p style="user-select: auto;">At Duolingo, this was becoming a real pain point because we were recreating all of this infrastructure across every project that needed agents. The infrastructure one team built for one system couldn’t easily be reused by another team working on a different system or platform, so teams kept rebuilding the same foundation from scratch.</p><p style="user-select: auto;">There was also a distribution problem. Once an agent had been made, we often wanted it to be available in different places. This requires the agent to be invokable across many surfaces like Slack, internal sites, a CLI, or another Temporal workflow. Without a shared execution layer, you would need to rebuild agents across those systems.</p><p style="user-select: auto;">Lastly, we wanted to provide all agents with the orchestration, evaluation, and observability they need to truly be production-ready.</p><h2 id="defining-an-agent" style="user-select: auto;">Defining an agent</h2><p style="user-select: auto;">To address these pain points, we built a system that allows developers to easily spin up agents by simply defining what the agent should do (the system prompt), what tools it should have (which MCPs should be enabled), and what it should have access to (which repos should be cloned to its workspace). Everything else is abstracted away.</p><p style="user-select: auto;">Agents are defined in a registry, making them reusable from different entry points. A simplified definition looks like this:</p><pre style="user-select: auto;" class="language-python" tabindex="0"><code class="language-python" style="user-select: auto;">AgentDefinition(
    name="incident_summary",
    description="Summarize incident context from prior investigation steps.",
    owner="Incident Team",
    system_prompt="Use the provided evidence to write a concise summary.",
    model="gpt-5.5",
    mcp_servers=("github", "sentry"),
    output_type=IncidentSummaryOutput,
)</code></pre><p style="user-select: auto;">This gives us a consistent way to describe what an agent is, who owns it, which provider it uses, what tools it needs, and what the output structure should be.</p>
<!--kg-card-begin: html-->
<p style="user-select: auto;">We then have a Temporal workflow called <code style="font-family: courier; border: 1px solid rgb(187, 187, 187); background: rgb(245, 242, 240); user-select: auto;">AgentWorkflow</code> that handles the rest.<br style="user-select: auto;">
<br style="user-select: auto;">
The goal of <code style="font-family: courier; border: 1px solid rgb(187, 187, 187); background: rgb(245, 242, 240); user-select: auto;">AgentWorkflow</code> is not to be the agent itself; instead, it serves as a wrapper that abstracts away the shared infrastructure and setup requirements.</p>
<!--kg-card-end: html-->
<p style="user-select: auto;">At a high level, it does four things:</p><ol style="user-select: auto;"><li style="user-select: auto;">Loads an agent’s definition</li><li style="user-select: auto;">Prepares the execution environment</li><li style="user-select: auto;">Runs the agent using an LLM provider SDK</li><li style="user-select: auto;">Returns the output of the agent</li></ol><p style="user-select: auto;">Once an agent is defined in the registry, triggering it is simple from the caller’s perspective. They only need to trigger the workflow with the agent name and user prompt as inputs.</p><pre style="user-select: auto;" class="language-python" tabindex="0"><code class="language-python" style="user-select: auto;">AgentWorkflow(
    agent_name="incident_summary",
    prompt="Summarize the investigation findings for this incident.",
)</code></pre><h2 id="why-temporal" style="user-select: auto;">Why Temporal?</h2><p style="user-select: auto;">Temporal is a durable workflow engine. It persists state, retries safely, and coordinates long-running work across systems.</p><p style="user-select: auto;">That maps really well to agents because they can:</p><ul style="user-select: auto;"><li style="user-select: auto;">Take several minutes to run</li><li style="user-select: auto;">Call external tools</li><li style="user-select: auto;">Wait for human input</li><li style="user-select: auto;">Fail in ways that need retry or debugging</li></ul><p style="user-select: auto;">Instead of treating an agent run as a one-off process, we can treat it as a workflow. The workflow owns the durable state and orchestration. Activities handle side effects—like preparing a workspace, cloning a repo, or saving results—while queries expose status while the workflow is running.</p><p style="user-select: auto;">We had also already built enough infrastructure around Temporal that we could trigger workflows from any entry point; since agents are run in a workflow, we already supported running agents from anywhere. You can hear more on that from Staff Software Engineer Zhihao Wang <a href="https://temporal.io/resources/case-studies/duolingo-temporal-nexus?ref=blog.duolingo.com" style="user-select: auto;"><u style="user-select: auto;">here</u></a> if you’re curious.</p><h2 id="decoupling-definition-from-execution" style="user-select: auto;">Decoupling definition from execution</h2><p style="user-select: auto;">Before building this platform, the prompt, the model, the SDK, the tooling, and the execution environment were all tightly coupled.</p><p style="user-select: auto;">AgentWorkflow changed that. We can create an agent by defining what it does, what tools it needs, and what it returns. The workflow manages everything about how that agent runs.</p><p style="user-select: auto;">This distinction is crucial for building an agent platform that can scale. Once execution becomes independent from behavior, we can evolve runtimes, models, tooling, and evaluation independently without changing the interface consumers use.</p><p style="user-select: auto;">That separation is what made the next iteration of the platform possible: support for the OpenAI Agents SDK.</p><h3 id="a-new-runtime" style="user-select: auto;">A new runtime</h3><p style="user-select: auto;">AgentWorkflow already supported a few runtimes, including the Claude Agents SDK and Codex CLI. Adding support for another runtime did not require changing how agents were defined or invoked; it simply became another implementation behind the same workflow abstraction.</p><p style="user-select: auto;">Adding this new runtime was very impactful. The OpenAI Agents SDK significantly improved the operational characteristics of the platform, specifically in two ways:</p><ol style="user-select: auto;"><li style="user-select: auto;">With Temporal’s plugin, MCP tool calls become Temporal activities. This makes the system more durable because tool failures can use the same retry policies, state management, and failure handling as any other workflow activity. It also makes the system more observable because every tool call—including inputs, outputs, failures, and retries—is visible in the Temporal UI.</li><li style="user-select: auto;">The OpenAI Agents SDK also supports routing requests through a proxy. This allowed us to use our internal LLM Gateway, which provides cost tracking, usage tracking, and provider abstraction. Rather than supporting separate SDK integrations for each model provider, we can route requests through the gateway and switch providers behind a consistent interface.</li></ol><h2 id="evaluating-agents" style="user-select: auto;">Evaluating agents</h2><p style="user-select: auto;">Once agents are reusable, the next challenge is knowing whether they are getting better or worse.</p><p style="user-select: auto;">This is especially important for agents that change code. It is not enough to ask whether the agent’s output sounds reasonable; we need to know whether it made the right change.</p><p style="user-select: auto;">That’s why we built agent eval infrastructure.</p><p style="user-select: auto;">Agent evals run the real agent against authored scenarios. They capture the agent’s output, change files, and git diff before grading the result.</p><p style="user-select: auto;">A simplified eval case looks like this:</p><pre style="user-select: auto;" class="language-python" tabindex="0"><code class="language-python" style="user-select: auto;">agent_name: fix_ci
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
      - type: no_op_consistency</code></pre><p style="user-select: auto;">This lets us test both the agent’s output and what it actually changes.</p><h3 id="how-grading-works" style="user-select: auto;">How grading works</h3><p style="user-select: auto;">We use several types of graders.</p>
<!--kg-card-begin: html-->
<p style="user-select: auto;"><code style="font-family: courier; border: 1px solid rgb(187, 187, 187); background: rgb(245, 242, 240); user-select: auto;">structured_output</code> checks fields in the agent’s structured response.<br style="user-select: auto;">
<br style="user-select: auto;">
<code style="font-family: courier; border: 1px solid rgb(187, 187, 187); background: rgb(245, 242, 240); user-select: auto;">diff_assertions</code> checks the actual repo diff. It can require specific changes, catch risky changes, limit the number of changed files, or restrict edits to certain paths.<br style="user-select: auto;">
<br style="user-select: auto;">
<code style="font-family: courier; border: 1px solid rgb(187, 187, 187); background: rgb(245, 242, 240); user-select: auto;">no_op_consistency</code> checks that the reported outcome matches the repo state. If the output indicates that no change was needed but files changed, the eval fails. If the output indicates that a fix was made but the diff is empty, the eval also fails.</p>
<!--kg-card-end: html-->
<p style="user-select: auto;">For cases where exact diff assertions are too brittle, we also support an optional LLM-as-judge. However, deterministic graders are the foundation. The LLM-as-judge is useful, but we do not want our only signal to be one model judging another model’s work.</p><p style="user-select: auto;">For agent evals to be useful, they need to inspect artifacts, not just prose.</p><h3 id="running-evals-as-workflows" style="user-select: auto;">Running evals as workflows</h3><p style="user-select: auto;">The eval system itself also runs on Temporal.</p><p style="user-select: auto;">The suite workflow loads eval cases, starts a child workflow for each case and repetition, aggregates results, renders a report, and optionally saves the run for a dashboard.</p><p style="user-select: auto;">This gives evals the same durability properties as production agent runs. A long-running eval case can keep running. A failed case is captured explicitly. Repetitions can run in parallel. Results can be persisted and reviewed later.</p><p style="user-select: auto;">This also makes evals feel less like a local script and more like part of the platform.</p><h2 id="from-weeks-to-minutes" style="user-select: auto;">From weeks to minutes</h2><p style="user-select: auto;">Before this platform, creating a production-ready agent was a complex multi-step project. Teams had to choose an SDK, learn its nuances, set up repository cloning, configure MCP servers, and wire up credentials. Depending on the use case, this setup could take several weeks.</p><p style="user-select: auto;">Now, creating an agent takes about 10 minutes. A developer can use an internal site to select MCPs, choose a model, and define a system prompt to immediately create an agent. From there, they can invoke it from anywhere without worrying about underlying details.</p><p style="user-select: auto;">That speedup is only part of the impact. Every agent created through the platform automatically gets durability, observability, orchestration, evaluation, and multi-entry-point invocation. Agents are also more useful because they can be used outside of the systems that created them. Once defined, they can be used by other teams, other workflows, and eventually other agents.</p><p style="user-select: auto;">Agents currently power workflows that fix CI failures, address code review comments, and support internal tools like our Slack bot for release managers. This bot uses specialized agents composed together to investigate crashes, identify relevant changes, and summarize findings.</p><h2 id="what%E2%80%99s-next" style="user-select: auto;">What’s next?</h2><p style="user-select: auto;">So far, this infrastructure provides a foundation for running and evaluating reusable agents.</p><p style="user-select: auto;">The main things we are focusing on now are:</p><ul style="user-select: auto;"><li style="user-select: auto;">Automating eval creation from engineer feedback on agent results to enable a continuous, low-effort improvement loop.</li><li style="user-select: auto;">Enabling agent orchestration. Because agents run as workflows, they can also be exposed as tools for other agents. This opens the door to larger autonomous systems where agents can trigger one another while Temporal manages durability for the entire system.</li></ul><h2 id="conclusion" style="user-select: auto;">Conclusion</h2><p style="user-select: auto;">Good abstractions have always been how developers move fast. When a complex problem is solved once and wrapped in a clean interface, everyone who follows inherits that work and writes better code without additional overhead.</p><p style="user-select: auto;">This idea is more important now than ever. AI generates code rapidly, but not necessarily high-quality code. It is trivial to have tools like Claude Code or Codex build an agent, but those tools do not automatically consider durability, observability, or evaluation. Left alone, every new agent becomes its own infrastructure problem. The more code we generate, the more valuable an abstraction that guarantees quality becomes.</p><p style="user-select: auto;">The platform we built is that abstraction. It does more than speed up creation; it changes the nature of the agents created. By moving infrastructure concerns into the platform, every new agent inherits them automatically, allowing developers to focus on behavior rather than durability or observability.</p><p style="user-select: auto;">Moving fast is usually framed as a tradeoff against building production-ready systems. This platform collapses that tradeoff: the same tools that allow developers and AI to move quickly also ensure what they build is ready for production.</p><p style="user-select: auto;">If working on practical, production-grade AI systems that make a real impact across the company interests you, we’re hiring!</p><div class="kg-card kg-button-card kg-align-center" style="user-select: auto;"><a href="https://careers.duolingo.com/?department=Engineering&amp;utm_source=blog.duolingo.com&amp;utm_medium=blog&amp;utm_campaign=prodready_blog_080426#careers" class="kg-btn kg-btn-accent" style="user-select: auto;">SEE OUR OPEN ROLES HERE</a></div>
            </div>
        </main>
        <div class="tags-container" style="user-select: auto;">
                <div class="tags-title" style="user-select: auto;">TAGS</div>
                        <div class="tags-list" style="user-select: auto;">
                        <div class="tag-item" style="user-select: auto;">
                            <a href="https://blog.duolingo.com/tag/life-at-duolingo" class="tag-text" style="user-select: auto; display: flex;">
                                Life at Duolingo
                            </a>
                        </div>
                        <div class="tag-item" style="user-select: auto;">
                            <a href="https://blog.duolingo.com/tag/engineering" class="tag-text" style="user-select: auto; display: flex;">
                                Engineering
                            </a>
                        </div>
                            </div>
        </div>
        <div class="social-share" style="user-select: auto;">
                <div class="title" style="user-select: auto;">SHARE ARTICLE</div>
                        <div class="icon-container" style="user-select: auto;">
                    <div class="share-article" style="user-select: auto;">
    <a class="inner-icon" href="https://www.linkedin.com/shareArticle?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&amp;title=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&amp;summary=See%20how%20we%20made%20AI%20agents%20easy%20to%20build%2C%20run%2C%20and%20improve%20in%20production.&amp;source=%5Bobject%20Object%5D" title="LinkedIn" target="_blank" rel="noopener" style="user-select: auto;">
        <div class="icon" style="user-select: auto;"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 28 28" fill="none" style="user-select: auto;">
  <path d="M20.3639 3.39807H8.30268C5.92405 3.39807 3.99512 5.327 3.99512 7.70564V19.7668C3.99512 22.1455 5.92405 24.0744 8.30268 24.0744H20.3639C22.7434 24.0744 24.6714 22.1455 24.6714 19.7668V7.70564C24.6714 5.327 22.7434 3.39807 20.3639 3.39807ZM10.8872 19.7668H8.30268V10.2902H10.8872V19.7668ZM9.59496 9.19778C8.76273 9.19778 8.08731 8.51718 8.08731 7.67807C8.08731 6.83896 8.76273 6.15836 9.59496 6.15836C10.4272 6.15836 11.1026 6.83896 11.1026 7.67807C11.1026 8.51718 10.428 9.19778 9.59496 9.19778ZM21.2254 19.7668H18.6408V14.9389C18.6408 12.0373 15.1948 12.257 15.1948 14.9389V19.7668H12.6103V10.2902H15.1948V11.8108C16.3975 9.58288 21.2254 9.41833 21.2254 13.9439V19.7668Z" fill="#1CB0F6" style="fill: color(display-p3 0.1098 0.6902 0.9647); fill-opacity: 1; user-select: auto;"></path>
</svg>
</div>
    </a>
    <a class="inner-icon" href="https://www.facebook.com/sharer/sharer.php?u=https://blog.duolingo.com/production-ready-ai-agent-platform/" title="Facebook" target="_blank" rel="noopener" style="user-select: auto;">
        <div class="icon" style="user-select: auto;"><svg width="23" height="22" viewBox="0 0 23 22" fill="none" xmlns="http://www.w3.org/2000/svg" style="user-select: auto;">
  <path d="M11.6681 -0.00646973C5.59946 -0.00646973 0.680176 4.91281 0.680176 10.9814C0.680176 16.4897 4.73801 21.0386 10.0254 21.8331V13.8932H7.30697V11.0045H10.0254V9.08272C10.0254 5.90062 11.5758 4.50406 14.2206 4.50406C15.4875 4.50406 16.1566 4.59746 16.4742 4.64031V7.16094H14.67C13.547 7.16094 13.1547 8.22566 13.1547 9.42554V11.0045H16.4456L15.9995 13.8932H13.1558V21.8561C18.519 21.1298 22.656 16.5435 22.656 10.9814C22.656 4.91281 17.7367 -0.00646973 11.6681 -0.00646973Z" fill="#1CB0F6" style="fill: color(display-p3 0.1098 0.6902 0.9647); fill-opacity: 1; user-select: auto;"></path>
</svg>
</div>
    </a>
    <a class="inner-icon" href="https://twitter.com/intent/tweet?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&amp;text=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&amp;media=https%3A%2F%2Fstorage.ghost.io%2Fc%2F7a%2F33%2F7a33d0f4-927d-4fe8-a6bf-96131b5e76d4%2Fcontent%2Fimages%2F2026%2F08%2Fcover_Production-ready-agent-AI.png" title="Twitter" target="_blank" rel="noopener" style="user-select: auto;">
        <div class="icon" style="user-select: auto;"><svg width="19" height="18" viewBox="0 0 19 18" fill="none" xmlns="http://www.w3.org/2000/svg" style="user-select: auto;">
  <path d="M1.10102 0.69751L7.48739 9.82583L0.977539 17.4325H3.43803L8.5878 11.3984L12.8097 17.4325H18.3045L11.613 7.85381L17.7216 0.69751H15.2992L10.5181 6.28491L6.61578 0.69751H1.10102Z" fill="#1CB0F6" style="fill: color(display-p3 0.1098 0.6902 0.9647); fill-opacity: 1; user-select: auto;"></path>
</svg>
</div>
    </a>
    <a class="inner-icon" href="https://story.kakao.com/share?url=https://blog.duolingo.com/production-ready-ai-agent-platform/&amp;title=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform&amp;media=https%3A%2F%2Fstorage.ghost.io%2Fc%2F7a%2F33%2F7a33d0f4-927d-4fe8-a6bf-96131b5e76d4%2Fcontent%2Fimages%2F2026%2F08%2Fcover_Production-ready-agent-AI.png" title="Share on KakaoTalk" target="_blank" rel="noopener" style="user-select: auto;">
        <div class="icon" style="user-select: auto;"><svg width="24" height="24" viewBox="0 0 25 23" fill="none" xmlns="http://www.w3.org/2000/svg" style="user-select: auto;">
  <path fill-rule="evenodd" clip-rule="evenodd" d="M12.0183 0.417969C5.39085 0.417969 0.0183105 4.65408 0.0183105 9.8795C0.0183105 13.2578 2.26439 16.2222 5.64308 17.8961C5.45927 18.53 4.46188 21.9742 4.42219 22.2448C4.42219 22.2448 4.39831 22.4481 4.52996 22.5256C4.66162 22.6032 4.81646 22.543 4.81646 22.543C5.194 22.4902 9.1945 19.6803 9.88692 19.1922C10.5787 19.2902 11.2909 19.341 12.0183 19.341C18.6456 19.341 24.0183 15.105 24.0183 9.8795C24.0183 4.65397 18.6456 0.417969 12.0183 0.417969ZM5.3845 13.1824C5.0027 13.1824 4.6922 12.8858 4.6922 12.5212V8.40835H3.61197C3.23731 8.40835 2.93258 8.1042 2.93258 7.73047C2.93258 7.35674 3.23743 7.05258 3.61197 7.05258H7.15704C7.53169 7.05258 7.83642 7.35674 7.83642 7.73047C7.83642 8.1042 7.53158 8.40835 7.15704 8.40835H6.07681V12.5212C6.07681 12.8858 5.76631 13.1824 5.3845 13.1824ZM10.8788 12.8676C10.9453 13.0562 11.1662 13.1734 11.4549 13.1734C11.6073 13.1734 11.7594 13.1404 11.895 13.078C12.0858 12.9902 12.2693 12.748 12.0586 12.0935L10.4033 7.73681C10.2864 7.40462 9.93203 7.06297 9.47984 7.05281C9.02892 7.06308 8.67457 7.40462 8.55791 7.73612L6.90192 12.0949C6.69169 12.7477 6.87515 12.9898 7.06599 13.0778C7.20134 13.1404 7.35365 13.1734 7.50607 13.1734C7.79476 13.1734 8.01549 13.0564 8.08184 12.8681L8.42488 11.9703H10.536L10.8788 12.8676ZM9.48042 8.77943L10.1719 10.7438H8.78892L9.48042 8.77943ZM13.1732 13.0814C12.8074 13.0814 12.5098 12.7967 12.5098 12.4468V7.74489C12.5098 7.36308 12.8269 7.05258 13.2165 7.05258C13.6062 7.05258 13.9232 7.36308 13.9232 7.74489V11.8122H15.3944C15.7603 11.8122 16.0579 12.097 16.0579 12.4468C16.0579 12.7967 15.7603 13.0814 15.3944 13.0814H13.1732ZM16.3264 12.4811C16.3264 12.8629 16.6369 13.1734 17.0187 13.1734C17.4005 13.1734 17.711 12.8629 17.7113 12.4807V10.9702L17.9515 10.73L19.5749 12.8812C19.7072 13.0563 19.9086 13.1564 20.1281 13.1564C20.2794 13.1564 20.4233 13.1082 20.5444 13.0167C20.692 12.9053 20.7874 12.7433 20.813 12.5601C20.8388 12.3769 20.7917 12.1948 20.6801 12.0472L18.9761 9.78962L20.5538 8.2122C20.6622 8.10362 20.7166 7.95397 20.7065 7.7907C20.6966 7.62881 20.6243 7.47293 20.503 7.35177C20.3729 7.22185 20.1994 7.14731 20.0266 7.14731C19.8784 7.14731 19.7419 7.202 19.6426 7.30135L17.711 9.23289V7.74489C17.711 7.36308 17.4005 7.05258 17.0187 7.05258C16.6369 7.05258 16.3264 7.36308 16.3264 7.74489V12.4811Z" fill="#1CB0F6" style="user-select: auto;"></path>
</svg>
</div>
    </a>
    <a class="inner-icon" href="whatsapp://send?text=Making%20production-ready%20agents%20the%20default%3A%20building%20Duolingo%E2%80%99s%20agent%20platform%20https://blog.duolingo.com/production-ready-ai-agent-platform/" title="WhatsApp" target="_blank" rel="noopener" style="user-select: auto;">
        <div class="icon" style="user-select: auto;"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 25" fill="none" style="user-select: auto;">
  <g clip-path="url(#clip0_570_1319)" style="user-select: auto;">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M12.2185 -5.72205e-06C5.71266 -5.72205e-06 0.438387 5.27413 0.438387 11.7808C0.438387 14.0064 1.05598 16.0881 2.12862 17.8638L0.00244141 24.1841L6.52467 22.096C8.21248 23.0291 10.1534 23.5614 12.2185 23.5614C18.7252 23.5614 23.9994 18.2866 23.9994 11.7806C23.9994 5.27467 18.7254 -5.72205e-06 12.2185 -5.72205e-06ZM12.2185 21.5875C10.2269 21.5875 8.37193 20.9901 6.82311 19.966L3.05447 21.1724L4.27942 17.5307C3.10546 15.9135 2.41185 13.9271 2.41185 11.7806C2.41198 6.37274 6.81127 1.97319 12.2185 1.97319C17.6257 1.97319 22.0258 6.37274 22.0258 11.7808C22.0258 17.1888 17.6266 21.5877 12.2185 21.5877V21.5875ZM17.7422 14.4574C17.4469 14.2957 15.9963 13.5127 15.7242 13.4021C15.4523 13.2918 15.2538 13.2342 15.0418 13.5276C14.83 13.8204 14.2281 14.4762 14.0458 14.6704C13.8627 14.8645 13.6864 14.8827 13.391 14.7206C13.0964 14.5594 12.1391 14.2052 11.0288 13.138C10.165 12.3074 9.59836 11.3004 9.43394 10.9931C9.26952 10.6854 9.43273 10.5286 9.58894 10.3847C9.72915 10.2547 9.90299 10.0444 10.0599 9.87457C10.2164 9.70477 10.2717 9.58138 10.3793 9.3844C10.4869 9.18742 10.4436 9.00994 10.3738 8.85669C10.3041 8.70384 9.75821 7.20117 9.53014 6.58991C9.30221 5.97864 9.04818 6.0696 8.87259 6.0626C8.69714 6.05655 8.4976 6.02358 8.29712 6.01618C8.09664 6.00851 7.76779 6.07175 7.4812 6.36211C7.19434 6.65261 6.39026 7.35093 6.33482 8.83099C6.27939 10.3101 7.30319 11.7805 7.44595 11.9864C7.58884 12.1928 9.40098 15.4001 12.4125 16.7191C15.4247 18.0377 15.4404 17.6356 15.993 17.6062C16.5459 17.577 17.7994 16.945 18.0764 16.2527C18.3535 15.5602 18.3757 14.9582 18.3052 14.83C18.2347 14.7019 18.0373 14.6187 17.7421 14.4572L17.7422 14.4574Z" fill="#1CB0F6" style="fill: color(display-p3 0.1098 0.6902 0.9647); fill-opacity: 1; user-select: auto;"></path>
  </g>
  <defs style="user-select: auto;">
    <clipPath id="clip0_570_1319" style="user-select: auto;">
      <rect width="24" height="24.1841" fill="white" style="fill: white; fill-opacity: 1; user-select: auto;"></rect>
    </clipPath>
  </defs>
</svg>
</div>
    </a>
    <a class="inner-icon" href="mailto:?subject=Check%20out%20this%20post%20from%20Duolingo&amp;body=Hi!%20I%20thought%20you%20might%20enjoy%20this%20post:%20Making%20production-ready%20agents%20the%20default:%20building%20Duolingo%E2%80%99s%20agent%20platform%0D%0A%0D%0Ahttps://blog.duolingo.com/production-ready-ai-agent-platform/" title="Email" target="_blank" rel="noopener" style="user-select: auto;">
        <div class="icon" style="user-select: auto;"><svg width="24" height="24" viewBox="0 0 27 22" fill="none" xmlns="http://www.w3.org/2000/svg" style="user-select: auto;">
  <path fill-rule="evenodd" clip-rule="evenodd" d="M4.2123 3.33389H22.7764C22.9775 3.33389 23.163 3.40059 23.312 3.51309L13.4944 12.1308L3.6767 3.51309C3.8257 3.40059 4.0112 3.33389 4.2123 3.33389ZM0.980505 3.99559C1.0975 2.31269 2.4998 0.983887 4.2123 0.983887H22.7764C24.489 0.983887 25.8912 2.31269 26.0082 3.99559H26.072V17.4474C26.0739 17.4759 26.0749 17.5046 26.0749 17.5334C26.0749 17.586 26.0739 17.6383 26.072 17.6904V17.7504H26.0693C25.9565 19.9266 24.1562 21.6564 21.9519 21.6564H5.0591C2.782 21.6564 0.936005 19.8105 0.936005 17.5334C0.936005 17.4755 0.940004 17.4181 0.947804 17.3615V3.99559H0.980505ZM3.2978 6.30749V14.8892L7.0331 11.6104L8.1861 10.5983L3.2978 6.30749ZM9.96731 12.1618L8.58341 13.3766L3.342 17.9773C3.5391 18.7417 4.2331 19.3064 5.0591 19.3064H21.9519C22.7778 19.3064 23.4719 18.7417 23.6689 17.9773L18.4276 13.3766L17.0325 12.152L14.5441 14.3363C13.9435 14.8635 13.0452 14.8635 12.4446 14.3363L9.96731 12.1618ZM18.8137 10.5886L19.9778 11.6104L23.722 14.8969V6.28019L18.8137 10.5886Z" fill="#1CB0F6" style="user-select: auto;"></path>
</svg>
</div>
    </a>

</div>
                            </div>
        </div>
    </div>
            <div class="related-desktop" style="user-select: auto;">
                
<div class="wrapper" style="user-select: auto;">
    <div class="section-divider" style="user-select: auto;"></div>
</div>
<section class="featured-articles with-title desktop-view most-recent-grid" style="user-select: auto;">
    <div class="wrapper" style="user-select: auto;">
        <h3 class="p-sb-b" style="user-select: auto;">RELATED ARTICLES</h3>
        <div class="featured-articles-content" style="user-select: auto;">
            <div class="featured-articles--grid relatedDesktopPosts" style="user-select: auto;">
                
    <div class="swiper-slide">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="about:blank#">
                    <img class="post-image" src="https://blog.duolingo.com/production-ready-ai-agent-platform/" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date"></time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link">
                        <span class="caption author"></span>
                    </a>
                </div>
                <a class="post-title-link"><h3 class="post-title"></h3></a>
            </div>
        </div>
    </div>

            
    <div class="swiper-slide">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/">
                    <img class="post-image" src="https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_AI-iOS-unit-test-generation-pipeline.png" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date">Jun 24</time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link" href="https://blog.duolingo.com/author/kush/">
                        <span class="caption author">Kush Agrawal</span>
                    </a>
                </div>
                <a class="post-title-link" href="https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/"><h3 class="post-title">How we built an automated unit test generation pipeline for iOS</h3></a>
            </div>
        </div>
    </div>

    <div class="swiper-slide">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="https://blog.duolingo.com/reduce-cpu-usage-97-percent/">
                    <img class="post-image" src="https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_How-a-simple-code-change-reduced-CPU-usage-by-97_.png" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date">Jun 22</time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link" href="https://blog.duolingo.com/author/fabien/">
                        <span class="caption author">Fabien Loudet</span>
                    </a>
                </div>
                <a class="post-title-link" href="https://blog.duolingo.com/reduce-cpu-usage-97-percent/"><h3 class="post-title">How a simple code change reduced CPU usage by 97%</h3></a>
            </div>
        </div>
    </div>

    <div class="swiper-slide">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="https://blog.duolingo.com/learning-polish-family-reunion/">
                    <img class="post-image" src="https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/05/cover_How-I-Used-Duolingo-to-Find-My-Family-in-Poland.png" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date">Jun 1</time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link" href="https://blog.duolingo.com/author/david-sawicki/">
                        <span class="caption author">David Sawicki</span>
                    </a>
                </div>
                <a class="post-title-link" href="https://blog.duolingo.com/learning-polish-family-reunion/"><h3 class="post-title">How I used Duolingo to find my family in Poland</h3></a>
            </div>
        </div>
    </div>
</div>
        </div>
    </div>
</section>

<div class="wrapper beforeFooter has-mobile-view" style="user-select: auto;">
    <div class="section-divider" style="user-select: auto;"></div>
</div>
            </div>
            <div class="related-mobile" style="user-select: auto;">
                
<div class="wrapper" style="user-select: auto;">
    <div class="section-divider" style="user-select: auto;"></div>
</div>
<section class="featured-articles with-title mobile-view bottomCarousel" style="user-select: auto;">
    <div class="wrapper" style="user-select: auto;">
        <h3 class="p-sb-b" style="user-select: auto;">RELATED ARTICLES</h3>
        <div class="featured-articles-content swiper-container withSpace swiper-initialized swiper-horizontal swiper-backface-hidden" style="user-select: auto;">
            <div class="swiper-wrapper relatedMobilePosts" id="swiper-wrapper-b10b219197824e686" aria-live="off" style="user-select: auto; transform: translate3d(0px, 0px, 0px);">
                
    <div class="swiper-slide">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="about:blank#">
                    <img class="post-image" src="https://blog.duolingo.com/production-ready-ai-agent-platform/" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date"></time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link">
                        <span class="caption author"></span>
                    </a>
                </div>
                <a class="post-title-link"><h3 class="post-title"></h3></a>
            </div>
        </div>
    </div>

            
    <div class="swiper-slide swiper-slide-active" role="group" aria-label="1 / 3" style="margin-right: 10px;">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/">
                    <img class="post-image" src="https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_AI-iOS-unit-test-generation-pipeline.png" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date">Jun 24</time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link" href="https://blog.duolingo.com/author/kush/">
                        <span class="caption author">Kush Agrawal</span>
                    </a>
                </div>
                <a class="post-title-link" href="https://blog.duolingo.com/ai-ios-unit-test-generation-pipeline/"><h3 class="post-title">How we built an automated unit test generation pipeline for iOS</h3></a>
            </div>
        </div>
    </div>

    <div class="swiper-slide swiper-slide-next" role="group" aria-label="2 / 3" style="margin-right: 10px;">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="https://blog.duolingo.com/reduce-cpu-usage-97-percent/">
                    <img class="post-image" src="https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/06/cover_How-a-simple-code-change-reduced-CPU-usage-by-97_.png" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date">Jun 22</time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link" href="https://blog.duolingo.com/author/fabien/">
                        <span class="caption author">Fabien Loudet</span>
                    </a>
                </div>
                <a class="post-title-link" href="https://blog.duolingo.com/reduce-cpu-usage-97-percent/"><h3 class="post-title">How a simple code change reduced CPU usage by 97%</h3></a>
            </div>
        </div>
    </div>

    <div class="swiper-slide" role="group" aria-label="3 / 3" style="margin-right: 10px;">
        <div class="featured-card">
            <div class="feature-card--image">
                <a class="post-link" href="https://blog.duolingo.com/learning-polish-family-reunion/">
                    <img class="post-image" src="https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2026/05/cover_How-I-Used-Duolingo-to-Find-My-Family-in-Poland.png" alt="">
                </a>
            </div>
            <div class="feature-card--content">
                <div class="caption-wrap">
                    <span class="caption">
                        <time class="post-date">Jun 1</time>
                    </span>
                    <span class="divider">
                        <svg xmlns="http://www.w3.org/2000/svg" width="3" height="13" viewBox="0 0 3 13" fill="none">
  <path d="M1.5 1L1.5 11.7217" stroke="#E5E5E5" stroke-width="2" stroke-linecap="round"></path>
</svg>
                    </span>
                    <a class="author-link" href="https://blog.duolingo.com/author/david-sawicki/">
                        <span class="caption author">David Sawicki</span>
                    </a>
                </div>
                <a class="post-title-link" href="https://blog.duolingo.com/learning-polish-family-reunion/"><h3 class="post-title">How I used Duolingo to find my family in Poland</h3></a>
            </div>
        </div>
    </div>
</div>
            <div class="swiper-pagination" id="swiperButtons" style="user-select: auto;"></div>
        <span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span></div>
    </div>
</section>

<div class="wrapper beforeFooter has-mobile-view" style="user-select: auto;">
    <div class="section-divider" style="user-select: auto;"></div>
</div>
            </div>
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
</article>


        </main>
        
    </div>



































<!-- Using MathJax, with the delimiters $ -->
<!-- Conflict with pygments for the .mo and .mi -->
























    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Glide.js/3.2.0/css/glide.core.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Glide.js/3.2.0/css/glide.theme.css">
    <!-- See BLOG-6 -->




<!-- Using MathJax, with the delimiters $ -->
<!-- Conflict with pygments for the .mo and .mi -->




<div id="sodo-search-root"></div><div class=" soundcite-audio"></div></body></html>