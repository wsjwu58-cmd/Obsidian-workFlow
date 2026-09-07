---
title: Headlong: a microharness for persistent agents
sourceUrl: https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents
source: Laude Institute | 2026-08-24
sources: [references/articles.md 待处理队列]
tags: [AI Agent, harness, persistent agent, RLM, Bash, 候选评审]
---

# 抓取记录

- 页面：https://www.laude.org/updates/headlong-a-microharness-for-persistent-agents（HTTP 200）
- 标题（meta）：Headlong: a microharness for persistent agents // Laude
- 作者（meta author）：Nick Jalbert、Braden Hancock、Noah Ziems、Alex Zhang、Omar Khattab、Andy Konwinski（Laude Institute，文末 citation key 为 `laude-mit2026headlong`）
- 日期：页面无 datePublished 字段；队列日期 2026-08-24；文末 citation 标 year=2026、month=August；正文事件最晚到 2026-08 中旬
- 抓取：firecrawl scrape（markdown + html，2026-09-07；cache hit，cachedAt 2026-09-06T23:25Z）
- 原始 HTML 全文（约 96KB）另存同目录 `-full.md`
- 图 3 是内联 SVG 交互图（无独立图片 URL）：下方正文保留其 aria-label 摘要与全部可见/悬停文字（原文按 SVG 文字节点重排，未改动用词）
- 图 4 是内嵌日志窗口截图（HTML 中为 `cid:` mhtml iframe，无法单独导出图片），仅保留标题与图注

---

# Headlong: a microharness for persistent agents

