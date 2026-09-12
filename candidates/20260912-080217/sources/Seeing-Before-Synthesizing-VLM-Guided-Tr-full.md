Title:

Content selection saved. Describe the issue below:

Description:

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2609.04183v1 \[cs.CV\] 03 Sep 2026

# Seeing Before Synthesizing: VLM-Guided Transition Event Discovery    for Weakly-Supervised Dense Video Captioning

Ye-Chan Kim
Seung hee Choi
SeungJu Cha
Si-Woo Kim
Affiliation: Hwiseon KimHyungee Kim
Dong-Jin Kim†Affiliation: Hanyang University, South Korea
Affiliation: {dpcksdl78, ermitaju1, sju9020, boreng0817, hwiseon9151, khjiiii2002, djdkim}@hanyang.ac.kr

###### Abstract

Weakly-Supervised Dense Video Captioning aims to localize and describe multiple events in untrimmed videos given only an ordered set of event-level captions per video.
Recent work synthesizes auxiliary transition captions via LLM to provide additional vision-language alignment, but these captions lack visual grounding and are rigidly assigned to every inter-event gap at a fixed location and duration.
To address these, we propose Seeing Before Synthesizing (SBS), a framework that adaptively provides visually grounded linguistic guidance only where warranted.
Leveraging a VLM, we generate frame-level narratives for the inter-event gaps and detect transitions from the semantic variation across them.
For identified transitions, we then refine inter-event temporal masks by blending the temporal midpoint with the semantic change point and selecting the width that maximizes vision-language alignment.
Experiments on ActivityNet Captions and YouCook2 demonstrate state-of-the-art performance in both captioning and localization.

## 1 Introduction

