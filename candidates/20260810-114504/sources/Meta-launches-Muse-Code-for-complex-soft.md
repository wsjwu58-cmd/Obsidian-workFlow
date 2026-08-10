# Meta launches Muse Code for complex software work with persistent AI agents

- **出处：** InfoWorld（News）
- **作者：** Prasanth Aby Thomas
- **发布：** 2026-08-06（采集 2026-08-09）
- **URL：** https://www.infoworld.com/article/4206084/meta-launches-muse-code-for-complex-software-work-with-persistent-ai-agents.html
- **副题：** Meta co-trained its Muse Spark 1.2 model with the terminal-based Muse Code agent, but analysts say the approach does not yet set it apart from rivals.

---

Meta has released a beta coding agent designed to handle complex software assignments across large codebases.

Available for macOS and Linux, Muse Code uses the company’s new Muse Spark 1.2 model. It includes specialized background agents that remain active throughout a session instead of being created separately for individual tasks.

The agents carry out work asynchronously and decide when to report their findings to the primary agent. Meta said keeping them active reduces repeated information gathering and the need for developer direction during difficult, multi-step tasks.

“Muse Code uses a local event log in which every model call, tool run, approval, and edit is appended,” Meta said in a post, adding that the record “makes the runtime replay-exact and restart-safe” and allows the agent to resume precisely where it stopped after a crash.

[Muse Spark 1.2](https://www.infoworld.com/article/4192724/metas-ai-chief-says-new-muse-spark-update-will-sharpen-coding-agentic-ai.html) is available through Muse Code and the Meta Model API, for which Meta announced expanded global access.

## Training and evaluation

Meta said it co-trained Muse Spark 1.2 with Muse Code to improve the model’s performance and usability when used with the agent. The training incorporated Muse Code’s tools and agent workflows, while Meta increased the computing resources used for coding and broadened the range of development environments.

The model was also trained on longer assignments, including whole-repository generation and large end-to-end software projects.

[Lian Jye Su](https://omdia.tech.informa.com/authors/lian-jye-su), chief analyst at Omdia, said Meta’s co-training approach was unlikely to provide a clear advantage because rivals were also developing their coding models and [agent harnesses](https://www.infoworld.com/article/4164601/harness-teams-of-coding-agents-with-squad.html) in close coordination.

“Other vendors, such as OpenAI and Anthropic, have been treating harness engineering as part of the training process,” Su said.

Optimizing the model and agent together could improve planning and context handling, but any competitive advantage would need to be demonstrated through better results on enterprise projects while reducing the need for human intervention, said [Pareekh Jain](https://pareekh.com/), CEO of Pareekh Consulting.

Meta reported that Muse Spark 1.2 achieved an 82.9% pass@1 score on Terminal-Bench 2.1, behind Claude Opus 5 but slightly ahead of GPT-5.6 Terra. On DeepSWE 1.1, the model scored 59.3%, trailing both rivals.

For Terminal-Bench 2.1 and DeepSWE 1.1, Meta evaluated each model with its selected coding agent rather than using the same agent throughout. It also acknowledged that rival proprietary models may have performed differently under tools and prompts designed specifically for them.

[Neil Shah](https://counterpointresearch.com/en/opinion-leader/10), vice president of research at Counterpoint Research, said cross-vendor comparisons would be more meaningful if models were evaluated with third-party tools or within the same agent harness.

“The key metric for CIOs is the pass rate against an enterprise’s own pipeline, which will determine the success of the model-and-harness bundle, or, in this case, Meta’s Muse Spark 1.2 and Muse Code,” Shah said. “This will be the real [benchmark](https://www.infoworld.com/article/4033758/why-benchmarks-are-key-to-ai-progress.html).”

## Enterprise adoption hurdles

Su said security and governance requirements could slow enterprise adoption, particularly where coding agents must be connected to existing identity systems.

“Many enterprises are still less willing to open up their CI/CD environments for AI tool integration,” Su said.

Shah said companies would need controls governing how agents access repositories, along with records showing how models and agent workflows handle enterprise data. He also cited the difficulty of forecasting token consumption and its effect on costs.

Meta’s pricing structure also creates a data-governance choice. The company said the lower-priced Contributor model may be used to improve its products, while the standard tier is not used for that purpose.

The Contributor tier costs $0.10 per million input tokens and $0.20 per million output tokens, compared with $1.25 and $4.25, respectively, for the standard tier.

“There is also a fear of vendor lock-in and reliance, as it may hurt long-term flexibility and system interoperability,” Su added.

Jain said adoption was likely to begin with narrowly defined, lower-risk work before companies allowed persistent agents to modify critical production code.
