Title:

Content selection saved. Describe the issue below:

Description:

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2609.04180v1 \[cs.CL\] 03 Sep 2026

# Knowledge Acquisition During Pre-training?   Large Language Models Learn Better With Auxiliary Views

Joseph Lee
Yidi Huang
Dokyoon Kim
Shu Yang
††thanks: Corresponding authorsLi Shen††footnotemark: Affiliation: University of Pennsylvania, Philadelphia, PA, USA
Email: [jiosephlee@gmail.com](mailto:)Email: [{yidi.huang,dokyoon.kim,shu.yang,li.shen}@pennmedicine.upenn.edu](mailto:)

###### Abstract

Gaps remain in our understanding of how large language models (LLMs) acquire knowledge during pre-training. We posit that auxiliary views, reformulations of knowledge, are causally helpful for learning. We design controlled experiments to isolate this. First, we confirm that repetition is necessary for acquisition and clarify that paraphrasing helps only at smaller batch sizes. Second, holding the token budget fixed, allocating tokens from document repetition to auxiliary views improves learning, counterintuitively, even for factual recall. Third, the effectiveness of auxiliary views is not contingent on the strength of the teacher model that generates them. Fourth, we identify forms of knowledge, contextual and foundational, that aid learning in the presence of prior knowledge gaps. Finally, we examine how these effects manifest mechanistically via layer-wise biases and compression. Together, our findings suggest that auxiliary representations of knowledge, which arise naturally in large pre-training corpora, are a key factor in the success of pre-training and offer a plausible explanation for why data diversity matters.

## 1 Introduction