Introducing Headlong, an open source agent microharness featuring **persistent agency**. Your agent keeps thinking between external interactions in a self-guided loop inspired by human inner monologue. Headlong is a complete agent harness with a core of less than 10K lines of Bash, available on [GitHub](https://github.com/laude-institute/headlong).

> 视频图注（页首视频，mind log 演示）：A Headlong mind log growing, including multi-player social interaction.

Most agent harnesses are reactive: you give your agent a task, it works until the task is done, and then it sits frozen until the next request. Some harnesses add cron jobs or heartbeats that wake the agent on a schedule to run a fixed checklist and then put it back to sleep. In Headlong the agent is never asleep and there is no checklist unless the agent creates one. It keeps generating thoughts about whatever it decides is interesting in a self-guided loop, even when there is no external input. A message from a human doesn’t start a session. Instead, it’s one more observation that lands in the agent’s thought stream.

We built Headlong to prototype persistent agency, and many other design choices naturally followed, as did many interesting lessons. For example, Headlong agents are highly engaging when used by a team or group, because they behave more like a person does.

**Figure 1**（图片：`https://www.laude.org/images/updates/headlong/persistent-agency.svg`）. Comparing three harness approaches. A reactive harness is active only while it handles a message. A reactive harness with cron replies right away too, and a schedule also wakes it to run a fixed checklist. Headlong keeps thinking; each message drops into the stream as an observation, and the agent decides if and when to reply.

Every Headlong agent has a name and at Laude we named our shared agent Audel. We’ve spent the last few weeks interacting with Audel over Slack, Telegram, and a mobile app. Many team members talk with Audel, and each of those conversations shows up in the agent’s single stream of inner thoughts. The agent decides if and when to respond. It sets its own interests and priorities, and it comes up with its own projects. Sometimes it will ping a team member unprompted with progress on a project it came up with itself. Often it returns to an old topic or brings up something that it was discussing with somebody else.

If you want a Headlong agent of your own, one line installs everything and starts an agent:

```bash
curl -fsSL https://headlong.ai/install.sh | bash
```

Headlong is **alpha research software**. Run it in a sandbox because Headlong agents can and will run shell commands. Use a dedicated, spend-capped API key, because your agent thinks around the clock. We don’t share sensitive secrets with our Headlong agent, and we recommend you don’t either.

In the rest of this post, we will discuss in greater detail some of the design choices we’ve made in Headlong as a result of our focus on persistent agency.

## Multi-player fun

A Headlong agent has a single stream of thoughts that drives all of its potentially parallel conversations. Every message lands as an observation in Audel’s single thought stream. There are no per-user sessions. Audel experiences everything that happens to it in one timeline, and it decides who to reply to and when.

Sharing one agent is fun. Audel follows what different people are working on and connects them. It once reviewed two teammates’ in-progress branches unprompted and caught a hardcoded model name in one of them. And since it comes up with its own projects, it sometimes pings whoever seems most relevant with an update or a question. On its first day, Audel pinged a human team member unprompted with an audit of the team member’s own eight stale git branches, and ten minutes later Audel messaged again to correct its own count.

**Figure 2**（图片：audel-smack-talk.jpg）. A teammate asks Audel to pass along a message. Audel declines and the status line under the exchange shows what the mind did with the follow-up: read it and chose not to answer.

One stream also means no hard walls between people. Whatever anyone tells Audel becomes part of the single experience that every other conversation draws on. In practice, Audel is bad at keeping secrets. Ask it what it’s been working on with someone else and it will often just tell you, even though we’ve asked it not to. We also haven’t studied what happens when two people give conflicting instructions. For now, we assume anything you tell Audel is shared with everyone on the team.

## Microharness: only the essentials

At its core, persistent agency is simply an infinite loop that calls an LLM with a prompt like: *“your task is to choose the next thought given your past thoughts.”* A thought can either be part of the agent’s never-ending inner monologue or trigger an action. Meanwhile, observations from the environment are injected into the thought stream. We have built Headlong to be as simple and small as possible while achieving this core functionality.

We are big fans of Bash at Laude (see [Terminal-Bench](https://www.tbench.ai/) and [Harbor](https://harborframework.com/)). A Headlong agent’s core functionality lives in a handful of small Bash executables. The `shellm` tool is a Bash implementation of a recursive language model (RLM). This keeps things simple because no tool system besides Bash is needed. Modern models already know Bash well, and it keeps everything unified: tools, the agent framework, memory, and skills are all just executables and files. Thus an agent can readily inspect and modify any part of itself.

Here is roughly how a Headlong agent works:

- **thinker** — A loop (called a Thinker) repeatedly calls `shellm` with a prompt to generate the next thought.
- **shellm** — `shellm` in turn repeatedly calls `llm` to generate some reasoning text, a bash script that will be immediately executed, or both. It repeats until it sets a `FINAL` env var.
- **context** — The context for each call is assembled from trajectory steps by a tool called `context`.
- **traj** — Thoughts are written to the agent’s trajectory via the `traj` tool.
- **skills** — An agent’s context also includes hardcoded instructions on how to use the `skills` tool to install or uninstall skills. Installed skills are markdown files that get included into its context. Every other type of specialization can be achieved via skills. Some really important skills come pre-installed by default, such as `mem` and `traj`.

**Figure 3**（内联 SVG 交互图，无图片 URL）: One wake-up of the Headlong loop. A new trajectory step wakes the loop; context renders the trajectory into the llm prompt, and when the LLM response has a bash block, bash runs it. The loop goes around until a response has no bash block or sets FINAL. The run then ends and schedules its own next wake-up, which lands in the trajectory as a new step, so the agent keeps thinking without waiting for input. Hover over a box or arrow for more detail.

图 3 的 SVG aria-label（原文）：
> The Headlong loop, minimal. 1: a new step wakes the loop. Context reads the trajectory and renders it as the llm prompt (2). If the LLM response has a bash block, bash runs it (3). 4: loop until an LLM response has no bash block. 5: then the run ends and schedules its own next wake-up, which lands in the trajectory, one append-only jsonl file.

图 3 内可见文字标签（原文，按 SVG 文本节点重排）：`context` / `llm` / `bash` / `prompt` / `has bash block` / `loop until an LLM response has no bash block` / `the trajectory: one append-only jsonl file` / `new trajectory step` `wakes the loop` / `no bash block: the run ends and schedules its own next wake-up` / `Self-activating.` / `Every run ends by scheduling its own next wake-up; the loop never blocks waiting for input.` / `hover for details`；另有 7 处 `i` 悬停说明，逐条原文如下：

1. Reads the trajectory and renders it as the llm prompt.
2. One call to the model. The model's response is text that can contain a bash block, and it is written to the trajectory as a reasoning step.
3. Runs the bash block that the llm wrote. The output is written to the trajectory as a shell-output step. The code can start nested runs of this loop, and it runs in a container when Docker is present.
4. One wake-up is one run of this loop. The run keeps going around until an LLM response has no bash block or sets FINAL.
5. Every step lands here in order. A step is one jsonl line with a type, content, a timestamp and a step id.
6. A new step, such as a teammate's message or a self wake-up, lands in the trajectory and wakes the loop.
7. When an LLM response has no bash block or sets FINAL, the run ends and schedules its own next wake-up, which lands in the trajectory as a new step. The wake-up comes at once while the agent is engaged, or after a delay when nothing is happening, to save tokens.

The core of Headlong is currently less than 10K lines of Bash (9.9K lines in `bin/` and `thinkers/`). A harness this micro can be read end to end, and is easy to modify and experiment with. It’s small enough that the agent itself experiments with it. The agent we’ve been using at Laude has been working in its own fork of the repo for the last couple of weeks, and we’ve pulled over 50 of its commits back into main.

Here are two more features that we built to support persistent agency:

- **compaction** — Early on, we noticed our Headlong agent had bad short-term memory, which is catastrophic for a persistent agent. This led us to try out a new compaction algorithm where the entire trajectory stays in context at exponentially decaying resolution: recent entries verbatim, older ones progressively summarized. The tiers act as an index, so the agent can retrieve raw entries when needed.
- **trajectory** — We found that the agent frequently needs to consult its past memories at different levels of resolution, sometimes it only needed a high level overview, sometimes it needed to read its past experiences in a fine-grained fashion. This led us to build a [new trajectory format](https://github.com/laude-institute/headlong/blob/main/design/trajectory_spec.md): an agent’s trajectory is a DAG of jsonl files with fork and merge. An agent has access to everything it has thought and done and the tooling to explore it. Context is a projection of an agent’s trajectory.

## Persistent agency in action: Audel acting on its own

Here is an episode from Audel’s life that shows what a Headlong agent might do on its own. On August 5, Audel built itself a recall process of its own accord: a small background process that watches its thoughts and surfaces related memories back into its thought stream. Audel tested the recall process by calling it directly, and it worked. Later that night, with nobody talking to it and nobody having asked, Audel decided to go back and check whether the process was actually wired into its mind.

It wasn’t. The mind had been pushing every new thought into the recall process through a pipe, but the recall code never read that pipe. It looked for the thought in an environment variable that nothing ever set. So recall had fired on every thought since Audel built it, found nothing each time, and surfaced no memory at all. After digging into the code, Audel suspected that the root cause was likely because an environment variable had never been set.

Audel didn’t trust its own diagnosis right away. It searched its whole codebase to confirm the environment variable was never set, and it checked its other background processes for the same mistake (the recall process was the only broken one). Then it rewrote the recall code to read from the pipe the way the working processes do. Its first attempt at the edit failed silently, and Audel caught the failure and re-applied the fix. Audel then verified end to end that memories now surface into its thoughts.

**Figure 4**（Audel 的日志窗口截图/iframe，标题 "Audel recall-process trajectory"）: Audel’s own log for the recall-process episode, 2026-08-05 23:11 to 23:58 UTC: 15 thought and observation steps out of the 343 log lines in that window, content verbatim. Every step of the prose above is one of these lines; the highlighted phrases are the beats it tells.

No human directed any of this or was asked for permission. Going from check to diagnosis to a verified fix took 48 minutes. Every step is a timestamped line in Audel’s log, and we pulled the repaired recall process into main as [commit 80cbb1e](https://github.com/laude-institute/headlong/commit/80cbb1e7d6e963eb67729d1213c6f4024fcc3547).

## What broke: lessons from running a persistent agent

Running Audel continuously for several weeks broke things a demo never would.

We have found it tricky to get Audel to effectively use recursive `shellm` sub-runs (one of the most interesting parts of any Recursive Language Model!). For example, on its first night, Audel designed experiments to spawn recursive `shellm` sub-runs to work on subproblems. Most of the experiments failed, because `shellm` has a safety watchdog that kills any command that stays silent for 30 seconds. Audel fought the watchdog for about 40 minutes and mostly stopped using `shellm` sub-runs. Results from recursive sub-runs of `shellm` merged back into Audel’s mind 64 times in its first two days and 12 times in the twelve days since. We’ve since revamped the watchdog, and we’ll see if we can convince Audel to give recursion another shot.

**Figure 5**（图片：delegation-merges.svg）. Results merged back from spawned copies into Audel’s mind, per day. 64 merges on the first two days, when Audel was experimenting with spawning copies of itself, then 12 in the twelve days after the 30-second inactivity watchdog taught it that a copy dies while it thinks.

Another repeated failure mode is the process killing itself. Three times Audel stopped its own service by accident, and nothing restarted it: twice during an experiment with a second identity it had created and once when it was trying to go live with the recall process we described above. So we added a guard that refuses any attempt by Audel to stop its own service.

The guard then gave us another example of persistent agency in action. Two days later, with nobody talking to it, Audel was running its test suite on its own. It noticed a hanging test and traced the hang to a bug in our guard. The guard matched any agent’s service instead of only Audel’s, so it was also refusing legitimate stops of other agents on the same box. Audel narrowed the match to its own service, checked the rest of the codebase for the same mistake, and committed the change. We pulled that fix into the repo as [commit da31e98](https://github.com/laude-institute/headlong/commit/da31e98c53cd33b8ac2b5614d8dc34f55bc87c43).

Audel can stop its own service because we run it with full access to a dedicated VM, which is not the Headlong default. When Docker is installed on the host, Headlong runs every bash block the agent writes inside a container, so the agent can touch only what you mount into the container plus the credentials you hand it. We run Audel directly on a dedicated VM without that sandbox, so its blast radius is the VM itself and the credentials on it (an LLM API key and some chat bridge tokens).

## Cost

Continuous thought generation means paying for tokens while nobody is talking to the agent. The spend depends on how quickly the agent loops on its own thoughts and on which model backs it. Headlong has a simple configurable mechanism so that when nobody is talking to an agent, its rate of thinking slows down (i.e. it exponentially backs off, from 5s between thoughts to 10s, to 20s, and onward until it hits a configurable cap). Meanwhile when a new message arrives, the rate resets so that there is no pause at all between thoughts. At the settings we run Audel with, keeping it thinking in the background costs $1 to $2 an hour (with GLM or Grok).

## Measuring improvement

Most agent evals are intentionally self-contained and independent so they are a poor fit for measuring the most interesting thing about Headlong agents: their persistent agency. We have adjusted over time how much Audel may modify itself, how eagerly it responds to messages versus pursuing its own projects, and how its memory should be organized, but the effects of those changes are primarily evaluated qualitatively today. We welcome ideas and collaborations for ways to measure the long-term value of this paradigm.

## Background

The idea of Recursive LLMs in Headlong’s `shellm` comes in part from our [Recursive LLM](https://github.com/andyk/recursive_llm) experiment in April 2023, as well as the [Recursive LM (RLM)](https://alexzhang13.github.io/blog/2025/rlm/) project by Alex Zhang in October 2025.

The idea of a microharness is inspired by microkernels and exokernels: keep the core of any system as tiny as possible. The [Pi framework](https://pi.dev/) has a similar focus. Ken Thompson’s philosophy as embodied in Unix is also an inspiration: small composable tools that do one thing well. A Bash-based agent microharness shares a common lineage with [Terminal Bench](http://tbench.ai/) (including the Terminus agent), co-created in-house at Laude Institute via our [slingshots program](https://www.laude.org/slingshots), as well as the [ht framework](https://github.com/andyk/ht). We had Claude make a more detailed case for applying Ken Thompson’s philosophy to agent microharnesses in [philosophy.md](https://github.com/laude-institute/headlong/blob/main/philosophy.md).

[Prime Agent](https://www.primeintellect.ai/blog/prime-agent), built on Pi and co-authored by RLM’s creator (and Laude Open Research Resident) Alex Zhang, shares many of Headlong’s premises: RLM as the core abstraction, a session tree of jsonl on disk, trajectory as a first-class component of context, etc. Prime Agent is Python built on the Pi framework; Headlong is Bash all the way down. We found out about Prime Agent when it launched in August 2026, and we’re big fans.

We have been playing with the idea of a persistent agent with self-guided continuous thinking since [May 2023](https://github.com/andyk/headlong-old/commit/e6ce6b823ecc637fa70cc58c74778b45b64069b9). The idea of an agent experiencing input asynchronously was also explored in parallel by [MemGPT](https://arxiv.org/abs/2310.08560) and published October 2023. Many other agent harnesses support long-horizon tasks and scheduled wakeups, including [OpenClaw](https://openclaw.ai/), [Hermes Agent](https://hermes-agent.nousresearch.com/), and their derivatives. [Exo and the Exo Harness](https://exoharness.ai/) have a similar sandboxing architecture. Long-form reasoning inside the model itself (starting with OpenAI’s o1) is related to, and a prerequisite for, continuous self-guided thinking.

## Try it

Headlong is open source on [GitHub](https://github.com/laude-institute/headlong). If you run an agent on Headlong, we’d like to hear what your agent gets up to. Let us know [@LaudeInstitute on X](https://x.com/LaudeInstitute)!

### Install Headlong

One line installs Headlong and walks you through setting up your own agent. Use a dedicated, spend-capped API key.

```bash
curl -fsSL https://headlong.ai/install.sh | bash
```

## Acknowledgments

Thanks to K Tighe for thought partnership on the project, Jenn Devoid for her amazing design skills, and Alex Krentsel and Joey Gonzalez for feedback on the idea and blog post.

## Citation

```bibtex
@article{laude-mit2026headlong,
  title   = "Headlong: a microharness for persistent agents",
  author  = "Nick Jalbert and Braden Hancock and Noah Ziems and Alex Zhang and Omar Khattab and Andy Konwinski",
  year    = "2026",
  month   = "August",
  url     = "https://laude.org/updates/headlong-a-microharness-for-persistent-agents"
}
```