![Refer to caption](https://arxiv.org/html/2609.04183v1/teaser_0526_sh.png)Figure 1: (a) Prior work [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") synthesizes captions from GT text alone, producing hallucinated descriptions (e.g., “pour a cup of water”) and rigidly bridging all gaps. (b) SBS generates visually grounded captions via VLM and selectively bridges gaps only when a genuine semantic transition is detected.

Dense Video Captioning (DVC) [Kim et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib7 ""); [Liu et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib11 ""); [Wu et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib10 "") extends standard video captioning [Wang et al. (2018)](https://arxiv.org/html/2609.04183v1#bib.bib4 ""); [Seo et al. (2022)](https://arxiv.org/html/2609.04183v1#bib.bib2 ""); [Zhao et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib3 "") by localizing and describing multiple temporal events in long, untrimmed videos. Conventional fully supervised DVC methods [Choi et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib6 ""); [Baek et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib9 "") typically rely on dense annotations, where each event is paired with both temporal boundaries and a natural-language description.
However, obtaining such fine-grained annotations is labor-intensive and difficult to scale, especially for real-world videos.

To alleviate this dependency, Weakly-Supervised Dense Video Captioning (WSDVC) [Duan et al. (2018)](https://arxiv.org/html/2609.04183v1#bib.bib12 ""); [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 ""); [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") has emerged.
It learns event localization and captioning from videos paired with temporally ordered descriptions, eliminating the need for start and end timestamps.
In this setting, each training video provides the sequence of event-level captions, but the temporal boundaries of the events remain unannotated.
Therefore, effectively aligning language supervision with the underlying visual content is crucial for learning fine-grained event localization.

To better support such Vision-Language (VL) alignment, recent studies have explored Large Language Model (LLM)-generated captions as auxiliary supervision when annotations are sparse or noisy [Wu et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib32 ""); [Shvetsova et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib33 ""); [Fan et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib39 "").
Since VL alignment serves as a crucial learning cue in WSDVC, SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 ""), an early attempt to apply this idea, uses an LLM to synthesize transition captions for each inter-event gap—the interval between two neighboring predicted event centers.
However, such approaches are not grounded in the visual content and resort to rigid, heuristic rules.
As a result, SAIL has no basis for the two decisions most essential to providing useful transition supervision in WSDVC: whether an inter-event gap actually contains a transition worth describing, and where within that gap the transition occurs.
This leads to two key limitations.

First, regarding whether to
introduce a caption, the existing method [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") blindly assumes that every inter-event gap must contain a transitional event.
However, this rigid assumption ignores the diverse nature of real videos, where some transitions are already sufficiently covered by adjacent Ground-Truth (GT) captions.
As a result, assigning auxiliary transition captions to every gap regardless of the video content adds redundant captions to already well-described regions, introducing noise rather than useful cues.
Moreover, since each transition caption is generated solely from the surrounding GT event descriptions, it is prone to hallucinating content that misrepresents the video ( [Figure1](https://arxiv.org/html/2609.04183v1#S1.F1 "In 1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning")).
Second, even when a transition does exist, each synthesized transition caption is misaligned with its visual region by a fixed rule.
In particular, prior work [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") assumes the transition always lies at the midpoint between two neighboring events and spans a fixed duration, without adapting to the observed transition pattern.
This can harm model training when the actual transitional event is displaced from the midpoint or covers a different duration.

To move beyond such rigid assumptions, we aim to provide transition cues that are selective and visually grounded, adaptive to each video’s content.
Building on this goal, we propose Seeing Before Synthesizing (SBS), a framework that employs a Vision-Language Model (VLM) [Li et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib23 "")’s eye into both decisions—whether to introduce a transition and where to place it.
It selectively synthesizes a transitional event guided by contextual flow, only when an informative event occurs, and places it according to the video content.

To realize this, the key question is determining whether an informative event exists within each inter-event gap.
Inspired by the observation in cognitive science that humans segment continuous activity into discrete events at points of substantial perceptual change [Tversky and Zacks (2013)](https://arxiv.org/html/2609.04183v1#bib.bib34 ""), we utilize the semantic change across frames as a proxy for an unannotated transition.
A naive way to capture such a semantic change in video is to track fluctuations in low-level visual features directly.
However, these signals are notoriously susceptible to non-semantic noise such as camera motion and lighting changes [Smeaton et al. (2010)](https://arxiv.org/html/2609.04183v1#bib.bib28 ""); [Schiappa et al. (2022)](https://arxiv.org/html/2609.04183v1#bib.bib29 ""), which can easily be mistaken for genuine event transitions.
We therefore repurpose the VLM as a transition-search tool, rather than a mere caption generator.
Specifically, we exploit it to translate each frame into a semantically abstract linguistic description.
The key advantage is that linguistic descriptions provide a more semantically abstract signal than raw visual features [Ye et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib30 ""), making transitions easily discernible, even when the visual appearance remains similar.

Concretely, we feed the semantic variation between caption embeddings of consecutive frames within each inter-event gap into an adaptive gate, whose threshold is determined by the local variation statistics of that gap.
If the signal surpasses the threshold—indicating a salient change—the gate treats the gap as a genuine transition and opens to activate inter-event supervision, closing otherwise.

Once the adaptive gate identifies a meaningful transition, the remaining challenge is where to align the transition caption within the visual region.
Prior work addresses this with a fixed temporal midpoint between neighboring event centers, which remains blind to the actual video content.
Instead, we identify a content-adaptive transition center by leveraging the semantic change point that exhibits the greatest variation.
We interpolate between the semantic change point and the midpoint, anchoring the center near
the change point
while keeping the transition event
from collapsing onto either of its neighboring event centers.
In addition, we select the width that best aligns the visual region with the transition caption.
The resulting temporal span defines the visual region for the transition caption, supplying additional alignment to the model.

Our contributions are as follows:

- •


We reformulate transition augmentation in WSDVC from text-only synthesis to visually grounded transition event discovery.

- •


We propose SBS, which repurposes a VLM as a transition-search tool to adaptively gate transition cues and localize transition regions through a semantic change point.

- •


We validate our method on ActivityNet and YouCook2, achieving state-of-the-art results in both
the captioning and localization tasks.


## 2 Related Work

Weakly-Supervised Dense Video Captioning.
In WSDVC, early approaches [Duan et al. (2018)](https://arxiv.org/html/2609.04183v1#bib.bib12 ""); [Chen and Jiang (2021)](https://arxiv.org/html/2609.04183v1#bib.bib13 "") employ a cycle-consistency framework that localizes temporal segments from captions and reconstructs the captions from those segments.
Recently, distinct from existing cycle-consistency frameworks, ILCACM [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "") proposed a method that employs Gaussian masks to construct event-specific visual features, implicitly learning localization and captioning through a reconstruction objective.
This reconstruction objective implicitly drives the simultaneous learning of both localization and captioning without relying on a cycle system.
Building upon this, SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") extended the ILCACM framework by introducing the concept of “transitional events”.
This approach utilizes an LLM to synthesize plausible captions for the intervals between given events based on their adjacent captions.
By providing such auxiliary language information, SAIL enables the model to delineate more fine-grained event boundaries.
However, the existing method only offers a naive application of inter-events, leaving the question of how to effectively leverage them while accounting for video characteristics largely unexplored.

LLM-generated captions for Vision-Language tasks.
In recent years, the remarkable success of LLMs across various language tasks [Achiam et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib36 ""); [Touvron et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib37 "") has demonstrated their exceptional zero-shot capabilities and common sense inference [Wei et al. (2022)](https://arxiv.org/html/2609.04183v1#bib.bib38 "").
This success has promoted extensive research into integrating common sense knowledge into vision-language tasks [Fan et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib39 ""); [Park et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib40 "").
Notably, HowToCaption [Shvetsova et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib33 "") addresses the fact that ASR subtitles only loosely correspond to the visual content by prompting an LLM to enrich these noisy narrations into human-style video captions.
Similarly, DIBS [Wu et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib32 "") targets the absence of dense annotations in unlabeled videos by exploiting diverse LLMs to generate rich, event-centric caption candidates.
However, since such enriched pseudo-labels often contain noisy or misaligned content, selectively leveraging this supplementary information remains underexplored.

## 3 Proposed Method

Our objective is to effectively capture the genuine transitions to improve both captioning and localization performance in WSDVC.
Formally, given a video VV containing NeN\_{e} distinct events, the goal is to generate a set of event timestamps and corresponding captions (tns,tne,Cn)n=1Ne(t\_{n}^{s},t\_{n}^{e},C\_{n})\_{n=1}^{N\_{e}}, where tnst\_{n}^{s} and tnet\_{n}^{e} denote the start and end times of the nn-th event, and CnC\_{n} represents the caption describing the nn-th event.
Since temporal annotations are unavailable, the model learns to infer temporal event boundaries by aligning video frames with their corresponding textual descriptions. The overall architecture is shown in [Figure2](https://arxiv.org/html/2609.04183v1#S3.F2 "In 3.1 Preliminaries ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

### 3.1 Preliminaries

Following [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 ""), we use a differentiable Gaussian mask to represent each event region in the video.
To generate these masks, we employ a Transformer decoder taking video features with NvN\_{v} frames 𝐯={vi}i=1Nv{\\mathbf{v}}=\\{{v}\_{i}\\}\_{i=1}^{N\_{v}}, extracted from the video VV using CLIP ViT-L/14 [Dosovitskiy et al. (2020)](https://arxiv.org/html/2609.04183v1#bib.bib26 ""); [Radford et al. (2021)](https://arxiv.org/html/2609.04183v1#bib.bib27 ""), and learnable event queries 𝐪n\\mathbf{q}\_{n} to produce event-specific representations 𝐨n\\mathbf{o}\_{n}.
Based on 𝐨n\\mathbf{o}\_{n}, we predict its temporal center cnc\_{n} and width wnw\_{n} for each event:
cn=Sig​(FCc​(𝐨n))∈\[0,1\],wn=Sig​(FCw​(𝐨n))∈\[0,1\]c\_{n}=\\textit{Sig}(\\text{FC}\_{c}(\\mathbf{o}\_{n})){\\in\[0,1\]},\\quad w\_{n}=\\textit{Sig}(\\text{FC}\_{w}(\\mathbf{o}\_{n})){\\in\[0,1\]}.
Here, Sig(⋅\\cdot) denotes the sigmoid function, and FCc​(⋅)\\text{FC}\_{c}(\\cdot), FCw​(⋅)\\text{FC}\_{w}(\\cdot) are linear layers for predicting nn-th event’s cnc\_{n} and wnw\_{n}.
We then construct Gaussian-based temporal masks to represent each event within the video:

|     |     |     |     |
| --- | --- | --- | --- |
|  | Mn,ie​v​t=𝒢⁡(ri,cn,wn)=exp⁡(−(ri−cn)22​(wn/τm)2),M\_{n,i}^{evt}=\\mathcal{G}(r\_{i};\\,c\_{n},\\,w\_{n})=\\exp\\!\\left(-\\frac{(r\_{i}-c\_{n})^{2}}{2(w\_{n}/\\tau\_{m})^{2}}\\right), |  | (1) |

where rir\_{i}∈\\in \[0, 1\] represents normalized temporal positions across the video ri=i−1Nv−1,i∈{1,…,Nv}r\_{i}=\\frac{i-1}{N\_{v}-1},i\\in\\{1,\\dots,N\_{v}\\}, and τm\\tau\_{m} is a hyperparameter controlling mask sharpness.

SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") further constructs inter-event masks to align the captions of transition events with the visual representation, capturing the continuous narrative between events.
These masks are aligned with LLM-synthesized transition captions, which act as an indirect training signal.
For each interval, they construct a static inter-event mask centered at the midpoint of adjacent centers cni​n​t​e​r=cn+cn+12c^{inter}\_{n}=\\frac{c\_{n}+c\_{n+1}}{2} with a predefined fixed width wi​n​t​e​rw^{inter}.
These masks serve as a bridge between the nn-th and (n+1)(n+1)-th events, providing a consistent temporal prior for the inter-event regions.

![Refer to caption](https://arxiv.org/html/2609.04183v1/main_fig.png)Figure 2: SBS Pipeline.
Using VLM-generated frame captions as a visually grounded narrative flow, SBS decides whether to introduce a transition in each gap via an adaptive gate and where to place it via an adaptive mask, providing grounded auxiliary supervision.

### 3.2 Adaptive Inter-Event

Unlike prior work that exclusively relies on video-blind GT captions to construct transition events, we ground auxiliary supervision in the visual content, leveraging the semantic progression of frame-level captions to adaptively identify transition events.

Narrative Generation.
Given an input video of NvN\_{v} frames, we utilize BLIP-2 [Li et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib23 "") to generate a frame-specific caption 𝒞i\\mathcal{C}\_{i} for each frame, yielding a temporal sequence 𝒞={𝒞1,…,𝒞Nv}\\mathcal{C}=\\{\\mathcal{C}\_{1},\\dots,\\mathcal{C}\_{N\_{v}}\\}.
This sequence 𝒞\\mathcal{C} serves as a dense narrative flow over the visual stream.
Building upon the frame-level narrative flow, we introduce Narrative-Aware Inter-Event Selection to determine whether a latent transition event exists within the temporal gaps between consecutive predicted events.

Narrative-Aware Inter-Event Selection.
We leverage the intuition [Tversky and Zacks (2013)](https://arxiv.org/html/2609.04183v1#bib.bib34 "") that stable semantic content yields little variation across frames, whereas an underlying event transition triggers a pronounced narrative shift.
To capture this shift, we measure the semantic dissimilarity within each inter-event gap.
For the nn-th and (n+1)(n+1)-th consecutive predicted events, we define the inter-event gap as the temporal span between their centers from cnc\_{n} to cn+1c\_{n+1}.
We map a normalized temporal coordinate x∈\[0,1\]x\\in\[0,1\] to a discrete frame index using
κ⁡(x)=clip⁡(⌊x⁡(Nv−1)⌋+1,1,Nv).\\kappa(x)=\\operatorname{clip}\\left(\\left\\lfloor x(N\_{v}-1)\\right\\rfloor+1,1,N\_{v}\\right).

Then, the frame indices of the nn-th inter-event search interval are given by bns=κ⁡(cn),bne=κ⁡(cn+1)b\_{n}^{s}=\\kappa(c\_{n}),b\_{n}^{e}=\\kappa(c\_{n+1}).
Within this temporal span, we collect the corresponding sequence of frame-level text embeddings {𝐳i}i=bnsbne\\{\\mathbf{z}\_{i}\\}\_{i=b\_{n}^{s}}^{b\_{n}^{e}}, where 𝐳i\\mathbf{z}\_{i} denotes the text embedding of caption 𝒞i\\mathcal{C}\_{i} encoded via a CLIP text encoder.
To quantify the semantic shift within the gap \[bns,…,bne\]\[b\_{n}^{s},\\dots,b\_{n}^{e}\], we compute the cosine dissimilarity did\_{i} between adjacent frame-level narratives:

|     |     |     |     |
| --- | --- | --- | --- |
|  | di=1−𝐳i⋅𝐳i+1‖𝐳i‖​‖𝐳i+1‖,d\_{i}=1-\\frac{\\mathbf{z}\_{i}\\cdot\\mathbf{z}\_{i+1}}{\\\|\\mathbf{z}\_{i}\\\|\\\|\\mathbf{z}\_{i+1}\\\|}, |  | (2) |

where did\_{i} represents the degree of semantic variation at a specific time step.
A high dissimilarity within the gap’s sequence 𝒟n={di}i=bnsbne−1\\mathcal{D}\_{n}=\\{d\_{i}\\}\_{i=b\_{n}^{s}}^{b\_{n}^{e}-1} signals a potential transition.
We thus feed this signal into an adaptive gating mechanism that decides whether a transition event should be synthesized.

Specifically, the gate determines the existence of an inter-event transition through a threshold adapted to each gap.
We compute the mean μ⁡(𝒟n)\\mu({\\mathcal{D}\_{n}}), and the standard deviation σ⁡(𝒟n)\\sigma({\\mathcal{D}\_{n}}) within the nn-th gap.
The adaptive threshold ηna​d​a​p\\eta^{adap}\_{n} is then formulated as: ηna​d​a​p=μ⁡(𝒟n)+β⋅σ⁡(𝒟n)\\eta^{adap}\_{n}=\\mu({\\mathcal{D}\_{n}})+\\beta\\cdot\\sigma({\\mathcal{D}\_{n}}), where β\\beta is a hyperparameter controlling the sensitivity to semantic shifts, following [Jeon et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib5 "").

To obtain a soft confidence score for each candidate inter-event interval, we employ a sigmoid-based gate gng\_{n} to estimate the probability of an inter-event’s existence:

|     |     |     |     |
| --- | --- | --- | --- |
|  | gn=Sig​(max​(𝒟n)−ηna​d​a​p).g\_{n}=\\textit{Sig}(\\text{max}(\\mathcal{D}\_{n})-\\eta^{adap}\_{n}). |  | (3) |

The gate value gn∈\[0,1\]g\_{n}\\in\[0,1\] serves as a confidence score for the existence of a transition within the nn-th gap.
We open the gate when gn≥0.5g\_{n}\\geq 0.5, otherwise the gate is closed, and no transitional event is injected into the gap.
We aim to apply transition supervision selectively, rather than uniformly across all gaps.
Through this selective mechanism, a transition cue is injected only into gaps whose semantic variation sufficiently exceeds the threshold.

Adaptive Inter-Event Masks.
While the gating mechanism identifies the necessity of a transition caption, the remaining challenge is to align it with its corresponding visual region.
To achieve this, we propose Adaptive Inter-Event Masks, which move beyond video-agnostic templates by dynamically estimating the temporal center and width for each transition based on the video’s flow and content.

Prior work [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") uniformly assigns a static midpoint cni​n​t​e​rc^{inter}\_{n} and a fixed width wi​n​t​e​rw^{inter} to every interval between the nn-th and (n+1)(n+1)-th events.
This rule serves as a temporal regularizer that keeps the transition event from collapsing onto either of its neighboring event centers.
In contrast, we refine the transition event’s center to account not only for this temporal prior but also for the semantic change point identified in the narrative flow.
Specifically, we define this semantic change point pnp\_{n} as the temporal position exhibiting the largest semantic dissimilarity within the nn-th gap:

|     |     |     |     |
| --- | --- | --- | --- |
|  | pn=in∗−1Nv−1,wherein∗=arg⁡maxi∈{bns,…,bne−1}​di.p\_{n}=\\frac{i\_{n}^{\*}-1}{N\_{v}-1},\\quad\\text{where}\\quad i\_{n}^{\*}=\\underset{i\\in\\{b\_{n}^{s},\\dots,b\_{n}^{e}-1\\}}{\\arg\\max}\\,d\_{i}. |  | (4) |

Based on pnp\_{n}, we refine the center cninter∗c\_{n}^{inter\*} with a hyperparameter α∈\[0,1\]\\alpha\\in\[0,1\]:

|     |     |     |     |
| --- | --- | --- | --- |
|  | cninter∗=(1−α)⋅cni​n​t​e​r+α⋅pn.c\_{n}^{inter\*}=(1-\\alpha)\\cdot c\_{n}^{inter}+\\alpha\\cdot p\_{n}. |  | (5) |

As a result, the mask center is anchored at a position that reflects both the temporal prior from the neighboring centers and the point where the actual semantic change occurs.
We then map cninter∗c\_{n}^{inter\*} to its corresponding discrete frame index
jn=κ(cninter∗)j\_{n}=\\kappa\_{\\mathrm{}}(c\_{n}^{inter\*}), and adopt VLM caption at frame jnj\_{n} as the linguistic description of the transition.

Next, we adaptively determine the optimal temporal width winter∗nw^{inter\*}\_{n}. To account for varying event durations and identify the width that best matches the underlying content, we evaluate cross-modal alignment between the video content and the caption at the refined center across multiple candidate widths.
For each candidate width from the predefined set w(k)∈Ω={w(1),…,w(K)}w^{(k)}\\in\\Omega=\\{w^{(1)},\\dots,w^{(K)}\\},
we generate a soft Gaussian mask
Mn,ii​n​t​e​r​(w(k))M\_{n,i}^{inter}(w^{(k)}) at the refined center cninter∗c\_{n}^{inter\*} and compute the masked video features
𝐯n′​(w(k))=𝐯⊙Mn,ii​n​t​e​r​(w(k))\\mathbf{v}\_{n}^{\\prime}(w^{(k)})=\\mathbf{v}\\odot M\_{n,i}^{inter}(w^{(k)}).
We then obtain the average pooled representation
𝐯¯n′​(w(k))\\bar{\\mathbf{v}}\_{n}^{\\prime}(w^{(k)})
and select the optimal width that maximizes the cross-modal alignment
with the inter-event’s caption embedding 𝐳jn\\mathbf{z}\_{j\_{n}}, recording the resulting alignment score sn∗s\_{n}^{\*}:

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | winter∗n\\displaystyle w^{inter\*}\_{n} | =arg⁡maxw(k)∈Ω​cos​(𝐯¯n′​(w(k)),𝐳jn),\\displaystyle=\\arg\\max\_{w^{(k)}\\in\\Omega}\\,\\text{cos}\\!\\left(\\bar{\\mathbf{v}}\_{n}^{\\prime}(w^{(k)}),\\;\\mathbf{z}\_{j\_{n}}\\right), |  | (6) |
|  | sn∗\\displaystyle s\_{n}^{\*} | =maxw(k)∈Ω⁡cos​(𝐯¯n′​(w(k)),𝐳jn),\\displaystyle=\\max\_{w^{(k)}\\in\\Omega}\\,\\text{cos}\\!\\left(\\bar{\\mathbf{v}}\_{n}^{\\prime}(w^{(k)}),\\;\\mathbf{z}\_{j\_{n}}\\right), |  |

where 𝐳jn\\mathbf{z}\_{j\_{n}} is the CLIP text embedding of the VLM caption generated at frame jnj\_{n}.

The final adaptive inter-event mask Mn,iinter∗M\_{n,i}^{inter\*} is formulated by substituting the optimal center cninter∗c\_{n}^{inter\*} and width wninter∗w\_{n}^{inter\*} into [Equation1](https://arxiv.org/html/2609.04183v1#S3.E1 "In 3.1 Preliminaries ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"):

|     |     |     |     |
| --- | --- | --- | --- |
|  | Mn,iinter∗=𝒢(ri;cninter∗,wninter∗).M\_{n,i}^{inter\*}=\\mathcal{G}\\!\\left(r\_{i};\\,c\_{n}^{inter\*},\\,w\_{n}^{inter\*}\\right). |  | (7) |

The resulting inter-event visual representation is obtained as
𝐯′n∗=𝐯⊙Mn,iinter∗\\mathbf{v^{\\prime}}\_{n}^{\*}=\\mathbf{v}\\odot M\_{n,i}^{inter\*},
which serves as the visual feature for the transition between the
nn-th and (n+1)(n+1)-th events.
By adaptively estimating these temporal parameters, SBS provides a more realistic and context-aware transitional event, thereby facilitating precise alignment between visual dynamics and auxiliary linguistic signals.

|     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Setting | Model | Features | Captioning | Localization |
| SODA\_c | METEOR | CIDEr | ROUGE-L | BLEU-4 | R@Avg | P@Avg | F1 |
| FullySupervised | CM2[Kim et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib7 "") | CLIP | 6.18 | 8.55 | 33.01 | – | 2.38 | 53.71 | 56.81 | 55.21 |
| E2DVC [Wu et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib10 "") | CLIP | 6.13 | 8.57 | 33.63 | – | 2.43 | 54.67 | 57.70 | 56.14 |
| CACMI [Jia et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib16 "") | CLIP | 6.39 | 8.68 | 33.80 | – | 2.44 | 55.89 | 58.05 | 57.10 |
| ROS-DVC [Baek et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib9 "") | CLIP | 6.45 | 8.45 | 35.04 | – | 2.36 | 55.35 | 55.65 | 55.50 |
| WeaklySupervised | WSDEC [Duan et al. (2018)](https://arxiv.org/html/2609.04183v1#bib.bib12 "") | C3D | – | 6.30 | 18.77 | 12.55 | 1.27 | 29.57 | 59.33 | 39.18 |
| ECG [Wu et al. (2021)](https://arxiv.org/html/2609.04183v1#bib.bib15 "") | C3D | – | 7.06 | 14.25 | – | 1.33 | – | – | – |
| EC-SL [Chen and Jiang (2021)](https://arxiv.org/html/2609.04183v1#bib.bib13 "") | C3D | – | 7.49 | 21.21 | 13.02 | 1.33 | – | – | – |
| PWS-DVC∗[Choi et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib14 "") | C3D | – | 7.28 | 20.59 | 12.71 | 1.35 | 40.85 | 55.82 | 47.09 |
| ILCACM [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "") | CLIP | 6.08 | 8.48 | 33.42 | 14.77 | 2.26 | 53.72 | 58.92 | 56.20 |
| SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") | CLIP | 6.29 | 8.63 | 35.38 | 15.29 | 2.30 | 54.39 | 59.87 | 57.00 |
| SBS (Ours) | CLIP | 6.49 | 8.87 | 36.87 | 15.60 | 2.47 | 56.13 | 60.38 | 58.18 |

Table 1: Comparison with state-of-the-art methods on ActivityNet validation set. SBS achieves state-of-the-art performance in both captioning and localization metrics. \* denotes results reported in [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "").

|     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Setting | Model | Features | Captioning | Localization |
| SODA\_c | METEOR | CIDEr | ROUGE-L | BLEU@N | R@Avg | P@Avg | F1 |
| WeaklySupervised | WSDEC∗[Duan et al. (2018)](https://arxiv.org/html/2609.04183v1#bib.bib12 "") | C3D | 2.11 | 1.47 | 8.43 | – | – | – | – | – |
| PWS-DVC∗[Choi et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib14 "") | C3D | 3.14 | 2.48 | 9.81 | – | – | – | – | – |
| ILCACM∗[Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "") | CLIP | 3.60 | 3.41 | 13.49 | 4.75 | 2.59 | 17.76 | 18.01 | 17.88 |
| SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") | CLIP | 4.08 | 3.63 | 14.61 | 5.42 | 2.94 | 20.76 | 21.13 | 20.94 |
| SBS (Ours) | CLIP | 4.24 | 3.99 | 16.28 | 5.80 | 3.25 | 22.39 | 21.95 | 22.17 |

Table 2: Comparison with previous methods on YouCook2 validation set.
SBS achieves the best performance in both captioning and localization metrics.
BLEU@N denotes the average of BLEU-1 through BLEU-4. \* denotes results reported in [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "").

### 3.3 Model Training and Inference

Following SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 ""), our training objective consists of a captioning
loss ℒcap\\mathcal{L}^{\\text{cap}} and a contrastive loss ℒcon\\mathcal{L}^{\\text{con}},
supplemented by our proposed gated attraction loss ℒattr\\mathcal{L}^{\\text{attr}}.
Specifically, ℒcap\\mathcal{L}^{\\text{cap}} trains the model to reconstruct
the GT caption CnC\_{n} from event region 𝐯⊙Mn,ie​v​t{\\mathbf{v}\\odot M\_{n,i}^{evt}} and its complement 𝐯⊙(1−Mn,ie​v​t){\\mathbf{v}\\odot(1-M\_{n,i}^{evt}}) with CE loss.
ℒcon\\mathcal{L}^{\\text{con}} encourages the visual feature
of each event region 𝐯⊙Mn,ie​v​t{\\mathbf{v}\\odot M\_{n,i}^{evt}} to be aligned with the text feature of its corresponding caption CnC\_{n}, utilizing margin ranking loss in the CLIP [Radford et al. (2021)](https://arxiv.org/html/2609.04183v1#bib.bib27 "") feature space.

Unlike SAIL, SBS selectively applies ℒattr\\mathcal{L}^{\\text{attr}} using gng\_{n} from  [Equation3](https://arxiv.org/html/2609.04183v1#S3.E3 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"):

|     |     |     |     |
| --- | --- | --- | --- |
|  | ℒnattr=gn⋅(1−cos(𝐯¯n′∗,𝐳jn)),\\mathcal{L}\_{n}^{\\text{attr}}=g\_{n}\\cdot\\left(1-\\text{cos}(\\bar{\\mathbf{v}}\_{n}^{{}^{\\prime}\*},\ \\mathbf{z}\_{j\_{n}})\\right), |  | (8) |

where gng\_{n} modulates the loss magnitude according to the transition confidence.

Additionally, we apply a similarity-based filtering step to guard against low-quality
VLM captions that may not accurately describe the visual content. Specifically, an
inter-event region is included in the loss computation only if the alignment score
sn∗s\_{n}^{\*} exceeds a predefined threshold θ\\theta
(i.e., sn∗≥θs\_{n}^{\*}\\geq\\theta).
This restricts training to reliably aligned inter-event pairs, preventing noisy or hallucinated captions from harming learning.
Let 𝒜={n∣gn≥0.5​and​sn∗≥θ}\\mathcal{A}=\\left\\{n\\mid g\_{n}\\geq 0.5\ \\text{and}\ s\_{n}^{\*}\\geq\\theta\\right\\} denote the set of all accepted intervals; the final attraction loss is:

|     |     |     |     |
| --- | --- | --- | --- |
|  | ℒattr=1\|𝒜\|​∑n∈𝒜ℒnattr.\\mathcal{L}^{\\text{attr}}=\\frac{1}{\|\\mathcal{A}\|}\\sum\_{n\\in\\mathcal{A}}\\mathcal{L}\_{n}^{\\text{attr}}. |  | (9) |

The overall training objective combines the base loss with the attraction loss, weighted by λattr\\lambda^{\\text{attr}}:

|     |     |     |     |
| --- | --- | --- | --- |
|  | ℒ=ℒcap+ℒcon+λattr​ℒattr.\\mathcal{L}=\\mathcal{L}^{\\text{cap}}+\\mathcal{L}^{\\text{con}}+\\lambda^{\\text{attr}}\\mathcal{L}^{\\text{attr}}. |  | (10) |

During inference, following [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 ""), the model first generates boundary-free captions to determine the event count, then produces Gaussian masks for each event to extract (cn,wn)(c\_{n},w\_{n}), which are mapped to timestamps, and refines the captions using event-specific masked features.
More details are provided in the supplementary material.

## 4 Experiments

Datasets.
We evaluate our method on two widely used DVC benchmarks.
ActivityNet Captions [Krishna et al. (2017)](https://arxiv.org/html/2609.04183v1#bib.bib21 "") contains 20K untrimmed videos averaging 120 seconds, each annotated with approximately 3.7 temporally localized events.
YouCook2 [Zhou et al. (2018)](https://arxiv.org/html/2609.04183v1#bib.bib22 "") consists of around 2K untrimmed cooking videos with an average duration of 320 seconds, where each video is accompanied by 7.7 localized events on average.

Evaluation Metrics.
We assess performance on both captioning and localization subtasks of DVC.
For captioning quality, we report METEOR [Banerjee and Lavie (2005)](https://arxiv.org/html/2609.04183v1#bib.bib18 ""), CIDEr [Vedantam et al. (2015)](https://arxiv.org/html/2609.04183v1#bib.bib17 ""), ROUGE-L [Lin (2004)](https://arxiv.org/html/2609.04183v1#bib.bib19 ""), and BLEU-N [Papineni et al. (2002)](https://arxiv.org/html/2609.04183v1#bib.bib20 "") using the official evaluation tool [Krishna et al. (2017)](https://arxiv.org/html/2609.04183v1#bib.bib21 ""), along with SODA\_c [Fujita et al. (2020)](https://arxiv.org/html/2609.04183v1#bib.bib25 "").
For event localization, we report mean Average Precision, mean Average Recall, and F1 score.
All metrics are computed across IoU thresholds of {0.3, 0.5, 0.7, 0.9} and averaged.

Implementation Details.
We adopt Distilled-GPT2 [Radford et al. (2019)](https://arxiv.org/html/2609.04183v1#bib.bib24 "") as the caption decoder and optimize all parameters with AdamW, following [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "").
On ActivityNet Captions, the learning rate is initialized to 1e-4, and training runs for 10 epochs in both the captioning and localization stages.
Also we use α=0.5\\alpha=0.5, β=2\\beta=2, θ=0.2\\theta=0.2, Ω={0.2,0.4,0.6}\\Omega=\\{0.2,0.4,0.6\\}, and λattr=0.4\\lambda\_{\\text{attr}}=0.4.
On YouCook2, we train 4 and 25 epochs for the captioning and localization stages, respectively.
All training is performed on a single NVIDIA A6000 GPU.
Additional details are provided in the supplementary material.

|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| VLMCaption | AdaptiveGate | AdaptiveMask | Captioning | Localization |
| (1) | (2) | (3) | S\_c | R-L | C | F1 |
| ✗ | ✗ | ✗ | 6.34 | 15.26 | 35.03 | 56.86 |
| ✓ | ✗ | ✗ | 6.29 | 15.45 | 35.73 | 57.73 |
| ✓ | ✓ | ✗ | 6.45 | 15.43 | 36.61 | 57.67 |
| ✓ | ✗ | ✓ | 6.48 | 15.50 | 36.51 | 57.80 |
| ✓ | ✓ | ✓ | 6.49 | 15.60 | 36.87 | 58.18 |

Table 3: Ablation study on key components. We first compare (1) the presence of VLM and then investigate the contributions of (2) Narrative-Aware Inter-Event Selection and (3) Adaptive Inter-Event Masks components within the VLM-based framework.

### 4.1 Comparison with State-of-the-Art

[Table1](https://arxiv.org/html/2609.04183v1#S3.T1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning") summarizes the captioning and localization results on ActivityNet Captions.
SBS achieves the best performance across both tasks among all weakly-supervised methods, obtaining a CIDEr of 36.87 and an F1 score of 58.18, which surpasses the previous state-of-the-art SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "").
The localization gains are attributed to improvements in both recall (56.13) and precision (60.38), indicating that our adaptive inter-event mechanism enhances temporal boundary estimation.
Notably, SBS even outperforms several fully-supervised methods on the majority of metrics, despite the absence of temporal boundary annotations during training.
As shown in [Table2](https://arxiv.org/html/2609.04183v1#S3.T2 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"), these improvements generalize to YouCook2, where SBS again achieves the highest scores in both captioning and localization among WSDVC methods.
The consistent gains across two benchmarks validate the effectiveness of our approach.

![Refer to caption](https://arxiv.org/html/2609.04183v1/Interevent_qual_sh_0526_final.png)Figure 3: Qualitative results about transition events.
Prior LLM-based method injects a transition into every gap, including uninformative ones.
Also, even for meaningful transitions, they describe regions misaligned with the actual transition, resulting in inaccurate captions.
In contrast, SBS generates transitions only where a meaningful change occurs, producing captions that are well aligned with both the actual transition and the underlying frames.

### 4.2 Ablation Studies

Component Ablation.
In [Table3](https://arxiv.org/html/2609.04183v1#S4.T3 "In 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"), we analyze the contribution of each component.
Replacing LLM-synthesized captions with VLM-generated ones already improves CIDEr, ROUGE-L and F1, confirming the benefit of visually grounded inter-event descriptions.
Adding Narrative-Aware Inter-Event Selection improves almost all captioning scores, showing that selective inter-event guidance suppresses noise while retaining informative transitions.
Furthermore, Adaptive Inter-Event Masks provide further improvements, showing that tailoring each mask’s center and width to the content captures transitions better than fixed templates.
Finally, combining all components achieves the best performance, confirming that auxiliary supervision tailored to each video is key to both captioning and localization.

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| Method | Captioning | Localization |
| S\_c | R-L | C | F1 |
| SAIL (LLM) | 6.29 | 15.29 | 35.38 | 57.00 |
| InternVL3-1B | 6.47 | 15.52 | 36.71 | 57.98 |
| Qwen2.5-VL-3B | 6.43 | 15.49 | 36.82 | 57.62 |
| xGen-MM-4B | 6.47 | 15.45 | 36.45 | 57.86 |
| SmolVLM2-2.2B | 6.44 | 15.49 | 36.50 | 57.94 |
| BLIP-2-2.7B | 6.49 | 15.60 | 36.87 | 58.18 |

Table 4: Ablation study on various VLMs, illustrating that SBS consistently improves performance regardless of the choice of the VLM model.

Analysis of VLM Captions. [Table4](https://arxiv.org/html/2609.04183v1#S4.T4 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning") examines the impact of the captioning model used to generate frame-level descriptions.
All VLM-based variants (BLIP-2 [Li et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib23 ""), InternVL3 [Zhu et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib31 ""), Qwen2.5-VL [Bai et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib35 ""), xGen-MM [Xue et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib41 "") and SmolVLM2 [Marafioti et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib42 "")) consistently outperform LLM-based SAIL across all metrics, confirming that visually grounded captions provide more reliable supervision than video-blind linguistic synthesis.
These results suggest that the primary gain stems from grounding captions in actual visual content rather than from the choice of the VLM. [Figure3](https://arxiv.org/html/2609.04183v1#S4.F3 "In 4.1 Comparison with State-of-the-Art ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning") further illustrates this distinction qualitatively: while LLM-based captions often hallucinate events absent from the video due to their reliance on linguistic context alone, VLM-generated captions faithfully describe what appears in each frame.

Analysis of Gate Activation Criteria.
To examine which signal best identifies genuine inter-event transitions, we compare three criteria for opening the adaptive gate: random activation, raw CLIP visual features, and our VLM-generated captions.
As shown in [Table5](https://arxiv.org/html/2609.04183v1#S4.T5 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"), random activation performs the worst, while raw visual features improve over random but still fall short, since low-level signals are easily confounded by non-semantic variation.
In contrast, our caption-based criterion achieves the best scores on both captioning and localization, showing that semantically abstract textual descriptions are a more reliable indicator of underlying transitions for adaptive gap selection.

Figure 4: Hyperparameter search for the interpolation coefficient α\\alpha. The X-axis denotes α\\alpha, and the Y-axis reports captioning and localization scores.
SAIL’s fixed midpoint [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "")(α=0)(\\alpha=0) yields the lowest scores, whereas interpolating the semantic change point (α>0)(\\alpha>0) consistently improves performance.

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| Method | Captioning | Localization |
| S\_c | R-L | C | F1 |
| SAIL | 6.29 | 15.29 | 35.38 | 57.00 |
| Random | 6.26 | 15.32 | 35.87 | 56.88 |
| Raw Video | 6.39 | 15.32 | 36.34 | 57.42 |
| Caption | 6.49 | 15.60 | 36.87 | 58.18 |

Table 5: Ablation study on gate activation criteria for inter-event supervision.
Textual semantic guides outperform raw visual features for adaptive gap selection.

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| Method | S\_c | C | F1 | Cos Sim |
| SAIL | 6.29 | 35.38 | 57.00 | 0.1460 |
| SBS (w/o F) | 6.43 | 36.41 | 57.89 | 0.2624 |
| SBS | 6.49 | 36.87 | 58.18 | 0.2699 |

Table 6: Cosine similarity between inter-event visual features and caption features.
Our method more faithfully represents inter-event regions.
w/o F denotes without similarity filtering method.

Analysis of Inter-Masks.
As shown in [Figure4](https://arxiv.org/html/2609.04183v1#S4.F4 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"), performance consistently improves when both the temporal midpoint and the semantic transition point are jointly considered, compared with relying solely on the temporal midpoint.
In particular, intermediate values of α\\alpha yield stable gains across all three metrics, with the best performance achieved at α=0.5\\alpha=0.5, where the model attains the highest captioning and localization scores.
Also, [Figure3](https://arxiv.org/html/2609.04183v1#S4.F3 "In 4.1 Comparison with State-of-the-Art ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning") shows that the adaptive masks align well with the event transition points in the video.

Analysis of Inter-Events.
To verify whether our VLM captions and adaptive mask construction effectively represent inter-event regions, we measure the cosine similarity between the pooled inter-event visual features and their corresponding caption features.
As shown in [Table6](https://arxiv.org/html/2609.04183v1#S4.T6 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"), we observe a substantial increase in average similarity compared to the LLM-based baseline.
This confirms that our approach, which combines visually grounded VLM captions with adaptive center blending and width selection, more faithfully captures the underlying inter-event content, ultimately providing higher-quality auxiliary supervision for training.

Comparisons with MLLM-based methods.
We compare MLLM-based models [Ren et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib43 ""); [Guo et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib44 ""); [Guo et al. (2024)](https://arxiv.org/html/2609.04183v1#bib.bib45 ""); [Yang et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib46 "") that explicitly address temporal grounding and dense captioning ( [Table7](https://arxiv.org/html/2609.04183v1#S4.T7 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning")).
Despite fully supervised training with large-scale data and substantially larger models, these MLLM-based methods still struggle with the compound challenge of simultaneously performing grounding and captioning.
In contrast, SBS effectively handles this task even under the weakly-supervised setting without any temporal annotations, while using a much smaller model.

|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
| Model | Fully | Backbone | Captioning | Localization |
| Supervised | Params | S\_c | C | F1 |
| TimeChat | ✓ | 7B | 4.7 | 19.0 | 36.9 |
| VTG-LLM | ✓ | 7B | 5.1 | 20.7 | 34.8 |
| TRACE | ✓ | 7B | 6.0 | 25.9 | 39.3 |
| TimeExpert | ✓ | 5.9B | 6.5 | 28.4 | 40.5 |
| SBS | ✗ | 133M | 6.49 | 36.87 | 58.18 |

Table 7: Comparison with MLLM-based models on ActivityNet Captions. Despite using weak supervision and a much smaller model, SBS outperforms fully-supervised MLLM-based methods.

Direct Evaluation of the Gate on Human-Annotated Transitions.

|     |     |     |     |
| --- | --- | --- | --- |
| Method | Recall | Precision | F1 |
| SAIL | 100 | 37.89 | 54.96 |
| Random | 37.90 | 49.48 | 42.92 |
| SBS | 74.99 | 64.29 | 69.23 |

Table 8: Comparison of transition identification performance on human-annotated gaps.
SBS’s gate substantially outperforms both always-inject (SAIL) and random gating in F1.

Since no ground-truth annotations exist for inter-event transitions, we constructed a manually verified transition validation set, then directly evaluated our gate on it.
We designed a multi-stage protocol, with human verification as the final arbiter.
(1) Gap extraction and sampling. From consecutive GT event pairs in ActivityNet validation videos, we randomly sampled 200 inter-event gaps.
(2) Initial transition proposal. Frames from each gap (1 fps) were fed into Gemini 3.5 Flash, prompted to judge whether a distinct transitional event—not covered by either adjacent GT caption—occurs in the gap, explicitly excluding camera cuts, angle changes, and mere continuations.
(3) Cross-verification. Each gap was independently re-judged by GPT-5.5 Pro with the identical prompt, without revealing the first model’s answer. Agreed labels became draft labels; disagreements were excluded.
(4) Human verification. All draft labels were then verified by human annotators, blind to our model’s outputs. We retained only gaps with unanimous agreement, to ensure label reliability. This yielded a final validation set of 95 gaps (36 gaps with a transition, 59 gaps without).
On this set, we evaluated the gate decision for each annotated gap ( [Table8](https://arxiv.org/html/2609.04183v1#S4.T8 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning")).
Our gate mechanism achieves substantially better transition detection than both SAIL’s always-inject strategy and random gating, suggesting that text-level semantic change is an effective signal for identifying genuine transitions and directly substantiating the whether-to-inject component of our central claim.

Computational Cost Analysis.

|     |     |     |     |
| --- | --- | --- | --- |
| Method | Train time | Inference time | GPU usage |
| ILCACM | 1H 42M 31S | 7M 16S | 33.08 GiB |
| SAIL | 1H 49M 50S | 7M 35S | 33.11 GiB |
| SBS | 1H 52M 53S | 7M 51S | 33.13 GiB |

Table 9: Model training computational cost comparison. The additional cost of SBS is negligible across all three metrics.

We measure the time and memory consumed during training and inference, averaged over five runs.
As shown in [Table9](https://arxiv.org/html/2609.04183v1#S4.T9 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"), the training and inference times of our method are nearly identical to those of the baseline [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 ""), and the memory consumption is comparable as well.
Since captions are extracted in advance and only their features are used, the captioning process adds almost no overhead, and the mask width selection is a simple dot product with negligible effect on the overall training time.

## 5 Conclusion

We present SBS, a framework that rethinks how inter-event information is utilized in WSDVC.
Our key insight is twofold: (1) transitions should be applied selectively, only where the video exhibits a transition, rather than uniformly across all gaps; (2) each transition should be localized according to the actual video content, rather than fixed at a heuristic midpoint.
To this end, SBS repurposes a VLM as a transition-search tool, grounding both decisions—whether and where—in visual evidence.
Experiments on ActivityNet Captions and YouCook2 confirm that SBS sets a new state-of-the-art in both captioning and localization, demonstrating the importance of adaptive, visually grounded inter-event utilization for WSDVC.

## Limitations

Our method grounds transition discovery in VLM-generated frame captions, so its effectiveness is bounded by the quality of those captions: when the VLM produces generic, repetitive, or inaccurate descriptions—particularly in domains underrepresented in its pre-training—the caption-space dissimilarity signal becomes unreliable, causing the adaptive gate to miss genuine transitions or open on spurious ones.

## Acknowledgments

This work was partly supported by the Institute of Information & Communications Technology Planning & Evaluation (IITP) grant funded by the Korean government (MSIT) RS-2025-25422680, Metacognitive AGI Framework and its Applications and the AI Seoul Tech Research Support Program of the Seoul Future Foundation.

## References

- Achiam et al. (2023)J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al.Gpt-4 technical report.
arXiv preprint arXiv:2303.08774.
Cited by: [§2](https://arxiv.org/html/2609.04183v1#S2.p2.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Baek et al. (2026)S. H. Baek, J. Lee, H. Lee, and J. W. ChoStay in your lane: role specific queries with overlap suppression loss for dense video captioning.
In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),
pp. 3432–3442.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.6.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Bai et al. (2025)S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding, C. Gao, C. Ge, et al.Qwen3-vl technical report.
arXiv preprint arXiv:2511.21631.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p2.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Banerjee and Lavie (2005)S. Banerjee and A. LavieMETEOR: an automatic metric for mt evaluation with improved correlation with human judgments.
In Proceedings of the acl workshop on intrinsic and extrinsic evaluation measures for machine translation and/or summarization,
pp. 65–72.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p2.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Chen and Jiang (2021)S. Chen and Y. JiangTowards bridging event captioner and sentence localizer for weakly supervised dense event captioning.
In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
pp. 8425–8435.
Cited by: [§2](https://arxiv.org/html/2609.04183v1#S2.p1.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.9.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Choi et al. (2026)S. h. Choi, M. Jeon, H. Oh, J. Lee, and D. KimFollow the saliency: supervised saliency for retrieval-augmented dense video captioning.
In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),
pp. 32808–32817.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Choi et al. (2023)W. Choi, J. Chen, and J. YoonPWS-dvc: enhancing weakly supervised dense video captioning with pretraining approach.
IEEE Access11, pp. 128162–128174.
Cited by: [Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.10.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 2](https://arxiv.org/html/2609.04183v1#S3.T2.2.1.4.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Dosovitskiy et al. (2020)A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, et al.An image is worth 16x16 words: transformers for image recognition at scale.
arXiv preprint arXiv:2010.11929.
Cited by: [§3.1](https://arxiv.org/html/2609.04183v1#S3.SS1.p1.1 "3.1 Preliminaries ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Duan et al. (2018)X. Duan, W. Huang, C. Gan, J. Wang, W. Zhu, and J. HuangWeakly supervised dense event captioning in videos.
Advances in Neural Information Processing Systems31.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p2.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§2](https://arxiv.org/html/2609.04183v1#S2.p1.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.7.2 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 2](https://arxiv.org/html/2609.04183v1#S3.T2.2.1.3.2 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Fan et al. (2023)L. Fan, D. Krishnan, P. Isola, D. Katabi, and Y. TianImproving clip training with language rewrites.
Advances in Neural Information Processing Systems36, pp. 35544–35575.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p3.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§2](https://arxiv.org/html/2609.04183v1#S2.p2.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Fujita et al. (2020)S. Fujita, T. Hirao, H. Kamigaito, M. Okumura, and M. NagataSoda: story oriented dense video captioning evaluation framework.
In Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part VI 16,
pp. 517–531.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p2.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Ge et al. (2025)S. Ge, Q. Chen, Z. Jiang, Y. Yin, L. Qin, Z. Chen, and Q. GuImplicit location-caption alignment via complementary masking for weakly-supervised dense video captioning.
In Proceedings of the AAAI Conference on Artificial Intelligence,
Vol. 39, pp. 3113–3121.
Cited by: [Appendix A](https://arxiv.org/html/2609.04183v1#A1.p1.1 "Appendix A Additional Implementation Details ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Appendix A](https://arxiv.org/html/2609.04183v1#A1.p3.1 "Appendix A Additional Implementation Details ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Appendix A](https://arxiv.org/html/2609.04183v1#A1.p4.1 "Appendix A Additional Implementation Details ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Appendix A](https://arxiv.org/html/2609.04183v1#A1.p5.1 "Appendix A Additional Implementation Details ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§1](https://arxiv.org/html/2609.04183v1#S1.p2.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§2](https://arxiv.org/html/2609.04183v1#S2.p1.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.1](https://arxiv.org/html/2609.04183v1#S3.SS1.p1.1 "3.1 Preliminaries ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.3](https://arxiv.org/html/2609.04183v1#S3.SS3.p4.1 "3.3 Model Training and Inference ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.11.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 2](https://arxiv.org/html/2609.04183v1#S3.T2.2.1.5.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p10.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§4](https://arxiv.org/html/2609.04183v1#S4.p3.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Guo et al. (2025)Y. Guo, J. Liu, M. Li, D. Cheng, X. Tang, D. Sui, Q. Liu, X. Chen, and K. ZhaoVtg-llm: integrating timestamp knowledge into video llms for enhanced video temporal grounding.
In Proceedings of the AAAI conference on artificial intelligence,
Vol. 39, pp. 3302–3310.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p6.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Guo et al. (2024)Y. Guo, J. Liu, M. Li, Q. Liu, X. Chen, and X. TangTrace: temporal grounding video llm via causal event modeling.
arXiv preprint arXiv:2410.05643.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p6.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Jeon et al. (2025)M. Jeon, S. Kim, Y. Kim, H. Kim, and D. KimSali4Vid: saliency-aware video reweighting and adaptive caption retrieval for dense video captioning.
In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing,
pp. 25777–25790.
Cited by: [§3.2](https://arxiv.org/html/2609.04183v1#S3.SS2.p5.1 "3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Jia et al. (2026)M. Jia, W. Meng, Z. Fu, Y. Li, Q. Zeng, Y. Zhang, J. Xin, R. Xu, J. Zhang, and X. ZhangExplicit temporal-semantic modeling for dense video captioning via context-aware cross-modal interaction.
In Proceedings of the AAAI Conference on Artificial Intelligence,
Vol. 40, pp. 5341–5349.
Cited by: [Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.5.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Kim et al. (2024)M. Kim, H. B. Kim, J. Moon, J. Choi, and S. T. KimDo you remember? dense video captioning with cross-modal memory retrieval.
In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
pp. 13894–13904.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.3.2 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Kim et al. (2026)Y. Kim, S. Cha, S. Kim, M. Jeon, H. Kim, and D. KimSAIL: similarity-aware guidance and inter-caption augmentation-based learning for weakly-supervised dense video captioning.
arXiv preprint arXiv:2603.05437.
Cited by: [Appendix A](https://arxiv.org/html/2609.04183v1#A1.p1.1 "Appendix A Additional Implementation Details ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Appendix B](https://arxiv.org/html/2609.04183v1#A2.p1.1 "Appendix B Computational Cost ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Figure 1](https://arxiv.org/html/2609.04183v1#S1.F1 "In 1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§1](https://arxiv.org/html/2609.04183v1#S1.p2.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§1](https://arxiv.org/html/2609.04183v1#S1.p3.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§1](https://arxiv.org/html/2609.04183v1#S1.p4.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§2](https://arxiv.org/html/2609.04183v1#S2.p1.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.1](https://arxiv.org/html/2609.04183v1#S3.SS1.p2.1 "3.1 Preliminaries ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.2](https://arxiv.org/html/2609.04183v1#S3.SS2.p8.1 "3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.3](https://arxiv.org/html/2609.04183v1#S3.SS3.p1.1 "3.3 Model Training and Inference ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.12.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 2](https://arxiv.org/html/2609.04183v1#S3.T2 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 2](https://arxiv.org/html/2609.04183v1#S3.T2.2.1.6.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Figure 4](https://arxiv.org/html/2609.04183v1#S4.F4 "In 4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§4.1](https://arxiv.org/html/2609.04183v1#S4.SS1.p1.1 "4.1 Comparison with State-of-the-Art ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Krishna et al. (2017)R. Krishna, K. Hata, F. Ren, L. Fei-Fei, and J. Carlos NieblesDense-captioning events in videos.
In Proceedings of the IEEE international conference on computer vision,
pp. 706–715.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p1.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§4](https://arxiv.org/html/2609.04183v1#S4.p2.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Li et al. (2023)J. Li, D. Li, S. Savarese, and S. HoiBlip-2: bootstrapping language-image pre-training with frozen image encoders and large language models.
In International conference on machine learning,
pp. 19730–19742.
Cited by: [Appendix A](https://arxiv.org/html/2609.04183v1#A1.p2.1 "Appendix A Additional Implementation Details ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§1](https://arxiv.org/html/2609.04183v1#S1.p5.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.2](https://arxiv.org/html/2609.04183v1#S3.SS2.p2.1 "3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p2.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Lin (2004)C. LinRouge: a package for automatic evaluation of summaries.
In Text summarization branches out,
pp. 74–81.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p2.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Liu et al. (2025)Z. Liu, X. Zhang, and J. LiuTask-specific information decomposition for end-to-end dense video captioning.
In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
pp. 16524–16536.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Marafioti et al. (2025)A. Marafioti, O. Zohar, M. Farré, M. Noyan, E. Bakouch, P. Cuenca, C. Zakka, L. B. Allal, A. Lozhkov, N. Tazi, V. Srivastav, J. Lochner, H. Larcher, M. Morlon, L. Tunstall, L. von Werra, and T. WolfSmolVLM: redefining small and efficient multimodal models.
arXiv preprint arXiv:2504.05299.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p2.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Papineni et al. (2002)K. Papineni, S. Roukos, T. Ward, and W. ZhuBleu: a method for automatic evaluation of machine translation.
In Proceedings of the 40th annual meeting of the Association for Computational Linguistics,
pp. 311–318.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p2.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Park et al. (2023)J. S. Park, J. Hessel, K. Chandu, P. P. Liang, X. Lu, P. West, Y. Yu, Q. Huang, J. Gao, A. Farhadi, et al.Localized symbolic knowledge distillation for visual commonsense models.
Advances in Neural Information Processing Systems36, pp. 11338–11352.
Cited by: [§2](https://arxiv.org/html/2609.04183v1#S2.p2.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Radford et al. (2021)A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, et al.Learning transferable visual models from natural language supervision.
In International conference on machine learning,
pp. 8748–8763.
Cited by: [§3.1](https://arxiv.org/html/2609.04183v1#S3.SS1.p1.1 "3.1 Preliminaries ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.3](https://arxiv.org/html/2609.04183v1#S3.SS3.p1.1 "3.3 Model Training and Inference ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Radford et al. (2019)A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever, et al.Language models are unsupervised multitask learners.
OpenAI blog1 (8), pp. 9.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p3.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Ren et al. (2024)S. Ren, L. Yao, S. Li, X. Sun, and L. HouTimechat: a time-sensitive multimodal large language model for long video understanding.
In 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),
pp. 14313–14323.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p6.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Schiappa et al. (2022)M. Schiappa, S. Vyas, H. Palangi, Y. Rawat, and V. VineetRobustness analysis of video-language models against visual and language perturbations.
Advances in Neural Information Processing Systems35, pp. 34405–34420.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p6.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Seo et al. (2022)P. H. Seo, A. Nagrani, A. Arnab, and C. SchmidEnd-to-end generative pretraining for multimodal video captioning.
In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
pp. 17959–17968.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Shvetsova et al. (2024)N. Shvetsova, A. Kukleva, X. Hong, C. Rupprecht, B. Schiele, and H. KuehneHowtocaption: prompting llms to transform video annotations at scale.
In European Conference on Computer Vision,
pp. 1–18.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p3.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§2](https://arxiv.org/html/2609.04183v1#S2.p2.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Smeaton et al. (2010)A. F. Smeaton, P. Over, and A. R. DohertyVideo shot boundary detection: seven years of trecvid activity.
Computer Vision and Image Understanding114 (4), pp. 411–418.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p6.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Touvron et al. (2023)H. Touvron, T. Lavril, G. Izacard, X. Martinet, M. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al.Llama: open and efficient foundation language models.
arXiv preprint arXiv:2302.13971.
Cited by: [§2](https://arxiv.org/html/2609.04183v1#S2.p2.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Tversky and Zacks (2013)B. Tversky and J. M. ZacksEvent perception.
Oxford handbook of cognitive psychology1 (2), pp. 3.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p6.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§3.2](https://arxiv.org/html/2609.04183v1#S3.SS2.p3.1 "3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Vedantam et al. (2015)R. Vedantam, C. Lawrence Zitnick, and D. ParikhCider: consensus-based image description evaluation.
In Proceedings of the IEEE conference on computer vision and pattern recognition,
pp. 4566–4575.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p2.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Wang et al. (2018)B. Wang, L. Ma, W. Zhang, and W. LiuReconstruction network for video captioning.
In Proceedings of the IEEE conference on computer vision and pattern recognition,
pp. 7622–7631.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Wei et al. (2022)J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al.Chain-of-thought prompting elicits reasoning in large language models.
Advances in neural information processing systems35, pp. 24824–24837.
Cited by: [§2](https://arxiv.org/html/2609.04183v1#S2.p2.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Wu et al. (2021)B. Wu, G. Niu, J. Yu, X. Xiao, J. Zhang, and H. WuWeakly supervised dense video captioning via jointly usage of knowledge distillation and cross-modal matching.
arXiv preprint arXiv:2105.08252.
Cited by: [Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.8.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Wu et al. (2024)H. Wu, H. Liu, Y. Qiao, and X. SunDibs: enhancing dense video captioning with unlabeled videos via pseudo boundary enrichment and online refinement.
In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
pp. 18699–18708.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p3.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[§2](https://arxiv.org/html/2609.04183v1#S2.p2.1 "2 Related Work ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Wu et al. (2025)K. Wu, P. Li, J. Fu, Y. Li, Y. Wu, Y. Liu, J. Wang, and S. ZhouEvent-equalized dense video captioning.
In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
pp. 8417–8427.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"),
[Table 1](https://arxiv.org/html/2609.04183v1#S3.T1.2.1.4.1 "In 3.2 Adaptive Inter-Event ‣ 3 Proposed Method ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Xue et al. (2024)L. Xue, M. Shu, A. Awadalla, J. Wang, A. Yan, S. Purushwalkam, H. Zhou, V. Prabhu, Y. Dai, M. S. Ryoo, et al.Xgen-mm (blip-3): a family of open large multimodal models.
arXiv preprint arXiv:2408.08872.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p2.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Yang et al. (2025)Z. Yang, Y. Yu, Y. Zhao, S. Lu, and S. BaiTimeexpert: an expert-guided video llm for video temporal grounding.
In 2025 IEEE/CVF International Conference on Computer Vision (ICCV),
pp. 24286–24296.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p6.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Ye et al. (2025)C. Ye, W. Chen, B. Hu, L. Zhang, Y. Zhang, and Z. MaoImproving video summarization by exploring the coherence between corresponding captions.
IEEE Transactions on Image Processing.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p6.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Zhao et al. (2023)Y. Zhao, I. Misra, P. Krähenbühl, and R. GirdharLearning video representations from large language models.
In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
pp. 6586–6597.
Cited by: [§1](https://arxiv.org/html/2609.04183v1#S1.p1.1 "1 Introduction ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Zhou et al. (2018)L. Zhou, C. Xu, and J. CorsoTowards automatic learning of procedures from web instructional videos.
In Proceedings of the AAAI conference on artificial intelligence,
Vol. 32.
Cited by: [§4](https://arxiv.org/html/2609.04183v1#S4.p1.1 "4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").

- Zhu et al. (2025)J. Zhu, W. Wang, Z. Chen, Z. Liu, S. Ye, L. Gu, H. Tian, Y. Duan, W. Su, J. Shao, et al.Internvl3: exploring advanced training and test-time recipes for open-source multimodal models.
arXiv preprint arXiv:2504.10479.
Cited by: [§4.2](https://arxiv.org/html/2609.04183v1#S4.SS2.p2.1 "4.2 Ablation Studies ‣ 4 Experiments ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning").


## Appendix

In this Appendix, we provide additional details and qualitative results to support our findings.

## Appendix A Additional Implementation Details

Frame Sampling.
Following ILCACM [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "") and SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 ""), we uniformly sample 32 and 100 frames per video for ActivityNet Captions and YouCook2, respectively.

VLM Settings.
For caption generation with BLIP-2 [Li et al. (2023)](https://arxiv.org/html/2609.04183v1#bib.bib23 ""), we employ the blip2-opt-2.7b model and use the prompt “What is happening in this image?”.
For InternVL3 and Qwen2.5-VL, we use the prompt “Describe this image briefly in one sentence.”, with the maximum number of newly generated tokens set to 30.

Additional Details.
We set the number of event queries to 22 for ActivityNet Captions and 18 for YouCook2. For the video encoder, we follow the ILCACM [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "") architecture, which consists of a single Conv1D layer (kernel size 5) followed by a single Transformer decoder layer. To prevent overfitting, we additionally apply label smoothing during training.

For inter-event processing, we sort the predicted event masks by their temporal centers such that c1≤c2≤⋯≤cNec\_{1}\\leq c\_{2}\\leq\\cdots\\leq c\_{N\_{e}}, following [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "").
Since gaps spanning only a few frames are unlikely to yield meaningful transitions or reliable statistics, we apply Narrative-Aware Inter-Event Selection only to gaps containing at least 4 frames, discarding any shorter gap.

Inference Details.
At test time, our model follows the same inference procedure as [Ge et al. (2025)](https://arxiv.org/html/2609.04183v1#bib.bib8 "") to generate temporally localized event captions.
First, the complete video embedding is decoded with a global context prompt, i.e., “\[FULL\]”, producing an initial set of event descriptions while adaptively estimating the number of events in the video.
The mask generation module then predicts the temporal center and width of each identified event, from which Gaussian attention masks are constructed.
Finally, each masked event representation is decoded with event-specific conditioning, i.e., “\[MASK\] 1 events:”, to refine the initial captions and generate more precise event descriptions.

Importantly, the VLM-generated narratives in SBS are generated offline before training and are used only to construct selective inter-event supervision during training.
Therefore, SBS introduces no VLM dependency at inference time.
The trained DVC model predicts event masks and captions using the same base WSDVC pipeline.

|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
| Method | Score | Time |
| S\_c | R-L | C | F1 | H |
| SAIL† (LLM) | 6.29 | 15.29 | 35.38 | 57.00 | 1H 38M |
| SBS (VLM) | 6.49 | 15.60 | 36.87 | 58.18 | 1H 46M |

Table A.1: Offline caption-generation time. SBS’s VLM-based generation requires comparable offline generation time to SAIL’s LLM-based synthesis (1H 46M vs. 1H 38M), while yielding better captioning and localization performance.
†\\dagger denotes that SAIL’s generation time was measured under our own re-implementation.

## Appendix B Computational Cost

We measure two types of cost: the offline caption generation time and the training/inference overhead.
For caption generation, we follow the LLM inference procedure described in SAIL [Kim et al. (2026)](https://arxiv.org/html/2609.04183v1#bib.bib1 "") to synthesize transition captions on ActivityNet Captions.
As shown in [TableA.1](https://arxiv.org/html/2609.04183v1#A1.T1 "In Appendix A Additional Implementation Details ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning"), our VLM-based caption generation requires comparable offline time to SAIL’s LLM-based synthesis (1H 46M vs. 1H 38M), while yielding clearly better captioning and localization scores.
Importantly, captions are generated offline before training, and only their precomputed features are loaded during training, so this step incurs no cost in the training loop.

## Appendix C More Qualitative Results

[FigureA.1](https://arxiv.org/html/2609.04183v1#A3.F1 "In Appendix C More Qualitative Results ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning") and [FigureA.2](https://arxiv.org/html/2609.04183v1#A3.F2 "In Appendix C More Qualitative Results ‣ Seeing Before Synthesizing: VLM-Guided Transition Event Discovery for Weakly-Supervised Dense Video Captioning") provide further qualitative comparisons on ActivityNet Captions and YouCook2, respectively, where blue boxes denote our VLM-based inter-event captions and red boxes denote the LLM-based ones used by prior work.
SBS selectively discards uninformative gaps in which no meaningful transition occurs between adjacent events, and instead supplies a transition guide only at moments of genuine change (e.g., when rafting begins or a jump is performed).
Furthermore, whereas the LLM-based method aligns its captions with mismatched regions due to hallucinated content and a fixed placement rule, SBS anchors each transition at the correct temporal location, yielding captions that are faithfully aligned with the underlying frames.

![Refer to caption](https://arxiv.org/html/2609.04183v1/anet_suppl.png)Figure A.1: Qualitative results about transition events on ActivityNet Captions.
![Refer to caption](https://arxiv.org/html/2609.04183v1/yc2_suppl.png)Figure A.2: Qualitative results about transition events on YouCook2.