Various aspects of data have been shown to be important in pre-training, including deduplication ( [Raffel et al., 2020](https://arxiv.org/html/2609.04180v1#bib.bib30 ""); [Lee et al., 2021](https://arxiv.org/html/2609.04180v1#bib.bib5 ""); [Zhang et al., 2022](https://arxiv.org/html/2609.04180v1#bib.bib37 "")), filtering ( [Weber et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib38 ""); [Li et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib39 "")), coverage and depth ( [Kandpal et al., 2023](https://arxiv.org/html/2609.04180v1#bib.bib28 "")), quality ( [Gunasekar et al., 2023](https://arxiv.org/html/2609.04180v1#bib.bib24 ""); [Longpre et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib35 "")), and diversity ( [Chen et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib36 ""); [Zhang et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib2 "")). However, these insights concern corpus characteristics, overlooking a fundamental question: how should knowledge be represented?

The complexity of this question can vary. For atomic facts like biographical attributes, representation is relatively trivial. But for complex domains such as biomedicine or law, where knowledge is multifaceted and interdependent, formulation is far less obvious. This is becoming relevant as researchers adapt LLMs to specialized domains via continued pre-training ( [Bai et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib18 ""); [Sellergren et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib19 ""); [Wang et al., 2025a](https://arxiv.org/html/2609.04180v1#bib.bib20 ""); [Luo et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib21 ""); [Colombo et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib22 ""); [Singhal et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib23 "")).

Figure 1: Three training mixes on OLMo-2-32B: Source, Para. 9, and Para. 9 + Aux. Across all metrics, paraphrases improve over source-only training, and auxiliary views yield substantially greater improvements. See Section [4](https://arxiv.org/html/2609.04180v1#S4 "4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") for full results.

Thus, for our experiments, we collect recent arXiv papers, legal opinions, and medical case studies to serve as self-contained domain knowledge. We continue pre-training on these texts and related formulations, to study the acquisition of complex knowledge that builds upon the LLM’s existing knowledge. In this setting, we study two research questions:

RQ 1: How should knowledge be represented in natural language?

RQ 2: What surrounding knowledge should be represented alongside it?

Our experiments reveal four main findings. (1) Acquisition of new knowledge benefits from repetition, and paraphrasing further helps, but the benefits of paraphrasing diminish at larger batch sizes. (2) Holding the token budget fixed, allocating tokens from document repetition to auxiliary views improves understanding and factual recall, inducing a distinct layer-wise bias and compression in how knowledge is encoded. (3) Furthermore, the effectiveness of these auxiliary views is not contingent on the strength of the teacher model that generates them. (4) Lastly, contextual and prerequisite knowledge aid learning in the presence of prior knowledge gaps.

Together, these results lead us to a central conjecture: during pre-training, LLMs benefit from auxiliary views (a web of explanations, analogies, and reformulations that humans generate as they learn and teach each other) and acquire a more generalizable encoding of knowledge. Conceptually diverse views, not just linguistically, of the same knowledge improves learning: broader conceptual understanding facilitates the memorization of specific facts better than brute memorization. Moreover, this ability emerges more strongly with scale: larger models learn better by integrating diverse views more effectively, encoding them with greater parameter efficiency and redistributing learning toward the middle and final layers.

Our findings provide a more operational account of what “diverse” data can mean in pre-training. Rather than treating diversity solely as a corpus-level property, diversity can be constructed around individual knowledge, through complementary views that help models form richer and more efficient representations. This offers principles for synthetic pre-training, especially in low-data domains, and explains why “diverse” data is helpful.

## 2 Related Works

Pre-training. Model size and data scale are the primary determinants of LLM capabilities ( [Brown et al., 2020](https://arxiv.org/html/2609.04180v1#bib.bib25 ""); [Kaplan et al., 2020](https://arxiv.org/html/2609.04180v1#bib.bib26 ""); [Carlini et al., 2023](https://arxiv.org/html/2609.04180v1#bib.bib16 ""); [Tirumala et al., 2022](https://arxiv.org/html/2609.04180v1#bib.bib29 ""); [Hoffmann et al., 2022](https://arxiv.org/html/2609.04180v1#bib.bib27 "")). The large-scale nature of pre-training has made the exact role of data difficult to understand. Existing studies, varying in corpora and models, often yield conflicting findings. Even the role of data repetition remains debated ( [Lee et al., 2021](https://arxiv.org/html/2609.04180v1#bib.bib5 ""); [Taylor et al., 2022](https://arxiv.org/html/2609.04180v1#bib.bib15 ""); [Hernandez et al., 2022](https://arxiv.org/html/2609.04180v1#bib.bib14 ""); [Xue et al., 2023](https://arxiv.org/html/2609.04180v1#bib.bib12 ""); [Muennighoff et al., 2023](https://arxiv.org/html/2609.04180v1#bib.bib13 "")).

Knowledge Acquisition during Pre-training. We therefore build upon previous efforts that study how pre-training instills knowledge in a controlled manner. [Allen-Zhu and Li (2024)](https://arxiv.org/html/2609.04180v1#bib.bib10 "") show that paraphrased augmentation increases the memorization of biographical facts from 9.7% to 96.6%. They find that inserting QAs about facts during pre-training increases memorization of held-out facts, whereas inserting QAs during instruction tuning does not. This strongly suggests the importance of data formulation in pre-training.

Further, [Chang et al. (2024)](https://arxiv.org/html/2609.04180v1#bib.bib17 "") intermittently injects fictional facts during pre-training, observing that knowledge is acquired incrementally upon each exposure and subject to decay, suggesting a gradual, not emergent, learning process. Confounding factors are controlled to clearly isolate the effect.

A limitation of these prior works is that [Chang et al. (2024)](https://arxiv.org/html/2609.04180v1#bib.bib17 "") and [Allen-Zhu and Li (2024)](https://arxiv.org/html/2609.04180v1#bib.bib10 "") only use biographical facts; they also provide conflicting views on the benefits of paraphrasing. We focus on complex knowledge and offer an explanation for these reported differences.

Domain Adaptation via Continued Pre-training.
Teaching large language models (LLMs) a specific set of new knowledge via continued pre-training is difficult
( [Wang et al., 2021](https://arxiv.org/html/2609.04180v1#bib.bib7 ""); [Jang et al., 2021](https://arxiv.org/html/2609.04180v1#bib.bib8 ""); [Hu et al., 2023](https://arxiv.org/html/2609.04180v1#bib.bib9 ""); [Ovadia et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib4 ""); [Hoffbauer et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib6 "")). For instance, a 70B model continually pretrained on Wiki-style documents, despite sophisticated augmentation, only recalls 62.7% of facts ( [Jiang et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib11 "")). In practice, continued pre-training is adopted to varying degrees. For example, MedGemma ( [Sellergren et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib19 "")) and TxGemma ( [Wang et al., 2025a](https://arxiv.org/html/2609.04180v1#bib.bib20 "")) do not perform any text-based continued pre-training, while Intern-S1 ( [Bai et al., 2025](https://arxiv.org/html/2609.04180v1#bib.bib18 "")) does so for 5 trillion tokens. Thus, our study aims to provide practical takeaways that can make continued pre-training more reliable.

| Blog. Direct Preference Optimization (DPO) offers a neat change of perspective. Instead of treating reward modeling and policy optimization as separate steps, DPO re-parameterizes the reward class so \[…\] has a closed form. That lets you fit the policy directly to human comparisons with a simple classification loss — no RL required. |
| --- |
| Stack Exchange.Q: How exactly does the partition function cancel out in the DPO derivation? They say the partition function term β​log⁡Z​(x)\\beta\\log Z(x) cancels — can someone show the algebraic steps explicitly? A: Short answer: because the partition function term in the reparameterization depends only on the prompt xx, it is identical for both completions and therefore subtracts out when you form the \[…\] |
| Textbook. The partition function term β​log⁡Z​(x)\\beta\\log Z(x) depends only on xx, so it cancels when forming differences. Preference models like Bradley–Terry depend only on reward differences, not on absolute reward values. Therefore the unknown normalization that made reward recovery hard is irrelevant to the likelihood of observed pairwise comparisons. This is precisely why we can reparameterize rewards in terms of \[…\] |

Table 1: We rewrite each document into three genres while preserving the underlying knowledge. The excerpts above illustrate an accessible, narrative blog; a question-and-answer Stack Exchange entry; and a formal textbook exposition.

| Original sentence | The added constraint is important, as it prevents the model from deviating too far from the distribution \[…\], as well as maintaining the generation diversity and \[…\] |
| --- | --- |
| Factual probe | In the paper “Direct Preference Optimization \[…\],” the authors state that the added constraint in the reinforcement learning objective not only prevents the model from deviating too far from the distribution on which the reward model is accurate, but also maintainsthe generation diversity. |
| Support sentences | \[…\] still expensive to estimate the partition functionZ⁡(x)Z(x) \[…\] the Bradley-Terry model depends only on the difference of rewards \[…\] Substituting the reparameterization \[…\] into the preference model, the partition function cancels, and we can express the human preference probability in terms of only the optimal policy π∗\\pi^{\*} and reference policy \[…\] |
| Inference probe | According to the paper “Direct Preference Optimization \[…\],” the expensive quantity from the optimal-policy form that becomes unnecessary to estimate once DPO rewrites the Bradley–Terry preference model in terms of policies is the partition function. |

Table 2: The factual probe extracts questions from knowledge-bearing sentences, converts them into statements with answers at the end, and adds context. The inference probe combines knowledge from one or more support sentences to infer information not explicitly stated. Here, it integrates the facts that Z⁡(x)Z(x) is expensive to estimate, that the Bradley–Terry model depends only on reward differences, and that the reparameterization causes Z⁡(x)Z(x) to cancel, thereby identifying the partition function as the quantity that no longer requires estimation. The target span of each probe is bolded.

## 3 Experimental Setup

Problem Formulation.
The pre-training objective for an autoregressive LM, ff parameterized by θ\\theta, is next-token prediction.
Given a corpus CC of documents d1,…,dM{d\_{1},\\dots,d\_{M}}, each a sequence of tokens (tm,1,…,tm,nm)(t\_{m,1},\\dots,t\_{m,n\_{m}}),
we minimize the loss function:

|     |     |     |     |
| --- | --- | --- | --- |
|  | L(θ)=−∑m=1M∑i=1nmlogP(tm,i∣tm,<i;θ)L(\\theta)=-\\sum\_{m=1}^{M}\\sum\_{i=1}^{n\_{m}}\\log P(t\_{m,i}\\mid t\_{m,<i};\\theta) |  | (1) |

We denote knowledge abstractly as KK, accessible through the sub-corpus 𝒞K={di∈𝒞∣di​ contains information about ​K}\\mathcal{C}\_{K}=\\{\\,d\_{i}\\in\\mathcal{C}\\mid d\_{i}\\text{ contains information about }K\\,\\}. Because KK is acquired only through next-token prediction over 𝒞K\\mathcal{C}\_{K}, the selection of tokens should matter. This motivates our central question: how should knowledge be represented in text, or specifically how should we construct documents d∈𝒞Kd\\in\\mathcal{C}\_{K} to better learn KK?

Observation. Knowledge is rarely represented once in a corpus. Consider “Attention Is All You Need” ( [Vaswani et al., 2017](https://arxiv.org/html/2609.04180v1#bib.bib44 "")). This document is followed by a proliferation of others conveying the same knowledge: tutorials, blogs with intuitive explanations, and forums answering questions. Such texts are natural byproducts of society’s collective effort to communicate and process knowledge.

We term such manifestations of the same knowledge auxiliary views. We make this distinction because human-generated views are rarely paraphrases: they discuss the knowledge in diverse contexts (e.g., Transformers’ advantages over other architectures) and forms (e.g., blogs, forums), collectively providing a more complete, contextualized picture of KK. We suspect pre-training is replete with these views, explaining its effectiveness beyond vague axes like quality or diversity. In our study, we frame paraphrasing as linguistic variation of a single view and set it as the control.

We also investigate the knowledge represented around KK. To acquire KK, a model may need prior knowledge it does not yet possess. We examine two types: contextual knowledge, which KK references, and prerequisite knowledge, the foundational concepts that KK presupposes.

### 3.1 Dataset

Documents.
We collect 36 documents across three domains to serve as KK: twelve computer science papers from arXiv, twelve legal opinions from U.S. federal appellate courts, and twelve medical case reports from PubMed Central. To prevent leakage from OLMo-2’s pre-training corpus, we select documents published after the cutoff date and verify their absence through the Infini-gram API ( [Liu et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib3 "")). Additional details are in Appendix [A](https://arxiv.org/html/2609.04180v1#A1 "Appendix A Data ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

Views. For each document, we synthetically generate auxiliary views via LLMs. Inspired by our earlier observation and prior work ( [Gunasekar et al., 2023](https://arxiv.org/html/2609.04180v1#bib.bib24 ""); [Allen-Zhu and Li, 2024](https://arxiv.org/html/2609.04180v1#bib.bib10 ""); [Jiang et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib11 "")), we construct textbooks, Stack Exchange–style Q&A, and blogs (Table [1](https://arxiv.org/html/2609.04180v1#S2.T1 "Table 1 ‣ 2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). Prerequisite knowledge is also generated as textbooks. Contextual knowledge is collected as cited arXiv papers and cited judicial opinions; medical case reports lack a citation structure, so we omit this domain. Paraphrases are generated with GPT-4.1, while auxiliary and prerequisite views are generated with GPT-5-mini. Details on data collection, preprocessing, and prompts are in Appendix [A](https://arxiv.org/html/2609.04180v1#A1 "Appendix A Data ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

Probes. To measure learning, we adopt LAMA-style probes ( [Petroni et al., 2019](https://arxiv.org/html/2609.04180v1#bib.bib32 ""); [Jiang et al., 2020](https://arxiv.org/html/2609.04180v1#bib.bib33 ""); [Zhong et al., 2021](https://arxiv.org/html/2609.04180v1#bib.bib34 "")), where the task is to predict a sentence’s final word or, following [Chang et al. (2024)](https://arxiv.org/html/2609.04180v1#bib.bib17 ""), a multi-word target. We design two probe types (Table [2](https://arxiv.org/html/2609.04180v1#S2.T2 "Table 2 ‣ 2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")): factual probes, which measure recall of information stated explicitly in the text, and inference probes, which require combining one or more facts to infer information not stated.

To construct factual probes, we filter for knowledge-bearing sentences, generate QA pairs from each, and convert them into self-contained cloze statements; we automate this with GPT-5.4, having verified that it adequately understands the documents. The pipeline yields 6,435 factual and 430 inference probes, along with multiple-choice variants (4,515 factual and 322 inference MCQs), exceeding the scale of prior work ( [Chang et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib17 "")). We manually validate 200 probes of each type. Full pipeline details are in Appendix [F](https://arxiv.org/html/2609.04180v1#A6 "Appendix F Prompts for Probe Construction (arXiv) ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"). Our dataset111 [https://huggingface.co/datasets/jiosephlee/auxiliary-views-knowledge-acquisition](https://huggingface.co/datasets/jiosephlee/auxiliary-views-knowledge-acquisition "") and code222 [https://github.com/jiosephlee/auxiliary-views-knowledge-acquisition](https://github.com/jiosephlee/auxiliary-views-knowledge-acquisition "") are publicly available.

### 3.2 Training Setup

We use the base OLMo-2 models (1B, 7B, 13B, and 32B) ( [OLMo et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib31 "")) for training. Following [Chang et al. (2024)](https://arxiv.org/html/2609.04180v1#bib.bib17 ""), we employ single-batch knowledge injection: the documents fit in one forward pass, and the rest of the batch is filled with general data. We perform N=100N=100 injections in our main experiments. In Source, the original document is injected every batch. In Para. M, we cycle through the original document and its MM paraphrases, repeating NM+1\\frac{N}{M+1} times. In Para. M + Aux., auxiliary views are injected alongside the paraphrased documents, with a blog, textbook chapter, and Stack Exchange Q&A inserted into every batch.

To remove the number of knowledge-bearing tokens as a confound, we token-match all conditions: since Para. M + Aux. introduces additional knowledge-bearing tokens, we upsample the chunks in Source and Para. M so that every condition sees the same number of tokens pertaining to KK. Consequently, Para. M + Aux. devotes fewer of its tokens to direct repetitions of the main document. Hyperparameters are in Appendix [E](https://arxiv.org/html/2609.04180v1#A5 "Appendix E Hyperparameters for Replication and Details for Reproduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

General Data. For general data replay, we stream tokens from the DCLM subset ( [Li et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib39 "")) of OLMo-2’s pre-training corpus.

Metrics. We evaluate the model’s performance on our probes throughout training:

- •


Log-Prob.: For cloze probes, we measure the joint log-probability of the target span.

- •


Target Rank: We measure the vocabulary rank of the correct target token under teacher forcing. For multi-token targets, we report the worst rank across the span; lower is better.

- •


Multiple-Choice Accuracy: For MCQ probes, we use 5-shot prompting with general-knowledge examples and constrain decoding to the answer choices.


Figure 2: Knowledge acquisition across model sizes under a fixed token budget. Auxiliary views (green) improve both factual recall and inference over Source (blue) and Para. 9 (orange); this advantage grows with model size.

## 4 Large Language Models Learn Better with Auxiliary Views

### 4.1 The Benefit of Auxiliary Views

Better Knowledge Acquisition. In Figure [1](https://arxiv.org/html/2609.04180v1#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), even under a matched token budget, allocating tokens to auxiliary views substantially improves performance on both factual and inference probes. This pattern holds across all of our metrics, including log probability, MCQA, and target rank (Figure [8](https://arxiv.org/html/2609.04180v1#A3.F8 "Figure 8 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). Furthermore, the ordering Para. 9 + Aux.>>Para. 9>>Source is established early during training and holds until convergence, though Source learns faster on factual probes for the first ∼\\sim20 steps. We attribute this effect to auxiliary views as all other factors, including data ordering, are held constant. The injected auxiliary views merely replace a portion of the direct views or paraphrases of the source document.

The improvement on inference is intuitive. Although source documents contain sufficient information to answer these probes, they offer only a single perspective. As Table [1](https://arxiv.org/html/2609.04180v1#S2.T1 "Table 1 ‣ 2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") illustrates, auxiliary views reformulate the knowledge in different styles and contexts, offering diverse perspectives on the material. Learning from these views should lead to a more generalizable understanding, whose benefits naturally emerge on inference probes.

Generalization to Factual Recall. Counterintuitively, auxiliary views also improve factual recall, even though every factual target span is a verbatim phrase from the source. One would expect diverting tokens away from source to hinder direct memorization, not help it. This suggests that auxiliary views encourage the model to encode the knowledge in a more generalized manner that, in turn, supports more effective factual recall ( [Spiro, 2017](https://arxiv.org/html/2609.04180v1#bib.bib45 "")); we return to this in Section [4.3](https://arxiv.org/html/2609.04180v1#S4.SS3 "4.3 Mechanistic Signatures of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") by examining how this effect emerges mechanistically.

Model Size Effects. The benefit of auxiliary views further emerges with scale. As shown in Figure [2](https://arxiv.org/html/2609.04180v1#S3.F2 "Figure 2 ‣ 3.2 Training Setup ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), the 1B model derives little advantage from them, while the gap over the Source and Para. 9 conditions widens steadily through 7B, 13B, and 32B. This trend is largely consistent across all domains (Figure [7](https://arxiv.org/html/2609.04180v1#A3.F7 "Figure 7 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). We discuss this further in Section [4.3](https://arxiv.org/html/2609.04180v1#S4.SS3 "4.3 Mechanistic Signatures of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") in which larger models appear to unlock an advantage from auxiliary views that smaller models cannot.

Which Auxiliary View? We again token-match every condition. Textbooks, blogs, and Stack Exchange Q&A all perform similarly, with a slight benefit from mixing view types on factual recall (Table [8](https://arxiv.org/html/2609.04180v1#A4.T8 "Table 8 ‣ Appendix D Additional Tables ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). Whether and how each view facilitates learning differently warrants further study.

Measuring Lexical Bias. A possible confounding factor is that the synthetically generated auxiliary views leak our probes, especially for inference probes where the target span, unlike factual probes, need not appear in the source. We address the question of lexical bias, whereby the model might favor particular phrases since auxiliary views and probes were produced by related model families (GPT-5-mini and GPT-5.4, respectively). We measure how often each probe’s target span occurs in the source, paraphrases, and auxiliary views.

Table [3](https://arxiv.org/html/2609.04180v1#S4.T3 "Table 3 ‣ 4.1 The Benefit of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") reports both frequency and coverage. Across all metrics, auxiliary views contain the target spans less frequently and with lower coverage than either the source or paraphrases. This strengthens our findings: auxiliary views perform better on the probes despite stating the targets less often.

Table 3: Frequency and coverage of our probe targets across documents. Freq. = occurrences per 1k tokens; Cover. = fraction of targets present at least once across the documents. Para. 49 averages Freq. over 49 paraphrased documents, while coverage records presence in any paraphrase.

| Probes | Corpus | Full target | Bigram |
| --- | --- | --- | --- |
|  |  | Freq. | Cover. | Freq. | Cover. |
| --- | --- | --- | --- | --- | --- |
| Factual | Source | 0.391 | 0.70 | 0.829 | 0.92 |
| Para. 49 | 0.222 | 0.60 | 0.681 | 0.91 |
| Aux. | 0.112 | 0.33 | 0.437 | 0.74 |
| Inference | Source | 1.225 | 0.51 | 0.703 | 0.71 |
| Para. 49 | 1.111 | 0.56 | 0.605 | 0.78 |
| Aux. | 1.070 | 0.51 | 0.628 | 0.77 |

Controlling for Upsampling.

To test whether the density of duplicates introduced by token-matched upsampling of Source and Para. 9 explains some of the gap, we reduce the degree of upsampling. At scale 0.5, the inserted auxiliary-view budget and the matching upsampling are both halved. In the no-upsampling regime, Source and Para. 9 receive no upsampling at all; auxiliary views instead directly replace the document budget so that it sees the source document far less. We report each metric’s peak over the 100-step training window to reduce any disadvantage to the Source baseline from overfitting. The gap narrows, but auxiliary views retain their advantage in both regimes (Table [4](https://arxiv.org/html/2609.04180v1#S4.T4 "Table 4 ‣ 4.1 The Benefit of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). More importantly, Source never improves as duplication is reduced; its accuracy only declines. Thus, repetition helps, but reallocating that token budget to auxiliary views is more effective.

| Matching | Condition | Factual | Inference |
| --- | --- | --- | --- |
| regime |  | MCQA | MCQA |
| --- | --- | --- | --- |
| 0.5 | Source | 0.382 | 0.444 |
| Para. 9 | 0.399 | 0.435 |
| Auxiliary views | 0.412 | 0.450 |
| No upsampling | Source | 0.380 | 0.421 |
| Para. 9 | 0.389 | 0.415 |
| Auxiliary views | 0.392 | 0.424 |

Table 4: Token-matching upsampling. Peak MCQA accuracy when matching upsampling is halved or removed; in the latter, auxiliary views partially replace the original documents instead of upsampling source to match. Auxiliary views retain their advantage, and Source never improves with less duplication.

### 4.2 Broader Generalization

Our findings generalize to a pre-training, human-written views, and another model family.

A Pre-training-Faithful Setting. Our experiments so far use continued pre-training with a new learning-rate schedule and a smaller batch size. These choices may affect whether our findings generalize to the original pre-training regime. We therefore replicate our experiment in a pre-training-faithful setup and obtain the same ordering (Table [5](https://arxiv.org/html/2609.04180v1#S4.T5 "Table 5 ‣ 4.2 Broader Generalization ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"); full setup details in Appendix [E](https://arxiv.org/html/2609.04180v1#A5 "Appendix E Hyperparameters for Replication and Details for Reproduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")).

| Condition | Fact. | Fact. | Inf. | Inf. |
| --- | --- | --- | --- | --- |
|  | log prob. | MCQA | log prob. | MCQA |
| --- | --- | --- | --- | --- |
| Pretrained model | -16.30 | 0.343 | -14.79 | 0.413 |
| Source (token-matched) | -10.00 | 0.372 | -12.85 | 0.421 |
| Para. 9 (token-matched) | -10.33 | 0.375 | -12.53 | 0.417 |
| Auxiliary views | -9.56 | 0.403 | -10.82 | 0.492 |

Table 5: A Pre-training-Faithful Setting. Final metrics after resuming OLMo-2 7B from step 925,000 with its optimizer state, original data stream and schedule, and a global batch size of 1,024. Auxiliary views yield the largest gains.

Human Auxiliary Views. To test whether our findings depend on synthetic text, we repeat the experiment with human-written auxiliary views collected from the open web. The benefit again grows with model size (Figure [3](https://arxiv.org/html/2609.04180v1#S4.F3 "Figure 3 ‣ 4.2 Broader Generalization ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")), mirroring the synthetic-view results. This experiment covers only two documents, so we treat it as suggestive rather than conclusive; nonetheless, it provides initial evidence that the effect is not merely an artifact of clean, synthetic text.

Figure 3: With human-written auxiliary views collected from the open web, the benefit grows with model size, consistent with our synthetic results. Δ\\Delta final log prob. is the difference between training with human auxiliary views and the Para. 9 condition. Results are averaged over two documents.

Beyond OLMo-2. We repeat the main experiment on Qwen-2.5-7B, and auxiliary views again yield the largest gains (Table [11](https://arxiv.org/html/2609.04180v1#A4.T11 "Table 11 ‣ Appendix D Additional Tables ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")).

### 4.3 Mechanistic Signatures of Auxiliary Views

![Refer to caption](https://arxiv.org/html/2609.04180v1/aux_base_minus_source_base_cosine_distance_all_projections.png)Figure 4: Per-channel difference (Para. 9 + Aux. minus Source) in cosine distance from the base model across layers and FFN channels (gate, up, and down projections). Red indicates channels that auxiliary views move more than source; blue indicates less movement. A negative band around layers 16–24 shows that auxiliary views change the upper-middle layers less than source while affecting the middle and final layers more.

Having established that auxiliary views improve knowledge acquisition, we ask how this phenomenon emerges mechanistically. We compare each trained model’s feed-forward network (FFN) weights against the base model along two axes: the magnitude of change (relative delta norm and cosine distance) and its concentration across channels (Gini coefficient), measured per layer and over training (Figures [10](https://arxiv.org/html/2609.04180v1#A3.F10 "Figure 10 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") and [9](https://arxiv.org/html/2609.04180v1#A3.F9 "Figure 9 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")).

Why MLP Channels? We focus our analysis on the feed-forward (MLP) layers for two reasons. First, they account for the majority of a transformer’s parameters, making them the natural locus for studying where knowledge is written during training. Second, they have comparatively clean interpretations: [Geva et al. (2021)](https://arxiv.org/html/2609.04180v1#bib.bib40 "") show that individual channels in FFN layers operate as key–value memories. This channel-level view lets us read parameter change as movement in the model’s memory rather than as an opaque aggregate.

Compression: Learning More by Changing Less. Based on Figure [9](https://arxiv.org/html/2609.04180v1#A3.F9 "Figure 9 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), paraphrasing induces the largest parameter movement of the three conditions, in both norm and cosine distance, yet adding auxiliary views reduces this magnitude, though still more than source-only training. We interpret this as evidence that the two conditions learn differently. Paraphrasing supplies many surface-level variants of a single view, and the model appears to expend parameter change absorbing this lexical variation. Auxiliary views instead supply the knowledge in genuinely distinct framings, which the model can apparently integrate with less weight movement. This is consistent with our conjecture that auxiliary views enable a more generalizable encoding of knowledge: forming a more general, reusable representation requires overwriting fewer parameters than memorizing surface forms. Magnitude of change is not the same as quality of learning.

Layer-wise Biases. Parameter change is not uniform across layers. All conditions concentrate change in the middle and final layers, with a pronounced dip in the upper-middle layers (Figure [10](https://arxiv.org/html/2609.04180v1#A3.F10 "Figure 10 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). Auxiliary views accentuate this structure. Relative to source-only training, training with auxiliary views changes the middle and final layers more, but changes less in the upper-middle band (layers ∼\\sim16–24). Figure [4](https://arxiv.org/html/2609.04180v1#S4.F4 "Figure 4 ‣ 4.3 Mechanistic Signatures of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") makes this bias visible: the delta in cosine distance (Para. 9 + Aux.−-Source) is negative in a band around layers 16–24 and positive elsewhere. Auxiliary views do not move more weight everywhere; they redistribute where learning occurs.

Model Size Effects. At 1B, where auxiliary views confer little benefit (Figure [2](https://arxiv.org/html/2609.04180v1#S3.F2 "Figure 2 ‣ 3.2 Training Setup ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")), the corresponding per-channel difference is almost uniformly negative or zero across all layers and projections (Figure [11](https://arxiv.org/html/2609.04180v1#A3.F11 "Figure 11 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")), lacking the layer-wise biases seen at 7B. The mechanistic signature of auxiliary views therefore emerges only at scale. This suggests that larger models encode auxiliary views differently, enabling greater generalization.

Figure 5: (Left) Inference-probe log probability while training OLMo-2-7B with a batch size of 64 on Source versus Para. 9. (Right) Final probe log probabilities for Source versus Para. 9 across model sizes and batch sizes. This experiment uses six documents to examine dynamics at smaller batch sizes.

## 5 Auxiliary Views Do Not Require a Strong Teacher

Auxiliary views inherently require a teacher: someone who understands the material and can communicate it to others. Naturally, our results could hinge on the generator’s strength, although our auxiliary text is generated by a relatively weak model, gpt-5-mini. To examine the influence of the teacher’s capabilities, we regenerate auxiliary views using eleven generator configurations spanning multiple model families, reasoning-effort levels, and sizes, while holding the training schedule and token budget fixed. Because generators that produce less auxiliary-view text require more repetition to match the token budget and may therefore overfit, we compare each at its peak over the 100-step training window.

Downstream factual accuracy is remarkably stable across generators (0.405–0.422, all above the Para. 9 baseline of 0.396; Table [13](https://arxiv.org/html/2609.04180v1#A4.T13 "Table 13 ‣ Appendix D Additional Tables ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). It is uncorrelated with generator size (Pearson r=−0.14r=-0.14, n=6n=6), as further corroborated by scaling within a model family (gpt-oss-20B→\\rightarrow120B: 0.422→\\rightarrow0.413; Gemma-4 12B→\\rightarrow31B: 0.414→\\rightarrow0.405), and likewise uncorrelated with the generator’s own factual accuracy (r=−0.24r=-0.24, n=10n=10, p=0.50p=0.50). Notably, gpt-oss-20B has the least measured domain knowledge, yet its views teach best.

However, the volume of generated view text, which does not measure teacher strength and can be controlled through prompting, does correlate with downstream accuracy (r=+0.62r=+0.62, p≈0.04p\\approx 0.04). Varying the reasoning effort of the same generator likewise leaves downstream performance essentially unchanged, even though it changes the generator’s own accuracy. Together, these results suggest that auxiliary views function as general data augmentation rather than as distillation from a strong teacher. The generator need only reformulate the provided text; stronger models do not necessarily perform better at this task, even in complex domains.

## 6 When Does Paraphrasing Help?

Paraphrasing is known to aid knowledge acquisition ( [Ovadia et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib4 "")), but prior reports conflict on its effectiveness. We revisit this question to show that its benefit is conditional, and in doing so reconcile these reports.

Paraphrasing prevents collapse. Repeated exposure improves performance only up to ∼\\sim20 exposures, after which Source saturates and then sharply degrades as the model overfits (Figure [5](https://arxiv.org/html/2609.04180v1#S4.F5 "Figure 5 ‣ 4.3 Mechanistic Signatures of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), left). Para. 9 prevents this collapse, sustaining improvement through ∼\\sim40 exposures. As with auxiliary views, this benefit emerges only at 7B and above; at 1B, paraphrasing is slightly harmful.

The benefit depends on batch size. However, we see that this advantage depends on batch size, likely because larger batches mix in more general data per step and this similarly suppresses overfitting. As batch size grows, Source becomes more stable and nearly matches Para. 9 by batch size 256, while Para. 9 stays roughly flat (Figure [5](https://arxiv.org/html/2609.04180v1#S4.F5 "Figure 5 ‣ 4.3 Mechanistic Signatures of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), rightmost). Paraphrasing’s inference gains thus come from preventing a degeneration that large batches also prevent; together, the two interventions become redundant.

Factual acquisition behaves differently. At small batch sizes, paraphrasing improves factual learning at 7B and above, whereas Source sees almost no gain from larger batches (aside from a small improvement at batch size 64 for 7B). We attribute this advantage to how paraphrasing semantically varies the facts: although factual probes are drawn explicitly from source sentences, they are recast as self-contained atomic statements, so Source’s verbatim memorization transfers less well. The advantage shrinks at larger batches and reverses at batch size 256 (7B and 13B), likely because the increased general-data mixing dilutes the gradient signal from the paraphrased text.

Table [5](https://arxiv.org/html/2609.04180v1#S4.T5 "Table 5 ‣ 4.2 Broader Generalization ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") supports this general interpretation at a batch size of 1,024: paraphrasing provides no consistent improvement over Source, while auxiliary views retain a substantial advantage.

Reconciling Prior Works. This batch-size dependence reconciles conflicting prior work: [Chang et al. (2024)](https://arxiv.org/html/2609.04180v1#bib.bib17 ""), at batch size 2048 with 2048-token chunks, reports degraded factual learning from paraphrasing, whereas [Allen-Zhu and Li (2024)](https://arxiv.org/html/2609.04180v1#bib.bib10 ""), at batch size 96 with 512-token chunks, reports gains. The two sit at opposite ends of the regime we characterize here.

## 7 Prior Knowledge Matters

| Model | Base | CPT |
| --- | --- | --- |
| OLMo-2-0425-1B | 0.4380 | 0.5454 |
| OLMo-2-1124-7B | 0.6859 | 0.7272 |

Table 6: The prior-knowledge gap. MCQA accuracy on prerequisite topics for each document, before (Base) and after (CPT) continued pre-training on synthetic textbooks covering that foundational knowledge.

Prior-Knowledge Gap. We first establish that the model lacks some of the foundational knowledge KK presupposes. We generate MCQA pairs on prerequisite topics for each document and measure the base model’s accuracy. As shown in Table [6](https://arxiv.org/html/2609.04180v1#S7.T6 "Table 6 ‣ 7 Prior Knowledge Matters ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), accuracy on this benchmark improves after continued pre-training on synthetic textbooks covering this material, confirming a gap that domain adaptation must contend with. Recent work has studied how such gaps shape learning ( [Wang et al., 2025b](https://arxiv.org/html/2609.04180v1#bib.bib41 ""); [Gekhman et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib42 ""); [Yang et al., 2024](https://arxiv.org/html/2609.04180v1#bib.bib43 "")), but the question remains open.

Complementary Benefits. Table [9](https://arxiv.org/html/2609.04180v1#A4.T9 "Table 9 ‣ Appendix D Additional Tables ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") reports the peak improvement over each run’s pretrained baseline. Relative to standard Para. 9, providing either contextual or prerequisite knowledge substantially improves acquisition. Under the stricter token-matched comparison, adding surrounding knowledge does not consistently surpass Para. 9. This is unsurprising; because contextual knowledge is largely tangential to the target material, allocating a fixed token budget to variations of the target knowledge should be more effective. Nevertheless, surrounding knowledge yields improvements comparable to adding paraphrases, which is a meaningful benefit. Furthermore, the two knowledge types exhibit distinct strengths: contextual knowledge drives larger factual gains across both domains, whereas prerequisite knowledge yields greater improvements in inference.

To ask whether these differences reflect surface overlap, we measure how often each probe’s target span appears in the inserted texts (Table [12](https://arxiv.org/html/2609.04180v1#A4.T12 "Table 12 ‣ Appendix D Additional Tables ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")). Cited works include factual targets about twice as often as prerequisite textbooks, so contextual knowledge’s relative factual advantage may partly reflect lexical presence. However, lexical overlap cannot explain the inference result: prerequisite knowledge contains the inference targets no more often than contextual knowledge, with lower bigram frequency, yet yields the larger inference improvement. This is consistent with prerequisite knowledge supplying foundations that support integration and inference.

## 8 Ablations

Learning Rate. Across our experiments, we use a fixed peak learning rate of 4e-5. Following [Parmar et al. (2024)](https://arxiv.org/html/2609.04180v1#bib.bib1 ""), however, continued-pre-training recipes should inherit the base model’s pre-training learning rate, and the 13B and 32B models were pre-trained at higher rates (9e-5 and 6e-5) than the 7B model (3e-5) [OLMo et al. (2024)](https://arxiv.org/html/2609.04180v1#bib.bib31 ""). Because learning rate strongly governs how much is learned, holding it fixed at 4e-5 may have caused us to underestimate the model-size effect and the overall effects of auxiliary views and paraphrasing. Consistent with this interpretation, the analysis in Figure [12](https://arxiv.org/html/2609.04180v1#A3.F12 "Figure 12 ‣ Appendix C Additional Plots ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") shows that the advantages of auxiliary views and paraphrasing over source-only training widen as the learning rate increases.

Order of Prior Knowledge. We vary whether prerequisite data appears at the beginning, middle, or end of training. No placement is consistently best across metrics (Table [10](https://arxiv.org/html/2609.04180v1#A4.T10 "Table 10 ‣ Appendix D Additional Tables ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views")), and the differences are small. We leave a fuller investigation of curriculum effects to future work.

## 9 Discussion & Conclusion

Auxiliary Views. To our knowledge, we are the first to isolate the significance of auxiliary views. The premise is intuitive: data augmentation can help, and diversity is an established principle in pre-training. However, diversity remains an underspecified principle that is difficult to operationalize when constructing data from scratch amid data scarcity. This motivates a clearer account of how variation improves learning and why.

Our study uncovers a phenomenon in which conceptual reformulations of a document, whether as a textbook or a blog, have an effect starkly distinct from mere paraphrasing: they substantially improve learning and induce a distinct layer-wise bias and compression in how knowledge is encoded. More strikingly, they improve factual recall even though the model sees the original document, from which our probes are constructed, less frequently. This points to an underlying effect: a model’s broader conceptual understanding directly facilitates its ability to memorize specific facts.

Furthermore, the model’s ability to encode auxiliary views effectively emerges only in our larger models and grows with model size. Larger models learn better by integrating diverse views more effectively, encoding them with greater parameter efficiency by moving fewer weights and redistributing learning toward the middle and final layers. Together, these results help explain the effectiveness of pre-training corpora beyond simple scale and provide a clearer mechanism for the commonly invoked notion of “good” and “diverse” data.

Practical Takeaways. We offer three recommendations for practitioners engaged in domain adaptation: (1) continue pre-training on prerequisite knowledge to close foundational gaps (2) apply paraphrasing when data is scarce, while recognizing that its benefit diminishes as batch size grows (3) and consider synthetic augmentation with auxiliary views.

We find the last point especially relevant for scientific domains. Open scientific corpora are constantly evolving, producing research that lacks the auxiliary views which surrounds established knowledge. Our results show that synthesizing such views is helpful for acquiring knowledge effectively. However, whether this remains effective for specialized, long-tailed knowledge for which LLMs may lack the expertise to generate high-quality auxiliary views remains an open question.

While the scope of this study may limit its generalizability, we hope these insights prove valuable to practitioners in domain adaptation, encourage greater consideration of how knowledge is represented, and provoke deeper discussion of the mechanisms of knowledge acquisition in LLMs.

## Acknowledgements

This work was supported in part by seed funding from the PSOM AI2D Center at Penn.

## Limitations

Our analysis is restricted to three domains, which may introduce corpus-level biases. While our main results regarding auxiliary views were consistent across each domain, this is not the case for our secondary results regarding contextual and prerequisite knowledge. We acknowledge that this limits the generalization of our findings.

Furthermore, the contextual-knowledge experiment covers only arXiv papers and legal opinions, because medical case reports lack an analogous citation structure. Its results establish different factual and inference biases for contextual and prerequisite knowledge, but not a consistent advantage over token-matched paraphrasing.

Our findings may also have limited generalizability to pre-training proper. While our pre-training-faithful control uses the original optimizer state, learning-rate schedule, and data at a batch size of 1,024, it is a 100-step experiment at a later checkpoint rather than pre-training from scratch.

Furthermore, our investigation of generator strength may not generalize to low-resource, highly specialized domains, where even comprehending the source material may challenge the generator. In such settings, it remains unclear whether teacher-model strength is irrelevant.

Finally, our results are constrained by the scale of the models we study (up to 32B). Because model scale is a primary determinant of LLM capabilities, our findings may not extend to substantially larger models.

## References

- Allen-Zhu and Li (2024)Z. Allen-Zhu and Y. LiPhysics of language models: part 3.1, knowledge storage and extraction.
In International Conference on Machine Learning,
pp. 1067–1077.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p2.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§2](https://arxiv.org/html/2609.04180v1#S2.p4.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p2.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§6](https://arxiv.org/html/2609.04180v1#S6.p6.1 "6 When Does Paraphrasing Help? ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Bai et al. (2025)L. Bai, Z. Cai, M. Cao, W. Cao, C. Chen, H. Chen, K. Chen, P. Chen, Y. Chen, Y. Chen, et al.Intern-s1: a scientific multimodal foundation model.
arXiv preprint arXiv:2508.15763.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p2.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Brown et al. (2020)T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al.Language models are few-shot learners.
Advances in neural information processing systems33, pp. 1877–1901.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Carlini et al. (2023)N. Carlini, D. Ippolito, M. Jagielski, K. Lee, F. Tramer, and C. ZhangQuantifying memorization across neural language models.
In The Eleventh International Conference on Learning Representations,
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Chang et al. (2024)H. Chang, J. Park, S. Ye, S. Yang, Y. Seo, D. Chang, and M. SeoHow do large language models acquire factual knowledge during pretraining?.
Advances in neural information processing systems37, pp. 60626–60668.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p3.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§2](https://arxiv.org/html/2609.04180v1#S2.p4.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p3.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p4.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§3.2](https://arxiv.org/html/2609.04180v1#S3.SS2.p1.1 "3.2 Training Setup ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§6](https://arxiv.org/html/2609.04180v1#S6.p6.1 "6 When Does Paraphrasing Help? ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Chen et al. (2025)Z. Chen, S. Wang, T. Xiao, Y. Wang, S. Chen, X. Cai, J. He, and J. WangRevisiting scaling laws for language models: the role of data quality and training strategies.
In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
pp. 23881–23899.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Colombo et al. (2024)P. Colombo, T. P. Pires, M. Boudiaf, D. Culver, R. Melo, C. Corro, A. F. Martins, F. Esposito, V. L. Raposo, S. Morgado, et al.Saullm-7b: a pioneering large language model for law.
arXiv preprint arXiv:2403.03883.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p2.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Gekhman et al. (2024)Z. Gekhman, G. Yona, R. Aharoni, M. Eyal, A. Feder, R. Reichart, and J. HerzigDoes fine-tuning llms on new knowledge encourage hallucinations?.
In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing,
pp. 7765–7784.
Cited by: [§7](https://arxiv.org/html/2609.04180v1#S7.p1.1 "7 Prior Knowledge Matters ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Geva et al. (2021)M. Geva, R. Schuster, J. Berant, and O. LevyTransformer feed-forward layers are key-value memories.
In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing,
pp. 5484–5495.
Cited by: [§4.3](https://arxiv.org/html/2609.04180v1#S4.SS3.p2.1 "4.3 Mechanistic Signatures of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Gunasekar et al. (2023)S. Gunasekar, Y. Zhang, J. Aneja, C. C. T. Mendes, A. Del Giorno, S. Gopi, M. Javaheripi, P. Kauffmann, G. de Rosa, O. Saarikivi, et al.Textbooks are all you need.
arXiv preprint arXiv:2306.11644.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p2.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Hernandez et al. (2022)D. Hernandez, T. Brown, T. Conerly, N. DasSarma, D. Drain, S. El-Showk, N. Elhage, Z. Hatfield-Dodds, T. Henighan, T. Hume, et al.Scaling laws and interpretability of learning from repeated data.
arXiv preprint arXiv:2205.10487.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Hoffbauer et al. (2024)J. Hoffbauer, S. Sawicki, M. Ulrich, T. Buz, K. Dobler, M. Schneider, and G. De MeloKnowledge acquisition through continued pretraining is difficult: a case study on r/AskHistorians.
In Proceedings of the 1st Workshop on Towards Knowledgeable Language Models (KnowLLM 2024), S. Li, M. Li, M. J. Zhang, E. Choi, M. Geva, P. Hase, and H. Ji (Eds.),
Bangkok, Thailand, pp. 96–108.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Hoffmann et al. (2022)J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai, E. Rutherford, D. de Las Casas, L. A. Hendricks, J. Welbl, A. Clark, et al.Training compute-optimal large language models.
In Proceedings of the 36th International Conference on Neural Information Processing Systems,
pp. 30016–30030.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Hu et al. (2023)N. Hu, E. Mitchell, C. D. Manning, and C. FinnMeta-learning online adaptation of language models.
arXiv preprint arXiv:2305.15076.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Jang et al. (2021)J. Jang, S. Ye, S. Yang, J. Shin, J. Han, G. Kim, S. J. Choi, and M. SeoTowards continual knowledge learning of language models.
arXiv preprint arXiv:2110.03215.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Jiang et al. (2024)Z. Jiang, Z. Sun, W. Shi, P. Rodriguez, C. Zhou, G. Neubig, X. Lin, W. Yih, and S. IyerInstruction-tuned language models are better knowledge learners.
In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p2.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Jiang et al. (2020)Z. Jiang, F. F. Xu, J. Araki, and G. NeubigHow can we know what language models know?.
Transactions of the Association for Computational Linguistics8.
Cited by: [§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p3.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Kandpal et al. (2023)N. Kandpal, H. Deng, A. Roberts, E. Wallace, and C. RaffelLarge language models struggle to learn long-tail knowledge.
In International conference on machine learning,
pp. 15696–15707.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Kaplan et al. (2020)J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D. AmodeiScaling laws for neural language models.
arXiv preprint arXiv:2001.08361.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Lee et al. (2021)K. Lee, D. Ippolito, A. Nystrom, C. Zhang, D. Eck, C. Callison-Burch, and N. CarliniDeduplicating training data makes language models better.
arXiv preprint arXiv:2107.06499.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Li et al. (2024)J. Li, A. Fang, G. Smyrnis, M. Ivgi, M. Jordan, S. Y. Gadre, H. Bansal, E. Guha, S. S. Keh, K. Arora, et al.Datacomp-lm: in search of the next generation of training sets for language models.
Advances in Neural Information Processing Systems37, pp. 14200–14282.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§3.2](https://arxiv.org/html/2609.04180v1#S3.SS2.p3.1 "3.2 Training Setup ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Liu et al. (2024)J. Liu, S. Min, L. Zettlemoyer, Y. Choi, and H. HajishirziInfini-gram: scaling unbounded n-gram language models to a trillion tokens.
arXiv preprint arXiv:2401.17377.
Cited by: [§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p1.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Longpre et al. (2024)S. Longpre, G. Yauney, E. Reif, K. Lee, A. Roberts, B. Zoph, D. Zhou, J. Wei, K. Robinson, D. Mimno, et al.A pretrainer’s guide to training data: measuring the effects of data age, domain coverage, quality, & toxicity.
In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers),
pp. 3245–3276.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Luo et al. (2025)X. Luo, A. Rechardt, G. Sun, K. K. Nejad, F. Yáñez, B. Yilmaz, K. Lee, A. O. Cohen, V. Borghesani, A. Pashkov, et al.Large language models surpass human experts in predicting neuroscience results.
Nature human behaviour9 (2), pp. 305–315.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p2.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Muennighoff et al. (2023)N. Muennighoff, A. Rush, B. Barak, T. Le Scao, N. Tazi, A. Piktus, S. Pyysalo, T. Wolf, and C. A. RaffelScaling data-constrained language models.
Advances in Neural Information Processing Systems36, pp. 50358–50376.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- OLMo et al. (2024)T. OLMo, P. Walsh, L. Soldaini, D. Groeneveld, K. Lo, S. Arora, A. Bhagia, Y. Gu, S. Huang, M. Jordan, et al.2 olmo 2 furious.
arXiv preprint arXiv:2501.00656.
Cited by: [§3.2](https://arxiv.org/html/2609.04180v1#S3.SS2.p1.1 "3.2 Training Setup ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§8](https://arxiv.org/html/2609.04180v1#S8.p1.1 "8 Ablations ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Ovadia et al. (2024)O. Ovadia, M. Brief, M. Mishaeli, and O. ElishaFine-tuning or retrieval? comparing knowledge injection in llms.
In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing,
pp. 237–250.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§6](https://arxiv.org/html/2609.04180v1#S6.p1.1 "6 When Does Paraphrasing Help? ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Parmar et al. (2024)J. Parmar, S. Satheesh, M. Patwary, M. Shoeybi, and B. CatanzaroReuse, don’t retrain: a recipe for continued pretraining of language models.
arXiv preprint arXiv:2407.07263.
Cited by: [§8](https://arxiv.org/html/2609.04180v1#S8.p1.1 "8 Ablations ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Petroni et al. (2019)F. Petroni, T. Rocktäschel, S. Riedel, P. Lewis, A. Bakhtin, Y. Wu, and A. MillerLanguage models as knowledge bases?.
In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), K. Inui, J. Jiang, V. Ng, and X. Wan (Eds.),
Hong Kong, China.
Cited by: [§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p3.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Raffel et al. (2020)C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. LiuExploring the limits of transfer learning with a unified text-to-text transformer.
Journal of machine learning research21 (140), pp. 1–67.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Sellergren et al. (2025)A. Sellergren, S. Kazemzadeh, T. Jaroensri, A. Kiraly, M. Traverse, T. Kohlberger, S. Xu, F. Jamil, C. Hughes, C. Lau, et al.Medgemma technical report.
arXiv preprint arXiv:2507.05201.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p2.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Singhal et al. (2025)K. Singhal, T. Tu, J. Gottweis, R. Sayres, E. Wulczyn, M. Amin, L. Hou, K. Clark, S. R. Pfohl, H. Cole-Lewis, et al.Toward expert-level medical question answering with large language models.
Nature Medicine31 (3), pp. 943–950.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p2.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Spiro (2017)R. J. SpiroRemembering information from text: the "state of schema" approach.
In Schooling and the acquisition of knowledge,
pp. 137–165.
Cited by: [§4.1](https://arxiv.org/html/2609.04180v1#S4.SS1.p3.1 "4.1 The Benefit of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Taylor et al. (2022)R. Taylor, M. Kardas, G. Cucurull, T. Scialom, A. Hartshorn, E. Saravia, A. Poulton, V. Kerkez, and R. StojnicGalactica: a large language model for science.
arXiv preprint arXiv:2211.09085.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Tirumala et al. (2022)K. Tirumala, A. Markosyan, L. Zettlemoyer, and A. AghajanyanMemorization without overfitting: analyzing the training dynamics of large language models.
Advances in Neural Information Processing Systems35, pp. 38274–38290.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Vaswani et al. (2017)A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. PolosukhinAttention is all you need.
Advances in neural information processing systems30.
Cited by: [§3](https://arxiv.org/html/2609.04180v1#S3.p4.1 "3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Wang et al. (2021)C. Wang, P. Liu, and Y. ZhangCan generative pre-trained language models serve as knowledge bases for closed-book qa?.
In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers),
pp. 3241–3251.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Wang et al. (2025a)E. Wang, S. Schmidgall, P. F. Jaeger, F. Zhang, R. Pilgrim, Y. Matias, J. Barral, D. Fleet, and S. AziziTxgemma: efficient and agentic llms for therapeutics.
arXiv preprint arXiv:2504.06196.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p2.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"),
[§2](https://arxiv.org/html/2609.04180v1#S2.p5.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Wang et al. (2025b)Z. Wang, Z. Shi, H. Zhou, S. Gao, Q. Sun, and J. LiTowards objective fine-tuning: how llms’ prior knowledge causes potential poor calibration?.
External Links: 2505.20903Cited by: [§7](https://arxiv.org/html/2609.04180v1#S7.p1.1 "7 Prior Knowledge Matters ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Weber et al. (2024)M. Weber, D. Fu, Q. Anthony, Y. Oren, S. Adams, A. Alexandrov, X. Lyu, H. Nguyen, X. Yao, V. Adams, et al.Redpajama: an open dataset for training large language models.
Advances in neural information processing systems37, pp. 116462–116492.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Xue et al. (2023)F. Xue, Y. Fu, W. Zhou, Z. Zheng, and Y. YouTo repeat or not to repeat: insights from scaling llm under token-crisis.
Advances in Neural Information Processing Systems36, pp. 59304–59322.
Cited by: [§2](https://arxiv.org/html/2609.04180v1#S2.p1.1 "2 Related Works ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Yang et al. (2024)Y. Yang, A. M. Bean, R. McCraith, and A. MahdiFine-tuning large language models with human-inspired learning strategies in medical question answering.
arXiv e-prints, pp. arXiv–2408.
Cited by: [§7](https://arxiv.org/html/2609.04180v1#S7.p1.1 "7 Prior Knowledge Matters ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Zhang et al. (2025)C. Zhang, H. Zhong, K. Zhang, C. Chai, R. Wang, X. Zhuang, T. Bai, Q. Jiantao, L. Cao, J. Fan, et al.Harnessing diversity for important data selection in pretraining large language models.
In International Conference on Learning Representations,
Vol. 2025, pp. 72980–73003.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Zhang et al. (2022)S. Zhang, S. Roller, N. Goyal, M. Artetxe, M. Chen, S. Chen, C. Dewan, M. Diab, X. Li, X. V. Lin, et al.Opt: open pre-trained transformer language models.
arXiv preprint arXiv:2205.01068.
Cited by: [§1](https://arxiv.org/html/2609.04180v1#S1.p1.1 "1 Introduction ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").

- Zhong et al. (2021)Z. Zhong, D. Friedman, and D. ChenFactual probing is \[mask\]: learning vs. learning to recall.
In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies,
pp. 5017–5033.
Cited by: [§3.1](https://arxiv.org/html/2609.04180v1#S3.SS1.p3.1 "3.1 Dataset ‣ 3 Experimental Setup ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views").


## Appendix A Data

### A.1 Dataset Construction

#### Document collection.

The arXiv set was manually collected. For medical documents, we use the NCBI E-utilities API to search PubMed Central for open-access case reports and download JATS XML. For legal documents, we use the CourtListener REST API to search U.S. federal appellate opinions. Across domains, we filter candidate documents to obtain twelve target documents of suitable length, e.g., court opinions longer than 4000 tokens were rejected to avoid awkward chunking.

#### Pre-training corpus check.

We check all 36 source documents against the Infini-gram API. For each document, we query the title and ten randomly sampled body sentences against the OLMo-2 pre-training mixture index, v4\_olmo-mix-1124\_llama, and find zero matches.

#### Cleaning.

For arXiv papers, we clean the raw LaTeX by removing comments, figures, tables, presentation-only commands, unresolved includes, page breaks, and bibliography/appendix material; expanding simple macros; extracting title, abstract, and main body; resolving revision commands; and repairing erroneous line breaks while preserving LaTeX environments. Medical case reports are converted from JATS XML into sectioned plain text. Legal opinions require additional PDF/OCR cleanup: we remove page headers, docket/page artifacts, decorative separators, extracted footnotes, and merge dangling sentences into paragraphs.

#### Contextual Knowledge.

In our study, contextual views are cited works associated with the source document. For arXiv documents, we resolve each paper to an arXiv identifier, retrieve reference metadata using Semantic Scholar and OpenAlex, identify references with arXiv identifiers, download their source packages, and clean them with the same arXiv cleaning procedure. For legal documents, we use CourtListener citation links to collect cited judicial opinions and apply the same legal-opinion cleaning procedure. We do not construct contextual views for medical documents because case reports lack an analogous citation structure in our setup.

### A.2 Synthetic Data Generation

#### Data statistics.

Table [7](https://arxiv.org/html/2609.04180v1#A1.T7 "Table 7 ‣ Data statistics. ‣ A.2 Synthetic Data Generation ‣ Appendix A Data ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views") summarizes the artifacts used in our experiments. We generate 49 paraphrases per source document, yielding 1764 paraphrases in total. For auxiliary views, NN counts the generated units obtained by splitting each view family into per-post blogs, per-question Stack Exchange Q&A, and per-chapter textbooks.

|     |     |     |     |
| --- | --- | --- | --- |
| Material | NN | Avg. Len. (tokens) | Total Tokens |
| Overall |
| Source Documents | 36 | 5858 | 210,888 |
| Paraphrases | 1764 | 6180 | 10,904,160 |
| Blogs | 225 | 1901 | 427,632 |
| Stack Exchange Q&A | 453 | 1290 | 584,392 |
| Textbook Chapters | 282 | 2239 | 631,403 |
| Prerequisite Chapters | 582 | 4282 | 2,492,392 |
| Contextual Documents | 639 | 10416 | 6,655,888 |
| Computer Science |
| Source Documents | 12 | 10550 | 126,598 |
| Paraphrases | 638 | 11002 | 7,019,384 |
| Blogs | 105 | 1920 | 201,648 |
| Stack Exchange Q&A | 242 | 1460 | 353,321 |
| Textbook Chapters | 158 | 2872 | 453,833 |
| Prerequisite Chapters | 187 | 4555 | 851,724 |
| Contextual Documents | 506 | 10791 | 5,460,148 |
| Medical |
| Source Documents | 12 | 3765 | 45,181 |
| Paraphrases | 588 | 3858 | 2,268,311 |
| Blogs | 72 | 1979 | 142,500 |
| Stack Exchange Q&A | 117 | 1068 | 124,973 |
| Textbook Chapters | 61 | 1404 | 85,666 |
| Prerequisite Chapters | 220 | 4589 | 1,009,582 |
| Contextual Documents | 0 | – | – |
| Legal |
| Source Documents | 12 | 3259 | 39,109 |
| Paraphrases | 589 | 3274 | 1,928,141 |
| Blogs | 48 | 1739 | 83,484 |
| Stack Exchange Q&A | 94 | 1129 | 106,098 |
| Textbook Chapters | 63 | 1459 | 91,904 |
| Prerequisite Chapters | 175 | 3606 | 631,086 |
| Contextual Documents | 133 | 8991 | 1,195,740 |

Table 7: Dataset statistics by text type and domain.

#### Paraphrases.

Paraphrases are generated from cleaned source documents on a paragraph-level basis. We preserve section headers verbatim and avoid paraphrasing LaTeX-only paragraphs. Domain-specific prompts are used for academic, legal, and medical text. The academic prompt preserves LaTeX formatting, equations, proper nouns, titles, section headers, and technical terminology; the legal prompt preserves legal meaning, party names, citations, quoted language, dates, docket numbers, and legal terms of art; and the medical prompt preserves diagnoses, medications, doses, routes, timelines, lab values, imaging findings, procedures, outcomes, and clinical terminology. We use GPT-4.1 to generate paraphrases with a temperature of 1 and a top-p of 0.975.

#### Auxiliary views.

For each document, we generate synthetic auxiliary views conditioned on the target document and intended to restate, explain, or pedagogically reorganize the same document-level content. The computer science setting generates textbook chapters for college students with a basic machine-learning background, Stack Exchange–style questions from a confused student followed by grounded answers, and technical blog posts for a broader technical audience. The medical setting adapts these formats to clinical education: case-based textbook sections for medical students or residents, clinical teaching Q&A, and clinical blog posts. The legal setting uses casebook/treatise-style chapters for law students, Law Stack Exchange–style Q&A, and analytic legal commentary. For each view family, we first generate an outline, list of questions, or list of blog ideas and then generate the individual chapters, answers, or posts from that plan. We use GPT-5 to generate the outlines and GPT-5-mini to generate the contents of the chapters, questions, or posts.

#### Prerequisite views.

Prerequisite views are generated separately from auxiliary views. For arXiv papers, we use a curriculum-design prompt to create prerequisite textbook chapters that teach the foundations needed to understand the paper while excluding the paper’s own novel ideas. For medical case reports, the prompt asks for general medical background–for example relevant anatomy, pathophysiology, pharmacology, diagnostic interpretation, differential diagnosis, and standard management–while explicitly forbidding patient-specific chronology, workup, treatment course, outcome, or novel observations from the source case. For legal opinions, the prompt similarly asks for doctrinal and procedural background while excluding the source case’s parties, facts, outcome, holding, and novel reasoning. When useful for legal background, we additionally include landmark or doctrinally foundational cited opinions as context for the generated prerequisite chapters. We use GPT-5 to generate the outlines and GPT-5-mini to generate the contents of the chapters.

## Appendix B Probe Generation

Our probe construction pipeline is adapted and refined for each domain (arXiv, legal, and medical). We present the pipeline for arXiv documents in Figure [6](https://arxiv.org/html/2609.04180v1#A2.F6 "Figure 6 ‣ Appendix B Probe Generation ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"); the full pipeline for all domains is available in our released code.

Figure 6: Overview of the probe-generation pipeline for arXiv documents. (A) Factual probe generation: We generate probes sentence by sentence to keep their ground truth close to the source document. Preprocessing: We first remove sentences containing minimal knowledge (to prevent noise from structural comments, e.g., “Let us first discuss the following results”). We then use heuristics to remove sentences likely to yield low-quality probes, such as those that are too short (e.g., “the sweep has 22 runs”) or contain excessive LaTeX code with no valid English extraction targets. Question extraction: From each remaining sentence, we extract 1–3 questions that capture its knowledge. Contextualization: Questions are made clear and self-contained while preserving the knowledge being tested. Cloze conversion: Questions are converted into cloze statements with answers at the end. Refinement: We ensure that all mathematical content is written in LaTeX and verify the preceding steps. (B) Compositional probe generation: Because not all atomic facts warrant a compositional probe, we employ a two-level approach. First, we divide the paper into sections and prompt an LLM to extract compositional questions. We define compositionality as either (1) inference, which reasons over supporting text to reach a new insight, or (2) synthesis, which combines several facts into a synthesized statement. We perform this process section by section for granularity, then repeat it with the entire paper to obtain more holistic questions. Cloze conversion: As in the factual pipeline, questions are converted into cloze statements with answers at the end. Refinement: Statements are formatted in LaTeX where needed and made self-contained by referencing the paper (e.g., “according to the paper”). Filtering: Finally, we ask the LLM to identify questions that are too simple, imprecise, or confusing; this step removes 15% of probes on average.

## Appendix C Additional Plots

Figure 7: Under a fixed token budget, auxiliary views improve both factual recall and inference, and their effect size increases with model size. This pattern also holds when averaging by domain, with factual probes for medical documents as the sole exception.

Figure 8: Under a fixed token budget, auxiliary views improve both factual recall and inference, and their effect size increases with model size. Lower ranks are better.

Figure 9: FFN parameter change over training (OLMo-2-7B). Paraphrasing induces the largest parameter movement, while auxiliary views reduce this magnitude toward source-only training. Both the concentration of change (Gini) and downstream performance converge by step ∼\\sim50 (performance not shown), whereas magnitude (relative delta norm and cosine distance) continues to grow afterward; parameters keep drifting after learning has effectively converged.Figure 10: Per-layer FFN parameter change from the base model over training (OLMo-2-7B). Magnitude (relative delta norm and cosine distance) and concentration (Gini) are shown for the gate, up, and down projections. All conditions concentrate change in the middle and final layers with a dip in the upper-middle layers; auxiliary views increase change in the middle and final layers but reduce it relative to source in the ∼\\sim16–24 band.![Refer to caption](https://arxiv.org/html/2609.04180v1/1B_delta_parameters.png)Figure 11: The same per-channel difference in cosine distance from the base model (Para. 9 + Aux. minus Source) as Figure [4](https://arxiv.org/html/2609.04180v1#S4.F4 "Figure 4 ‣ 4.3 Mechanistic Signatures of Auxiliary Views ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), but for the 1B model. Unlike the structured pattern at 7B, the difference is either blue (negative) or white, indicating that auxiliary views change parameters slightly less than source nearly everywhere, with no organized layer-wise band. The only exceptions are a few isolated channels in down\_proj at the deepest layers. Figure 12: Effect of peak learning rate (2e-5, 4e-5, and 8e-5) on knowledge acquisition for the 7B model. We report final log probability on factual and inference probes (left two panels) and final accuracy on factual and inference MCQA (right two panels), comparing source documents alone (Source), 49 paraphrases (Para. 49), and 49 paraphrases plus auxiliary views (Para. 49 + Aux.). Across all metrics, the advantages of auxiliary views and paraphrases grow with learning rate.

## Appendix D Additional Tables

| Auxiliary views | Factual | Factual | Inference | Inference |
| --- | --- | --- | --- | --- |
|  | log prob. | MCQA | log prob. | MCQA |
| --- | --- | --- | --- | --- |
| Textbooks | -11.358 | 0.394 | -12.218 | 0.457 |
| Stack Exchange | -11.642 | 0.398 | -12.216 | 0.450 |
| Blogs | -11.570 | 0.388 | -12.189 | 0.447 |
| Mixed | -11.087 | 0.398 | -11.665 | 0.450 |

Table 8: Auxiliary-view families. Metrics for OLMo-2 7B after training on token-matched textbooks, Stack Exchange–style Q&A, blogs, or their mixture. The families perform similarly; mixing them performs best on both log-probability metrics and factual MCQA, while textbooks perform best on inference MCQA. Higher is better for every metric.

| Domain | Condition | Peak factual Δ\\Delta LP | Peak inference Δ\\Delta LP |
| --- | --- | --- | --- |
| arXiv | Para. 9 (standard) | 4.344 | 2.575 |
| Para. 9 (token-matched) | 7.117 | 4.723 |
| ++ Prerequisite | 6.690 | 4.629 |
| ++ Contextual | 6.893 | 4.574 |
| Legal | Para. 9 (standard) | 3.817 | 0.719 |
| Para. 9 (token-matched) | 8.222 | 2.049 |
| ++ Prerequisite | 6.663 | 2.331 |
| ++ Contextual | 6.768 | 2.184 |
| All | Para. 9 (standard) | 4.231 | 2.028 |
| Para. 9 (token-matched) | 7.349 | 3.950 |
| ++ Prerequisite | 6.684 | 3.967 |
| ++ Contextual | 6.866 | 3.881 |

Table 9: Contextual and prerequisite knowledge. Peak improvement in log probability from each run’s pretrained baseline. The added-knowledge conditions and token-matched Para. 9 use the same inserted-token budget; standard Para. 9 is included as a non-token-matched reference. Adding surrounding knowledge yields improvements comparable to adding paraphrases. Higher Δ\\Delta LP is better. Medical is omitted because case reports lack an analogous citation structure.

| Placement | Factual | Factual | Inference | Inference |
| --- | --- | --- | --- | --- |
|  | Δ\\Delta LP | Δ\\Delta MCQA | Δ\\Delta LP | Δ\\Delta MCQA |
| --- | --- | --- | --- | --- |
| Front | 6.320 | 0.022 | 3.639 | 0.068 |
| Middle | 6.591 | 0.026 | 3.847 | 0.053 |
| End | 6.680 | 0.025 | 3.706 | 0.053 |

Table 10: Prerequisite-knowledge ordering. Peak improvement from the pretrained baseline when prerequisite data appears at the front, middle, or end of training. Higher is better for every metric, including Δ\\Delta log probability. No placement is consistently best.

| Condition | Fact. | Fact. | Inf. | Inf. |
| --- | --- | --- | --- | --- |
|  | log prob. | MCQA | log prob. | MCQA |
| --- | --- | --- | --- | --- |
| Pretrained model | -15.31 | 0.440 | -15.02 | 0.478 |
| Source | -15.48 | 0.489 | -18.82 | 0.512 |
| Para. 9 | -13.28 | 0.516 | -16.24 | 0.559 |
| Auxiliary views | -10.98 | 0.548 | -12.74 | 0.562 |

Table 11: Qwen-2.5-7B. Final metrics under the same injection setup as the main experiment. The advantage of auxiliary views generalizes to Qwen-2.5-7B.Table 12: Frequency and coverage of our probe targets across contextual and prerequisite knowledge. Freq. = occurrences per 1k (words for the full target, OLMo
tokens for bigrams); Cover. = fraction of targets present at least once (full
target) or the mean fraction of a target’s bigrams present (bigram). Prerequisites = generated textbook chapters; Cited Works = cited papers or legal opinions.

| Probes | Corpus | Full target | Bigram |
| --- | --- | --- | --- |
|  |  | Freq. | Cover. | Freq. | Cover. |
| --- | --- | --- | --- | --- | --- |
| Factual | Prerequisites | 0.031 | 0.12 | 0.129 | 0.54 |
| Cited Works | 0.039 | 0.24 | 0.141 | 0.72 |
| Inference | Prerequisites | 0.827 | 0.21 | 0.154 | 0.47 |
| Cited Works | 0.838 | 0.25 | 0.095 | 0.54 |

| Generator | Generator factual | Params | Words | Downstream factual |
|  | MCQA acc. | (B) | (M) | MCQA acc. |
| None (pretrained OLMo-2 7B) | – | – | – | 0.361 |
| Para. 9 (token-matched baseline) | – | – | – | 0.396 |
| gpt-5-mini (original; mixed) | – | – | 1.08 | 0.415 |
| gpt-5-mini (low reasoning) | 0.657 | – | 1.04 | 0.419 |
| gpt-5-mini (high reasoning) | 0.673 | – | 1.10 | 0.420 |
| gpt-5.4-mini (low reasoning) | 0.718 | – | 0.84 | 0.416 |
| gpt-5.4-mini (high reasoning) | 0.749 | – | 0.72 | 0.414 |
| gpt-oss-20B (low reasoning) | 0.539 | 20.9 | 0.72 | 0.422 |
| gpt-oss-120B (low reasoning) | 0.599 | 116.8 | 0.79 | 0.413 |
| Gemma-4 12B IT | 0.565 | 12 | 0.36 | 0.414 |
| Gemma-4 31B IT | 0.662 | 31 | 0.35 | 0.405 |
| GLM-5 (high reasoning) | 0.728 | 744 | 0.66 | 0.406 |
| GLM-5.2 (high reasoning) | 0.758 | 744 | 0.90 | 0.418 |

Table 13: Auxiliary-view generation. Peak factual MCQA accuracy after training OLMo-2 7B on views from different generators under the same schedule and token budget. Generator accuracy measures five-shot prior domain knowledge; Words (M) counts generated blogs, Stack Exchange posts, and textbooks. Downstream accuracy is uncorrelated with generator size among open-weight generators (Pearson r=−0.14r=-0.14, n=6n=6) or generator accuracy (r=−0.24r=-0.24, n=10n=10), but correlates moderately with view-text volume (r=+0.62r=+0.62, n=11n=11, p=0.042p=0.042).

## Appendix E Hyperparameters for Replication and Details for Reproduction

For training, we use the TRL library. Unless otherwise noted, our experiments use the following defaults:
learning rate 4×10−54\\times 10^{-5}, context size 4096, batch size 256, weight decay 0.1,
cosine decay scheduler with 0.1 warm-up ratio and minimum learning rate ratio of 0.1, seed 42, max gradient norm of 1, and the AdamW optimizer
(β1=0.9\\beta\_{1}=0.9, β2=0.999\\beta\_{2}=0.999, ϵ=10−8\\epsilon=10^{-8}) with BF16 training.

Pre-training-faithful continuation. For the experiment in Table [5](https://arxiv.org/html/2609.04180v1#S4.T5 "Table 5 ‣ 4.2 Broader Generalization ‣ 4 Large Language Models Learn Better with Auxiliary Views ‣ Knowledge Acquisition During Pre-training?Large Language Models Learn Better With Auxiliary Views"), we resume OLMo-2 7B from checkpoint step 925,000 using the OLMo framework. We restore the checkpoint’s optimizer state and continue with the original pre-training data stream and learning-rate schedule, a global batch size of 1,024, and a sequence length of 4,096. We inject domain data for 100 optimizer steps using the same conditions as in the main experiments.

## Appendix F Prompts for Probe Construction (arXiv)

We provide some of the prompts used in our pipeline to construct factual and inference probes for the arXiv documents. The complete set of prompts, adapted for each domain (legal and medical), is available in our code.

1\. Prompt to extract atomic facts from a paragraph:

[⬇](data:text/plain;base64,WW91IHdpbGwgYmUgZ2l2ZW4gdHdvIGlucHV0cywgYSBzZWN0aW9uIG9mIGFuIGFjYWRlbWljIHBhcGVyIGZvciBjb250ZXh0IGFuZCBhIHNpbmdsZSBzZW50ZW5jZSBkcmF3biBmcm9tIHRoYXQgc2VjdGlvbi4gUGFwZXJzIG9mdGVuIGludGVyd2VhdmUgdmFyaW91cyBwaWVjZXMgb2Yga25vd2xlZGdlIHRvZ2V0aGVyIGluIGFjYWRlbWljIHdyaXRpbmcuIFdoaWxlIGVhY2ggc2VudGVuY2UgaXMgaW50ZXJ3b3ZlbiB3aXRoIG90aGVycywgdGhlcmUgaXMgYXRvbWljIGtub3dsZWRnZSB0aGF0IGNhbiBiZSBleHRyYWN0ZWQgZnJvbSBhIHBhcnRpY3VsYXIgc2VudGVuY2UuIFdyaXRlIHF1ZXN0aW9ucyB0aGF0IHRlc3RzIGZvciB0aGlzIGF0b21pYyBrbm93bGVkZ2UuIFNwZWNpZmljYWxseSwgeW91ciB0YXNrIGlzIHRvIGV4dHJhY3QgcXVlc3Rpb25zIGZyb20gdGhlIHByb3ZpZGVkIHNlbnRlbmNlIHdpdGggY2xlYXIgYW5zd2VycywgZWFjaCAxIHRvIDQgd29yZHMgbG9uZy4gCiAgIApFeHRyYWN0IDEtMyBxdWVzdGlvbnMgZnJvbSB0aGUgc2VudGVuY2UuIAogIAojIyMgRGV0YWlsZWQgSW5zdHJ1Y3Rpb25zCkNvbnNpZGVyIHRoZXNlIGluc3RydWN0aW9ucyBhcyB5b3UgZXh0cmFjdCBlYWNoIHF1ZXN0aW9uOgotIFRoZSBxdWVzdGlvbiBzaG91bGQgYmUgbmF0dXJhbCBhbmQgbWVhbmluZ2Z1bCwgaW4gd2hpY2ggdGhlIGFuc3dlciBpcyBjb25zaWRlcmVkIGEgbWFpbiBmYWN0IHByZXNlbnRlZCBieSB0aGUgc2VudGVuY2UuCi0gVGhlIGFuc3dlciBzaG91bGQgYmUgbm9uLXRyaXZpYWwgYW5kIG5vbi1vYnZpb3VzLiBJdCBzaG91bGQgbm90IGJlIGRlZHVjaWJsZSBmcm9tIHRoZSBzZW50ZW5jZSBpdHNlbGYuCi0gVGhlIGFuc3dlciB0byB0aGUgcXVlc3Rpb24gc2hvdWxkIGJlIGEgbWVhbmluZ2Z1bCwgY29oZXJlbnQgcGhyYXNlLCAxLTQgd29yZHMgbG9uZywgdGFrZW4gZnJvbSB0aGUgc2VudGVuY2UuIFNpbXBsaWZ5IHRoZSBhbnN3ZXIgYnkgc3RyaXBwaW5nIGRldGVybWluZXJzIHN1Y2ggYXMgInNvbWUiIG9yICJhIiBvciAiYW4iIG9yICJ0aGUiIGZyb20gdGhlIGFuc3dlci4gRmVlbCBmcmVlIHRvIGFkanVzdCB0aGUgYW5zd2VyIHRvIGZpdCB0aGUgcXVlc3Rpb24sIGJ1dCB0aGUgbWVhbmluZyBzaG91bGQgYmUgdGhlIHNhbWUuCi0gVGhlIGFuc3dlciBtdXN0ICpOT1QqIGludm9sdmUgYW55ICpzcGVjaWFsIGNoYXJhY3RlcnMqIG9yICptYXRoZW1hdGljYWwgbm90YXRpb24qLiBBZ2FpbiwgYW55IHF1ZXN0aW9uIHdpdGggYW4gYW5zd2VyIHRoYXQgY29udGFpbnMgbWF0aGVtYXRpY2FsIG5vdGF0aW9uIHNob3VsZCBub3QgYmUgdXNlZC4KLSBUaGUgcXVlc3Rpb24gc2hvdWxkIGhhdmUgYSBhIGNsZWFyLCBzaW5nbGUgYW5zd2VyIGFuZCAqTk9UKiBtdWx0aXBsZSB2YWxpZCBhbnN3ZXJzLiAKLSBFYWNoIHF1ZXN0aW9uIHNob3VsZCBiZSB3cml0dGVuIHNlcGFyYXRlbHkgYW5kIGluZGVwZW5kZW50bHkgb2YgdGhlIG90aGVyIHF1ZXN0aW9ucywgc28gZG9uJ3QgcmVmZXJlbmNlIG90aGVyIHF1ZXN0aW9ucyBpbiB0aGUgc2FtZSBxdWVzdGlvbi4KCiMjIyBEZW1vbnN0cmF0aW9uIDEKQ29udGV4dDogIlxcdGl0bGV7RGlyZWN0IFByZWZlcmVuY2UgT3B0aW1pemF0aW9uOiBZb3VyIExhbmd1YWdlIE1vZGVsIGlzIFNlY3JldGx5IGEgUmV3YXJkIE1vZGVsfVxuXFxzdWJzZWN0aW9ue0NhbiBEUE8gc2NhbGUgdG8gcmVhbCBwcmVmZXJlbmNlIGRhdGFzZXRzP31cbk5leHQsIHdlIGV2YWx1YXRlIGZpbmUtdHVuaW5nIHBlcmZvcm1hbmNlIG9mIERQTyBvbiBzdW1tYXJpemF0aW9uIGFuZCBzaW5nbGUtdHVybiBkaWFsb2d1ZS4gRm9yIHN1bW1hcml6YXRpb24sIGF1dG9tYXRpYyBldmFsdWF0aW9uIG1ldHJpY3Mgc3VjaCBhcyBST1VHRSBjYW4gYmUgcG9vcmx5IGNvcnJlbGF0ZWQgd2l0aCBodW1hbiBwcmVmZXJlbmNlc35cY2l0ZXB7c3RpZW5ub24yMDIybGVhcm5pbmd9LCBhbmQgcHJpb3Igd29yayBoYXMgZm91bmQgdGhhdCBmaW5lLXR1bmluZyBMTXMgdXNpbmcgUFBPIG9uIGh1bWFuIHByZWZlcmVuY2VzIHRvIHByb3ZpZGUgbW9yZSBlZmZlY3RpdmUgc3VtbWFyaWVzLiBXZSBldmFsdWF0ZSBkaWZmZXJlbnQgbWV0aG9kcyBieSBzYW1wbGluZyBjb21wbGV0aW9ucyBvbiB0aGUgdGVzdCBzcGxpdCBvZiBUTDtEUiBzdW1tYXJpemF0aW9uIGRhdGFzZXQsIGFuZCBjb21wdXRpbmcgdGhlIGF2ZXJhZ2Ugd2luIHJhdGUgYWdhaW5zdCByZWZlcmVuY2UgY29tcGxldGlvbnMgaW4gdGhlIHRlc3Qgc2V0LiIKClNlbnRlbmNlOiAiV2UgZXZhbHVhdGUgZGlmZmVyZW50IG1ldGhvZHMgYnkgc2FtcGxpbmcgY29tcGxldGlvbnMgb24gdGhlIHRlc3Qgc3BsaXQgb2YgVEw7RFIgc3VtbWFyaXphdGlvbiBkYXRhc2V0LCBhbmQgY29tcHV0aW5nIHRoZSBhdmVyYWdlIHdpbiByYXRlIGFnYWluc3QgcmVmZXJlbmNlIGNvbXBsZXRpb25zIGluIHRoZSB0ZXN0IHNldC4iCgpRdWVzdGlvbnM6Ci0gIlRoZSBhdXRob3JzIGV2YWx1YXRlIERQTydzIGZpbmUtdHVuaW5nIHBlcmZvcm1hbmNlIGFnYWluc3Qgb3RoZXIgbWV0aG9kcyBvbiBzdW1tYXJpemF0aW9uIGJ5IHNhbXBsaW5nIGNvbXBsZXRpb25zIG9uIHRoZSB0ZXN0IHNwbGl0IG9mIHdoYXQgZGF0YXNldD8iLCBBbnN3ZXI6ICJUTDtEUiBzdW1tYXJpemF0aW9uIgotICJUaGUgZmluZS10dW5pbmcgcGVyZm9ybWFuY2Ugb2YgRFBPIGFuZCBvdGhlciBtZXRob2RzIG9uIHN1bW1hcml6YXRpb24gYXJlIGV2YWx1YXRlZCBieSBzYW1wbGluZyBjb21wbGV0aW9ucyBvbiB0aGUgdGVzdCBzcGxpdCBvZiB0aGUgVEw7RFIgc3VtbWFyaXphdGlvbiBkYXRhc2V0IGFuZCBjb21wdXRpbmcgdGhlIGF2ZXJhZ2Ugd2luIHJhdGUgYWdhaW5zdCB3aGF0PyIsIEFuc3dlcjogInJlZmVyZW5jZSBjb21wbGV0aW9ucyIKCiMjIyBEZW1vbnN0cmF0aW9uIDIKQ29udGV4dDogIlx0aXRsZXtEaXJlY3QgUHJlZmVyZW5jZSBPcHRpbWl6YXRpb246IFlvdXIgTGFuZ3VhZ2UgTW9kZWwgaXMgU2VjcmV0bHkgYSBSZXdhcmQgTW9kZWx9XG5XaGlsZSBsYXJnZS1zY2FsZSB1bnN1cGVydmlzZWQgbGFuZ3VhZ2UgbW9kZWxzIChMTXMpIGxlYXJuIGJyb2FkIHdvcmxkIGtub3dsZWRnZSBhbmQgc29tZSByZWFzb25pbmcgc2tpbGxzLCBhY2hpZXZpbmcgcHJlY2lzZSBjb250cm9sIG9mIHRoZWlyIGJlaGF2aW9yIGlzIGRpZmZpY3VsdCBkdWUgdG8gdGhlIGNvbXBsZXRlbHkgdW5zdXBlcnZpc2VkIG5hdHVyZSBvZiB0aGVpciB0cmFpbmluZy4gRXhpc3RpbmcgbWV0aG9kcyBmb3IgZ2FpbmluZyBzdWNoIHN0ZWVyYWJpbGl0eSBjb2xsZWN0IGh1bWFuIGxhYmVscyBvZiB0aGUgcmVsYXRpdmUgcXVhbGl0eSBvZiBtb2RlbCBnZW5lcmF0aW9ucyBhbmQgZmluZS10dW5lIHRoZSB1bnN1cGVydmlzZWQgTE0gdG8gYWxpZ24gd2l0aCB0aGVzZSBwcmVmZXJlbmNlcywgb2Z0ZW4gd2l0aCByZWluZm9yY2VtZW50IGxlYXJuaW5nIGZyb20gaHVtYW4gZmVlZGJhY2sgKFJMSEYpLiIKClNlbnRlbmNlOiAiRXhpc3RpbmcgbWV0aG9kcyBmb3IgZ2FpbmluZyBzdWNoIHN0ZWVyYWJpbGl0eSBjb2xsZWN0IGh1bWFuIGxhYmVscyBvZiB0aGUgcmVsYXRpdmUgcXVhbGl0eSBvZiBtb2RlbCBnZW5lcmF0aW9ucyBhbmQgZmluZS10dW5lIHRoZSB1bnN1cGVydmlzZWQgTE0gdG8gYWxpZ24gd2l0aCB0aGVzZSBwcmVmZXJlbmNlcywgb2Z0ZW4gd2l0aCByZWluZm9yY2VtZW50IGxlYXJuaW5nIGZyb20gaHVtYW4gZmVlZGJhY2sgKFJMSEYpLiIKClF1ZXN0aW9uczoKLSAiV2hhdCBkbyBleGlzdGluZyBtZXRob2RzIGNvbGxlY3QgdG8gc3RlZXIgdW5zdXBlcnZpc2VkIGxhbmd1YWdlIG1vZGVscywgPyIsIEFuc3dlcjogImh1bWFuIGxhYmVscyIKLSAiRXhpc3RpbmcgbWV0aG9kcyBmb3Igc3RlZXJpbmcgdW5zdXBlcnZpc2VkIGxhbmd1YWdlIG1vZGVscyBjb2xsZWN0IGh1bWFuIGxhYmVscyBvZiB0aGUgcXVhbGl0eSBvZiB3aGF0PyIsIEFuc3dlcjogInJlbGF0aXZlIHF1YWxpdHkgb2YgbW9kZWwgZ2VuZXJhdGlvbnMiCi0gIkV4aXN0aW5nIG1ldGhvZHMgYWxpZ24gdW5zdXBlcnZpc2VkIGxhbmd1YWdlIG1vZGVscyBieSBmaW5lLXR1bmluZyBvbiB3aGF0PyIsIEFuc3dlcjogImh1bWFuIHByZWZlcmVuY2VzIgotICJFeGlzdGluZyBtZXRob2RzIGZvciBzdGVlcmluZyB1bnN1cGVydmlzZWQgbGFuZ3VhZ2UgbW9kZWxzIHZpYSBmaW5lLXR1bmluZyBvbiBodW1hbiBwcmVmZXJlbmNlcyBvZnRlbiB1c2Ugd2hhdD8iLCBBbnN3ZXI6ICJSTEhGIg==)

Youwillbegiventwoinputs,asectionofanacademicpaperforcontextandasinglesentencedrawnfromthatsection.Papersofteninterweavevariouspiecesofknowledgetogetherinacademicwriting.Whileeachsentenceisinterwovenwithothers,thereisatomicknowledgethatcanbeextractedfromaparticularsentence.Writequestionsthattestsforthisatomicknowledge.Specifically,yourtaskistoextractquestionsfromtheprovidedsentencewithclearanswers,each1to4wordslong.

Extract1-3questionsfromthesentence.

###DetailedInstructions

Considertheseinstructionsasyouextracteachquestion:

-Thequestionshouldbenaturalandmeaningful,inwhichtheanswerisconsideredamainfactpresentedbythesentence.

-Theanswershouldbenon-trivialandnon-obvious.Itshouldnotbededuciblefromthesentenceitself.

-Theanswertothequestionshouldbeameaningful,coherentphrase,1-4wordslong,takenfromthesentence.Simplifytheanswerbystrippingdeterminerssuchas"some"or"a"or"an"or"the"fromtheanswer.Feelfreetoadjusttheanswertofitthequestion,butthemeaningshouldbethesame.

-Theanswermust\*NOT\*involveany\*specialcharacters\*or\*mathematicalnotation\*.Again,anyquestionwithananswerthatcontainsmathematicalnotationshouldnotbeused.

-Thequestionshouldhaveaaclear,singleanswerand\*NOT\*multiplevalidanswers.

-Eachquestionshouldbewrittenseparatelyandindependentlyoftheotherquestions,sodon’treferenceotherquestionsinthesamequestion.

###Demonstration1

Context:"\\\title{DirectPreferenceOptimization:YourLanguageModelisSecretlyaRewardModel}\n\\\subsection{CanDPOscaletorealpreferencedatasets?}\nNext,weevaluatefine-tuningperformanceofDPOonsummarizationandsingle-turndialogue.Forsummarization,automaticevaluationmetricssuchasROUGEcanbepoorlycorrelatedwithhumanpreferences~\citep{stiennon2022learning},andpriorworkhasfoundthatfine-tuningLMsusingPPOonhumanpreferencestoprovidemoreeffectivesummaries.WeevaluatedifferentmethodsbysamplingcompletionsonthetestsplitofTL;DRsummarizationdataset,andcomputingtheaveragewinrateagainstreferencecompletionsinthetestset."

Sentence:"WeevaluatedifferentmethodsbysamplingcompletionsonthetestsplitofTL;DRsummarizationdataset,andcomputingtheaveragewinrateagainstreferencecompletionsinthetestset."

Questions:

-"TheauthorsevaluateDPO’sfine-tuningperformanceagainstothermethodsonsummarizationbysamplingcompletionsonthetestsplitofwhatdataset?",Answer:"TL;DRsummarization"

-"Thefine-tuningperformanceofDPOandothermethodsonsummarizationareevaluatedbysamplingcompletionsonthetestsplitoftheTL;DRsummarizationdatasetandcomputingtheaveragewinrateagainstwhat?",Answer:"referencecompletions"

###Demonstration2

Context:"\title{DirectPreferenceOptimization:YourLanguageModelisSecretlyaRewardModel}\nWhilelarge-scaleunsupervisedlanguagemodels(LMs)learnbroadworldknowledgeandsomereasoningskills,achievingprecisecontroloftheirbehaviorisdifficultduetothecompletelyunsupervisednatureoftheirtraining.Existingmethodsforgainingsuchsteerabilitycollecthumanlabelsoftherelativequalityofmodelgenerationsandfine-tunetheunsupervisedLMtoalignwiththesepreferences,oftenwithreinforcementlearningfromhumanfeedback(RLHF)."

Sentence:"Existingmethodsforgainingsuchsteerabilitycollecthumanlabelsoftherelativequalityofmodelgenerationsandfine-tunetheunsupervisedLMtoalignwiththesepreferences,oftenwithreinforcementlearningfromhumanfeedback(RLHF)."

Questions:

-"Whatdoexistingmethodscollecttosteerunsupervisedlanguagemodels,?",Answer:"humanlabels"

-"Existingmethodsforsteeringunsupervisedlanguagemodelscollecthumanlabelsofthequalityofwhat?",Answer:"relativequalityofmodelgenerations"

-"Existingmethodsalignunsupervisedlanguagemodelsbyfine-tuningonwhat?",Answer:"humanpreferences"

-"Existingmethodsforsteeringunsupervisedlanguagemodelsviafine-tuningonhumanpreferencesoftenusewhat?",Answer:"RLHF"

2\. Prompt to extract atomic facts from a paragraph with context:

[⬇](data:text/plain;base64,WW91IHdpbGwgYmUgZ2l2ZW4gdHdvIGlucHV0cywgYSBzZWN0aW9uIG9mIGFuIGFjYWRlbWljIHBhcGVyIGZvciBjb250ZXh0LCBhIHNpbmdsZSBzZW50ZW5jZSBkcmF3biBmcm9tIHRoYXQgc2VjdGlvbiwgYW5kIGEgcXVlc3Rpb24gZXh0cmFjdGVkIGZyb20gdGhlIHNlbnRlbmNlIGFzIHdlbGwgYXMgaXRzIGNvcnJlc3BvbmRpbmcgYW5zd2VyLiBZb3VyIHRhc2sgaXMgdG8gdGhlbiB0dXJuIHRoZSBxdWVzdGlvbiBpbnRvIGEgc2VsZi1jb250YWluZWQsIHByZWNpc2UgcXVlc3Rpb24uIEFwcHJvYWNoIHRoaXMgdGFzayBzdGVwLWJ5LXN0ZXAgYXMgb3V0bGluZWQgYmVsb3cuCgpXaGlsZSB5b3Ugc2hvdWxkIHVzZSB5b3VyIGV4cGVydGlzZSBvbiB0aGlzIGRvbWFpbiB0byBoYW5kbGUgYW5kIHVuZGVyc3RhbmQgdGhlc2UgdGV4dHMsIGFsbCBpbmZvcm1hdGlvbiB3cml0dGVuIGludG8gdGhlIHF1ZXN0aW9ucyBhbmQgYW5zd2VycyAqTVVTVCogb3JpZ2luYXRlIGZyb20gdGhlIHByb3ZpZGVkIGNvbnRleHQgb3Igc2VudGVuY2UuIERvIG5vdCBhZGQsIGluZmVyLCBvciBjb3JyZWN0IGluZm9ybWF0aW9uIHVzaW5nIHlvdXIgaW50ZXJuYWwga25vd2xlZGdlLiBFdmVyeSBkZXRhaWwgc2hvdWxkIGJlIHRyYWNlYWJsZSBiYWNrIHRvIHRoZSBzb3VyY2UgdGV4dC4gQXMgeW91IHdyaXRlIGFuZCByZXdyaXRlIHRoZSBxdWVzdGlvbnMsIGFsc28gbWFrZSBzdXJlIHRvIGFjY3VyYXRlbHkgcmVwcmVzZW50IHRoZSBrbm93bGVkZ2UgaW4gdGhlIG9yaWdpbmFsIHNlbnRlbmNlIHdpdGhvdXQgZGlzdG9ydGlvbi4gU3RyaXZlIHRvIHVzZSBwaHJhc2luZyBhcyBjbG9zZSBhcyBwb3NzaWJsZSB0byB0aGUgb3JpZ2luYWwgdGV4dCwgYnV0IHByaW9yaXRpemUgY2xhcml0eSBhbmQgc2VsZi1jb250YWlubWVudC4gTGFzdGx5LCB0aGUgcXVlc3Rpb25zIHNob3VsZCBiZSB3cml0dGVuIHdlbGwgYW5kIGNsZWFybHkgc28gdGhhdCB0aGV5IGFyZSBlYXN5IHRvIHJlYWQuCiAgICAKIyMjIEluc3RydWN0aW9ucwpUaGUgb3ZlcmFsbCBnb2FsIG9mIHRoaXMgdGFzayBpcyB0byBtYWtlIHRoZSBxdWVzdGlvbnMgY2xlYXIgYnkgaW5jb3Jwb3JhdGluZyB0aGUgcmVsZXZhbnQgY29udGV4dC4gVGhpcyBlbnN1cmVzIHRoZSBxdWVzdGlvbiBpcyB1bmFtYmlndW91cyBhbmQgZG9lc24ndCByZXF1aXJlIGxvb2tpbmcgYmFjayB0byB0aGUgc291cmNlIG1hdGVyaWFsLgoKRm9yIGVhY2ggcXVlc3Rpb246CjEuICBSZXdyaXRlIHRoZSBxdWVzdGlvbiBzbyB0aGF0IGl0IHN0YXJ0cyB3aXRoIG9uZSBvZiB0aGUgZm9sbG93aW5nIHRlbXBsYXRlcy4gCiAgICAtICJJbiB0aGUgcGFwZXIgJ3t0aXRsZX0nLCAuLi4iCiAgICAtICJBY2NvcmRpbmcgdG8gdGhlIHBhcGVyICd7dGl0bGV9JywuLi4iCiAgICAtICJJbiB0aGUgcGFwZXIgJ3t0aXRsZX0nLCB0aGUgYXV0aG9ycyByZW1hcmsgdGhhdC4uLiIKICAgIC0gIkluIHRoZSBwYXBlciAne3RpdGxlfScsIHRoZSBhdXRob3JzIHN0YXRlIHRoYXQuLi4iCiAgICAtICJBY2NvcmRpbmcgdG8gdGhlIHBhcGVyICd7dGl0bGV9JywgcHJpb3Igd29yayBoYXMuLi4iCiAgICAtICJJbiB0aGUgdGhlb3JldGljYWwgYW5hbHlzaXMgb2YgdGhlIHBhcGVyICJ7dGl0bGV9Ii4uLiIKICAgIC0gIkluIHRoZSBwYXBlciAne3RpdGxlfScsIHRoZSByZXN1bHRzIHN1Z2dlc3QgdGhhdC4uLiIKICAgIFRoaXMgaXMgYSBub24tZXhoYXVzdGl2ZSBsaXN0IG9mIHRlbXBsYXRlcywgYW5kIHlvdSBzaG91bGQgdXNlIHlvdXIgb3duIGp1ZGdlbWVudCB0byBjaG9vc2UgdGhlIG1vc3QgYXBwcm9wcmlhdGUgdGVtcGxhdGUgb3IgbW9kaWZ5IHRoZSB0ZW1wbGF0ZSB0byBmaXQgdGhlIHNlbnRlbmNlLgoyLiAgQWRkIHN1ZmZpY2llbnQgY29udGV4dC4gU3BlY2lmaWNhbGx5LCB1c2UgdGhlICpwcm92aWRlZCBjb250ZXh0KiB0byBzdXBwbHkgd2hhdGV2ZXIgaW5mb3JtYXRpb24gaXMgbmVlZGVkIHRvIG1ha2UgdGhlIHF1ZXN0aW9uIHNlbGYtY29udGFpbmVkIGFuZCB1bmFtYmlndW91cy4gRm9yIGluc3RhbmNlLCAiRG8gaHVtYW5zIGFuZCBHUFQ0IGFncmVlIG9mdGVuIHdpdGggZWFjaCBvdGhlcj8iIHNob3VsZCBiZSBjbGFyaWZpZWQgaW50byAiSW4gdGhlIHBhcGVyICcuLi4nLCBkaWQgaHVtYW5zIGFuZCBHUFQ0IG9mdGVuIGFncmVlIG9yIGRpc2FncmVlIHdpdGggZWFjaCBvdGhlciBkdXJpbmcgdGhlIGV2YWx1YXRpb24gb2YgRFBPPyIgaWYgdGhpcyBub3Rpb24gd2FzIGluIHRoZSBjb250ZXh0IG9mIGV2YWx1YXRpbmcgRFBPIGluIGFuIGFjYWRlbWljIHBhcGVyLiBUaGUgZ29hbCBpcyB0byBlbnN1cmUgc29tZW9uZSByZWFkaW5nIGp1c3QgdGhlIHF1ZXN0aW9uIHdvdWxkIHVuZGVyc3RhbmQgZXhhY3RseSB3aGF0IGlzIGJlaW5nIGFza2VkIHdpdGhvdXQgbmVlZGluZyBhZGRpdGlvbmFsIGNvbnRleHQuCjMuICBDbGFyaWZ5IHByb25vdW5zIGFuZCByZWZlcmVudGlhbCB0ZXJtcy4gQ2hlY2sgdGhlIHNlbnRlbmNlIGZvciBwcm9ub3VucyAoaXQsIHRoaXMsIHRoYXQsIHRoZXNlLCB0aG9zZSkgb3IgZGVtb25zdHJhdGl2ZSBwaHJhc2VzICh0aGlzIGVxdWF0aW9uLCB0aGF0IG1ldGhvZCwgdGhlc2UgcmVzdWx0cykgdGhhdCByZWZlciB0byBlbnRpdGllcyBub3QgZXhwbGljaXRseSBkZWZpbmVkIHdpdGhpbiB0aGUgc2VudGVuY2UgaXRzZWxmLiBTZWFyY2ggdGhlIHN1cnJvdW5kaW5nIGNvbnRleHQgdG8gaWRlbnRpZnkgd2hhdCB0aGVzZSB0ZXJtcyByZWZlcmVuY2UsIHRoZW4gaW5jb3Jwb3JhdGUgdGhhdCBjbGFyaWZ5aW5nIGluZm9ybWF0aW9uIGludG8gdGhlIHF1ZXN0aW9uIHRvIG1ha2UgaXQgc2VsZi1jb250YWluZWQuCjQuICBDbGFyaWZ5IENvbnRleHQtRGVwZW5kZW50IFRlcm1zLiBOYW1lZCBlbnRpdGllcyAoZS5nLiwgdGhlb3JlbXMsIGVxdWF0aW9ucywgcHJvcGVyIG5vdW5zKSBkbyBub3QgbmVlZCBjbGFyaWZpY2F0aW9uLiBIb3dldmVyLCBpZiB0aGVyZSBhcmUgdW5uYW1lZCBvciBjb250ZXh0LXNwZWNpZmljIHRlcm1zIChlLmcuLCAkZiQsICJ0aGUgbW9kZWwiLCAidGhlIGxvc3MiKSwgY2xhcmlmeSB0aGVpciBmdWxsIGNvbnRleHQuIEZvciBpbnN0YW5jZSwgInRoZSBncmFkaWVudCIgbWlnaHQgcmVmZXIgdG8gdGhlIGdlbmVyYWwgY29uY2VwdCBvZiBhIGdyYWRpZW50IG9yIHRvIHRoZSBncmFkaWVudCBvZiBhIHNwZWNpZmljIGZ1bmN0aW9uIG1lbnRpb25lZCBlYXJsaWVyIGluIHRoZSBjb250ZXh0Lgo1LiAgRGlzYW1iaWd1YXRlIGV4cGVyaW1lbnRzLiBUaGVyZSBhcmUgb2Z0ZW4gbnVtZXJvdXMgZXhwZXJpbWVudHMgaW4gYSBwYXBlciwgYW5kIHNvIHN1cHBseSBlbm91Z2ggZXhwZXJpbWVudGFsIGNvbnRleHQgc28gdGhhdCB0aGUgcXVlc3Rpb24gaXMgYWJvdXQgd2hpY2ggZXhwZXJpbWVudCB0aGUgcXVlc3Rpb24gaXMgYXNraW5nIGFib3V0LiAKNi4gIEhhbmRsZSBhY3Jvbnltcy4gSWYgdGhlIGFuc3dlciBpcyBhbiBhY3JvbnltIGFuZCB0aGUgYWNyb255bSBhcHBlYXJzIGZyZXF1ZW50bHkgaW4gdGhlIGNvbnRleHQsIGZlZWwgZnJlZSB0byBsZWF2ZSBpdCBhcyBhbiBhY3JvbnltIHdpdGhvdXQgZGVmaW5pbmcgaXQuCjcuICBEbyBub3QgbGVhayB0aGUgYW5zd2VyLiBQbGVhc2UgbWFrZSBzdXJlIHRoYXQgKnRoZSBhbnN3ZXIgaXMgbm90IHJldmVhbGVkKiBpbiB0aGUgcXVlc3Rpb24uIFRoZSBhbnN3ZXIgc2hvdWxkIG5ldmVyIGFwcGVhciBpbiB0aGUgcXVlc3Rpb24uCjguICBNYWludGFpbiB0aGUgZXNzZW5jZSBvZiB0aGUgb3JpZ2luYWwgcXVlc3Rpb24gZHVyaW5nIGFsbCBvZiB0aGlzLgo5LiAgRG8gbm90IGNoYW5nZSB0aGUgYW5zd2VyLiBNaW5vciBncmFtbWF0aWNhbCBhZGp1c3RtZW50cyB0byB0aGUgYW5zd2VyIGFyZSBhbGxvd2VkIG9ubHkgaWYgbmVjZXNzYXJ5IHRvIGZpdCB0aGUgcmVzdHJ1Y3R1cmVkIHF1ZXN0aW9uIChlLmcuLCBhZGp1c3RpbmcgdmVyYiB0ZW5zZSwgZGV0ZXJtaW5lcnMgbGlrZSAidGhlIikuCjEwLiBBdm9pZCBxdW90aW5nIHRoZSBzb3VyY2Ugc2VudGVuY2UgZGlyZWN0bHkgaW4gdGhlIHF1ZXN0aW9uLgoxMS4gUmVmaW5lIFF1ZXN0aW9uLiBUaGUgcmV3cml0dGVuIHF1ZXN0aW9uIGNhbiBiZSBicm9rZW4gdXAgaW50byBtdWx0aXBsZSBzZW50ZW5jZXMgaWYgdGhlIHF1ZXN0aW9uIGJlY29tZXMgdmVyYm9zZS4gTWFrZSBzdXJlIHRoZSBxdWVzdGlvbiBpcyB3cml0dGVuIGNsZWFybHkgYW5kIGdyYW1tYXRpY2FsbHkgY29ycmVjdC4gRG8gbm90IHB1dCBhbnkgb2YgdGhlIGNvbnRleHQgaW4gcGFyZW50aGVzaXMgb3IgZm9sbG93ZWQgYWZ0ZXIgYW4gImkuZS4iLgoKVGhpbmsgY2FyZWZ1bGx5IGFuZCBjcml0aWNhbGx5IHRocm91Z2ggdGhpcyB0YXNrLCBmb2xsb3dpbmcgdGhlIHN0ZXAtYnktc3RlcCBpbnN0cnVjdGlvbnMgb3V0bGluZWQgYWJvdmUuIFRoZW4sIHByb3ZpZGUgdGhlIGZpbmFsIG91dHB1dCwgbGlzdGluZyBlYWNoIHF1ZXN0aW9uIGFuZCBpdHMgY29ycmVzcG9uZGluZyBhbnN3ZXIu)

Youwillbegiventwoinputs,asectionofanacademicpaperforcontext,asinglesentencedrawnfromthatsection,andaquestionextractedfromthesentenceaswellasitscorrespondinganswer.Yourtaskistothenturnthequestionintoaself-contained,precisequestion.Approachthistaskstep-by-stepasoutlinedbelow.

Whileyoushoulduseyourexpertiseonthisdomaintohandleandunderstandthesetexts,allinformationwrittenintothequestionsandanswers\*MUST\*originatefromtheprovidedcontextorsentence.Donotadd,infer,orcorrectinformationusingyourinternalknowledge.Everydetailshouldbetraceablebacktothesourcetext.Asyouwriteandrewritethequestions,alsomakesuretoaccuratelyrepresenttheknowledgeintheoriginalsentencewithoutdistortion.Strivetousephrasingascloseaspossibletotheoriginaltext,butprioritizeclarityandself-containment.Lastly,thequestionsshouldbewrittenwellandclearlysothattheyareeasytoread.

###Instructions

Theoverallgoalofthistaskistomakethequestionsclearbyincorporatingtherelevantcontext.Thisensuresthequestionisunambiguousanddoesn’trequirelookingbacktothesourcematerial.

Foreachquestion:

1.Rewritethequestionsothatitstartswithoneofthefollowingtemplates.

-"Inthepaper’{title}’,..."

-"Accordingtothepaper’{title}’,..."

-"Inthepaper’{title}’,theauthorsremarkthat..."

-"Inthepaper’{title}’,theauthorsstatethat..."

-"Accordingtothepaper’{title}’,priorworkhas..."

-"Inthetheoreticalanalysisofthepaper"{title}"..."

-"Inthepaper’{title}’,theresultssuggestthat..."

Thisisanon-exhaustivelistoftemplates,andyoushoulduseyourownjudgementtochoosethemostappropriatetemplateormodifythetemplatetofitthesentence.

2.Addsufficientcontext.Specifically,usethe\*providedcontext\*tosupplywhateverinformationisneededtomakethequestionself-containedandunambiguous.Forinstance,"DohumansandGPT4agreeoftenwitheachother?"shouldbeclarifiedinto"Inthepaper’...’,didhumansandGPT4oftenagreeordisagreewitheachotherduringtheevaluationofDPO?"ifthisnotionwasinthecontextofevaluatingDPOinanacademicpaper.Thegoalistoensuresomeonereadingjustthequestionwouldunderstandexactlywhatisbeingaskedwithoutneedingadditionalcontext.

3.Clarifypronounsandreferentialterms.Checkthesentenceforpronouns(it,this,that,these,those)ordemonstrativephrases(thisequation,thatmethod,theseresults)thatrefertoentitiesnotexplicitlydefinedwithinthesentenceitself.Searchthesurroundingcontexttoidentifywhatthesetermsreference,thenincorporatethatclarifyinginformationintothequestiontomakeitself-contained.

4.ClarifyContext-DependentTerms.Namedentities(e.g.,theorems,equations,propernouns)donotneedclarification.However,ifthereareunnamedorcontext-specificterms(e.g.,$f$,"themodel","theloss"),clarifytheirfullcontext.Forinstance,"thegradient"mightrefertothegeneralconceptofagradientortothegradientofaspecificfunctionmentionedearlierinthecontext.

5.Disambiguateexperiments.Thereareoftennumerousexperimentsinapaper,andsosupplyenoughexperimentalcontextsothatthequestionisaboutwhichexperimentthequestionisaskingabout.

6.Handleacronyms.Iftheanswerisanacronymandtheacronymappearsfrequentlyinthecontext,feelfreetoleaveitasanacronymwithoutdefiningit.

7.Donotleaktheanswer.Pleasemakesurethat\*theanswerisnotrevealed\*inthequestion.Theanswershouldneverappearinthequestion.

8.Maintaintheessenceoftheoriginalquestionduringallofthis.

9.Donotchangetheanswer.Minorgrammaticaladjustmentstotheanswerareallowedonlyifnecessarytofittherestructuredquestion(e.g.,adjustingverbtense,determinerslike"the").

10.Avoidquotingthesourcesentencedirectlyinthequestion.

11.RefineQuestion.Therewrittenquestioncanbebrokenupintomultiplesentencesifthequestionbecomesverbose.Makesurethequestioniswrittenclearlyandgrammaticallycorrect.Donotputanyofthecontextinparenthesisorfollowedafteran"i.e.".

Thinkcarefullyandcriticallythroughthistask,followingthestep-by-stepinstructionsoutlinedabove.Then,providethefinaloutput,listingeachquestionanditscorrespondinganswer.

3\. Prompt to generate inference questions from the text:

[⬇](data:text/plain;base64,WW91IGhhdmUgYmVlbiBnaXZlbiBhIHNlY3Rpb24gb2YgYW4gYWNhZGVtaWMgdGV4dC4gWW91ciB0YXNrcyBpcyB0byB0ZXN0IHRoZSByZWFkZXIncyB1bmRlcnN0YW5kaW5nIG9mIHRoZSB0ZXh0LiBIb3dldmVyLCB5b3Ugc2hvdWxkIG5vdCB0ZXN0IGFueXRoaW5nIHRoYXQgY2FuIGJlIHJlY2FsbGVkIGZyb20gcmVhZGluZyBhIHNpbmdsZSBzZW50ZW5jZS4gQ3JlYXRlIHF1ZXN0aW9ucyB0aGF0IGludGVncmF0ZSwgY29ubmVjdCwgYW5kIHN5bnRoZXNpemUgaW5mb3JtYXRpb24gYWNyb3NzIHNldmVyYWwgc2VudGVuY2VzIGFuZCBhaW0gYXQgbWVhc3VyaW5nIGEgZGVlcGVyIHVuZGVyc3RhbmRpbmcuIFlvdXIgcXVlc3Rpb24gbXVzdCBub3QgYmUgb2J2aW91cyBmcm9tIGEgc2luZ2xlIHNlbnRlbmNlIGFscmVhZHkgaW4gdGhlIHBhcGVyLCBhbmQgdHJ1bHkgcmVxdWlyZSBzZXZlcmFsIHNlbnRlbmNlcyB0byBzeW50aGVzaXplIHRoZSBhbnN3ZXIuIExhc3RseSwgdGhlIGFuc3dlciB0byB0aGUgcXVlc3Rpb24gbXVzdCBiZSBhIGNvaGVyZW50IHBocmFzZSwgZnJvbSAxIHRvIDUgd29yZHMgbG9uZy4KCkZvciBlYWNoIHF1ZXN0aW9uLCBzaG93IG1lIHRoZSBzZW50ZW5jZXMgaW4gdGhlIHRleHQgdGhhdCB5b3UncmUgcHVsbGluZyBmcm9tIHRvIGFuc3dlciB0aGUgcXVlc3Rpb24uIFRoZSBxdWVzdGlvbiBzaG91bGQgYmUgbm9uLW9idmlvdXMgZnJvbSB0aGVzZSBzZW50ZW5jZXMgYW5kIHJlcXVpcmUgY29tcG9zaW5nIGluZm9ybWF0aW9uIGZyb20gYWxsIG9mIHRoZW0gdG8gYW5zd2VyIHRoZSBxdWVzdGlvbi4KClByb3ZpZGUgdGhlIG91dHB1dCBpbiBKU09OIGZvcm1hdCwgYXMgYSBkaWN0aW9uYXJ5IHdpdGggYSBzaW5nbGUga2V5ICJxYV9pdGVtcyIgd2hpY2ggaXMgYSBsaXN0IG9mIGRpY3Rpb25hcmllcyB3aXRoIHRoZSBmb2xsb3dpbmcga2V5czoKLSAicXVlc3Rpb24iOiAoc3RyaW5nKSAKLSAiYW5zd2VyIjogKHN0cmluZykKLSAidGV4dF9xdW90ZXMiOiBsaXN0IG9mIHNlbnRlbmNlcyBmcm9tIHRoZSB0ZXh0IHRoYXQgeW91J3JlIHB1bGxpbmcgZnJvbSB0byBhbnN3ZXIgdGhlIHF1ZXN0aW9uLg==)

Youhavebeengivenasectionofanacademictext.Yourtasksistotestthereader’sunderstandingofthetext.However,youshouldnottestanythingthatcanberecalledfromreadingasinglesentence.Createquestionsthatintegrate,connect,andsynthesizeinformationacrossseveralsentencesandaimatmeasuringadeeperunderstanding.Yourquestionmustnotbeobviousfromasinglesentencealreadyinthepaper,andtrulyrequireseveralsentencestosynthesizetheanswer.Lastly,theanswertothequestionmustbeacoherentphrase,from1to5wordslong.

Foreachquestion,showmethesentencesinthetextthatyou’repullingfromtoanswerthequestion.Thequestionshouldbenon-obviousfromthesesentencesandrequirecomposinginformationfromallofthemtoanswerthequestion.

ProvidetheoutputinJSONformat,asadictionarywithasinglekey"qa\_items"whichisalistofdictionarieswiththefollowingkeys:

-"question":(string)

-"answer":(string)

-"text\_quotes":listofsentencesfromthetextthatyou’repullingfromtoanswerthequestion.

## Appendix G Prompts for Synthetic Data Generation (arXiv)

1\. Prompt to synthesize Stack Exchange–style question–answer pairs:

Question generation:

[⬇](data:text/plain;base64,WW91IGFyZSBhIGNvbmZ1c2VkIHN0dWRlbnQgcmVhZGluZyB0aGlzIHJlc2VhcmNoIHBhcGVyLiBZb3UgYXJlIHN0cnVnZ2xpbmcgd2l0aCBzcGVjaWZpYyBjb25jZXB0cywgZGV0YWlscywgYW5kIGNvbm5lY3Rpb25zIGluIHRoaXMgcGFwZXIuIEdlbmVyYXRlIGEgbGlzdCBvZiBzZXZlcmFsIFN0YWNrIEV4Y2hhbmdlIHN0eWxlIHF1ZXN0aW9ucyB0aGF0IHlvdSB3b3VsZCBhc2sgdG8gY2xhcmlmeSB5b3VyIHVuZGVyc3RhbmRpbmcuCgpZb3VyIHF1ZXN0aW9ucyBzaG91bGQ6Ci0gVmFyeSBpbiBsZXZlbHMgb2YgdW5kZXJzdGFuZGluZywgZnJvbSBtaXNsZWQgdG8gcHJvZm91bmQuCi0gVmFyeSBpbiBjb21wbGV4aXR5LCBmcm9tIHNpbXBsZSB0byBkZWVwLgotIFZhcnkgaW4gdHlwZSwgZnJvbSBjb25jZXB0dWFsIHRvIGRldGFpbC1zcGVjaWZpYy4KLSBGb2N1cyBvbiBjbGFyaWZ5aW5nIHRoZSBjb25jZXB0cyBhbmQgZGV0YWlscyBvZiB0aGUgcGFwZXIuIERvIG5vdCBhc2sgdGFuZ2VudGlhbCBxdWVzdGlvbnMuCgpBcyB5b3UgZ2VuZXJhdGUgdGhlIHF1ZXN0aW9ucywgcGxlYXNlIG1ha2Ugc3VyZSB0byBjb25zaWRlciB0aGUgZm9sbG93aW5nOgotIE1ha2Ugc3VyZSB0aGUgcXVlc3Rpb25zIGFyZSBzZWxmLWNvbnRhaW5lZCBhbmQgdW5hbWJpZ3VvdXMKLSBQbGVhc2Ugd3JpdGUgYW55IG1hdGhlbWF0aWNhbCBub3RhdGlvbiBpbiBMYVRlWCBvbmx5IGUuZy4gIiR4XjIkIiBvciAiJFxwaSQiLiBEbyBub3QgdXNlIHVuaWNvZGUgbWF0aGVtYXRpY2FsIGNoYXJhY3RlcnMgZS5nLiAicGkiLgoKRm9yIGVhY2ggcXVlc3Rpb24sIHByb3ZpZGU6Ci0gQSBgdGl0bGVgIGluIFN0YWNrIEV4Y2hhbmdlIHF1ZXN0aW9uIGZvcm1hdAotIFRoZSBgcXVlc3Rpb25fYm9keWAgd2l0aCBjb250ZXh0IGFuZCB3aGF0IHNwZWNpZmljYWxseSB5b3UncmUgY29uZnVzZWQgYWJvdXQKCiMjIEV4YW1wbGUgUXVlc3Rpb24KCiJIb3cgY2FuIFRyYW5zZm9ybWVycyBoYW5kbGUgYXJiaXRyYXJ5IGxlbmd0aCBpbnB1dD8KClRoZSB0cmFuc2Zvcm1lciwgaW50cm9kdWNlZCBpbiB0aGUgcGFwZXIgQXR0ZW50aW9uIElzIEFsbCBZb3UgTmVlZCwgaXMgYSBwb3B1bGFyIG5ldyBuZXVyYWwgbmV0d29yayBhcmNoaXRlY3R1cmUgdGhhdCBpcyBjb21tb25seSB2aWV3ZWQgYXMgYW4gYWx0ZXJuYXRpdmUgdG8gcmVjdXJyZW50IG5ldXJhbCBuZXR3b3JrcywgbGlrZSBMU1RNcyBhbmQgR1JVcy4KCkhvd2V2ZXIsIGhhdmluZyBnb25lIHRocm91Z2ggdGhlIHBhcGVyLCBhcyB3ZWxsIGFzIHNldmVyYWwgb25saW5lIGV4cGxhbmF0aW9ucywgSSBzdGlsbCBoYXZlIHRyb3VibGUgd3JhcHBpbmcgbXkgaGVhZCBhcm91bmQgaG93IHRoZXkgd29yay4iCgojIyMgT3V0cHV0IEZvcm1hdApQcm92aWRlIHRoZSBvdXRwdXQgYXMgYSBKU09OIG9iamVjdCB3aXRoIGEgc2luZ2xlIGtleSAicXVlc3Rpb25zIiwgd2hpY2ggaXMgYSBsaXN0IG9mIHF1ZXN0aW9uIGRpY3Rpb25hcmllcy4KRXhhbXBsZToKewogICJxdWVzdGlvbnMiOiBbCiAgICB7CiAgICAgICJ0aXRsZSI6ICJXaHkgZG9lcyB0aGUgcGFydGl0aW9uIGZ1bmN0aW9uIGNhbmNlbCBvdXQgaW4gRFBPIGRlcml2YXRpb24/IiwKICAgICAgInF1ZXN0aW9uX2JvZHkiOiAiSSdtIHJlYWRpbmcgdGhlIERQTyBwYXBlciBhbmQgSSB1bmRlcnN0YW5kIHRoYXQgdGhleSBzdGFydCB3aXRoIHRoZSBLTC1yZWd1bGFyaXplZCBvYmplY3RpdmUsIGJ1dCBJJ20gY29uZnVzZWQgYWJvdXQgaG93IHRoZSBwYXJ0aXRpb24gZnVuY3Rpb24gWih4KSBjYW5jZWxzIG91dCB3aGVuIHRoZXkgbW92ZSB0byBwYWlyd2lzZSBwcmVmZXJlbmNlcy4gQ2FuIHNvbWVvbmUgZXhwbGFpbiB0aGlzIHN0ZXAgaW50dWl0aXZlbHk/IiwKICAgIH0KICBdCn0=)

Youareaconfusedstudentreadingthisresearchpaper.Youarestrugglingwithspecificconcepts,details,andconnectionsinthispaper.GeneratealistofseveralStackExchangestylequestionsthatyouwouldasktoclarifyyourunderstanding.

Yourquestionsshould:

-Varyinlevelsofunderstanding,frommisledtoprofound.

-Varyincomplexity,fromsimpletodeep.

-Varyintype,fromconceptualtodetail-specific.

-Focusonclarifyingtheconceptsanddetailsofthepaper.Donotasktangentialquestions.

Asyougeneratethequestions,pleasemakesuretoconsiderthefollowing:

-Makesurethequestionsareself-containedandunambiguous

-PleasewriteanymathematicalnotationinLaTeXonlye.g."$x^2$"or"$\pi$".Donotuseunicodemathematicalcharacterse.g."pi".

Foreachquestion,provide:

-A‘title‘inStackExchangequestionformat

-The‘question\_body‘withcontextandwhatspecificallyyou’reconfusedabout

##ExampleQuestion

"HowcanTransformershandlearbitrarylengthinput?

Thetransformer,introducedinthepaperAttentionIsAllYouNeed,isapopularnewneuralnetworkarchitecturethatiscommonlyviewedasanalternativetorecurrentneuralnetworks,likeLSTMsandGRUs.

However,havinggonethroughthepaper,aswellasseveralonlineexplanations,Istillhavetroublewrappingmyheadaroundhowtheywork."

###OutputFormat

ProvidetheoutputasaJSONobjectwithasinglekey"questions",whichisalistofquestiondictionaries.

Example:

{

"questions":\[\
\
{\
\
"title":"WhydoesthepartitionfunctioncanceloutinDPOderivation?",\
\
"question\_body":"I’mreadingtheDPOpaperandIunderstandthattheystartwiththeKL-regularizedobjective,butI’mconfusedabouthowthepartitionfunctionZ(x)cancelsoutwhentheymovetopairwisepreferences.Cansomeoneexplainthisstepintuitively?",\
\
}\
\
\]

}

Answer generation:

[⬇](data:text/plain;base64,QSBncmFkdWF0ZSBzdHVkZW50IGhhcyBhc2tlZCBhIHF1ZXN0aW9uIGFib3V0IGEgcmVzZWFyY2ggcGFwZXIuIFByb3ZpZGUgYSBjbGVhciwgZGV0YWlsZWQgU3RhY2sgRXhjaGFuZ2Ugc3R5bGUgYW5zd2VyIHRoYXQ6CgotIFRob3JvdWdobHkgYWRkcmVzc2VzIHRoZWlyIHF1ZXN0aW9uIAotIERvbid0IG1ha2UgaXQgdG9vIGxlbmd0aHk7IGl0IHNob3VsZCBiZSBjb25jaXNlIGFuZCB0byB0aGUgcG9pbnQgbGlrZSBhIFN0YWNrIEV4Y2hhbmdlIGFuc3dlcgotIFdyaXRlIGluIHByb3NlIHJhdGhlciB0aGFuIHN0cnVjdHVyZWQgYnVsbGV0IHBvaW50cyBpbiBvbmUgY29oZXNpdmUgYW5zd2VyCi0gUHJvdmlkZXMgaW50dWl0aXZlIGV4cGxhbmF0aW9ucyBhbG9uZ3NpZGUgdGVjaG5pY2FsIGRldGFpbHMKLSBDb25uZWN0cyB0byBicm9hZGVyIGNvbmNlcHRzIHdoZW4gcmVsZXZhbnQKLSBJcyBlZHVjYXRpb25hbCBhbmQgYWNjZXNzaWJsZQoKUGxlYXNlIHdyaXRlIGFueSBtYXRoZW1hdGljYWwgbm90YXRpb24gaW4gTGFUZVggb25seSBlLmcuICIkeF4yJCIgb3IgIiRccGkkIi4gRG8gbm90IHVzZSB1bmljb2RlIG1hdGhlbWF0aWNhbCBjaGFyYWN0ZXJzIGUuZy4gInBpIi4gQWxzbywgcGxlYXNlIG1ha2Ugc3VyZSB0aGF0IHlvdXIgYW5zd2VyIGlzIGdyb3VuZGVkIGluIHRoZSBwYXBlcjsgZG8gbm90IHByb3ZpZGUgYW55IGluZm9ybWF0aW9uIHRoYXQgaXMgaW5jb25zaXN0ZW50IHdpdGggdGhlIHBhcGVyLgoKQWdhaW4sIHBsZWFzZSB3cml0ZSBhbGwgbWF0aCBpbiBMYVRlWC4KCkZvcm1hdCB5b3VyIHJlc3BvbnNlIGFzIGEgY29tcHJlaGVuc2l2ZSBTdGFjayBFeGNoYW5nZSBhbnN3ZXIuCgojIyMgRXhhbXBsZQoKUXVlc3Rpb246CiJJIGtub3cgdGhhdCBpbiB0aGUgbWF0aCBvbiB3aGljaCB0aGUgdHJhbnNmb3JtZXIgaXMgYmFzZWQgdGhlcmUgaXMgbm8gcmVzdHJpY3Rpb24gb24gdGhlIGxlbmd0aCBvZiBpbnB1dC4gQnV0IEkgc3RpbGwgY2FuJ3QgdW5kZXJzdGFuZCB3aHkgd2Ugc2hvdWxkIGZpeCBpdCBpbiB0aGUgZnJhbWV3b3JrcyAoUHlUb3JjaCkuIEJlY2F1c2Ugb2YgdGhpcyBwcm9ibGVtIFRyYW5zZm9ybWVyLVhMIGhhcyBiZWVuIGNyZWF0ZWQuCgpDYW4geW91IGV4cGxhaW4gdG8gbWUgd2hlcmUgdGhpcyBwcm9ibGVtIGlzIGhpZGluZywgcGxlYXNlPyIKCkFuc3dlcjoKIlRoZSByZXN0cmljdGlvbiBpbiB0aGUgbWF4aW11bSBsZW5ndGggb2YgdGhlIHRyYW5zZm9ybWVyIGlucHV0IGlzIGR1ZSB0byB0aGUgbmVlZGVkIGFtb3VudCBvZiBtZW1vcnkgdG8gY29tcHV0ZSB0aGUgc2VsZi1hdHRlbnRpb24gb3ZlciBpdC4KClRoZSBhbW91bnQgb2YgbWVtb3J5IG5lZWRlZCBieSB0aGUgc2VsZi1hdHRlbnRpb24gaW4gdGhlIFRyYW5zZm9ybWVyIGlzIHF1YWRyYXRpYyBvbiB0aGUgbGVuZ3RoIG9mIHRoZSBpbnB1dC4gVGhpcyBtZWFucyB0aGF0IGluY3JlYXNpbmcgdGhlIG1heGltdW0gbGVuZ3RoIG9mIHRoZSBpbnB1dCwgaW5jcmVhc2VzIGRyYXN0aWNhbGx5IHRoZSBuZWVkZWQgbWVtb3J5IGZvciBzZWxmLWF0dGVudGlvbi4gVGhlIG1heGltdW0gbGVuZ3RoIGlzIHRoYXQgd2hpY2ggbWFrZXMgdGhlIG1vZGVsIHVzZSB1cCB0aGUgd2hvbGUgbWVtb3J5IG9mIHRoZSBHUFUgZm9yIGF0IGxlYXN0IG9uZSBzZW50ZW5jZSAob25jZSB0aGUgb3RoZXIgZWxlbWVudHMgb2YgdGhlIG1vZGVsIGFyZSBhbHNvIHRha2VuIGludG8gYWNjb3VudCwgbGlrZSB0aGUgZW1iZWRkaW5ncyB3aGljaCB0YWtlIGEgbG90IG9mIG1lbW9yeSkuCgpUcmFuc2Zvcm1lci1YTCBpcyBjZXJ0YWlubHkgYSB3YXkgdG8gdGFrZSBpbnRvIGFjY291bnQgYXMgbXVjaCBjb250ZXh0IGFzIHBvc3NpYmxlIGluIGxhbmd1YWdlIG1vZGVsaW5nIChpdHMgcm9sZSBpcyBhbmFsb2dvdXMgdG8gdHJ1bmNhdGVkIGJhY2stcHJvcGFnYXRpb24gdGhyb3VnaCB0aW1lIGluIExTVE0gbGFuZ3VhZ2UgbW9kZWxzKS4gSG93ZXZlciwgdGhlIGdyYWRpZW50cyBhcmUgbm90IHByb3BhZ2F0ZWQgdGhyb3VnaCB0aGUgYXR0ZW50aW9uIG92ZXIgdGhlIG1lbW9yeSBzZWdtZW50LCBvbmx5IHRocm91Z2ggdGhlIGN1cnJlbnQgc2VnbWVudC4KClRoZXJlIGhhdmUgYmVlbiBzZXZlcmFsIGFyY2hpdGVjdHVyYWwgYXR0ZW1wdHMgdG8gcmVkdWNlIHRoZSBhbW91bnQgb2YgbWVtb3J5IG5lZWRlZCBieSB0cmFuc2Zvcm1lcnMsIGxpa2UgdXNpbmcgbG9jYWxpdHktY29uc3RyYWludHMgaW4gdGhlIGF0dGVudGlvbiAoRHluYW1pYyBDb252b2x1dGlvbnMgbW9kZWwpIG9yIHVzaW5nIGxvY2FsaXR5LXNlbnNpdGl2ZSBoYXNoaW5nIChSZWZvcm1lciBtb2RlbCkuCgpUaGVyZSBoYXZlIGJlZW4gb3RoZXIgaW1wbGVtZW50YXRpb24gYXR0ZW1wdHMsIGxpa2UgZ3JhZGllbnQgY2hlY2twb2ludGluZyhlLmcuIHRoaXMpLCB3aGljaCBpcyBhIGdlbmVyYWwgdGVjaG5pcXVlIHRvIHJ1biBjb21wdXRhdGlvbnMgdGhhdCBkb24ndCBmaXQgYXQgb25jZSBpbiB0aGUgR1BVIG1lbW9yeSI=)

Agraduatestudenthasaskedaquestionaboutaresearchpaper.Provideaclear,detailedStackExchangestyleanswerthat:

-Thoroughlyaddressestheirquestion

-Don’tmakeittoolengthy;itshouldbeconciseandtothepointlikeaStackExchangeanswer

-Writeinproseratherthanstructuredbulletpointsinonecohesiveanswer

-Providesintuitiveexplanationsalongsidetechnicaldetails

-Connectstobroaderconceptswhenrelevant

-Iseducationalandaccessible

PleasewriteanymathematicalnotationinLaTeXonlye.g."$x^2$"or"$\pi$".Donotuseunicodemathematicalcharacterse.g."pi".Also,pleasemakesurethatyouranswerisgroundedinthepaper;donotprovideanyinformationthatisinconsistentwiththepaper.

Again,pleasewriteallmathinLaTeX.

FormatyourresponseasacomprehensiveStackExchangeanswer.

###Example

Question:

"Iknowthatinthemathonwhichthetransformerisbasedthereisnorestrictiononthelengthofinput.ButIstillcan’tunderstandwhyweshouldfixitintheframeworks(PyTorch).BecauseofthisproblemTransformer-XLhasbeencreated.

Canyouexplaintomewherethisproblemishiding,please?"

Answer:

"Therestrictioninthemaximumlengthofthetransformerinputisduetotheneededamountofmemorytocomputetheself-attentionoverit.

Theamountofmemoryneededbytheself-attentionintheTransformerisquadraticonthelengthoftheinput.Thismeansthatincreasingthemaximumlengthoftheinput,increasesdrasticallytheneededmemoryforself-attention.ThemaximumlengthisthatwhichmakesthemodeluseupthewholememoryoftheGPUforatleastonesentence(oncetheotherelementsofthemodelarealsotakenintoaccount,liketheembeddingswhichtakealotofmemory).

Transformer-XLiscertainlyawaytotakeintoaccountasmuchcontextaspossibleinlanguagemodeling(itsroleisanalogoustotruncatedback-propagationthroughtimeinLSTMlanguagemodels).However,thegradientsarenotpropagatedthroughtheattentionoverthememorysegment,onlythroughthecurrentsegment.

Therehavebeenseveralarchitecturalattemptstoreducetheamountofmemoryneededbytransformers,likeusinglocality-constraintsintheattention(DynamicConvolutionsmodel)orusinglocality-sensitivehashing(Reformermodel).

Therehavebeenotherimplementationattempts,likegradientcheckpointing(e.g.this),whichisageneraltechniquetoruncomputationsthatdon’tfitatonceintheGPUmemory"

LaTeX formatting refinement:

[⬇](data:text/plain;base64,WW91IHdpbGwgYmUgZ2l2ZW4gYSB0ZXh0LiBZb3VyIG9ubHkgdGFzayBpcyB0byBjb3JyZWN0IGFueSBtYXRoZW1hdGljYWwgbm90YXRpb24gaW5zaWRlIGl0IHRvIGJlIHZhbGlkIExhVGVYLiBZb3UgbXVzdCBub3QgY2hhbmdlIGFueSBvdGhlciBwYXJ0IG9mIHRoZSB0ZXh0LgogICAgLSBDb252ZXJ0IHVuaWNvZGUgbWF0aCBjaGFyYWN0ZXJzIGxpa2UgJ3BpJyB0byB0aGVpciBMYVRlWCBlcXVpdmFsZW50ICckXFxwaSQnLgogICAgLSBFbnN1cmUgYWxsIG1hdGhlbWF0aWNhbCBleHByZXNzaW9ucyBhcmUgZW5jbG9zZWQgaW4gJyQuLi4kJyBmb3IgaW5saW5lIG1hdGggb3IgJyQkLi4uJCQnIGZvciBkaXNwbGF5IG1hdGguCiAgICAtIFJldHVybiB0aGUgZnVsbCwgY29ycmVjdGVkIHRleHQu)

Youwillbegivenatext.YouronlytaskistocorrectanymathematicalnotationinsideittobevalidLaTeX.Youmustnotchangeanyotherpartofthetext.

-Convertunicodemathcharacterslike’pi’totheirLaTeXequivalent’$\\\pi$’.

-Ensureallmathematicalexpressionsareenclosedin’$...$’forinlinemathor’$$...$$’fordisplaymath.

-Returnthefull,correctedtext.

2\. Prompt to synthesize textbook-style explanations:

Textbook outline generation:

[⬇](data:text/plain;base64,IyMjIEluc3RydWN0aW9ucwpZb3Ugd2lsbCBiZSBnaXZlbiBhIHJlc2VhcmNoIHBhcGVyIGFuZCB5b3VyIHRhc2sgaXMgdG8gY3JlYXRlIGEgZGV0YWlsZWQgb3V0bGluZSBmb3IgYSB0ZXh0Ym9vayB0aGF0IGNvbXByZWhlbnNpdmVseSBleHBsYWlucyB0aGUgZ2l2ZW4gcmVzZWFyY2ggcGFwZXIuIEJ1dCwgaXQgc2hvdWxkIGdvIGJleW9uZCBtZXJlIGV4cGxhaW5pbmcsIGFuZCBiZSBhIHByb3BlciBwZWRhZ29naWNhbCB0ZXh0Ym9vayB0aGF0IGFpbXMgdG8gZnVsbHkgZWR1Y2F0ZSB0aGUgcmVhZGVyIG9uIHdoYXQgdGhlIHBhcGVyIGlzIGFib3V0LiBUaGUgdGV4dGJvb2sgc2hvdWxkIGJlIGFpbWVkIGF0IGNvbGxlZ2Ugc3R1ZGVudHMgd2hvIGhhdmUgYSBiYXNpYyB1bmRlcnN0YW5kaW5nIG9mIG1hY2hpbmUgbGVhcm5pbmcuCgpUaGUgb3V0bGluZSBzaG91bGQ6Ci0gQnJlYWsgZG93biB0aGUgcGFwZXIgaW50byBjb2hlcmVudCBjaGFwdGVycy4KLSBGb3IgZWFjaCBjaGFwdGVyLCBwcm92aWRlIGE6CiAgICAtIHRpdGxlCiAgICAtIGRlc2NyaXB0aW9uCiAgICAtIGxpc3Qgb2Ygc3VidG9waWNzIHRvIGNvdmVyCi0gQ292ZXIgYWxsIGtleSBjb25jZXB0cywgbWV0aG9kcywgYW5kIHJlc3VsdHMgZnJvbSB0aGUgcGFwZXIuCi0gRW5zdXJlIGEgbG9naWNhbCBmbG93IG9mIGluZm9ybWF0aW9uLCBmcm9tIGludHJvZHVjdGlvbiB0byBjb25jbHVzaW9uLgotIFdoaWxlIHRoZSB0ZXh0Ym9vayBzaG91bGQgYmUgY29tcHJlaGVuc2l2ZSwgaXQgc2hvdWxkIGFsc28gYXJ0aWN1bGF0ZSBhbmQgdG8gdGhlIHBvaW50LiBEb24ndCBjcmVhdGUgdW5uZWNlc3NhcnkgY2hhcHRlcnMuCgojIyMgT3V0cHV0IEZvcm1hdApQcm92aWRlIHRoZSBvdXRwdXQgYXMgYSBKU09OIG9iamVjdCB3aXRoIGEgc2luZ2xlIGtleSAib3V0bGluZSIsIHdoaWNoIGlzIGEgbGlzdCBvZiBjaGFwdGVyIG9iamVjdHMuIEVhY2ggY2hhcHRlciBvYmplY3QgbXVzdCBoYXZlIHRoZSBmb2xsb3dpbmcga2V5czoKLSAiY2hhcHRlcl90aXRsZSI6IEEgc3RyaW5nIGZvciB0aGUgdGl0bGUgb2YgdGhlIGNoYXB0ZXIuCi0gImRlc2NyaXB0aW9uIjogQSBzdHJpbmcgZGVzY3JpYmluZyB0aGUgY2hhcHRlcidzIGNvbnRlbnQuCi0gInN1YnRvcGljcyI6IEEgbGlzdCBvZiBzdHJpbmdzLCB3aGVyZSBlYWNoIHN0cmluZyBpcyBhIHN1YnRvcGljLg==)

###Instructions

Youwillbegivenaresearchpaperandyourtaskistocreateadetailedoutlineforatextbookthatcomprehensivelyexplainsthegivenresearchpaper.But,itshouldgobeyondmereexplaining,andbeaproperpedagogicaltextbookthataimstofullyeducatethereaderonwhatthepaperisabout.Thetextbookshouldbeaimedatcollegestudentswhohaveabasicunderstandingofmachinelearning.

Theoutlineshould:

-Breakdownthepaperintocoherentchapters.

-Foreachchapter,providea:

-title

-description

-listofsubtopicstocover

-Coverallkeyconcepts,methods,andresultsfromthepaper.

-Ensurealogicalflowofinformation,fromintroductiontoconclusion.

-Whilethetextbookshouldbecomprehensive,itshouldalsoarticulateandtothepoint.Don’tcreateunnecessarychapters.

###OutputFormat

ProvidetheoutputasaJSONobjectwithasinglekey"outline",whichisalistofchapterobjects.Eachchapterobjectmusthavethefollowingkeys:

-"chapter\_title":Astringforthetitleofthechapter.

-"description":Astringdescribingthechapter’scontent.

-"subtopics":Alistofstrings,whereeachstringisasubtopic.

Chapter generation:

[⬇](data:text/plain;base64,IyMjIEluc3RydWN0aW9ucwpZb3Ugd2lsbCBiZSBnaXZlbiBhIGNoYXB0ZXIgdGl0bGUsIGRlc2NyaXB0aW9uLCBhbmQgc3VidG9waWNzIGFuZCwgYmFzZWQgb24gdGhvc2UgdG9waWNzLCB5b3VyIGpvYiBpcyB0byB3cml0ZSBhIGRldGFpbGVkLCBjb2hlc2l2ZSB0ZXh0Ym9vayBjaGFwdGVyIGFkZHJlc3NlZCB0byBhIGNvbGxlZ2Ugc3R1ZGVudCB3aG8gaXMgbGVhcm5pbmcgdGhpcyBtYXRlcmlhbCBmb3IgdGhlIGZpcnN0IHRpbWUuIAoKVGhlIGNoYXB0ZXIgc2hvdWxkIGJlIGNvbXByZWhlbnNpdmUgYW5kIHN1aXRhYmxlIGZvciBzb21lb25lIGxlYXJuaW5nIHRoaXMgbWF0ZXJpYWwgdG8gdW5kZXJzdGFuZCByZXNlYXJjaCBwYXBlcnMgaW4gdGhlIGZpZWxkLiBEb24ndCBqdXN0IGJyaWVmbHkgZGVzY3JpYmUgdGhlIHN1YnRvcGljcywgYnV0IHJhdGhlciBlbGFib3JhdGUgb24gdGhlIGNvbmNlcHRzIGF0IGZ1bGwgbGVuZ3RoIGFuZCBleHBsYWluIHRoZW0gd2l0aCBhIGZvY3VzIG9uIGludHVpdGlvbi4gU3BlbGwgZXZlcnl0aGluZyBvdXQgY2xlYXJseSBzbyB0aGVyZSBpcyBubyBhbWJpZ3VpdHkuIERlZGljYXRlIG11bHRpcGxlIHBhcmFncmFwaHMgdG8gZWFjaCBzdWJ0b3BpYyBidXQgYmUgYXJ0aWN1bGF0ZSBhbmQgY29uY2lzZSB3aGVuIGFwcHJvcHJpYXRlLiBXcml0ZSBpbiBmdWxsIHByb3NlLCByYXRoZXIgdGhhbiBidWxsZXQgcG9pbnRzLiBNb3N0IGltcG9ydGFudGx5LCBwbGVhc2UgbWFrZSBzdXJlIHRoYXQgeW91ciBjaGFwdGVyIGlzIGdyb3VuZGVkIGluIHRoZSBwYXBlcjsgZG8gbm90IHByb3ZpZGUgYW55IGluZm9ybWF0aW9uIG9yIGRldGFpbHMgdGhhdCBpcyBub3QgZnJvbSB0aGUgcGFwZXIuCgpTdGFydCB3aXRoIHRoZSBjaGFwdGVyIHRpdGxlIGluIHRoZSBmaXJzdCBsaW5lLiBTZXBhcmF0ZSBlYWNoIHN1YnRvcGljIHdpdGggYSBzZWN0aW9uIGhlYWRlciAiIyIuIEFsc28sIHBsZWFzZSB3cml0ZSBhbGwgbWF0aGVtYXRpY2FsIG5vdGF0aW9uIGluIExhVGVYIG9ubHkgZS5nLiAiJHheMiQiIG9yICIkXHBpJCIuIERvIG5vdCB1c2UgdW5pY29kZSBtYXRoZW1hdGljYWwgY2hhcmFjdGVycyBlLmcuICJwaSIuIEFnYWluLCBQTEVBU0Ugd3JpdGUgYWxsIG1hdGggaW4gTGFUZVgu)

###Instructions

Youwillbegivenachaptertitle,description,andsubtopicsand,basedonthosetopics,yourjobistowriteadetailed,cohesivetextbookchapteraddressedtoacollegestudentwhoislearningthismaterialforthefirsttime.

Thechaptershouldbecomprehensiveandsuitableforsomeonelearningthismaterialtounderstandresearchpapersinthefield.Don’tjustbrieflydescribethesubtopics,butratherelaborateontheconceptsatfulllengthandexplainthemwithafocusonintuition.Spelleverythingoutclearlysothereisnoambiguity.Dedicatemultipleparagraphstoeachsubtopicbutbearticulateandconcisewhenappropriate.Writeinfullprose,ratherthanbulletpoints.Mostimportantly,pleasemakesurethatyourchapterisgroundedinthepaper;donotprovideanyinformationordetailsthatisnotfromthepaper.

Startwiththechaptertitleinthefirstline.Separateeachsubtopicwithasectionheader"#".Also,pleasewriteallmathematicalnotationinLaTeXonlye.g."$x^2$"or"$\pi$".Donotuseunicodemathematicalcharacterse.g."pi".Again,PLEASEwriteallmathinLaTeX.

3\. Prompt to synthesize blog-post-style explanations:

Blog post idea generation:

[⬇](data:text/plain;base64,IyMjIEluc3RydWN0aW9ucwpZb3UgYXJlIGEgY3JlYXRpdmUgdGVjaCBibG9nZ2VyIGFuZCBjb250ZW50IHN0cmF0ZWdpc3QuIEJhc2VkIG9uIHRoZSBwcm92aWRlZCByZXNlYXJjaCBwYXBlciwgZ2VuZXJhdGUgYSBsaXN0IG9mIGEgZmV3IGJsb2cgcG9zdHMgdGhhdCBleHBsYWluIHRoZSBwYXBlciBpbiBhIHdheSB0aGF0IGlzIGFjY2Vzc2libGUgdG8gYSB3aWRlciBhdWRpZW5jZS4gVGhleSBzaG91bGQgZWFjaCBmb2N1cyBvbiBhIGRpZmZlcmVudCwgbWFpbiBhc3BlY3Qgb2YgdGhlIHBhcGVyLgoKRm9yIGVhY2ggYmxvZyBpZGVhLCBwcm92aWRlOgotIEEgYHRpdGxlYC4KLSBBIGJyaWVmIGBkZXNjcmlwdGlvbmAgb2Ygd2hhdCB0aGUgYmxvZyBwb3N0IHdpbGwgY292ZXIuCgojIyMgT3V0cHV0IEZvcm1hdApQcm92aWRlIHRoZSBvdXRwdXQgYXMgYSBKU09OIG9iamVjdCB3aXRoIGEgc2luZ2xlIGtleSAiYmxvZ3MiLCB3aGljaCBpcyBhIGxpc3Qgb2YgYmxvZyBvYmplY3RzLiBFYWNoIGJsb2cgb2JqZWN0IG11c3QgaGF2ZSB0aGUgZm9sbG93aW5nIGtleXM6Ci0gInRpdGxlIjogQSBzdHJpbmcgZm9yIHRoZSB0aXRsZSBvZiB0aGUgYmxvZyBwb3N0LgotICJkZXNjcmlwdGlvbiI6IEEgc3RyaW5nIGRlc2NyaWJpbmcgdGhlIGJsb2cgcG9zdCdzIGNvbnRlbnQu)

###Instructions

Youareacreativetechbloggerandcontentstrategist.Basedontheprovidedresearchpaper,generatealistofafewblogpoststhatexplainthepaperinawaythatisaccessibletoawideraudience.Theyshouldeachfocusonadifferent,mainaspectofthepaper.

Foreachblogidea,provide:

-A‘title‘.

-Abrief‘description‘ofwhattheblogpostwillcover.

###OutputFormat

ProvidetheoutputasaJSONobjectwithasinglekey"blogs",whichisalistofblogobjects.Eachblogobjectmusthavethefollowingkeys:

-"title":Astringforthetitleoftheblogpost.

-"description":Astringdescribingtheblogpost’scontent.

Blog post generation:

[⬇](data:text/plain;base64,WW91IHdpbGwgYmUgZ2l2ZW4gYW4gYWNhZGVtaWMgcGFwZXIgYW5kIGEgYmxvZyBwb3N0IGlkZWEgYWJvdXQgdGhlIHBhcGVyLiBXcml0ZSBhIGJsb2cgcG9zdCBiYXNlZCBvbiB0aGUgYmxvZyBpZGVhLgoKQXMgeW91IHdyaXRlIHRoZSBibG9nIHBvc3QsIHBsZWFzZSBtYWtlIHN1cmUgdG8gY29uc2lkZXIgdGhlIGZvbGxvd2luZzoKLSBXcml0ZSBpbiBhIHRlY2huaWNhbCBibG9nIHN0eWxlLiBJdCBzaG91bGQgYmUgbGVzcyBmb3JtYWwgYnV0IG5vdCB0b28gaW5mb3JtYWwuIEl0IHNob3VsZCBiZSBjb25jaXNlIGFuZCB0byB0aGUgcG9pbnQuIAotIFNpbXBsaWZ5IGNvbXBsZXggY29uY2VwdHMgZnJvbSB0aGUgcGFwZXIgZm9yIGEgYnJvYWRlciBhdWRpZW5jZS4KLSBXcml0ZSBpbiBmdWxsLCBjb21wbGV0ZSBzZW50ZW5jZXMgYW5kIHByZWZlciBwYXJhZ3JhcGhzIG92ZXIgYnVsbGV0IHBvaW50cywgYnV0IHVzZSBidWxsZXQgcG9pbnRzIHdoZW4gYXBwcm9wcmlhdGUuCi0gS2VlcCBhbGwgZGV0YWlscyBncm91bmRlZCBpbiB0aGUgcGFwZXIuIERvIG5vdCBtYWtlIHVwIGFueSBpbmZvcm1hdGlvbi4KLSBQbGVhc2Ugd3JpdGUgYW55IG1hdGhlbWF0aWNhbCBub3RhdGlvbiBpbiBMYVRlWCBvbmx5IGUuZy4gIiR4XjIkIiBvciAiJFxwaSQiLiBEbyBub3QgdXNlIHVuaWNvZGUgbWF0aGVtYXRpY2FsIGNoYXJhY3RlcnMgZS5nLiAicGkiLiAKCllvdXIgb3V0cHV0IHNob3VsZCBiZSB0aGUgZnVsbCB0ZXh0IG9mIHRoZSBibG9nIHBvc3QsIHN0YXJ0aW5nIHdpdGggdGhlIGJsb2cgdGl0bGUgYXMgYSBtYXJrZG93biBoZWFkZXIuIFVzZSAnIycgdG8gZGVub3RlIHRoZSBibG9nIHRpdGxlLCAnIyMnIHRvIGRlbm90ZSBkaWZmZXJlbnQgc2VjdGlvbnMsIGFuZCBzbyBvbi4=)

Youwillbegivenanacademicpaperandablogpostideaaboutthepaper.Writeablogpostbasedontheblogidea.

Asyouwritetheblogpost,pleasemakesuretoconsiderthefollowing:

-Writeinatechnicalblogstyle.Itshouldbelessformalbutnottooinformal.Itshouldbeconciseandtothepoint.

-Simplifycomplexconceptsfromthepaperforabroaderaudience.

-Writeinfull,completesentencesandpreferparagraphsoverbulletpoints,butusebulletpointswhenappropriate.

-Keepalldetailsgroundedinthepaper.Donotmakeupanyinformation.

-PleasewriteanymathematicalnotationinLaTeXonlye.g."$x^2$"or"$\pi$".Donotuseunicodemathematicalcharacterse.g."pi".

Youroutputshouldbethefulltextoftheblogpost,startingwiththeblogtitleasamarkdownheader.Use’#’todenotetheblogtitle,’##’todenotedifferentsections,andsoon.

4\. Prompt to generate prerequisite-knowledge chapters:

Prerequisite chapter-list generation:

[⬇](data:text/plain;base64,IyMjIEluc3RydWN0aW9ucwpZb3UgYXJlIGFuIGV4cGVydCBjdXJyaWN1bHVtIGRlc2lnbmVyLiBCYXNlZCBvbiB0aGUgcHJvdmlkZWQgcmVzZWFyY2ggcGFwZXIsIGNyZWF0ZSBhIGxpc3Qgb2YgdGV4dGJvb2sgY2hhcHRlcnMgdGhhdCB3b3VsZCBwcm92aWRlIGFsbCB0aGUgbmVjZXNzYXJ5IHByaW9yIGtub3dsZWRnZSB0byB1bmRlcnN0YW5kIHRoaXMgcGFwZXIuIFRoZSBjaGFwdGVycyBzaG91bGQgbm90IGNvbnRhaW4gdGhlIG5vdmVsIGlkZWFzIHByZXNlbnRlZCBpbiB0aGUgcGFwZXIgaXRzZWxmLCBidXQgcmF0aGVyIHRoZSBmb3VuZGF0aW9uYWwgY29uY2VwdHMgdXBvbiB3aGljaCB0aGUgcGFwZXIgaXMgYnVpbHQuCgpGb3IgZWFjaCBjaGFwdGVyLCBwcm92aWRlOgotIEEgYHRpdGxlYC4KLSBBIGdlbmVyYWwgYGRlc2NyaXB0aW9uYCBvZiB3aGF0IHRoZSBjaGFwdGVyIGNvdmVycy4KLSBBIGxpc3Qgb2YgYHN1YnRvcGljc2AgdGhhdCBzaG91bGQgYmUgaW5jbHVkZWQuCgojIyMgT3V0cHV0IEZvcm1hdApQcm92aWRlIHRoZSBvdXRwdXQgYXMgYSBKU09OIG9iamVjdCB3aXRoIGEgc2luZ2xlIGtleSAiY2hhcHRlcnMiLCB3aGljaCBpcyBhIGxpc3Qgb2YgY2hhcHRlciBkaWN0aW9uYXJpZXMuCkV4YW1wbGU6CnsKICAiY2hhcHRlcnMiOiBbCiAgICB7CiAgICAgICJ0aXRsZSI6ICJDaGFwdGVyIDE6IEludHJvZHVjdGlvbiB0byBQcm9iYWJpbGl0eSBUaGVvcnkiLAogICAgICAiZGVzY3JpcHRpb24iOiAiVGhpcyBjaGFwdGVyIGNvdmVycyB0aGUgYmFzaWNzIG9mIHByb2JhYmlsaXR5Li4uIiwKICAgICAgInN1YnRvcGljcyI6IFsiUmFuZG9tIFZhcmlhYmxlcyIsICJQcm9iYWJpbGl0eSBEaXN0cmlidXRpb25zIiwgIkJheWVzJyBUaGVvcmVtIl0KICAgIH0KICBdCn0=)

###Instructions

Youareanexpertcurriculumdesigner.Basedontheprovidedresearchpaper,createalistoftextbookchaptersthatwouldprovideallthenecessarypriorknowledgetounderstandthispaper.Thechaptersshouldnotcontainthenovelideaspresentedinthepaperitself,butratherthefoundationalconceptsuponwhichthepaperisbuilt.

Foreachchapter,provide:

-A‘title‘.

-Ageneral‘description‘ofwhatthechaptercovers.

-Alistof‘subtopics‘thatshouldbeincluded.

###OutputFormat

ProvidetheoutputasaJSONobjectwithasinglekey"chapters",whichisalistofchapterdictionaries.

Example:

{

"chapters":\[\
\
{\
\
"title":"Chapter1:IntroductiontoProbabilityTheory",\
\
"description":"Thischaptercoversthebasicsofprobability...",\
\
"subtopics":\["RandomVariables","ProbabilityDistributions","Bayes’Theorem"\]\
\
}\
\
\]

}

Chapter generation:

[⬇](data:text/plain;base64,IyMjIEluc3RydWN0aW9ucwpZb3Ugd2lsbCBiZSBnaXZlbiBhIGNoYXB0ZXIgdGl0bGUsIGRlc2NyaXB0aW9uLCBhbmQgc3VidG9waWNzIGFuZCwgYmFzZWQgb24gdGhvc2UgdG9waWNzLCB5b3VyIGpvYiBpcyB0byB3cml0ZSBhIGRldGFpbGVkLCBjb2hlc2l2ZSB0ZXh0Ym9vayBjaGFwdGVyIGFkZHJlc3NlZCB0byBhIGNvbGxlZ2Ugc3R1ZGVudCB3aG8gaXMgbGVhcm5pbmcgdGhpcyBtYXRlcmlhbCBmb3IgdGhlIGZpcnN0IHRpbWUuIAoKVGhlIGNoYXB0ZXIgc2hvdWxkIGJlIGNvbXByZWhlbnNpdmUgYW5kIHN1aXRhYmxlIGZvciBzb21lb25lIGxlYXJuaW5nIHRoaXMgbWF0ZXJpYWwgdG8gdW5kZXJzdGFuZCByZXNlYXJjaCBwYXBlcnMgaW4gdGhlIGZpZWxkLiBCZWdpbiB3aXRoIGFuIGludHJvZHVjdGlvbiB0byB0aGUgY2hhcHRlciwgdGhlbiBjb3ZlciBlYWNoIHN1YnRvcGljIGluIHR1cm4uIERvbid0IGp1c3QgYnJpZWZseSBkZXNjcmliZSB0aGUgc3VidG9waWNzLCBidXQgcmF0aGVyIGVsYWJvcmF0ZSBvbiB0aGUgY29uY2VwdHMgYXQgZnVsbCBsZW5ndGggYW5kIGV4cGxhaW4gdGhlbSB3aXRoIGEgZm9jdXMgb24gaW50dWl0aW9uLiBTcGVsbCBldmVyeXRoaW5nIG91dCBjbGVhcmx5IHNvIHRoZXJlIGlzIG5vIGFtYmlndWl0eS4gRGVkaWNhdGUgbXVsdGlwbGUgcGFyYWdyYXBocyB0byBlYWNoIHN1YnRvcGljLiBXcml0ZSBpbiBmdWxsIHByb3NlLCByYXRoZXIgdGhhbiBidWxsZXQgcG9pbnRzLiAKClNlcGFyYXRlIGVhY2ggc3VidG9waWMgd2l0aCBhIHNlY3Rpb24gaGVhZGVyICIjIi4KCkFsc28sIHBsZWFzZSB3cml0ZSBhbGwgbWF0aGVtYXRpY2FsIG5vdGF0aW9uIGluIExhVGVYIG9ubHkgZS5nLiAiJHheMiQiIG9yICIkXHBpJCIuIERvIG5vdCB1c2UgdW5pY29kZSBtYXRoZW1hdGljYWwgY2hhcmFjdGVycyBlLmcuICJwaSIu)

###Instructions

Youwillbegivenachaptertitle,description,andsubtopicsand,basedonthosetopics,yourjobistowriteadetailed,cohesivetextbookchapteraddressedtoacollegestudentwhoislearningthismaterialforthefirsttime.

Thechaptershouldbecomprehensiveandsuitableforsomeonelearningthismaterialtounderstandresearchpapersinthefield.Beginwithanintroductiontothechapter,thencovereachsubtopicinturn.Don’tjustbrieflydescribethesubtopics,butratherelaborateontheconceptsatfulllengthandexplainthemwithafocusonintuition.Spelleverythingoutclearlysothereisnoambiguity.Dedicatemultipleparagraphstoeachsubtopic.Writeinfullprose,ratherthanbulletpoints.

Separateeachsubtopicwithasectionheader"#".

Also,pleasewriteallmathematicalnotationinLaTeXonlye.g."$x^2$"or"$\pi$".Donotuseunicodemathematicalcharacterse.g."pi".