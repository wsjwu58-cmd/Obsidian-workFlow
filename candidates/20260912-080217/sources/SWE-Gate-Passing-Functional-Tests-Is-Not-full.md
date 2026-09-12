Title:

Content selection saved. Describe the issue below:

Description:

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2609.04167v1 \[cs.SE\] 03 Sep 2026

# SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents

Xin He
Yanlin Wang
††thanks: Yanlin Wang is the corresponding author.Mingwei Liu
Jiachi Chen
Hongyu Zhang
Guanbin Li

###### Abstract

Repository-level software engineering benchmarks have significantly advanced the evaluation of coding agents, but existing benchmarks primarily measure whether generated patches pass functional tests and overlook review-derived acceptance constraints (review constraints) that often influence whether a patch is acceptable in real-world software development. We introduce SWE-Gate, a repository-level benchmark for software engineering agents that explicitly evaluates review constraint compliance alongside functional correctness. SWE-Gate derives review constraints from real pull request review comments and synthesizes repository-level repair instances around these constraints. Each instance provides separate functional and constraint tests, together with non-compliant and gold patches, enabling explicit separation between issue resolution capability and review constraint compliance. We construct SWE-Gate with 303 repository-level repair instances spanning 75 open-source Python repositories across diverse software domains. Experiments with four LLM backends spanning different capability levels under a common coding-agent scaffold reveal a substantial gap between functional success and success under the complete repair specification: among 644 repairs that pass the functional tests, 221 fail to satisfy the provided review constraints. These findings show that functional-only evaluation overestimates agents’ ability to satisfy the full requirements of repository-level repair tasks. The replication package including code, data, and experimental results is available at https://github.com/DeepSoftwareAnalytics/SWE-Gate.

1School of Software Engineering, Sun Yat-sen University

2College of Computer Science and Technology, Zhejiang University

3School of Big Data and Software Engineering, Chongqing University

4School of Computer Science and Engineering, Sun Yat-sen University

## Introduction

Recent advances in large language models (LLMs) have transformed automated software engineering, evolving from early function-level code generation benchmarks \[ [1](https://arxiv.org/html/2609.04167v1#bib.bib1 ""), [2](https://arxiv.org/html/2609.04167v1#bib.bib27 "")\] to repository-level agents capable of understanding large codebases \[ [3](https://arxiv.org/html/2609.04167v1#bib.bib41 ""), [4](https://arxiv.org/html/2609.04167v1#bib.bib8 ""), [5](https://arxiv.org/html/2609.04167v1#bib.bib23 "")\], localizing defects, and repairing real software issues using code, version history, tests, and natural-language reports \[ [6](https://arxiv.org/html/2609.04167v1#bib.bib59 ""), [7](https://arxiv.org/html/2609.04167v1#bib.bib60 ""), [8](https://arxiv.org/html/2609.04167v1#bib.bib58 ""), [9](https://arxiv.org/html/2609.04167v1#bib.bib57 "")\]. Repository-level repair has consequently become an important measure of practical programming ability. SWE-Bench \[ [6](https://arxiv.org/html/2609.04167v1#bib.bib59 "")\], the de facto benchmark, constructs tasks from real issue–pull request pairs and evaluates patches with executable functional tests, driving systems such as SWE-Agent \[ [7](https://arxiv.org/html/2609.04167v1#bib.bib60 "")\] and OpenHands \[ [8](https://arxiv.org/html/2609.04167v1#bib.bib58 "")\].

Despite their success, existing repository-level benchmarks largely adopt a single evaluation criterion: a repair is considered successful if the generated patch passes the functional test suite which is typically provided with the PR and mainly assesses whether the reported issue has been functionally resolved. However, in practice, a patch that resolves the reported issue and passes functional tests is not necessarily accepted \[ [10](https://arxiv.org/html/2609.04167v1#bib.bib62 ""), [11](https://arxiv.org/html/2609.04167v1#bib.bib61 "")\]. During code review, repository maintainers frequently require contributors to satisfy additional requirements beyond functional correctness. We call such requirements _review-derived acceptance constraints_ ( _gates_): additional, objectively testable requirements that restrict which functionally correct repairs are acceptable. For brevity, we refer to them as _review constraints_ hereafter. These requirements are often reflected in review comments that request changes before a patch can be accepted. Examples of such requirements include preserving backward compatibility, maintaining established exception semantics, or following repository-specific implementation conventions \[ [12](https://arxiv.org/html/2609.04167v1#bib.bib56 ""), [13](https://arxiv.org/html/2609.04167v1#bib.bib55 ""), [14](https://arxiv.org/html/2609.04167v1#bib.bib54 "")\].

For example, a Pydantic pull request sought to add conditional serialization for extra fields. Its initial implementation provided the requested behavior by introducing a new core-schema representation, but a reviewer noted that changing this public interface would be breaking and recommended adding an extras\_ser\_exclude\_if parameter instead.111https://github.com/pydantic/pydantic/pull/12657#discussion˙r2671466868 The contributor subsequently adopted this backward-compatible design.

The two requirements can be tested separately. A functional test checks whether qualifying extra fields are omitted from serialized output, whereas a compatibility test checks whether the existing public schema remains unchanged and usable by code written against the previous format. A patch may therefore pass the functional test while failing compatibility, showing that implementing the requested behavior does not necessarily satisfy the review constraint raised during review.

Existing benchmarks answer whether a model can generate a functionally correct repair, but not whether that repair also complies with review-derived review constraints. These are separable evaluation dimensions: issue tests establish functional success, whereas constraint tests determine whether a functional repair also meets additional acceptance requirements. Evaluating only the first may therefore overestimate agents’ ability to satisfy complete repair requirements.

To bridge this gap, we introduce SWE-Gate, the first repository-level benchmark to evaluate review constraint compliance alongside functional correctness using separate executable tests. Rather than manually inventing rules or attaching them to unrelated tasks, SWE-Gate derives natural-language constraints from maintainer reviews and synthesizes realistic repairs around their engineering intent. Each instance includes a non-compliant patch that passes functional tests but violates the constraint and a gold patch that passes both, demonstrating that the dimensions are separable, executable, and jointly satisfiable.

Using SWE-Gate, we evaluate representative LLMs on 303 repository-level repair instances spanning 75 repositories across six software domains. Our experiments reveal that many repairs that successfully pass functional tests nevertheless violate review constraints, demonstrating that functional success alone does not establish that an agent-generated repair satisfies the full set of repository requirements or is acceptable for integration.

Our contributions are summarized as follows:

- •


We introduce SWE-Gate, the first repository-level software engineering benchmark that incorporates executable review constraints into realistic software repair tasks.

- •


We propose a dual-dimension evaluation protocol that separately measures functional correctness and review constraint compliance with executable tests.

- •


We develop a semi-automated construction framework and use it to create 303 quality-assured instances across 75 repositories and six domains, then characterize constraint following across four LLM backends evaluated under a common Mini-SWE-Agent scaffold.


## Related Work

Early benchmarks such as HumanEval and MBPP evaluate function-level programs with unit tests \[ [15](https://arxiv.org/html/2609.04167v1#bib.bib51 ""), [16](https://arxiv.org/html/2609.04167v1#bib.bib50 "")\], whereas RepoBench, RepoCoder, and CrossCodeEval introduce repository or cross-file context, with subsequent work further studying repository-level code generation\[ [17](https://arxiv.org/html/2609.04167v1#bib.bib49 ""), [3](https://arxiv.org/html/2609.04167v1#bib.bib41 ""), [18](https://arxiv.org/html/2609.04167v1#bib.bib39 ""), [19](https://arxiv.org/html/2609.04167v1#bib.bib4 "")\]; multilingual code evaluation and real-fault corpora are further represented by xCodeEval, Defects4J, and BugsInPy \[ [20](https://arxiv.org/html/2609.04167v1#bib.bib48 ""), [21](https://arxiv.org/html/2609.04167v1#bib.bib38 ""), [22](https://arxiv.org/html/2609.04167v1#bib.bib37 "")\]. Pre-trained code models have substantially advanced code representation and understanding \[ [23](https://arxiv.org/html/2609.04167v1#bib.bib21 ""), [24](https://arxiv.org/html/2609.04167v1#bib.bib20 "")\], while subsequent work has incorporated richer contextual information into code intelligence\[ [25](https://arxiv.org/html/2609.04167v1#bib.bib18 ""), [26](https://arxiv.org/html/2609.04167v1#bib.bib19 ""), [27](https://arxiv.org/html/2609.04167v1#bib.bib16 "")\]. Recent studies further examine context utilization, task-relevant retrieval, and the quality of repository-level agent trajectories, including work on context use and retrieval \[ [28](https://arxiv.org/html/2609.04167v1#bib.bib17 ""), [29](https://arxiv.org/html/2609.04167v1#bib.bib13 ""), [30](https://arxiv.org/html/2609.04167v1#bib.bib24 ""), [31](https://arxiv.org/html/2609.04167v1#bib.bib25 ""), [32](https://arxiv.org/html/2609.04167v1#bib.bib14 "")\] and on selecting high-quality trajectories for more effective agent supervision \[ [33](https://arxiv.org/html/2609.04167v1#bib.bib6 "")\], advancing the study of LLMs for repository-level software engineering tasks.

SWE-bench formulates repository-level repair as resolving real GitHub issues with executable tests \[ [6](https://arxiv.org/html/2609.04167v1#bib.bib59 "")\], motivating agents such as SWE-agent, OpenHands, and Agentless \[ [7](https://arxiv.org/html/2609.04167v1#bib.bib60 ""), [8](https://arxiv.org/html/2609.04167v1#bib.bib58 ""), [9](https://arxiv.org/html/2609.04167v1#bib.bib57 "")\]. Multi-agent approaches such as MAGIS further explore collaborative issue resolution, while recent repair-agent research also investigates how agents explore and select repair strategies \[ [34](https://arxiv.org/html/2609.04167v1#bib.bib7 ""), [35](https://arxiv.org/html/2609.04167v1#bib.bib3 "")\], reflecting the broader adoption of LLM-based agents in software engineering. Later benchmarks extend languages, enterprise projects, repository evolution, freshness, contamination control, multimodal issues, and security \[ [36](https://arxiv.org/html/2609.04167v1#bib.bib47 ""), [37](https://arxiv.org/html/2609.04167v1#bib.bib43 ""), [38](https://arxiv.org/html/2609.04167v1#bib.bib46 ""), [39](https://arxiv.org/html/2609.04167v1#bib.bib45 ""), [40](https://arxiv.org/html/2609.04167v1#bib.bib36 ""), [41](https://arxiv.org/html/2609.04167v1#bib.bib35 ""), [42](https://arxiv.org/html/2609.04167v1#bib.bib42 ""), [43](https://arxiv.org/html/2609.04167v1#bib.bib2 ""), [44](https://arxiv.org/html/2609.04167v1#bib.bib5 ""), [45](https://arxiv.org/html/2609.04167v1#bib.bib10 ""), [46](https://arxiv.org/html/2609.04167v1#bib.bib12 ""), [47](https://arxiv.org/html/2609.04167v1#bib.bib9 "")\], but still primarily evaluate tested functional behavior. Related empirical studies have also highlighted that benchmark design and contextual assumptions can substantially affect the realism of LLM-based code-generation evaluation \[ [48](https://arxiv.org/html/2609.04167v1#bib.bib11 "")\].
Scalable task construction has been explored by SWE-smith, which synthesizes test-breaking tasks within repositories \[ [49](https://arxiv.org/html/2609.04167v1#bib.bib34 "")\], and SWE-Mirror, which transfers the semantic essence of real issues across repositories \[ [50](https://arxiv.org/html/2609.04167v1#bib.bib40 "")\]. Recent work further investigates automated construction of software engineering datasets, including automated SWE data construction and LLM-assisted rebuilding of code-intelligence benchmarks \[ [51](https://arxiv.org/html/2609.04167v1#bib.bib22 ""), [52](https://arxiv.org/html/2609.04167v1#bib.bib26 "")\]. SWE-Gate is inspired by SWE-Mirror’s cross-repository transfer paradigm but instead transfers review-derived review constraints together with their bug patterns, applicability conditions, and validation requirements, producing separate functional and constraint tests as well as non-compliant and gold repairs.

Passing available tests does not necessarily establish patch correctness because weak suites can admit overfitting repairs \[ [10](https://arxiv.org/html/2609.04167v1#bib.bib62 ""), [53](https://arxiv.org/html/2609.04167v1#bib.bib33 ""), [54](https://arxiv.org/html/2609.04167v1#bib.bib32 "")\], a problem also observed in SWE-bench evaluations \[ [11](https://arxiv.org/html/2609.04167v1#bib.bib61 "")\]. Moreover, code reviews address maintainability, consistency, compatibility, and other engineering concerns beyond functional defects \[ [12](https://arxiv.org/html/2609.04167v1#bib.bib56 ""), [55](https://arxiv.org/html/2609.04167v1#bib.bib31 ""), [13](https://arxiv.org/html/2609.04167v1#bib.bib55 ""), [14](https://arxiv.org/html/2609.04167v1#bib.bib54 "")\]. These concerns also require engineering knowledge beyond the target code, with project and testing knowledge shown to improve LLM-based test generation \[ [56](https://arxiv.org/html/2609.04167v1#bib.bib15 "")\]. More broadly, surveys of code LLMs and LLM-based software engineering document the limitations of narrow evaluation criteria for complex development tasks \[ [57](https://arxiv.org/html/2609.04167v1#bib.bib29 ""), [58](https://arxiv.org/html/2609.04167v1#bib.bib28 "")\]. Constraint-aware code benchmarks have begun evaluating additional requirements \[ [59](https://arxiv.org/html/2609.04167v1#bib.bib52 "")\], while repository-level work attaches design constraints but relies on LLM-based verification \[ [60](https://arxiv.org/html/2609.04167v1#bib.bib53 "")\]; such judges can exhibit subjectivity and evaluation biases \[ [61](https://arxiv.org/html/2609.04167v1#bib.bib44 ""), [62](https://arxiv.org/html/2609.04167v1#bib.bib30 "")\]. In contrast, SWE-Gate constructs every instance around a review-derived constraint and separately executes functional and constraint tests, enabling deterministic evaluation of both dimensions.

## SWE-Gate Benchmark

SWE-Gate adopts a constraint-first construction strategy because a review-derived constraint is tied to a particular functional and code context rather than being a standalone rule that can be appended to an arbitrary issue. Moreover, directly reusing the source issue–pull request pair preserves a public one-to-one correspondence between the task and its known repair. SWE-Gate instead jointly abstracts the bug pattern, engineering intent, and applicability conditions from real review discussions and instantiates them in distinct, compatible repository contexts. This strategy preserves the authenticity of the original review requirement, expands a single constraint into multiple contextually valid tasks across repositories and domains, and mitigates direct solution memorization without claiming to eliminate all training-data contamination. Figure [1](https://arxiv.org/html/2609.04167v1#Sx3.F1 "Figure 1 ‣ SWE-Gate Benchmark ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents") illustrates the resulting construction pipeline.

![Refer to caption](https://arxiv.org/html/2609.04167v1/swe_if_instance_construction_pipeline.png)Figure 1: Overview of the SWE-Gate construction pipeline. SWE-Gate reconstructs issue–pull request artifacts, uses LLM-based processing to extract atomic review suggestions and select verifiable constraint seeds, transfers the seeds into compatible repository contexts, and validates the resulting instances through executable tests and quality assurance.

### Benchmark Instance

Each SWE-Gate instance is a repository-level repair task that combines natural-language descriptions, patches, and executable tests to evaluate issue resolution and constraint following (Figure [2](https://arxiv.org/html/2609.04167v1#Sx3.F2 "Figure 2 ‣ Benchmark Instance ‣ SWE-Gate Benchmark ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents")).

Figure 2: SWE-Gate benchmark instance schema.

- •


Issue Description. A natural-language specification of the observed incorrect behavior and expected functionality, without revealing the root cause or repair strategy.

- •


Mutant Patch. A patch that injects a reproducible target defect into the original repository while preserving the surrounding engineering context.

- •


Functional Test. An executable test that exposes the defect and validates its repair.

- •


Constraint Description. A natural-language engineering requirement that the repair must satisfy beyond functional correctness.

- •


Constraint Test. An executable test that validates compliance with the review constraint.

- •


Non-compliant Patch. A reference repair that passes the functional test but violates the constraint.

- •


Gold Patch. A reference repair that passes both the functional and constraint tests.


Among these artifacts, the non-compliant patch and the gold patch play a central role in the design of SWE-Gate instances. The non-compliant patch demonstrates that a patch can fix the issue while violating the review constraint; therefore, the review constraint is not merely a restatement of the functional requirement. The gold patch demonstrates that the review constraint is satisfiable and can hold simultaneously with the functional repair. Together, they show that constraint compliance is not implied by functional correctness, can be validated separately, and is jointly satisfiable with a functional repair.

### Constraint-First Instance Construction

#### Repository Selection

SWE-Gate distinguishes between two types of repository roles: _seed repositories_ and _instance repositories_. Seed repositories provide engineering knowledge from real code review discussions, while instance repositories provide the code contexts needed to construct executable benchmark instances.

Seed repositories are mature open-source Python projects. These projects typically have active development communities, rich pull request review histories, and high community adoption. We select such repositories because their review comments are more likely to reflect engineering requirements raised by maintainers during real software development.

Because constraints are context-dependent, candidate instance repositories are selected from related functionality or domains; for example, data-processing constraints prioritize that ecosystem and CLI constraints prioritize command-line projects. This domain mapping only defines a search space rather than presuming transferability: synthesis must still verify every target location against the seed’s semantic and validation requirements. Representative mappings appear in the supplementary material .

#### Constraint Extraction

Before the two LLM-assisted extraction stages, SWE-Gate collects merged pull requests from seed repositories through the GitHub API. For each pull request, we retrieve the pull request itself, review comments, linked issues, changed files, and the final unified diff. Inline review comments retain their file paths, line locations, and diff hunks. Together, these artifacts form the raw data used as input to the first stage.

Inspired by the atomic-suggestion stage of DesignHunter in SWE-Shield \[ [60](https://arxiv.org/html/2609.04167v1#bib.bib53 "")\], the first-stage LLM extracts only suggestions explicitly stated in review comments. It decomposes comments containing multiple requests into atomic records of the reviewer-identified problem, requested change, rationale, category, source identifiers, and confidence, without inferring unstated rules. Rule-based filtering then removes workflow, documentation-only, test-only, formatting, naming, typographical, vague, and otherwise unverifiable requests. Linking each retained record to its source comment and original and revised diff context preserves review and implementation traceability.

Second, deterministic checks require a linked issue, substantive suggestion, and sufficient diff context. An LLM then evaluates each survivor with its issue, review, and code evidence. Candidates are retained only when the issue is user-visible, the diff supports the root cause or repair direction, the review adds rather than restates a requirement, and the governed control flow, API, error behavior, state, or representation can be validated independently. The LLM must identify a plausible functional but non-compliant repair, justify non-implication and transferability, and propose separate executable oracles. Candidates lacking code support, separability, or distinct oracles are rejected.

Each retained candidate becomes a structured _constraint seed_ that preserves the normalized engineering intent and behavioral scope while removing incidental repository wording. It records the constraint, category, rationale, comments, and code evidence; the issue, root cause, relevant change, bug pattern, and an example non-compliant repair; scenario features and retrieval cues for compatible contexts; and non-redundancy, transferability, and separate oracle specifications. Complete issue, review, code, and diff provenance remains linked by a stable identifier. At this stage, oracle proposals establish suitability for instantiation; executable tests are realized only after transfer.

#### Instance Synthesis

Building on SWE-Mirror’s demonstrated cross-repository transfer paradigm \[ [50](https://arxiv.org/html/2609.04167v1#bib.bib40 "")\], SWE-Gate transfers a constraint seed into a compatible target repository, jointly instantiating its functional bug pattern and review-derived constraint as an executable repair task with separate oracles.

The agent first explores the repository’s source files, tests, existing abstractions, and implementation conventions to locate a compatible synthesis anchor. An anchor is a concrete implementation context in which the agent can introduce a user-visible functional failure while preserving an independently testable review constraint. Candidate anchors are rejected when the constraint is not naturally motivated by the target context, every plausible functional repair would necessarily satisfy the constraint, or the functional and constraint dimensions cannot be validated separately.

Rather than generating all mutually dependent artifacts at once, the synthesis agent follows a progressive two-phase generate–execute–refine workflow. First, it creates mutant.patch and a functional-only function\_test.patch, verifying that the test passes on the original repository and fails on the mutant. It revises the anchor, injected bug, or test until this relationship holds. Second, it creates constraint\_test.patch, a natural functional but non-compliant non-compliant.patch, and a compliant gold.patch. The former must pass the functional test and fail the constraint test; the latter must pass both. Execution feedback refines the test and repairs. If a failure shows that the functional task cannot support a separable violation, the agent revisits the first phase, regenerates dependent artifacts, and reruns the full matrix. This progressive construction strategy first establishes a valid functional task and then adds the stricter constraint-compliance relationships, reducing the difficulty of producing all interdependent patches and tests correctly in a single generation step.

Let FF and CC denote functional and constraint tests, and RR, MM, NN, and GG the original repository, mutant patch, non-compliant repair, and gold repair. Valid instances satisfy Table [1](https://arxiv.org/html/2609.04167v1#Sx3.T1 "Table 1 ‣ Instance Synthesis ‣ Constraint-First Instance Construction ‣ SWE-Gate Benchmark ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

| Repository State | Notation | FF | CC |
| --- | --- | --- | --- |
| Original Repository | RR | Pass | – |
| Mutant Bug | R+MR+M | Fail | – |
| Non-compliant Repair | R+M+NR+M+N | Pass | Fail |
| Gold Repair | R+M+GR+M+G | Pass | Pass |

Table 1: Validation matrix for a SWE-Gate instance. Following the fail-to-pass repair paradigm \[ [6](https://arxiv.org/html/2609.04167v1#bib.bib59 "")\], the original repository passes FF and the mutant one fails it. The non-compliant repair passes FF but fails CC, whereas the gold repair passes both, establishing constraint separability and satisfiability.

Finally, the agent writes issue.md in a realistic user or contributor voice, describing only the visible failure without exposing injected locations, hidden tests, reference repairs, or validation internals. Any included reproduction program must run against the constructed buggy state, although this requirement is prompt-guided rather than independently rule-enforced. The separate constraint.md states the review-derived requirement, remains aligned with its test, and avoids revealing an expected implementation.

### Quality Assurance

Executable validity alone does not exclude artificial, semantically inconsistent, or otherwise unsuitable LLM-generated instances. We manually inspected pilot candidates, consolidated recurring semantic rejection reasons into a failure-pattern taxonomy, and encoded this human-derived taxonomy as criteria for scalable LLM review.

Each candidate first undergoes basic structural checks to ensure that the required artifacts, execution commands, and provenance fields are complete. It is then validated in a containerized environment using the complete validation matrix: the original repository must pass the functional test, the injected bug must fail it, the non-compliant repair must pass the functional test but fail the constraint test, and the gold repair must pass both tests. Patch-application failures, execution timeouts, and other infrastructure errors are not treated as expected test failures. This Docker-based validation automatically rejects candidates whose functional and constraint behaviors cannot be independently established.

Only candidates that pass the Docker validation matrix proceed to LLM-based semantic review. The reviewer receives the constraint seed, source provenance, generated artifacts, and execution results, and applies the rejection criteria derived from manual inspection. Common semantic failure patterns include constraints that merely restate the functional issue, constraint descriptions that prescribe a particular API or implementation strategy, constraint tests that enforce behavior not stated in the natural-language description, benchmark-specific helpers or abstractions introduced solely to make the constraint testable, constraints that are not naturally motivated by the synthesized scenario, and descriptions that expose hidden evaluation artifacts. The complete taxonomy and corresponding rejection rationales are provided in the supplementary material .

Finally, all instances retained after LLM-based screening are manually inspected. This final review verifies that the issue resembles a realistic user-reported defect, the constraint remains faithful to its review-derived seed and arises naturally from the target repository, the issue and constraint are non-redundant, the non-compliant repair represents a natural functional solution, and the gold patch provides a general repository-consistent repair rather than hard-coding the generated tests. Stage-wise candidate counts and rejection reasons are reported in the supplementary material.

### Dataset Characteristics

The current version of SWE-Gate contains 303 repository-level repair instances covering 75 open-source Python repositories. SWE-Gate covers multiple software domains, including data analysis, web frameworks, testing frameworks, command-line tools, configuration management, symbolic computation, and data validation. This repository diversity enables the benchmark to evaluate review constraints across different code contexts, rather than only measuring local conventions in a single project or a single project family.

Because a constraint may involve several engineering concerns, SWE-Gate uses a multi-label taxonomy. The most frequent categories are _Error Semantics_ (152 instances, 50.2%) and _Schema / Metadata / Typing_ (143, 47.2%). The taxonomy also covers ordering and argument preservation, encoding and escaping, scope generalization, compatibility, sentinel distinctions, performance, idempotence, and resource lifecycle requirements. Table [5](https://arxiv.org/html/2609.04167v1#Sx4.T5 "Table 5 ‣ RQ2: How Does Explicit Constraint Guidance Affect Repair Outcomes? ‣ Evaluation ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents") reports the complete category counts together with category-level model performance. This distribution shows that code review evaluates interface behavior, exception semantics, metadata consistency, and other engineering properties beyond whether functional tests pass.

## Evaluation

### Experimental Setup

We evaluate all 303 instances. For each, an agent receives the target repository and issue description and generates a repair. Its patch is applied to a clean repository containing the injected bug and evaluated by both functional and constraint suites. Any generated changes to benchmark test files are discarded before execution, preventing evaluation leakage and ensuring that only the repair patch is assessed.

Under _Constraint-Provided_ (+C+C), the agent also receives the natural-language constraint; under _Constraint-Omitted_ (−C-C), it receives only the same repository and issue. Instances, framework, interaction budget, and hidden functional and constraint tests are identical, so the only difference is whether constraint guidance is visible during repair. The +C+C condition measures intended SWE-Gate performance, while −C-C is a controlled input ablation.

##### Evaluation Models.

We evaluate GPT-5.5, GPT-5.4-mini, DeepSeek-V4-Flash, and GPT-4o-mini, spanning providers and capability levels that support repository-level engineering. All use Mini-SWE-Agent with at most 100 interaction steps. The standard SWE-Bench execution pipeline validates each patch in an isolated container.

##### Evaluation Metrics.

We report three complementary metrics. Let NN be the total number of instances, NFN\_{F} the number of generated patches that pass the functional tests, and NF∩CN\_{F\\cap C} the number that pass both the functional and constraint tests.

- •


Functional Success Rate (FSR). The proportion of all instances for which the generated patch resolves the reported functional issue:



|     |     |     |
| --- | --- | --- |
|  | FSR=NFN.\\mathrm{FSR}=\\frac{N\_{F}}{N}. |  |

- •


Constraint Following Rate (CFR). The proportion of functionally successful repairs that also satisfy the review constraint:



|     |     |     |
| --- | --- | --- |
|  | CFR=NF∩CNF.\\mathrm{CFR}=\\frac{N\_{F\\cap C}}{N\_{F}}. |  |

- •


Joint Success Rate (JSR). The proportion of all instances for which the generated patch satisfies both the functional requirement and the review constraint:



|     |     |     |
| --- | --- | --- |
|  | JSR=NF∩CN.\\mathrm{JSR}=\\frac{N\_{F\\cap C}}{N}. |  |


JSR is the primary metric of SWE-Gate because it captures complete success under the benchmark’s dual evaluation protocol. For the input ablation, we also report the percentage-point difference between the two conditions. For any metric M∈{FSR,CFR,JSR}M\\in\\{\\mathrm{FSR},\\mathrm{CFR},\\mathrm{JSR}\\}, we define

|     |     |     |
| --- | --- | --- |
|  | Δ​M=M+C−M−C.\\Delta M=M\_{+C}-M\_{-C}. |  |

A positive Δ​M\\Delta M indicates a higher observed rate when the review constraint is provided to the agent.

### RQ1: How Do Coding Agents Perform under SWE-Gate’s Dual Evaluation?

Table [2](https://arxiv.org/html/2609.04167v1#Sx4.T2 "Table 2 ‣ RQ1: How Do Coding Agents Perform under SWE-Gate’s Dual Evaluation? ‣ Evaluation ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents") reports functional and joint performance under the intended +C+C setting.

| Model | F.Pass | J.Pass | FSR | CFR | JSR |
| --- | --- | --- | --- | --- | --- |
| GPT-5.5 | 227 | 160 | 74.9 | 70.5 | 52.8 |
| GPT-5.4-mini | 187 | 120 | 61.7 | 64.2 | 39.6 |
| DeepSeek-V4-Flash | 202 | 130 | 66.7 | 64.4 | 42.9 |
| GPT-4o-mini | 28 | 13 | 9.2 | 46.4 | 4.3 |

Table 2: Overall performance in the Constraint-Provided setting. Rates are reported as percentages. _F. Pass_ denotes the number of generated patches that pass the functional test suite.
_J. Pass_ ( _Joint Pass_) denotes the number of patches that pass both the functional and constraint test suites.

The models differ substantially in functional repair performance. GPT-5.5 achieves the highest FSR at 74.9%, followed by DeepSeek-V4-Flash at 66.7% and GPT-5.4-mini at 61.7%. GPT-4o-mini resolves only 9.2% of the instances, showing that SWE-Gate remains difficult for a substantially weaker model.

Functional success, however, does not imply joint success. GPT-5.5 produces 227 functionally successful repairs, but only 160 also pass constraint validation. The corresponding CFR is 70.5%, meaning that 29.5% of its functionally successful repairs violate the accompanying constraint. The same gap appears for every evaluated model.

##### Failures Hidden by Functional-Only Evaluation.

We call a patch that passes functional validation but fails constraint validation a _hidden failure_. Such a patch would be accepted under an evaluation protocol that observes only issue-related functional tests. We define the Hidden Failure Rate (HFR) as

|     |     |     |
| --- | --- | --- |
|  | HFR=NF−NF∩CNF=1−CFR.\\mathrm{HFR}=\\frac{N\_{F}-N\_{F\\cap C}}{N\_{F}}=1-\\mathrm{CFR}. |  |

| Model | F. Pass | Hidden Failures | HFR |
| --- | --- | --- | --- |
| GPT-5.5 | 227 | 67 | 29.5 |
| GPT-5.4-mini | 187 | 67 | 35.8 |
| DeepSeek-V4-Flash | 202 | 72 | 35.6 |
| GPT-4o-mini | 28 | 15 | 53.6 |
| Total | 644 | 221 | 34.3 |

Table 3: Functionally successful repairs that fail review constraint
validation in the Constraint-Provided setting. Rates are percentages.

Across the four models, 644 generated patches pass the functional tests, but only 423 pass both test suites. SWE-Gate therefore identifies 221 hidden failures, corresponding to 34.3% of all functional successes. The HFR ranges from 29.5% for GPT-5.5 to 53.6% for GPT-4o-mini. These results demonstrate that functional-only evaluation leaves a substantial fraction of constraint-violating repairs undetected. More precisely, they show that functional success does not entail review constraint compliance under SWE-Gate’s executable evaluation protocol.

##### Answer to RQ1.

Current coding agents resolve a substantial fraction of SWE-Gate’s functional issues, but their joint success rates are consistently lower than their functional success rates. Across all evaluated model–instance pairs, 221 of 644 functional successes fail constraint validation. SWE-Gate therefore provides an additional, independently executable evaluation signal that is not captured by functional tests alone.

### RQ2: How Does Explicit Constraint Guidance Affect Repair Outcomes?

|  | FSR | CFR | JSR |
| --- | --- | --- | --- |
| Model | −C-C | +C+C | Δ\\Delta | −C-C | +C+C | Δ\\Delta | −C-C | +C+C | Δ\\Delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.5 | 75.6 | 74.9 | -0.7 | 54.6 | 70.5 | +15.9 | 41.3 | 52.8 | +11.5 |
| GPT-5.4-mini | 71.6 | 61.7 | -9.9 | 50.7 | 64.2 | +13.5 | 36.3 | 39.6 | +3.3 |
| DeepSeek-V4-Flash | 70.0 | 66.7 | -3.3 | 54.2 | 64.4 | +10.2 | 38.0 | 42.9 | +4.9 |
| GPT-4o-mini | 15.8 | 9.2 | -6.6 | 20.8 | 46.4 | +25.6 | 3.3 | 4.3 | +1.0 |

Table 4: Constraint input ablation. +C+C provides the natural-language review constraint; −C-C omits it while retaining the same hidden functional and constraint tests. Δ\\Delta is +C+C minus −C-C in percentage points.

| Constraint Category | N | GPT-5.5 | GPT-5.4-mini | DeepSeek-V4-Flash | GPT-4o-mini |
| --- | --- | --- | --- | --- | --- |
| FSR | CFR | JSR | FSR | CFR | JSR | FSR | CFR | JSR | FSR | CFR | JSR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Error semantics | 152 | 75.0 | 72.8 | 54.6 | 67.1 | 72.5 | 48.7 | 70.4 | 66.4 | 46.7 | 9.2 | 78.6 | 7.2 |
| Schema / metadata / typing | 143 | 72.7 | 68.3 | 49.7 | 62.2 | 60.7 | 37.8 | 64.3 | 64.1 | 41.3 | 11.9 | 52.9 | 6.3 |
| Ordering / argument preservation | 86 | 60.5 | 76.9 | 46.5 | 51.2 | 75.0 | 38.4 | 62.8 | 79.6 | 50.0 | 7.0 | 66.7 | 4.7 |
| Encoding / escaping / quoting | 74 | 81.1 | 68.3 | 55.4 | 60.8 | 51.1 | 31.1 | 79.7 | 55.9 | 44.6 | 5.4 | 0.0 | 0.0 |
| Scope generalization | 62 | 87.1 | 63.0 | 54.8 | 66.1 | 46.3 | 30.6 | 69.4 | 53.5 | 37.1 | 12.9 | 0.0 | 0.0 |
| Compatibility / deprecation | 55 | 74.5 | 75.6 | 56.4 | 56.4 | 71.0 | 40.0 | 63.6 | 77.1 | 49.1 | 12.7 | 28.6 | 3.6 |
| Missing vs. empty / sentinel distinction | 51 | 74.5 | 81.6 | 60.8 | 60.8 | 74.2 | 45.1 | 56.9 | 75.9 | 43.1 | 17.6 | 66.7 | 11.8 |
| Performance / structure | 41 | 75.6 | 71.0 | 53.7 | 68.3 | 78.6 | 53.7 | 75.6 | 74.2 | 56.1 | 9.8 | 75.0 | 7.3 |
| Idempotence / duplicate processing | 30 | 60.0 | 72.2 | 43.3 | 46.7 | 71.4 | 33.3 | 46.7 | 71.4 | 33.3 | 0.0 | – | 0.0 |
| Lifecycle cleanup / resource | 19 | 84.2 | 62.5 | 52.6 | 68.4 | 53.8 | 36.8 | 73.7 | 57.1 | 42.1 | 10.5 | 50.0 | 5.3 |

Table 5: Performance by review constraint category in the Constraint-Provided condition. FSR and JSR are calculated over all instances in each category, whereas CFR is calculated over functionally successful repairs. “–” indicates that CFR is undefined because the model has no functional success in that category. Categories are multi-label and therefore not mutually exclusive.

Table [4](https://arxiv.org/html/2609.04167v1#Sx4.T4 "Table 4 ‣ RQ2: How Does Explicit Constraint Guidance Affect Repair Outcomes? ‣ Evaluation ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents") compares the controlled input conditions.

Providing the constraint increases JSR for every model. The largest gain is observed for GPT-5.5, whose JSR rises from 41.3% to 52.8%, an improvement of 11.5 percentage points. DeepSeek-V4-Flash and GPT-5.4-mini improve by 4.9 and 3.3 points, respectively, while GPT-4o-mini improves by 1.0 point. Across all four models, the number of joint successes increases from 360 to 423.

Providing the constraint description also substantially improves CFR for all four models. GPT-5.5 achieves the highest CFR improvement, increasing from 54.6% under the Constraint-Omitted condition to 70.5% under the Constraint-Provided condition. The CFR of GPT-5.4-mini increases from 50.7% to 64.2%, while that of DeepSeek-V4-Flash increases from 54.2% to 64.4%. GPT-4o-mini exhibits the largest relative change, with its CFR increasing from 20.8% to 46.4%. Overall, providing the constraint improves CFR by 10.2–25.6 percentage points across the evaluated models. These results show that, among functionally successful repairs, explicit constraint guidance substantially increases the likelihood of satisfying the corresponding engineering requirement.

At the same time, FSR does not improve under the Constraint-Provided condition. It decreases slightly for GPT-5.5 and by 3.3–9.9 percentage points for the other models. One possible explanation is that satisfying an additional requirement increases the complexity of the repair and may steer an agent away from a simpler functionally adequate patch. Because each condition contains one generation per model and instance, these results should be interpreted as an observed trade-off under the controlled input ablation rather than as a general causal claim about model behavior.

##### Answer to RQ2.

Explicit constraint descriptions improve the observed joint success rate for all evaluated models and substantially increase the fraction of functional repairs that also satisfy constraint validation. However, this improvement is accompanied by lower functional success for three models and a small decrease for GPT-5.5. Constraint information therefore improves compliance and overall joint success in these runs, but does not uniformly improve functional repair.

### RQ3: Which Review Constraint Categories Remain Challenging?

Table [5](https://arxiv.org/html/2609.04167v1#Sx4.T5 "Table 5 ‣ RQ2: How Does Explicit Constraint Guidance Affect Repair Outcomes? ‣ Evaluation ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents") analyzes overlapping categories under +C+C; rows are not mutually exclusive and their counts should not be summed. For the three stronger models, Scope Generalization has CFRs of 63.0%, 46.3%, and 53.5%, while Lifecycle Cleanup/Resource reaches 62.5%, 53.8%, and 57.1%. These constraints demand coverage beyond the immediate failure or preservation across a resource lifecycle, making them difficult to satisfy with a narrowly localized patch.

Encoding/Escaping/Quoting is also difficult for GPT-5.4-mini and DeepSeek-V4-Flash, which satisfy only 51.1% and 55.9% of constraints after functional success, while Schema/Metadata/Typing yields 60.7–68.3% across stronger models. By contrast, Missing-vs.-Empty/Sentinel Distinction reaches 74.2–81.6%, and Ordering/Argument Preservation 75.0–79.6%. The larger functional–joint gaps in the former categories therefore reflect conditional difficulty in satisfying the review constraint, not only variation in functional repair rates.

Model profiles also differ: DeepSeek-V4-Flash leads Ordering/Argument Preservation at 79.6% CFR, GPT-5.4-mini leads Performance/Structure at 78.6%, and GPT-5.5 reaches 81.6% on Missing-vs.-Empty/Sentinel Distinction. GPT-4o-mini has too few functional successes in most categories for stable conclusions, so its high conditional values should not be interpreted as superior constraint following. Since categories overlap and several are small, all comparisons are descriptive, but they show that aggregate scores obscure which engineering requirements agents fail.

##### Answer to RQ3.

Constraint-following difficulty is not uniform across engineering requirements. Among functionally successful repairs, Scope Generalization, Lifecycle Cleanup/Resource, Encoding/Escaping/Quoting, and Schema/Metadata/Typing yield some of the lowest CFR values for the three stronger models. In contrast, Missing-vs.-Empty/Sentinel Distinction and Ordering/Argument Preservation are satisfied more frequently. These results show that aggregate scores hide meaningful differences in the review constraints that agents fail to follow.

## Conclusion

We introduced SWE-Gate, a repository-level benchmark that derives review constraints from real pull request reviews, constructs repair tasks around them, and evaluates constraint compliance separately from functional correctness. Across 303 instances from 75 Python repositories, 221 of 644 functionally successful repairs fail to satisfy the provided constraints, showing that functional-only evaluation overestimates agents’ ability to satisfy complete repair requirements. Future work should extend SWE-Gate beyond Python and develop reliable evaluation methods for review requirements that cannot yet be expressed as executable tests. Incorporating broader maintainer feedback into instance construction could further improve the realism of transferred tasks and reduce potential bias introduced by LLM-assisted synthesis and screening.

## Acknowledgments

This work is supported by the National Natural Science Foundation of China (Grant No. 92582202, No. 62302534)

## References

- \[1\]E. Shi, F. Zhang, Y. Wang, B. Chen, L. Du, H. Zhang, S. Han, D. Zhang, and H. Sun (2023)SoTaNa: the open-source software development assistant.
External Links: 2308.13416,
[Link](https://arxiv.org/abs/2308.13416 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[2\]Y. Wang, W. Zhong, Y. Huang, E. Shi, M. Yang, J. Chen, H. Li, Y. Ma, Q. Wang, and Z. Zheng (2024)Agents in software engineering: survey, landscape, and vision.
External Links: 2409.09030,
[Link](https://arxiv.org/abs/2409.09030 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[3\]F. Zhang, B. Chen, Y. Zhang, J. Keung, J. Liu, D. Zan, Y. Mao, J. Lou, and W. Chen (2023)RepoCoder: repository-level code completion through iterative retrieval and generation.
In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, H. Bouamor, J. Pino, and K. Bali (Eds.),
Singapore, pp. 2471–2484.
External Links: [Link](https://aclanthology.org/2023.emnlp-main.151/ ""),
[Document](https://dx.doi.org/10.18653/v1/2023.emnlp-main.151 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[4\]Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma, W. Zhong, J. Chen, M. Mao, and Z. Zheng (2025)Llm hallucinations in practical code generation: phenomena, mechanism, and mitigation.
Proceedings of the ACM on Software Engineering2 (ISSTA), pp. 481–503.
Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[5\]D. Zheng, Y. Wang, E. Shi, X. Liu, Y. Ma, H. Zhang, and Z. Zheng (2025)Top general performance = top domain performance? domaincodebench: a multi-domain code generation benchmark.
External Links: 2412.18573,
[Link](https://arxiv.org/abs/2412.18573 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[6\]C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. R. Narasimhan (2024)SWE-bench: can language models resolve real-world github issues?.
In The Twelfth International Conference on Learning Representations,
External Links: [Link](https://openreview.net/forum?id=VTF8yNQM66 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Table 1](https://arxiv.org/html/2609.04167v1#Sx3.T1 "In Instance Synthesis ‣ Constraint-First Instance Construction ‣ SWE-Gate Benchmark ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[7\]J. Yang, C. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press (2024)SWE-agent: agent-computer interfaces enable automated software engineering.
In Advances in Neural Information Processing Systems, A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (Eds.),
Vol. 37, pp. 50528–50652.
External Links: [Document](https://dx.doi.org/10.52202/079017-1601 ""),
[Link](https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[8\]X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan, Y. Song, B. Li, J. Singh, H. H. Tran, F. Li, R. Ma, M. Zheng, B. Qian, D. Shao, N. Muennighoff, Y. Zhang, B. Hui, J. Lin, R. Brennan, H. Peng, H. Ji, and G. Neubig (2025)OpenHands: an open platform for AI software developers as generalist agents.
In The Thirteenth International Conference on Learning Representations,
External Links: [Link](https://openreview.net/forum?id=OJd3ayDDoF "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[9\]C. S. Xia, Y. Deng, S. Dunn, and L. Zhang (2024)Agentless: demystifying llm-based software engineering agents.
External Links: 2407.01489,
[Link](https://arxiv.org/abs/2407.01489 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p1.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[10\]Z. Qi, F. Long, S. Achour, and M. Rinard (2015)An analysis of patch plausibility and correctness for generate-and-validate patch generation systems.
In Proceedings of the 2015 International Symposium on Software Testing and Analysis,
ISSTA 2015, New York, NY, USA, pp. 24–36.
External Links: ISBN 9781450336208,
[Link](https://doi.org/10.1145/2771783.2771791 ""),
[Document](https://dx.doi.org/10.1145/2771783.2771791 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p2.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[11\]B. Yu, Y. Zhu, P. He, and D. Kang (2025)UTBoost: rigorous evaluation of coding agents on SWE-bench.
In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.),
Vienna, Austria, pp. 3762–3774.
External Links: [Link](https://aclanthology.org/2025.acl-long.189/ ""),
[Document](https://dx.doi.org/10.18653/v1/2025.acl-long.189 ""),
ISBN 979-8-89176-251-0Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p2.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[12\]A. Bacchelli and C. Bird (2013)Expectations, outcomes, and challenges of modern code review.
In 2013 35th International Conference on Software Engineering (ICSE),
Vol. , pp. 712–721.
External Links: [Document](https://dx.doi.org/10.1109/ICSE.2013.6606617 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p2.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[13\]C. Sadowski, E. Söderberg, L. Church, M. Sipko, and A. Bacchelli (2018)Modern code review: a case study at google.
In Proceedings of the 40th International Conference on Software Engineering: Software Engineering in Practice,
ICSE-SEIP ’18, New York, NY, USA, pp. 181–190.
External Links: ISBN 9781450356596,
[Link](https://doi.org/10.1145/3183519.3183525 ""),
[Document](https://dx.doi.org/10.1145/3183519.3183525 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p2.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[14\]P. C. Rigby and C. Bird (2013)Convergent contemporary software peer review practices.
In Proceedings of the 2013 9th Joint Meeting on Foundations of Software Engineering,
ESEC/FSE 2013, New York, NY, USA, pp. 202–212.
External Links: ISBN 9781450322379,
[Link](https://doi.org/10.1145/2491411.2491444 ""),
[Document](https://dx.doi.org/10.1145/2491411.2491444 "")Cited by: [Introduction](https://arxiv.org/html/2609.04167v1#Sx1.p2.1 "Introduction ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[15\]M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba (2021)Evaluating large language models trained on code.
External Links: 2107.03374,
[Link](https://arxiv.org/abs/2107.03374 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[16\]J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton (2021)Program synthesis with large language models.
External Links: 2108.07732,
[Link](https://arxiv.org/abs/2108.07732 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[17\]T. Liu, C. Xu, and J. McAuley (2023)RepoBench: benchmarking repository-level code auto-completion systems.
External Links: 2306.03091,
[Link](https://arxiv.org/abs/2306.03091 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[18\]Y. Ding, Z. Wang, W. U. Ahmad, H. Ding, M. Tan, N. Jain, M. K. Ramanathan, R. Nallapati, P. Bhatia, D. Roth, and B. Xiang (2023)CrossCodeEval: a diverse and multilingual benchmark for cross-file code completion.
In Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track,
External Links: [Link](https://openreview.net/forum?id=wgDcbBMSfh "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[19\]Y. Li, E. Shi, D. Zheng, K. Duan, J. Chen, and Y. Wang (2024)Repomincoder: improving repository-level code generation based on information loss screening.
In Proceedings of the 15th Asia-Pacific Symposium on Internetware,
pp. 229–238.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[20\]M. A. M. Khan, M. S. Bari, X. L. Do, W. Wang, M. R. Parvez, and S. Joty (2023)XCodeEval: a large scale multilingual multitask benchmark for code understanding, generation, translation and retrieval.
External Links: 2303.03004,
[Link](https://arxiv.org/abs/2303.03004 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[21\]R. Just, D. Jalali, and M. D. Ernst (2014)Defects4J: a database of existing faults to enable controlled testing studies for java programs.
In Proceedings of the 2014 International Symposium on Software Testing and Analysis,
ISSTA 2014, New York, NY, USA, pp. 437–440.
External Links: ISBN 9781450326452,
[Link](https://doi.org/10.1145/2610384.2628055 ""),
[Document](https://dx.doi.org/10.1145/2610384.2628055 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[22\]R. Widyasari, S. Q. Sim, C. Lok, H. Qi, J. Phan, Q. Tay, C. Tan, F. Wee, J. E. Tan, Y. Yieh, B. Goh, F. Thung, H. J. Kang, T. Hoang, D. Lo, and E. L. Ouh (2020)BugsInPy: a database of existing bugs in python programs to enable controlled testing and debugging studies.
In Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering,
ESEC/FSE 2020, New York, NY, USA, pp. 1556–1560.
External Links: ISBN 9781450370431,
[Link](https://doi.org/10.1145/3368089.3417943 ""),
[Document](https://dx.doi.org/10.1145/3368089.3417943 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[23\]D. Guo, S. Lu, N. Duan, Y. Wang, M. Zhou, and J. Yin (2022)Unixcoder: unified cross-modal pre-training for code representation.
In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
pp. 7212–7225.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[24\]J. Lin, Y. Wang, Y. Yang, L. Zhang, and Y. Xie (2026)Towards better code understanding in decoder-only models with contrastive learning.
In Proceedings of the AAAI Conference on Artificial Intelligence,
Vol. 40, pp. 32006–32014.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[25\]H. Guo, X. Chen, Y. Huang, Y. Wang, X. Ding, Z. Zheng, X. Zhou, and H. Dai (2023)Snippet comment generation based on code context expansion.
ACM Transactions on Software Engineering and Methodology33 (1), pp. 1–30.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[26\]Y. Wang, Y. Huang, D. Guo, H. Zhang, and Z. Zheng (2024)Sparsecoder: identifier-aware sparse transformer for file-level code summarization.
In 2024 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER),
pp. 614–625.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[27\]Y. Wang, E. Shi, L. Du, X. Yang, Y. Hu, S. Han, H. Zhang, and D. Zhang (2021)Cocosum: contextual code summarization with multi-relational graph neural network.
arXiv preprint arXiv:2107.01933.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[28\]Y. Wang, K. Duan, D. Zheng, E. Shi, F. Zhang, Y. Wang, J. Chen, X. Liu, Y. Ma, H. Zhang, et al. (2026)Towards an understanding of context utilization in code intelligence.
ACM Computing Surveys58 (11), pp. 1–43.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[29\]Y. Wang, Y. Wang, D. Guo, J. Chen, R. Zhang, Y. Ma, and Z. Zheng (2025)Rlcoder: reinforcement learning for repository-level code completion.
In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE),
pp. 1140–1152.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[30\]T. Jiang, Y. Wang, Y. Wang, D. Guo, E. Shi, Y. Ma, J. Chen, and Z. Zheng (2026)AlignCoder: aligning retrieval with target intent for repository-level code completion.
External Links: 2601.19697,
[Link](https://arxiv.org/abs/2601.19697 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[31\]Y. Wang, S. Wang, Y. Wang, B. Zhang, D. Guo, J. Chen, and Z. Zheng (2026)RepoReasoner: evaluating repository-level code reasoning ability of long-context language models.
Proceedings of the ACM on Software Engineering3 (FSE), pp. 2790–2812.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[32\]W. Gu, J. Chen, Y. Wang, T. Jiang, X. Li, M. Liu, X. Liu, Y. Ma, and Z. Zheng (2025)What to retrieve for effective retrieval-augmented code generation? an empirical study and beyond.
arXiv preprint arXiv:2503.20589.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[33\]D. Zheng, R. Ye, Y. Wang, Y. Ye, H. Zhang, E. Shi, X. Liu, Y. Ma, J. Yu, and Z. Zheng (2026)SWE-prime: fewer trajectories, better performance.
External Links: 2608.27449,
[Link](https://arxiv.org/abs/2608.27449 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p1.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[34\]W. Tao, Y. Zhou, Y. Wang, W. Zhang, H. Zhang, and Y. Cheng (2024)Magis: llm-based multi-agent framework for github issue resolution.
Advances in Neural Information Processing Systems37, pp. 51963–51993.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[35\]T. Jiang, Y. Wang, X. He, D. Guo, J. Chen, M. Wen, E. Shi, X. Liu, Y. Ma, and G. Li (2026)PhoenixRepair: rethinking repair strategy exploration in software agents.
arXiv preprint arXiv:2607.18859.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[36\]D. Zan, Z. Huang, W. Liu, H. Chen, S. Xin, L. Zhang, Q. Liu, L. Aoyan, L. Chen, X. Zhong, S. Liu, Y. Xiao, L. Chen, Y. Zhang, J. Su, T. Liu, R. LONG, M. Ding, and l. xiang (2025)Multi-swe-bench: a multilingual benchmark for issue resolving.
In Advances in Neural Information Processing Systems, D. Belgrave, C. Zhang, H. Lin, R. Pascanu, P. Koniusz, M. Ghassemi, and N. Chen (Eds.),
Vol. 38, pp. .
External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2025/file/5afa9cb1e917b898ad418216dc726fbd-Paper-Datasets_and_Benchmarks_Track.pdf "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[37\]D. Zan, Z. Huang, A. Yu, S. Lin, Y. Shi, W. Liu, D. Chen, Z. Qi, H. Yu, L. Yu, D. Ran, M. Zeng, B. Shen, P. Bian, G. Liang, B. Guan, P. Huang, T. Xie, Y. Wang, and Q. Wang (2024)SWE-bench-java: a github issue resolving benchmark for java.
External Links: 2408.14354,
[Link](https://arxiv.org/abs/2408.14354 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[38\]X. Deng, J. Da, E. Pan, Y. Y. He, C. Ide, K. Garg, N. Lauffer, A. Park, N. Pasari, C. Rane, K. Sampath, M. Krishnan, S. Kundurthy, S. Hendryx, Z. Wang, V. Bharadwaj, J. Holm, R. Aluri, C. B. C. Zhang, N. Jacobson, B. Liu, and B. Kenstler (2025)SWE-bench pro: can ai agents solve long-horizon software engineering tasks?.
External Links: 2509.16941,
[Link](https://arxiv.org/abs/2509.16941 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[39\]T. Joshi, S. Chowdhury, and F. Uysal (2025)SWE-bench-cl: continual learning for coding agents.
External Links: 2507.00014,
[Link](https://arxiv.org/abs/2507.00014 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[40\]L. Zhang, S. He, C. Zhang, Y. Kang, B. Li, C. Xie, J. Wang, M. Wang, Y. Huang, S. Fu, E. Nallipogu, Q. Lin, Y. Dang, S. Rajmohan, and D. Zhang (2025)SWE-bench goes live!.
In Advances in Neural Information Processing Systems, D. Belgrave, C. Zhang, H. Lin, R. Pascanu, P. Koniusz, M. Ghassemi, and N. Chen (Eds.),
Vol. 38, pp. .
External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2025/file/d83c4a745789690f82e86d0ef752ae7c-Paper-Datasets_and_Benchmarks_Track.pdf "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[41\]I. Badertdinov, A. Golubev, M. Nekrashevich, A. Shevtsov, S. Karasik, A. Andriushchenko, M. Trofimova, D. Litvintseva, and B. Yangel (2025)SWE-rebench: an automated pipeline for task collection and decontaminated evaluation of software engineering agents.
In Advances in Neural Information Processing Systems, D. Belgrave, C. Zhang, H. Lin, R. Pascanu, P. Koniusz, M. Ghassemi, and N. Chen (Eds.),
Vol. 38, pp. .
External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2025/file/21bec6ace947b1b58967b945c8ac0f10-Paper-Datasets_and_Benchmarks_Track.pdf "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[42\]J. Yang, C. E. Jimenez, A. L. Zhang, K. Lieret, J. Yang, X. Wu, O. Press, N. Muennighoff, G. Synnaeve, K. R. Narasimhan, D. Yang, S. I. Wang, and O. Press (2024)SWE-bench multimodal: do ai systems generalize to visual software domains?.
External Links: 2410.03859,
[Link](https://arxiv.org/abs/2410.03859 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[43\]L. Guo, W. Tao, R. Jiang, Y. Wang, J. Chen, X. Liu, Y. Ma, M. Mao, H. Zhang, and Z. Zheng (2025)Omnigirl: a multilingual and multimodal benchmark for github issue resolution.
Proceedings of the ACM on Software Engineering2 (ISSTA), pp. 24–46.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[44\]D. Zheng, Y. Wang, E. Shi, R. Zhang, Y. Ma, H. Zhang, and Z. Zheng (2025)Humanevo: an evolution-aware benchmark for more realistic evaluation of repository-level code generation.
In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE),
pp. 1372–1384.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[45\]Y. Wang, Y. Wang, S. Wang, D. Guo, J. Chen, J. Grundy, X. Liu, Y. Ma, M. Mao, H. Zhang, et al. (2024)RepoTransBench: a real-world multilingual benchmark for repository-level code translation.
arXiv preprint arXiv:2412.17744.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[46\]Y. Wang, B. Zhang, Y. Wang, D. Guo, T. Y. Zhuo, J. Chen, M. Liu, X. Zhang, and Z. Zheng (2026)ArkRepoBench: a repository-level code completion benchmark for harmonyos development.
In Findings of the Association for Computational Linguistics: ACL 2026,
pp. 19409–19429.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[47\]Y. Wang, Z. Zhang, C. Wang, X. Xu, M. Liu, Y. Wang, J. Chen, and Z. Zheng (2026)RealSec-bench: a benchmark for evaluating secure code generation in real-world repositories.
In Findings of the Association for Computational Linguistics: ACL 2026,
pp. 35866–35883.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[48\]D. Zheng, Y. Wang, E. Shi, R. Zhang, Y. Ma, H. Zhang, and Z. Zheng (2024)Towards more realistic evaluation of llm-based code generation: an experimental study and beyond.
arXiv preprint arXiv:2406.06918.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[49\]J. Yang, K. Lieret, C. Jimenez, A. Wettig, K. Khandpur, Y. Zhang, B. Hui, O. Press, L. Schmidt, and D. Yang (2025)SWE-smith: scaling data for software engineering agents.
In Advances in Neural Information Processing Systems, D. Belgrave, C. Zhang, H. Lin, R. Pascanu, P. Koniusz, M. Ghassemi, and N. Chen (Eds.),
Vol. 38, pp. .
External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2025/file/8b86cf5ace600c48fd188efbb8dedec8-Paper-Datasets_and_Benchmarks_Track.pdf "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[50\]J. Wang, D. Zan, S. Xin, S. Liu, Y. Wu, and K. Shen (2025)SWE-mirror: scaling issue-resolving datasets by mirroring issues across repositories.
External Links: 2509.08724,
[Link](https://arxiv.org/abs/2509.08724 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Instance Synthesis](https://arxiv.org/html/2609.04167v1#Sx3.SSx2.SSSx3.p1.1 "Instance Synthesis ‣ Constraint-First Instance Construction ‣ SWE-Gate Benchmark ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[51\]L. Guo, Y. Wang, C. Li, W. Tao, P. Yang, J. Chen, H. Song, D. Tang, and Z. Zheng (2025)SWE data construction, automatically!.
Proceedings of the ACM on Software Engineering3, pp. 525 – 546.
Note: \*External Links: [Link](https://api.semanticscholar.org/CorpusID:284488853 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[52\]K. Yang, X. Mao, S. Wang, Y. Wang, T. Zhang, B. Lin, Y. Qin, Z. Zhang, Y. Lu, and K. Al-Sabahi (2025)Large language models are qualified benchmark builders: rebuilding pre-training datasets for advancing code intelligence tasks.
In 2025 IEEE/ACM 33rd International Conference on Program Comprehension (ICPC),
Vol. , pp. 298–309.
External Links: [Document](https://dx.doi.org/10.1109/ICPC66645.2025.00038 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p2.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[53\]E. K. Smith, E. T. Barr, C. Le Goues, and Y. Brun (2015)Is the cure worse than the disease? overfitting in automated program repair.
In Proceedings of the 2015 10th Joint Meeting on Foundations of Software Engineering,
ESEC/FSE 2015, New York, NY, USA, pp. 532–543.
External Links: ISBN 9781450336758,
[Link](https://doi.org/10.1145/2786805.2786825 ""),
[Document](https://dx.doi.org/10.1145/2786805.2786825 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[54\]J. Yang, A. Zhikhartsev, Y. Liu, and L. Tan (2017)Better test cases for better automated program repair.
In Proceedings of the 2017 11th Joint Meeting on Foundations of Software Engineering,
ESEC/FSE 2017, New York, NY, USA, pp. 831–841.
External Links: ISBN 9781450351058,
[Link](https://doi.org/10.1145/3106237.3106274 ""),
[Document](https://dx.doi.org/10.1145/3106237.3106274 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[55\]M. Beller, A. Bacchelli, A. Zaidman, and E. Juergens (2014)Modern code reviews in open-source projects: which problems do they fix?.
In Proceedings of the 11th Working Conference on Mining Software Repositories,
MSR 2014, New York, NY, USA, pp. 202–211.
External Links: ISBN 9781450328630,
[Link](https://doi.org/10.1145/2597073.2597082 ""),
[Document](https://dx.doi.org/10.1145/2597073.2597082 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[56\]A. Li, M. Liu, Z. Chen, Z. Pei, Z. Li, D. Dai, Y. Wang, and Z. Zheng (2025)Knowledge matters: injecting project and testing knowledge into llm-based unit test generation.
arXiv preprint arXiv:2511.14224.
Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[57\]Z. Zheng, K. Ning, Y. Wang, J. Zhang, D. Zheng, M. Ye, and J. Chen (2024)A survey of large language models for code: evolution, benchmarking, and future trends.
External Links: 2311.10372,
[Link](https://arxiv.org/abs/2311.10372 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[58\]Z. Zheng, K. Ning, Q. Zhong, J. Chen, W. Chen, L. Guo, W. Wang, and Y. Wang (2024)Towards an understanding of large language models in software engineering tasks.
External Links: 2308.11396,
[Link](https://arxiv.org/abs/2308.11396 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[59\]G. Duan, M. Liu, Y. Wang, C. Wang, X. Peng, and Z. Zheng (2025)A hierarchical and evolvable benchmark for fine-grained code instruction following with multi-turn feedback.
External Links: 2507.00699,
[Link](https://arxiv.org/abs/2507.00699 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[60\]K. Yu, Z. Zhou, J. Zeng, Y. Wang, X. Du, Z. Yuan, J. Liu, Z. Zhou, Y. Wang, C. Wang, and X. Peng (2026)Does pass rate tell the whole story? evaluating design constraint compliance in llm-based issue resolution.
ArXivabs/2604.05955.
External Links: [Link](https://api.semanticscholar.org/CorpusID:287209367 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents"),
[Constraint Extraction](https://arxiv.org/html/2609.04167v1#Sx3.SSx2.SSSx2.p2.1 "Constraint Extraction ‣ Constraint-First Instance Construction ‣ SWE-Gate Benchmark ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[61\]L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, H. Zhang, J. Gonzalez, and I. Stoica (2023)Judging llm-as-a-judge with mt-bench and chatbot arena.
In Advances in Neural Information Processing Systems, A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine (Eds.),
Vol. 36, pp. 46595–46623.
External Links: [Document](https://dx.doi.org/10.52202/075280-2020 ""),
[Link](https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").

- \[62\]P. Wang, L. Li, L. Chen, Z. Cai, D. Zhu, B. Lin, Y. Cao, L. Kong, Q. Liu, T. Liu, and Z. Sui (2024)Large language models are not fair evaluators.
In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.),
Bangkok, Thailand, pp. 9440–9450.
External Links: [Link](https://aclanthology.org/2024.acl-long.511/ ""),
[Document](https://dx.doi.org/10.18653/v1/2024.acl-long.511 "")Cited by: [Related Work](https://arxiv.org/html/2609.04167v1#Sx2.p3.1 "Related Work ‣ SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents").