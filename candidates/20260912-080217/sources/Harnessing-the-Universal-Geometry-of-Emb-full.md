Title:

Content selection saved. Describe the issue below:

Description:

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2505.12540v4 \[cs.LG\] 26 Jan 2026

# Harnessing the Universal Geometry of Embeddings

Rishi Jha
Collin Zhang
Vitaly Shmatikov
John X. Morris
Affiliation: Department of Computer Science
Affiliation: Cornell University

###### Abstract

We introduce the first method for translating text embeddings from one vector space to another without any paired data, encoders, or predefined sets of matches. Our unsupervised approach translates any embedding to and from a universal latent representation (i.e., a universal semantic structure conjectured by the Platonic Representation Hypothesis). Our translations achieve high cosine similarity across model pairs with different architectures, parameter counts, and training datasets.

The ability to translate unknown embeddings into a different space while preserving their geometry has serious implications for security. An adversary with access to a database of only embedding vectors can extract sensitive information about underlying documents, sufficient for classification and attribute inference.

Figure 1: Left: input embeddings from different model families (T5-based GTR \[ [47](https://arxiv.org/html/2505.12540v4#bib.bibx47 "")\] and BERT-based GTE \[ [32](https://arxiv.org/html/2505.12540v4#bib.bibx32 "")\]) are fundamentally incomparable. Right:
given unpaired embedding samples from different models on different texts, our model learns a latent representation where they are closely aligned.![Refer to caption](https://arxiv.org/html/2505.12540v4/diagram.png)Figure 2: Given only a vector database from an unknown model, vec2vec translates the database into the space of a known model using latent structure alone. Converted embeddings reveal sensitive information about the original documents, such as the topic of an email (pictured, real example).

## 1 Introduction

Text embeddings are the backbone of modern NLP, powering tasks like retrieval, RAG, classification, and clustering. There are many embedding models trained on different datasets, data shufflings, and initializations. An embedding of a text encodes its semantics: a good model maps texts with similar semantics to vectors close to each other in the embedding space. Since semantics is a property of text, different embeddings of the same text should encode the same semantics. In practice, however, different models encode texts into completely different and incompatible vector spaces.

The Platonic Representation Hypothesis \[ [18](https://arxiv.org/html/2505.12540v4#bib.bibx18 "")\] conjectures that all vision models of sufficient size converge to the same latent representation. We propose a stronger, constructive version of this hypothesis for text models: the universal latent structure of text representations can be learned and, furthermore, harnessed to translate representations from one space to another without any paired data or encoders.

In this work, we show that the Strong Platonic Representation Hypothesis holds in practice. Given unpaired examples of embeddings from two models with different architectures and training data, our method learns a latent representation in which the embeddings are almost identical ( [Figure1](https://arxiv.org/html/2505.12540v4#S0.F1 "In Harnessing the Universal Geometry of Embeddings")).

We draw inspiration from research on aligning word embeddings across languages \[ [62](https://arxiv.org/html/2505.12540v4#bib.bibx62 ""), [10](https://arxiv.org/html/2505.12540v4#bib.bibx10 ""), [15](https://arxiv.org/html/2505.12540v4#bib.bibx15 ""), [9](https://arxiv.org/html/2505.12540v4#bib.bibx9 "")\] and unsupervised image translation
\[ [36](https://arxiv.org/html/2505.12540v4#bib.bibx36 ""), [70](https://arxiv.org/html/2505.12540v4#bib.bibx70 "")\]. Our vec2vec method uses adversarial losses and cycle consistency to learn to encode embeddings into a shared latent space and decode with minimal loss. This makes unsupervised translation possible. We use a basic adversarial approach with vector space preservation \[ [46](https://arxiv.org/html/2505.12540v4#bib.bibx46 "")\] to learn a mapping from an unknown embedding distribution to a known one.

vec2vec is the
first method to successfully translate embeddings from the space of one model to another without paired data.111Prior work has successfully translated _word_ embeddings between languages, typically relying on overlapping vocabularies across languages. In contrast, we translate embeddings of entire sequences between model spaces.vec2vec
translations achieve cosine similarity as high as 0.960.96 to the ground-truth vectors in their target embedding spaces and perfect matching on over 80008000 shuffled embeddings (without access to the set of possible matches in advance).

To show that our translations preserve not only the relative geometry of embeddings but also the semantics of underlying inputs, we extract information from them using zero-shot attribute inference and inversion, without any knowledge of the model that produced the original embeddings.222







Our code is available [on GitHub.](https://github.com/rjha18/vec2vec/ "")

## 2 Problem formulation: unsupervised embedding translation

Consider a collection of embedding vectors {u1,…​un}\\{u\_{1},\\ldots u\_{n}\\}, for example, a dump of a compromised vector database, where each ui=M1​(di)u\_{i}=M\_{1}(d\_{i}) is generated by an unknown encoder M1:𝕍s→ℝdM1M\_{1}:\\mathbb{V}^{s}\\rightarrow\\mathbb{R}^{d\_{M\_{1}}} from an unknown document did\_{i}. We cannot make queries to M1M\_{1} and do not know its training data, nor architectural details. Our goal is to extract any information about the documents did\_{i}.

![Refer to caption](https://arxiv.org/html/2505.12540v4/spaces.png)Figure 3: Unsupervised embedding translation. With access to only ui=M1​(di)u\_{i}=M\_{1}(d\_{i}), vec2vec seeks to generate a translation F⁡(ui)F(u\_{i}) that is close in M2M\_{2}’s embedding space to the ideal embedding vi=M2​(di)v\_{i}=M\_{2}(d\_{i}) without access to did\_{i}, viv\_{i}, or M1M\_{1}.

We do assume access to a different encoder M2M\_{2} that we can query at will to generate new embeddings in some other space. We also assume high-level distributional knowledge about the hidden documents: their modality (text) and language (e.g., English). To extract information, we may translate {u1,…​un}\\{u\_{1},\\ldots u\_{n}\\} into the output space of M2M\_{2} and apply techniques like inversion that require the encoder.

Limitations of correspondence methods.
There is significant prior research on the problem of matching or correspondence between sets of embedding vectors \[ [1](https://arxiv.org/html/2505.12540v4#bib.bibx1 ""), [49](https://arxiv.org/html/2505.12540v4#bib.bibx49 ""), [8](https://arxiv.org/html/2505.12540v4#bib.bibx8 ""), [54](https://arxiv.org/html/2505.12540v4#bib.bibx54 "")\]. These methods typically assume that the two (or more) sets of embeddings are generated by different encoders on the _same or highly-overlapping inputs_. In other words, for each unknown vector, there must already exist a set of candidate vectors in a different embedding. In practice, it is unrealistic to expect that such a database be available, so these methods are not directly applicable. Some matching methods, however, support translation between embedding spaces without overlapping inputs. Our experiments demonstrate that these methods struggle significantly, even when correspondence exists.

Our task is inherently more challenging than matching, because we do not assume access to encoder M1M\_{1}, nor do we have additional representations of documents d1,…,dn{d\_{1},\\ldots,d\_{n}} beyond their embeddings ui=M1​(di)u\_{i}=M\_{1}(d\_{i}). Therefore, we rely solely on unsupervised translation from M1M\_{1} to M2M\_{2}. The effectiveness of such unsupervised translation approaches thus critically depends on identifying and leveraging shared geometric structures within the embedding spaces produced by M1M\_{1} and M2M\_{2}.

The Strong Platonic Representation Hypothesis.
Our hope that unsupervised embedding translation is possible at all rests on the stronger version of the Platonic Representation Hypothesis \[ [18](https://arxiv.org/html/2505.12540v4#bib.bibx18 "")\]. Our conjecture is as follows:
_neural networks trained with the same objective and modality, but with different data and model architectures, converge to a universal latent space such that a translation between their respective representations can be learned without any pairwise correspondence._

Translation enables information extraction. Solving unsupervised translation will allow us to use information extraction tools designed to operate on vectors produced by known encoders. For example, we could apply inversion models \[ [43](https://arxiv.org/html/2505.12540v4#bib.bibx43 ""), [67](https://arxiv.org/html/2505.12540v4#bib.bibx67 "")\] to recover unknown documents {di}\\{d\_{i}\\}.

## 3 Our method: vec2vec

Unsupervised translation has been successful in computer vision, using a combination of cycle consistency and adversarial regularization \[ [36](https://arxiv.org/html/2505.12540v4#bib.bibx36 ""), [70](https://arxiv.org/html/2505.12540v4#bib.bibx70 "")\]. Our design of vec2vec is inspired in part by these methods. We aim to learn embedding-space translations that are cycle-consistent (mapping to and from an embedding space should end in the same place) and indistinguishable (embeddings for the same text from either space should have identical latents).

### 3.1 Architecture

We propose a modular architecture, where embeddings are encoded and decoded using space-specific adapter modules and passed through a shared backbone network. [Figure2](https://arxiv.org/html/2505.12540v4#S0.F2 "In Harnessing the Universal Geometry of Embeddings") shows these components. Input adapters A1:ℝd→ℝZA\_{1}:\\mathbb{R}^{d}\\to\\mathbb{R}^{Z} and A2:ℝd→ℝZA\_{2}:\\mathbb{R}^{d}\\to\\mathbb{R}^{Z} transform embeddings from each encoder-specific space into a universal latent representation of dimension ZZ. The shared backbone T:ℝZ→ℝZT:\\mathbb{R}^{Z}\\to\\mathbb{R}^{Z} extracts a common latent embedding from adapted inputs. Output adapters B1:ℝZ→ℝdB\_{1}:\\mathbb{R}^{Z}\\to\\mathbb{R}^{d} and B2:ℝZ→ℝdB\_{2}:\\mathbb{R}^{Z}\\to\\mathbb{R}^{d} translate these common latent embeddings back into the encoder-specific spaces. Thus, translation functions F1,F2F\_{1},F\_{2} and additional reconstruction mappings R1,R2R\_{1},R\_{2} are defined as:

|     |     |     |
| --- | --- | --- |
|  | F1=B2∘T∘A1,F2=B1∘T∘A2R1=B1∘T∘A1R2=B2∘T∘A2F\_{1}=B\_{2}\\circ T\\circ A\_{1},\\quad F\_{2}=B\_{1}\\circ T\\circ A\_{2}\\quad R\_{1}=B\_{1}\\circ T\\circ A\_{1}\\quad R\_{2}=B\_{2}\\circ T\\circ A\_{2} |  |

Parameters of all components are collectively denoted θ={A1,A2,T,B1,B2}\\theta=\\{A\_{1},A\_{2},T,B\_{1},B\_{2}\\}.

Unlike images, embeddings do not have any spatial bias. Instead of CNNs, we use multilayer perceptrons (MLP) with residual connections, layer normalization, and SiLU nonlinearities. Discriminators mirror this structure but omit residual connections to simplify adversarial learning.

### 3.2 Optimization

In addition to the ‘generator’ networks FF and RR, we introduce discriminators operating on both the latent representations of FF (D1ℓ,D2ℓD\_{1}^{\\ell},D\_{2}^{\\ell}) and the output embeddings (D1,D2D\_{1},D\_{2}).

Our goal is to train the parameters of θ\\theta by solving:

|     |     |     |     |
| --- | --- | --- | --- |
|  | θ∗=arg⁡minθ​maxD1,D2,D1ℓ,D2ℓ​ℒadv​(F1,F2,D1,D2,D1ℓ,D2ℓ)+λgen​ℒgen​(θ),\\theta^{\*}=\\arg\\min\_{\\theta}\\max\_{D\_{1},D\_{2},D\_{1}^{\\ell},D\_{2}^{\\ell}}\\mathcal{L}\_{\\text{adv}}(F\_{1},F\_{2},D\_{1},D\_{2},D\_{1}^{\\ell},D\_{2}^{\\ell})+\\lambda\_{\\text{gen}}\\mathcal{L}\_{\\text{gen}}(\\theta), |  | (1) |

where ℒadv\\mathcal{L}\_{\\text{adv}} and ℒgen\\mathcal{L}\_{\\text{gen}} represent adversarial and generator-specific constraints respectively and hyperparameter λgen\\lambda\_{\\rm gen} controls their tradeoff.

Adversarial.
The adversarial loss encourages generated embeddings to match the empirical distributions of original embeddings both at the embedding and latent levels. Specifically, applying the standard GAN loss formulation \[ [13](https://arxiv.org/html/2505.12540v4#bib.bibx13 "")\] to both levels yields:

|     |     |     |     |
| --- | --- | --- | --- |
|  | ℒadv​(F1,F2,D1,D2,D1ℓ,D2ℓ)\\displaystyle\\mathcal{L}\_{\\text{adv}}(F\_{1},F\_{2},D\_{1},D\_{2},D\_{1}^{\\ell},D\_{2}^{\\ell}) | =ℒGAN​(D1,F1)+ℒGAN​(D2,F2)\\displaystyle=\\mathcal{L}\_{\\text{GAN}}(D\_{1},F\_{1})+\\mathcal{L}\_{\\text{GAN}}(D\_{2},F\_{2}) |  |
|  |  | +ℒGAN​(D1ℓ,T∘A1)+ℒGAN​(D2ℓ,T∘A2).\\displaystyle\\quad+\\mathcal{L}\_{\\text{GAN}}(D\_{1}^{\\ell},T\\circ A\_{1})+\\mathcal{L}\_{\\text{GAN}}(D\_{2}^{\\ell},T\\circ A\_{2}). |  |

Generator.
Because adversarial losses alone do not guarantee that translated embeddings preserve semantics \[ [70](https://arxiv.org/html/2505.12540v4#bib.bibx70 "")\], we introduce three additional constraints to help the generator learn a useful mapping:

Reconstruction enforces that an embedding, when mapped into the latent space and back into its original embedding space, closely matches its initial representation:

|     |     |     |
| --- | --- | --- |
|  | ℒrec​(R1,R2)=𝔼x∼p​‖R1​(x)−x‖22+𝔼y∼q​‖R2​(y)−y‖22.\\displaystyle\\mathcal{L}\_{\\text{rec}}(R\_{1},R\_{2})=\\mathbb{E}\_{x\\sim p}\\\|R\_{1}(x)-x\\\|\_{2}^{2}+\\mathbb{E}\_{y\\sim q}\\\|R\_{2}(y)-y\\\|\_{2}^{2}. |  |

where pp and qq are distributions of embeddings sampled from M1M\_{1} and M2M\_{2}, respectively.

Cycle-consistency acts as an unsupervised proxy for supervised pair alignment, ensuring that FF and GG can translate an embedding to the other embedding space and back again with minimal corruption:

|     |     |     |
| --- | --- | --- |
|  | ℒCC​(F1,F2)=𝔼x∼p​‖F2​(F1​(x))−x‖22+𝔼y∼q​‖F1​(F2​(y))−y‖22.\\displaystyle\\mathcal{L}\_{\\text{CC}}(F\_{1},F\_{2})=\\mathbb{E}\_{x\\sim p}\\\|F\_{2}(F\_{1}(x))-x\\\|\_{2}^{2}+\\mathbb{E}\_{y\\sim q}\\\|F\_{1}(F\_{2}(y))-y\\\|\_{2}^{2}. |  |

Vector space preservation (VSP) ensures that pairwise relationships between translated embeddings are consistent with the target space \[ [46](https://arxiv.org/html/2505.12540v4#bib.bibx46 ""), [65](https://arxiv.org/html/2505.12540v4#bib.bibx65 "")\]. Given a batch of BB embeddings x1,…,xBx\_{1},...,x\_{B} and y1,…,yBy\_{1},...,y\_{B}, we sum their average pairwise distances after translation by both F1F\_{1} and F2F\_{2}:

|     |     |     |     |
| --- | --- | --- | --- |
|  | ℒVSP(F1,F2)=1B2∑i=1B∑j=1B\[\\displaystyle\\mathcal{L}\_{\\text{VSP}}(F\_{1},F\_{2})=\\frac{1}{B^{2}}\\sum\_{i=1}^{B}\\sum\_{j=1}^{B}\\bigg\[ | ‖M1​(xi)⋅M1​(xj)−F2​(M2​(yi))⋅F2​(M2​(yj))‖22\\displaystyle\\\|M\_{1}(x\_{i})\\cdot M\_{1}(x\_{j})-F\_{2}(M\_{2}(y\_{i}))\\cdot F\_{2}(M\_{2}(y\_{j}))\\\|\_{2}^{2} |  |\
|  |  | +∥M2(yi)⋅M2(yj)−F1(M1(xi))⋅F1(M1(xj))∥22\]\\displaystyle+\\\|M\_{2}(y\_{i})\\cdot M\_{2}(y\_{j})-F\_{1}(M\_{1}(x\_{i}))\\cdot F\_{1}(M\_{1}(x\_{j}))\\\|\_{2}^{2}\\bigg\] |  |

Combining these losses yields:
ℒgen​(θ)=λrec​ℒrec​(R1,R2)+λCC​ℒCC​(F1,F2)+λVSP​ℒVSP​(F1,F2)\\mathcal{L}\_{\\text{gen}}(\\theta)=\\lambda\_{\\text{rec}}\\mathcal{L}\_{\\text{rec}}(R\_{1},R\_{2})+\\lambda\_{\\text{CC}}\\mathcal{L}\_{\\text{CC}}(F\_{1},F\_{2})+\\lambda\_{\\text{VSP}}\\mathcal{L}\_{\\text{VSP}}(F\_{1},F\_{2}), where hyperparameters λCC\\lambda\_{\\text{CC}}, λrec\\lambda\_{\\text{rec}}, and λVSP\\lambda\_{\\text{VSP}} control relative importance.

## 4 Experimental setup

### 4.1 Preliminaries

Datasets.
We use the Natural Questions (NQ)\[ [25](https://arxiv.org/html/2505.12540v4#bib.bibx25 "")\] dataset of user queries and Wikipedia-sourced answers for training (a 22-million subset) and evaluation (a 6553665536 subset). To evaluate information extraction, we use
TweetTopic\[ [2](https://arxiv.org/html/2505.12540v4#bib.bibx2 "")\], a dataset of tweets multi-labeled by 19 topics; a random 81928192-record subset of
Pseudo Re-identified MIMIC-III (MIMIC)\[ [28](https://arxiv.org/html/2505.12540v4#bib.bibx28 "")\], a pseudo re-identified version of the MIMIC dataset \[ [19](https://arxiv.org/html/2505.12540v4#bib.bibx19 "")\] of patient records multi-labeled by 2673 MedCAT \[ [24](https://arxiv.org/html/2505.12540v4#bib.bibx24 "")\] disease descriptions; and a random 5050-email subset of
the Enron Email Corpus (Enron)\[ [21](https://arxiv.org/html/2505.12540v4#bib.bibx21 "")\], an unlabeled, public dataset of
internal emails from a defunct energy company. In [AppendixD](https://arxiv.org/html/2505.12540v4#A4 "Appendix D Text-image retrieval on MS COCO ‣ Harnessing the Universal Geometry of Embeddings"), we ablate a model on MS COCO\[ [34](https://arxiv.org/html/2505.12540v4#bib.bibx34 "")\], a captioned image dataset, to evaluate performance on multimodal retrieval.

Models. [Table1](https://arxiv.org/html/2505.12540v4#S4.T1 "In 4.1 Preliminaries ‣ 4 Experimental setup ‣ Harnessing the Universal Geometry of Embeddings") lists the embedding models representing four size categories, five transformer backbones, and two output dimensionalities. Granite is multilingual; CLIP is multimodal. Since Qwen is very compute-intensive, we only evaluate it for a single model pair in [AppendixC](https://arxiv.org/html/2505.12540v4#A3 "Appendix C Translating to and from Qwen ‣ Harnessing the Universal Geometry of Embeddings").

| Model | Params (M) | Backbone | Year | Dims | Max Seq. |
| --- | --- | --- | --- | --- | --- |
| \[ [47](https://arxiv.org/html/2505.12540v4#bib.bibx47 "")\] gtr | 110 | T5 | 2021 | 768 | 512 |
| \[ [50](https://arxiv.org/html/2505.12540v4#bib.bibx50 "")\] clip | 151 | CLIP | 2021 | 512 | 77 |
| \[ [58](https://arxiv.org/html/2505.12540v4#bib.bibx58 "")\] e5 | 109 | BERT | 2022 | 768 | 512 |
| \[ [32](https://arxiv.org/html/2505.12540v4#bib.bibx32 "")\] gte | 109 | BERT | 2023 | 768 | 512 |
| \[ [68](https://arxiv.org/html/2505.12540v4#bib.bibx68 "")\] stella | 109 | BERT | 2023 | 768 | 512 |
| \[ [14](https://arxiv.org/html/2505.12540v4#bib.bibx14 "")\] granite | 278 | RoBERTa | 2024 | 768 | 512 |
| \[ [69](https://arxiv.org/html/2505.12540v4#bib.bibx69 "")\] qwen | 4000 | Qwen3 | 2025 | 2560 | 32K |

Table 1: Embedding models used in our experiments.

Training.
Unless otherwise specified, each vec2vec is trained on two sets of embeddings generated from disjoint sets of 11 million 6464-token sequences sampled from NQ (see [Section7](https://arxiv.org/html/2505.12540v4#S7 "7 Ablations ‣ Harnessing the Universal Geometry of Embeddings") for experiments with fewer embeddings). Due to GAN instability \[ [53](https://arxiv.org/html/2505.12540v4#bib.bibx53 "")\], we select the best of multiple initializations (see [AppendixE](https://arxiv.org/html/2505.12540v4#A5 "Appendix E Initialization robustness by model backbone ‣ Harnessing the Universal Geometry of Embeddings")) and leave more robust training to future work. See [AppendixA](https://arxiv.org/html/2505.12540v4#A1 "Appendix A Compute ‣ Harnessing the Universal Geometry of Embeddings") for compute details.

### 4.2 Evaluating translation

Let ui=M1​(di)u\_{i}=M\_{1}(d\_{i}) and vi=M2​(di)v\_{i}=M\_{2}(d\_{i}) denote the source and target embeddings of the same input did\_{i}. The goal of translation is to generate a vector that is as close to viv\_{i} as possible. We say that (ui,vj)(u\_{i},v\_{j}) are “aligned” by the translator FF if vjv\_{j} is the closest embedding to F⁡(ui)F(u\_{i}): j=arg⁡mink⁡cos⁡(F⁡(ui),vk).j=\\arg\\min\_{k}\\cos\\bigl(F(u\_{i}),v\_{k}\\bigr).
A perfect translator F∗F^{\*} satisfies i=arg⁡mink⁡cos⁡(F∗​(ui),vk)i=\\arg\\min\_{k}\\cos\\bigl(F^{\*}(u\_{i}),v\_{k}\\bigr) for all ii.

Given (unknown) embeddings {M2​(dj)}j=0n\\{M\_{2}(d\_{j})\\}\_{j=0}^{n} ordered by decreasing cosine similarity to F⁡(ui)F(u\_{i}), let rir\_{i} be the rank of the correct embedding vi=M2​(di)v\_{i}=M\_{2}(d\_{i}). To measure quality of FF, we use three metrics. Mean Cosine Similarity measures how close translations are, on average, to their targets. Top-1 Accuracy is the fraction of translations whose target is closer than any other embedding. Mean Rank is the average
rank of targets with respect to translations. The ideal translator F∗F^{\*} achieves mean similarity of 1.01.0, top-1 accuracy of 1.01.0, and mean rank of 1.01.0. Recall that a random alignment corresponds to a mean rank of n2\\frac{n}{2}. Formally,

|     |     |     |
| --- | --- | --- |
|  | cos(ui,vi)=1n∑i=1n\[1−cos(F(ui),vi)\]Top-1(r)=1n∑i=1n𝟏{ri=1}Rank(r)=1n∑i=1nri\\cos(u\_{i},v\_{i})=\\frac{1}{n}\\sum\_{i=1}^{n}\\bigl\[1-\\cos\\bigl(F(u\_{i}),v\_{i}\\bigr)\\bigr\]\\quad\\text{Top-1}(r)=\\frac{1}{n}\\sum\_{i=1}^{n}\\mathbf{1}\\{r\_{i}=1\\}\\quad\\text{Rank(r)}=\\frac{1}{n}\\sum\_{i=1}^{n}r\_{i} |  |

vec2vec is the first unsupervised embedding translator, thus there is no direct baseline. As our Naïve baseline, we simply use F⁡(x)=xF(x)=x to measure geometric similarity between embedding spaces. The second (pseudo)baseline is Oracle-aided optimal transport. It assumes that candidate targets are known and is thus strictly easier than vec2vec and the Naïve baseline. We solve optimal assignment, π∗=arg⁡min⁡∑i=1nπ⁡cos⁡(ui,vπ⁡(i))\\pi^{\*}=\\arg\\min\_{\\pi}\\sum\_{i=1}^{n}\\cos(u\_{i},v\_{\\pi(i)}), via either the Hungarian, Earth Mover’s Distance, Sinkhorn, or (Entropic) Gromov-Wasserstein algorithms, choosing the solver with the lowest rank for each experiment. See [AppendixB](https://arxiv.org/html/2505.12540v4#A2 "Appendix B Oracle-aided optimal transport baseline ‣ Harnessing the Universal Geometry of Embeddings") for more details.

### 4.3 Evaluating information extraction

We measure whether translation preserves semantics via attribute inference:
for each translated embedding F​(M1​(di))F(M\_{1}(d\_{i})), our goal is to infer attributes ci⊆𝒞c\_{i}\\subseteq\\mathcal{C} of did\_{i}.

The first method we use is zero-shot embedding attribute inference: calculate pairwise cosine similarities between F​(M1​(di))F(M\_{1}(d\_{i})) and the embeddings of all attributes in 𝒞\\mathcal{C}, identify top kk closest attributes, and measure whether they are correct via top-kk accuracy: 1n∑i=0n𝟏{\|cik∩ci\|≥1}\\frac{1}{n}\\sum\_{i=0}^{n}\\mathbf{1}\\left\\{\|c^{k}\_{i}\\cap c\_{i}\|\\geq 1\\right\\}.

The second method is embedding inversion that recovers text inputs from embeddings. Since \[ [43](https://arxiv.org/html/2505.12540v4#bib.bibx43 "")\] requires a pre-trained inversion model for each embedding space, we use \[ [67](https://arxiv.org/html/2505.12540v4#bib.bibx67 "")\] instead to generate an approximation di′d^{\\prime}\_{i} of did\_{i} from F​(M1​(di))F(M\_{1}(d\_{i})) in a zero-shot manner. We measure the extracted information using LLM judge accuracy: the fraction of translated embeddings for which GPT-4o determines that d′d^{\\prime} reveals information in dd. See [AppendixH](https://arxiv.org/html/2505.12540v4#A8 "Appendix H Prompt for measuring information extraction ‣ Harnessing the Universal Geometry of Embeddings") for our prompt.

In addition to the Naïve baseline, we also consider an Oracle attribute inference: zero-shot classification with the correct embedding M2​(d)M\_{2}(d) and class labels M2​(𝒞)M\_{2}(\\mathcal{C}).

## 5 vec2vec learns to translate embeddings without any paired data

We first show that vec2vec learns a universal latent space, then demonstrate that this space preserves the geometry of all embeddings. Therefore, we can use it like a universal language of text encoders to translate their representations without any paired data.

![Refer to caption](https://arxiv.org/html/2505.12540v4/cosine_heatmaps.png)Figure 4: Pairwise cosine similarities of input embeddings (left) and their vec2vec latents (middle) across different embedding pairs. The absolute difference between the heatmaps plots is on the right. All numbers are computed on the same batch of 1024 NQ texts.

vec2vec learns a universal latent space.vec2vec projects embeddings M1,2,…M\_{1,2,\\ldots} into a shared latent space via compositions of input adapters (A1,2,…A\_{1,2,\\ldots}) and a shared translator TT. [Figure4](https://arxiv.org/html/2505.12540v4#S5.F4 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings") shows that even when the embeddings ui=M1​(di)u\_{i}=M\_{1}(d\_{i}) and vi=M2​(di)v\_{i}=M\_{2}(d\_{i}) are far apart (i.e., have low cosine similarity), their representations in vec2vec’s latent space are incredibly close: T⁡(A1​(ui))≈T⁡(A2​(vi))T(A\_{1}(u\_{i}))\\approx T(A\_{2}(v\_{i})). [Figure1](https://arxiv.org/html/2505.12540v4#S0.F1 "In Harnessing the Universal Geometry of Embeddings") visualizes this (via two-dimensional projections) for vec2vec trained on GTE and GTR embeddings: the embeddings are far apart, but their latents
are _nearly overlapping_.

|  | vec2vec | Naïve Baseline | OT Baseline |
| --- | --- | --- | --- |
| M1M\_{1} | M2M\_{2} | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gra. | gtr | 0.80 (0.0) | 0.99 | 1.19 (0.1) | -0.03 (0.0) | 0.00 | 4168.73 (9.2) | 0.70 (0.0) | 0.00 | 2773.72 (8.6)‡ |
| gte | 0.87 (0.0) | 0.95 | 1.18 (0.0) | 0.01 (0.0) | 0.00 | 4088.58 (9.2) | 0.85 (0.0) | 0.00 | 2680.02 (8.6)‡ |
| ste. | 0.79 (0.0) | 0.98 | 1.05 (0.0) | 0.01 (0.0) | 0.00 | 4208.26 (9.2) | 0.67 (0.0) | 0.00 | 3446.52 (8.8)‡ |
| e5 | 0.85 (0.0) | 0.98 | 1.11 (0.0) | 0.02 (0.0) | 0.00 | 4111.60 (9.2) | 0.83 (0.0) | 0.00 | 3569.59 (8.7)‡ |
| gtr | gra. | 0.81 (0.0) | 0.99 | 1.02 (0.0) | -0.03 (0.0) | 0.00 | 4169.76 (9.2) | 0.70 (0.0) | 0.00 | 2775.17 (8.6)‡ |
| gte | 0.87 (0.0) | 0.93 | 2.31 (0.1) | 0.04 (0.0) | 0.00 | 4080.92 (9.2) | 0.85 (0.0) | 0.00 | 3070.69 (8.9)‡ |
| ste. | 0.80 (0.0) | 0.99 | 1.03 (0.0) | 0.00 (0.0) | 0.00 | 4198.78 (9.2) | 0.67 (0.0) | 0.00 | 3559.06 (9.1)‡ |
| e5 | 0.83 (0.0) | 0.84 | 2.88 (0.2) | 0.03 (0.0) | 0.00 | 4082.84 (9.2) | 0.83 (0.0) | 0.00 | 3888.01 (8.9)‡ |
| gte | gra. | 0.75 (0.0) | 0.95 | 1.22 (0.0) | 0.01 (0.0) | 0.00 | 4079.81 (9.3) | 0.69 (0.0) | 0.00 | 2664.38 (8.6)‡ |
| gtr | 0.75 (0.0) | 0.91 | 2.64 (0.1) | 0.04 (0.0) | 0.00 | 4084.15 (9.2) | 0.70 (0.0) | 0.00 | 3064.16 (8.9)‡ |
| ste. | 0.89 (0.0) | 1.00 | 1.00 (0.0) | 0.56 (0.0) | 1.00 | 1.00 (0.0) | 0.71 (0.0) | 1.00 | 1.00 (0.0)† |
| e5 | 0.87 (0.0) | 0.99 | 5.19 (0.5) | 0.68 (0.0) | 1.00 | 1.00 (0.0) | 0.84 (0.0) | 1.00 | 1.00 (0.0)† |
| ste. | gra. | 0.80 (0.0) | 0.98 | 1.08 (0.0) | 0.01 (0.0) | 0.00 | 4209.08 (9.3) | 0.69 (0.0) | 0.00 | 3419.44 (8.8)‡ |
| gtr | 0.82 (0.0) | 1.00 | 1.10 (0.0) | 0.00 (0.0) | 0.00 | 4192.31 (9.2) | 0.70 (0.0) | 0.00 | 3555.64 (9.0)‡ |
| gte | 0.92 (0.0) | 1.00 | 1.00 (0.0) | 0.56 (0.0) | 1.00 | 1.00 (0.0) | 0.87 (0.0) | 1.00 | 1.00 (0.0)† |
| e5 | 0.86 (0.0) | 1.00 | 1.00 (0.0) | 0.38 (0.0) | 0.99 | 1.03 (0.0) | 0.83 (0.0) | 1.00 | 1.00 (0.0)† |
| e5 | gra. | 0.81 (0.0) | 0.99 | 2.20 (0.2) | 0.02 (0.0) | 0.00 | 4120.60 (9.3) | 0.69 (0.0) | 0.00 | 3526.02 (8.7)‡ |
| gtr | 0.74 (0.0) | 0.82 | 2.56 (0.0) | 0.03 (0.0) | 0.00 | 4080.76 (9.3) | 0.70 (0.0) | 0.00 | 3877.03 (8.8)‡ |
| gte | 0.90 (0.0) | 1.00 | 1.01 (0.0) | 0.68 (0.0) | 1.00 | 1.00 (0.0) | 0.86 (0.0) | 1.00 | 1.00 (0.0)† |
| ste. | 0.78 (0.0) | 1.00 | 1.00 (0.0) | 0.38 (0.0) | 1.00 | 1.00 (0.0) | 0.69 (0.0) | 1.00 | 1.00 (0.0)† |

Table 2: In-distribution translations: vec2vecs trained on NQ and evaluated on a 65536 text subset of NQ (chunked in batches of size 8192). The rank metric varies from 1 to 8192, thus 4096 corresponds to a random ordering. Standard errors are shown in parentheses. Bold denotes best value. Symbols denote the lowest-rank solver for specific experiments: Sinkhorn† and Gromov-Wasserstein‡.

vec2vec translations mirror target geometry. [Table2](https://arxiv.org/html/2505.12540v4#S5.T2 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings") shows that vec2vec generates embeddings with near-optimal assignment across model pairs, achieving cosine similarity scores up to 0.92, top-1 accuracies up to 100%, and ranks as low as 1. In same-backbone pairings (e.g., (gte, e5)), vec2vec’s top-1 accuracy and rank are comparable to both the naïve baseline and (surprisingly) the oracle-aided optimal transport. Although the embeddings generated by vec2vec are significantly closer to the ground truth than the naïve baseline, in same-backbone pairings the embeddings are close enough to be compatible. In cross-backbone pairings, vec2vec is far superior on all metrics, while baseline methods perform similarly to random guessing.

|  | TweetTopic | MIMIC |
| --- | --- | --- |
| M1M\_{1} | M2M\_{2} | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gran. | gtr | 0.74 (0.0) | 0.99 | 1.09 (0.1) | 0.74 (0.0) | 0.60 | 23.38 (1.6) |
| gte | 0.85 (0.0) | 0.95 | 1.26 (0.1) | 0.85 (0.0) | 0.08 | 346.21 (7.8) |
| stel. | 0.77 (0.0) | 0.96 | 1.11 (0.0) | 0.72 (0.0) | 0.13 | 242.23 (6.1) |
| e5 | 0.83 (0.0) | 0.87 | 3.10 (0.7) | 0.84 (0.0) | 0.12 | 361.06 (8.7) |
| gtr | gran. | 0.79 (0.0) | 0.98 | 2.41 (0.6) | 0.78 (0.0) | 0.51 | 35.27 (1.9) |
| gte | 0.85 (0.0) | 0.96 | 1.29 (0.2) | 0.84 (0.0) | 0.12 | 279.56 (6.9) |
| stel. | 0.77 (0.0) | 0.96 | 1.10 (0.0) | 0.72 (0.0) | 0.27 | 127.92 (4.4) |
| e5 | 0.80 (0.0) | 0.53 | 13.38 (1.2) | 0.82 (0.0) | 0.01 | 1413.80 (18.3) |
| gte | gran. | 0.73 (0.0) | 0.94 | 1.33 (0.1) | 0.73 (0.0) | 0.09 | 342.15 (7.8) |
| gtr | 0.71 (0.0) | 0.95 | 1.29 (0.1) | 0.69 (0.0) | 0.12 | 256.63 (6.4) |
| stel. | 0.86 (0.0) | 1.00 | 1.00 (0.0) | 0.85 (0.0) | 1.00 | 1.00 (0.0) |
| e5 | 0.83 (0.0) | 0.91 | 1.57 (0.2) | 0.86 (0.0) | 0.54 | 17.71 (0.9) |
| stel. | gran. | 0.79 (0.0) | 0.99 | 1.09 (0.1) | 0.77 (0.0) | 0.14 | 221.95 (5.9) |
| gtr | 0.77 (0.0) | 1.00 | 1.00 (0.0) | 0.75 (0.0) | 0.56 | 17.70 (1.0) |
| gte | 0.90 (0.0) | 1.00 | 1.00 (0.0) | 0.91 (0.0) | 1.00 | 1.00 (0.0) |
| e5 | 0.85 (0.0) | 0.98 | 1.05 (0.0) | 0.85 (0.0) | 0.51 | 26.33 (1.2) |
| e5 | gran. | 0.79 (0.0) | 0.98 | 1.08 (0.0) | 0.78 (0.0) | 0.21 | 151.09 (4.6) |
| gtr | 0.67 (0.0) | 0.80 | 3.10 (0.6) | 0.66 (0.0) | 0.01 | 1029.64 (14.9) |
| gte | 0.87 (0.0) | 0.99 | 1.02 (0.0) | 0.87 (0.0) | 0.60 | 32.59 (2.6) |
| stel. | 0.75 (0.0) | 0.98 | 1.06 (0.0) | 0.75 (0.0) | 0.46 | 32.12 (1.4) |

Table 3: Out-of-distribution translations: vec2vecs trained on NQ and evaluated on the entire TweetTopic test set (800 tweets) and an 8192-record subset of MIMIC. The rank metric varies from 1 to 800 (for TweetTopic) and 8192 (for MIMIC), thus 400 and, respectively, 4096 correspond to a random ordering. Standard errors are shown in parentheses.

[Table3](https://arxiv.org/html/2505.12540v4#S5.T3 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings") shows that this performance extends to out-of-distribution data. Our vec2vec translators were trained on NQ (drawn from Wikipedia), yet exhibit high cosine similarity, high accuracy, and low rank when evaluated on tweets (which are far more colloquial and use emojis) and medical records (which contain domain-specific jargon unlikely to appear in NQ). In [AppendixF](https://arxiv.org/html/2505.12540v4#A6 "Appendix F Full out-of-distribution translation results ‣ Harnessing the Universal Geometry of Embeddings"), we show that baseline methods fail on cross-backbone embedding pairs.

|  | vec2vec | OT Baseline |
| --- | --- | --- |
| M1M\_{1} | M2M\_{2} | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gra. | clip | 0.78 (0.0) | 0.35 | 226.62 (3.2) | 0.76 (0.0) | 0.00 | 4073.58 (9.4)‡ |
| gtr | 0.73 (0.0) | 0.13 | 711.23 (5.9) | 0.59 (0.0) | 0.00 | 4096.78 (9.2)‡ |
| gte | 0.62 (0.0) | 0.00 | 3233.41 (9.8) | 0.76 (0.0) | 0.00 | 4026.96 (9.4)‡ |
| ste. | 0.77 (0.0) | 0.31 | 286.69 (3.6) | 0.76 (0.0) | 0.00 | 3955.71 (8.9)‡ |
| e5 | 0.64 (0.0) | 0.01 | 2568.21 (9.4) | 0.77 (0.0) | 0.00 | 3771.52 (9.1)‡ |
| clip | gra. | 0.74 (0.0) | 0.72 | 4.46 (0.1) | 0.69 (0.0) | 0.00 | 4053.11 (9.4)‡ |
| gtr | 0.67 (0.0) | 0.27 | 155.11 (2.1) | 0.49 (0.0) | 0.00 | 4096.35 (9.2)‡ |
| gte | 0.75 (0.0) | 0.00 | 2678.90 (8.9) | 0.85 (0.0) | 0.00 | 4025.81 (9.3)‡ |
| ste. | 0.72 (0.0) | 0.61 | 22.50 (0.5) | 0.67 (0.0) | 0.00 | 3951.73 (8.9)‡ |
| e5 | 0.73 (0.0) | 0.01 | 1692.28 (8.2) | 0.83 (0.0) | 0.00 | 3771.38 (9.0)‡ |

Table 4: Translations between unimodal and multimodal (CLIP) embeddings: vec2vecs trained on NQ and evaluated on a 65536 text subset of NQ (chunked in batches of size 8192). Rank varies from 1 to 8192, thus 4096 corresponds to a random ordering. Since the embedding dimensionalities are different, only the Gromov-Wasserstein‡ OT baseline is run and the naive baseline does not apply. Bold denotes best value.

Finally, [Table4](https://arxiv.org/html/2505.12540v4#S5.T4 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings") shows that vec2vec can even translate to and from the space of CLIP, a multimodal embedding model which was trained in part on _image_ data. While the translations are not as strong as in [Table2](https://arxiv.org/html/2505.12540v4#S5.T2 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings"), vec2vec consistently outperforms the optimal transport baseline. These results show the promise of our method at adapting to new modalities: in particular, the embedding space of CLIP has been successfully connected to other modalities such as heatmaps, audio, and depth charts \[ [12](https://arxiv.org/html/2505.12540v4#bib.bibx12 "")\].

## 6 Using vec2vec translations to extract information

In this section, we show that vec2vec translations not only preserve the geometric structure of embeddings but also retain sufficient semantics to enable attribute inference.

|  | TweetTopic (k=1k=1) | MIMIC (k=10k=10) |
| --- | --- | --- |
| M1M\_{1} | M2M\_{2} | vec2vec | Naïve | M1M\_{1} | M2M\_{2} | vec2vec | Naïve | M1M\_{1} | M2M\_{2} |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gran. | gtr | 0.25 | 0.10 | 0.30 | 0.24 | 0.19 | 0.11 | 0.76 | 0.88 |
| gte | 0.32 | 0.09 | 0.30 | 0.34 | 0.36 | 0.13 | 0.76 | 1.00 |
| stel. | 0.24 | 0.10 | 0.30 | 0.28 | 0.27 | 0.04 | 0.76 | 0.96 |
| e5 | 0.31 | 0.18 | 0.30 | 0.31 | 0.19 | 0.20 | 0.76 | 0.97 |
| gtr | gran. | 0.34 | 0.08 | 0.24 | 0.30 | 0.16 | 0.12 | 0.88 | 0.76 |
| gte | 0.33 | 0.13 | 0.24 | 0.34 | 0.28 | 0.05 | 0.88 | 1.00 |
| stel. | 0.30 | 0.10 | 0.24 | 0.28 | 0.25 | 0.07 | 0.88 | 0.96 |
| e5 | 0.30 | 0.04 | 0.24 | 0.31 | 0.09 | 0.09 | 0.88 | 0.97 |
| gte | gran. | 0.37 | 0.04 | 0.34 | 0.30 | 0.18 | 0.11 | 1.00 | 0.76 |
| gtr | 0.24 | 0.13 | 0.34 | 0.24 | 0.10 | 0.03 | 1.00 | 0.88 |
| stel. | 0.31 | 0.20 | 0.34 | 0.28 | 0.68 | 0.83 | 1.00 | 0.96 |
| e5 | 0.37 | 0.30 | 0.34 | 0.31 | 0.37 | 0.63 | 1.00 | 0.97 |
| stel. | gran. | 0.35 | 0.07 | 0.28 | 0.30 | 0.23 | 0.09 | 0.96 | 0.76 |
| gtr | 0.26 | 0.13 | 0.28 | 0.24 | 0.22 | 0.09 | 0.96 | 0.88 |
| gte | 0.38 | 0.36 | 0.28 | 0.34 | 0.90 | 0.98 | 0.96 | 1.00 |
| e5 | 0.35 | 0.34 | 0.28 | 0.31 | 0.38 | 0.46 | 0.96 | 0.97 |
| e5 | gran. | 0.33 | 0.15 | 0.31 | 0.30 | 0.14 | 0.07 | 0.97 | 0.76 |
| gtr | 0.26 | 0.22 | 0.31 | 0.24 | 0.11 | 0.04 | 0.97 | 0.88 |
| gte | 0.34 | 0.28 | 0.31 | 0.34 | 0.47 | 0.66 | 0.97 | 1.00 |
| stel. | 0.26 | 0.16 | 0.31 | 0.28 | 0.36 | 0.40 | 0.97 | 0.96 |

Table 5: Information leakage via top-kk zero-shot attribute inference: vec2vecs trained on NQ and evaluated on the TweetTopic test set (800 tweets) and an 8192-record subset of MIMIC. M1M\_{1} and M2M\_{2} represent ideal zero-shot inference: attributes and embeddings are encoded using the same model.![Refer to caption](https://arxiv.org/html/2505.12540v4/enron_heatmap.png)Figure 5: Leakage of information via inversion. Trained on NQ and evaluated on a 50-email subset of the Enron Email Corpus. Cells denote judge accuracy.

Zero-shot attribute inference. [Table5](https://arxiv.org/html/2505.12540v4#S6.T5 "In 6 Using vec2vec translations to extract information ‣ Harnessing the Universal Geometry of Embeddings") shows that attribute inference on vec2vec translations consistently outperforms the naïve baseline and often does better than the ideal zero-shot baseline which performs inference on ground-truth document and attribute embeddings in the same space (this baseline is imaginary since these embeddings are not available in our setting).

vec2vec translations even work for embeddings of medical records, which are much further from the training distribution than tweets. The attributes in this case are MedCAT disease descriptions, very few of which occur in the training data. Attribute inference on translated embeddings is comparable to the naïve baseline in same-backbone pairings and outperforms it (often greatly) in cross-backbone pairings. The fact that vec2vec preserves the semantics of concepts like "alveolar periostitis" (which never appears in its training data) is evidence that its latent space is indeed a universal representation.

Zero-shot inversion.
Inversion, i.e., reconstruction of text inputs, is more ambitious than attribute inference. vec2vec translations retain enough semantic information that off-the-shelf, zero-shot inversion methods like \[ [67](https://arxiv.org/html/2505.12540v4#bib.bibx67 "")\], developed for embeddings computed by standard encoders, extract information for as many as 80% of emails and 67% of tweets given _only_ their translated embeddings, for some model pairs ( [Figure5](https://arxiv.org/html/2505.12540v4#S6.F5 "In 6 Using vec2vec translations to extract information ‣ Harnessing the Universal Geometry of Embeddings") and [AppendixG](https://arxiv.org/html/2505.12540v4#A7 "Appendix G Zero-shot inversion on TweetTopic ‣ Harnessing the Universal Geometry of Embeddings")). These inversions are imperfect and we leave development of specialized inverters for translated embeddings to future work. Nevertheless, as exemplified in [Figure6](https://arxiv.org/html/2505.12540v4#S6.F6 "In 6 Using vec2vec translations to extract information ‣ Harnessing the Universal Geometry of Embeddings"), they still extract potentially sensitive information such as individual and company names, dates, promotions, financial information, outages, and even lunch orders. In [AppendixH](https://arxiv.org/html/2505.12540v4#A8 "Appendix H Prompt for measuring information extraction ‣ Harnessing the Universal Geometry of Embeddings"), we show the prompt we use to measure extraction.

Ground Truth: “Subject: EnronBashing on Frontline `\n` Body:…"

Generation: “Some emails discussing NROn Employee/s Complaint To thePublic…"

Ground Truth: “Subject: Trades for 3/1/02`\n` Body: `\n`John, `\n` The following trades…"

Generation: “… future transactions may await John G…"

Ground Truth: “The following expense report is ready for approval…"

Generation: “The upcoming expense statement from YYYY MM Dec…"Figure 6: Examples of Enron Email Corpus inversions that infer entities and content.

## 7 Ablations

| Method | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- |
| vec2vec | 0.75 (0.0) | 0.91 | 2.64 (0.1) |
| Naïve Baseline | 0.04 (0.0) | 0.00 | 4084.15 (9.2) |
| OT Baseline | 0.70 (0.0) | 0.00 | 3064.16 (8.9) |
| – VSP loss | 0.58 (0.0) | 0.00 | 4196.64 (9.2) |
| – CC loss | 0.50 (0.0) | 0.00 | 3941.36 (9.3) |
| – latent GAN | 0.49 (0.0) | 0.00 | 3897.09 (9.5) |
| – VSP and CC loss | 0.47 (0.0) | 0.00 | 3365.24 (9.3) |
| – hyperparam. tuning | 0.50 (0.0) | 0.00 | 4011.73 (9.3) |

Table 6: gte →\\to gtr translators trained without individual components of our method on NQ and evaluated on a 65536-text subset of NQ (chunked in batches of 8192). The rank metric varies from 1 to 8192, thus 4096 corresponds to a random ordering. Standard errors are shown in parentheses.

Each component of our method is important. We ablate our method subtractively, measuring the key metrics after removing individual components of our algorithm (described in [Section3](https://arxiv.org/html/2505.12540v4#S3 "3 Our method: vec2vec ‣ Harnessing the Universal Geometry of Embeddings")). [Table6](https://arxiv.org/html/2505.12540v4#S7.T6 "In 7 Ablations ‣ Harnessing the Universal Geometry of Embeddings") shows that each component appears to be critical to building good translations. While vec2vec’s cos⁡(⋅)\\cos(\\cdot) is higher than the naïve baseline, it performs worse across the board than the OT baseline and does not preserve the geometry of the vector space.

| NN | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- |
| 1000000 | 0.75 (0.0) | 0.92 | 2.73 (0.2) |
| --- | --- | --- | --- |
| 10000 | 0.57 (0.0) | 0.01 | 1462.21 (20.) |
| 50000 | 0.74 (0.0) | 0.81 | 3.91 (0.6) |
| 100000 | 0.74 (0.0) | 0.85 | 4.52 (0.4) |
| 500000 | 0.75 (0.0) | 0.92 | 2.73 (0.2) |

Table 7: gte →\\to gtr translators trained with different amounts of GTE data: vec2vec models trained on NQ and evaluated an 8192-record subset of NQ. The rank metric varies from 1 to 8192, thus 4096 corresponds to a random ordering. Standard errors are shown in parentheses.

vec2vecs can be trained with significantly less data. In [Sections5](https://arxiv.org/html/2505.12540v4#S5 "5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings") and [6](https://arxiv.org/html/2505.12540v4#S6 "6 Using vec2vec translations to extract information ‣ Harnessing the Universal Geometry of Embeddings"), we use 1M-point subsets of NQ to train our vec2vec models. Now, we train the gte →\\to gtr vec2vec with 1M GTR embeddings but fewer GTE embeddings. [Table7](https://arxiv.org/html/2505.12540v4#S7.T7 "In 7 Ablations ‣ Harnessing the Universal Geometry of Embeddings") shows that with as few as 10K embeddings, the translators still learn something (i.e. are better than random). Translations trained on 50K embeddings are almost as good as those trained on 1M. Translations generally improve with more training data.

## 8 Related work

Representation alignment.
Similarities between representations of
different neural networks are investigated in \[ [26](https://arxiv.org/html/2505.12540v4#bib.bibx26 ""), [31](https://arxiv.org/html/2505.12540v4#bib.bibx31 ""), [59](https://arxiv.org/html/2505.12540v4#bib.bibx59 ""), [5](https://arxiv.org/html/2505.12540v4#bib.bibx5 ""), [18](https://arxiv.org/html/2505.12540v4#bib.bibx18 ""), [61](https://arxiv.org/html/2505.12540v4#bib.bibx61 ""), [30](https://arxiv.org/html/2505.12540v4#bib.bibx30 "")\]. Methods based on CCA \[ [42](https://arxiv.org/html/2505.12540v4#bib.bibx42 "")\], SVCCA, \[ [51](https://arxiv.org/html/2505.12540v4#bib.bibx51 "")\], CKA \[ [23](https://arxiv.org/html/2505.12540v4#bib.bibx23 ""), [38](https://arxiv.org/html/2505.12540v4#bib.bibx38 "")\], ICA \[ [63](https://arxiv.org/html/2505.12540v4#bib.bibx63 "")\], time-series \[ [39](https://arxiv.org/html/2505.12540v4#bib.bibx39 "")\], and GUIs \[ [16](https://arxiv.org/html/2505.12540v4#bib.bibx16 "")\] have been used to compare embeddings from different subspaces.
\[ [37](https://arxiv.org/html/2505.12540v4#bib.bibx37 ""), [45](https://arxiv.org/html/2505.12540v4#bib.bibx45 ""), [40](https://arxiv.org/html/2505.12540v4#bib.bibx40 ""), [57](https://arxiv.org/html/2505.12540v4#bib.bibx57 ""), [48](https://arxiv.org/html/2505.12540v4#bib.bibx48 "")\] harness representation similarity for zero-shot stitching, substitution, domain transfer, and multimodal adaptation. All rely on some amount of paired data, which is difficult
to reduce \[ [6](https://arxiv.org/html/2505.12540v4#bib.bibx6 "")\]. Our method does not just measure similarity, we learn how to _translate_ representations across spaces without any paired data.

Optimal transport. The problem of unsupervised optimal transport has been studied for image style transfer \[ [17](https://arxiv.org/html/2505.12540v4#bib.bibx17 ""), [36](https://arxiv.org/html/2505.12540v4#bib.bibx36 ""), [70](https://arxiv.org/html/2505.12540v4#bib.bibx70 "")\], word translation \[ [62](https://arxiv.org/html/2505.12540v4#bib.bibx62 ""), [10](https://arxiv.org/html/2505.12540v4#bib.bibx10 ""), [15](https://arxiv.org/html/2505.12540v4#bib.bibx15 ""), [9](https://arxiv.org/html/2505.12540v4#bib.bibx9 ""), [20](https://arxiv.org/html/2505.12540v4#bib.bibx20 "")\], and natural language sequence translation \[ [52](https://arxiv.org/html/2505.12540v4#bib.bibx52 ""), [27](https://arxiv.org/html/2505.12540v4#bib.bibx27 ""), [1](https://arxiv.org/html/2505.12540v4#bib.bibx1 ""), [4](https://arxiv.org/html/2505.12540v4#bib.bibx4 ""), [64](https://arxiv.org/html/2505.12540v4#bib.bibx64 ""), [3](https://arxiv.org/html/2505.12540v4#bib.bibx3 "")\].
Our method builds on these works, which often employ a combination of cycle-consistency and adversarial loss. Importantly, unlike prior word and sequence translation methods, multiple representations of the same input (e.g., heavily overlapping word vocabularies) are unavailable in our setting. \[ [54](https://arxiv.org/html/2505.12540v4#bib.bibx54 "")\] proposes a solver for matching small sets of embeddings between different vision-language models.
Our method goes well beyond matching by taking unknown embeddings and _generating_ matching embeddings in the space of another model.

Embedding inversion. An emerging line of research investigates decoding text from language model embeddings \[ [55](https://arxiv.org/html/2505.12540v4#bib.bibx55 ""), [29](https://arxiv.org/html/2505.12540v4#bib.bibx29 ""), [43](https://arxiv.org/html/2505.12540v4#bib.bibx43 "")\] and outputs \[ [44](https://arxiv.org/html/2505.12540v4#bib.bibx44 ""), [7](https://arxiv.org/html/2505.12540v4#bib.bibx7 ""), [66](https://arxiv.org/html/2505.12540v4#bib.bibx66 "")\].
vec2vec helps apply these to unknown embeddings, without an encoder or paired data, by translating them to the space of a known model.

Bridging modality gaps. Previous work has noted an inherent “gap” between image- and text-based models \[ [33](https://arxiv.org/html/2505.12540v4#bib.bibx33 "")\] and proposed various ways to unify the modalities \[ [56](https://arxiv.org/html/2505.12540v4#bib.bibx56 "")\]. Some approaches feed image embeddings directly into language models \[ [22](https://arxiv.org/html/2505.12540v4#bib.bibx22 ""), [60](https://arxiv.org/html/2505.12540v4#bib.bibx60 ""), [11](https://arxiv.org/html/2505.12540v4#bib.bibx11 ""), [35](https://arxiv.org/html/2505.12540v4#bib.bibx35 "")\], while others generate captions from image embeddings \[ [41](https://arxiv.org/html/2505.12540v4#bib.bibx41 "")\] or even from text embeddings themselves \[ [43](https://arxiv.org/html/2505.12540v4#bib.bibx43 "")\]. \[ [12](https://arxiv.org/html/2505.12540v4#bib.bibx12 "")\] introduces a shared embedding space that integrates inputs from multiple modalities, including text, audio, and vision. In contrast, our post-hoc approach directly translates between representations and complements these systems by enabling inputs from a wide variety of embedding models.

## 9 Discussion and Future Work

The Platonic Representation Hypothesis conjectures that the representation spaces of modern neural networks are converging. We assert the Strong Platonic Representation Hypothesis: the latent universal representation can be learned and harnessed to translate between representation spaces without any encoders or paired data.

In [Section5](https://arxiv.org/html/2505.12540v4#S5 "5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings"), we demonstrated
that our vec2vec method successfully translates embeddings generated from unseen documents by unseen encoders, and the translator is robust to (sometimes very) out-of-distribution inputs. This suggests that vec2vec learns domain-agnostic translations based on the universal geometric relationships which encode the same semantics in multiple embedding spaces.

In [Section6](https://arxiv.org/html/2505.12540v4#S6 "6 Using vec2vec translations to extract information ‣ Harnessing the Universal Geometry of Embeddings"), we showed that vec2vec translations preserve sufficient input semantics to enable attribute inference.
We extracted sensitive disease information from patient records and partial content from corporate emails, with access only to document embeddings and no access to the encoder that produced them. Better translation methods will enable higher-fidelity extraction, confirming once again that embeddings reveal (almost) as much as their inputs.

Our findings provide compelling evidence for the Strong Platonic Representation Hypothesis for text-based models. Our preliminary results on CLIP suggest that the universal geometry can be harnessed in other modalities, too. The results in this paper are but a _lower bound_ on inter-representation translation. Better and more stable learning algorithms, architectures, and other methodological improvements will support scaling to more data, more model families, and more modalities.

## Acknowledgments and Disclosure of Funding

This research is supported in part by the Google Cyber NYC Institutional Research Program. RJ is supported by the Digital Life Initiative Fellowship and JM by the National Science Foundation.

## References

- \[1\]David Alvarez-Melis and Tommi. Jaakkola
“Gromov-Wasserstein Alignment of Word Embedding Spaces”, 2018
arXiv: [https://arxiv.org/abs/1809.00013](https://arxiv.org/abs/1809.00013 "")
- \[2\]Dimosthenis Antypas, Asahi Ushio, Francesco Barbieri and Jose Camacho-Collados
“Multilingual Topic Classification in X: Dataset and Analysis”
In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_Miami, Florida, USA: Association for Computational Linguistics, 2024, pp. 20136–20152
DOI: [10.18653/v1/2024.emnlp-main.1123](https://dx.doi.org/10.18653/v1/2024.emnlp-main.1123 "")
- \[3\]Mikel Artetxe, Gorka Labaka and Eneko Agirre
“A robust self-learning method for fully unsupervised cross-lingual mappings of word embeddings”
In _Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_Melbourne, Australia: Association for Computational Linguistics, 2018, pp. 789–798
DOI: [10.18653/v1/P18-1073](https://dx.doi.org/10.18653/v1/P18-1073 "")
- \[4\]Mikel Artetxe, Gorka Labaka, Eneko Agirre and Kyunghyun Cho
“Unsupervised Neural Machine Translation”, 2018
arXiv: [https://arxiv.org/abs/1710.11041](https://arxiv.org/abs/1710.11041 "")
- \[5\]Yamini Bansal, Preetum Nakkiran and Boaz Barak
“Revisiting Model Stitching to Compare Neural Representations”, 2021
arXiv: [https://arxiv.org/abs/2106.07682](https://arxiv.org/abs/2106.07682 "")
- \[6\]Irene Cannistraci, Luca Moschella, Valentino Maiorca, Marco Fumero, Antonio Norelli and Emanuele Rodolà
“Bootstrapping Parallel Anchors for Relative Representations”, 2023
arXiv: [https://arxiv.org/abs/2303.00721](https://arxiv.org/abs/2303.00721 "")
- \[7\]Nicholas Carlini, Daniel Paleka, Krishnamurthy Dvijotham, Thomas Steinke, Jonathan Hayase, A. Cooper, Katherine Lee, Matthew Jagielski, Milad Nasr, Arthur Conmy, Itay Yona, Eric Wallace, David Rolnick and Florian Tramèr
“Stealing Part of a Production Language Model”, 2024
arXiv: [https://arxiv.org/abs/2403.06634](https://arxiv.org/abs/2403.06634 "")
- \[8\]Liqun Chen, Zhe Gan, Yu Cheng, Linjie Li, Lawrence Carin and Jingjing Liu
“Graph Optimal Transport for Cross-Domain Alignment”, 2020
arXiv: [https://arxiv.org/abs/2006.14744](https://arxiv.org/abs/2006.14744 "")
- \[9\]Xilun Chen and Claire Cardie
“Unsupervised Multilingual Word Embeddings”, 2018
arXiv: [https://arxiv.org/abs/1808.08933](https://arxiv.org/abs/1808.08933 "")
- \[10\]Alexis Conneau, Guillaume Lample, Marc’Aurelio Ranzato, Ludovic Denoyer and Hervé Jégou
“Word Translation Without Parallel Data”, 2018
arXiv: [https://arxiv.org/abs/1710.04087](https://arxiv.org/abs/1710.04087 "")
- \[11\]Runpei Dong, Chunrui Han, Yuang Peng, Zekun Qi, Zheng Ge, Jinrong Yang, Liang Zhao, Jianjian Sun, Hongyu Zhou, Haoran Wei, Xiangwen Kong, Xiangyu Zhang, Kaisheng Ma and Li Yi
“DreamLLM: Synergistic Multimodal Comprehension and Creation”, 2024
arXiv: [https://arxiv.org/abs/2309.11499](https://arxiv.org/abs/2309.11499 "")
- \[12\]Rohit Girdhar, Alaaeldin El-Nouby, Zhuang Liu, Mannat Singh, Kalyan Alwala, Armand Joulin and Ishan Misra
“ImageBind: One Embedding Space To Bind Them All”, 2023
arXiv: [https://arxiv.org/abs/2305.05665](https://arxiv.org/abs/2305.05665 "")
- \[13\]Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville and Yoshua Bengio
“Generative adversarial networks”
In _Commun. ACM_ 63.11New York, NY, USA: Association for Computing Machinery, 2020, pp. 139–144
DOI: [10.1145/3422622](https://dx.doi.org/10.1145/3422622 "")
- \[14\]IBM Granite
“Granite Embedding Models”, 2024
URL: [https://github.com/ibm-granite/granite-embedding-models/](https://github.com/ibm-granite/granite-embedding-models/ "")
- \[15\]Edouard Grave, Armand Joulin and Quentin Berthet
“Unsupervised Alignment of Embeddings with Wasserstein Procrustes”, 2018
arXiv: [https://arxiv.org/abs/1805.11222](https://arxiv.org/abs/1805.11222 "")
- \[16\]Florian Heimerl, Christoph Kralj, Torsten Moller and Michael Gleicher
“embComp: Visual Interactive Comparison of Vector Embeddings”
In _IEEE Transactions on Visualization and Computer Graphics_ 28.8Institute of ElectricalElectronics Engineers (IEEE), 2022, pp. 2953–2969
DOI: [10.1109/tvcg.2020.3045918](https://dx.doi.org/10.1109/tvcg.2020.3045918 "")
- \[17\]Xun Huang, Ming-Yu Liu, Serge Belongie and Jan Kautz
“Multimodal Unsupervised Image-to-Image Translation”, 2018
arXiv: [https://arxiv.org/abs/1804.04732](https://arxiv.org/abs/1804.04732 "")
- \[18\]Minyoung Huh, Brian Cheung, Tongzhou Wang and Phillip Isola
“The Platonic Representation Hypothesis”, 2024
arXiv: [https://arxiv.org/abs/2405.07987](https://arxiv.org/abs/2405.07987 "")
- \[19\]Alistair Johnson, Tom Pollard, Lu Shen, Li-wei Lehman, Mengling Feng, Mohammad Ghassemi, Benjamin Moody, Peter Szolovits, Leo Anthony and Roger Mark
“MIMIC-III, a freely accessible critical care database”
In _Scientific data_ 3.1Nature Publishing Group, 2016, pp. 1–9

- \[20\]Armand Joulin, Piotr Bojanowski, Tomas Mikolov, Hervé Jégou and Edouard Grave
“Loss in Translation: Learning Bilingual Word Mapping with a Retrieval Criterion”
In _Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing_Brussels, Belgium: Association for Computational Linguistics, 2018, pp. 2979–2984
DOI: [10.18653/v1/D18-1330](https://dx.doi.org/10.18653/v1/D18-1330 "")
- \[21\]Bryan Klimt and Yiming Yang
“The enron corpus: a new dataset for email classification research”
In _Proceedings of the 15th European Conference on Machine Learning_, ECML’04
Pisa, Italy: Springer-Verlag, 2004, pp. 217–226
DOI: [10.1007/978-3-540-30115-8\_22](https://dx.doi.org/10.1007/978-3-540-30115-8_22 "")
- \[22\]Jing Koh, Ruslan Salakhutdinov and Daniel Fried
“Grounding language models to images for multimodal inputs and outputs”
In _International Conference on Machine Learning_, 2023, pp. 17283–17300
PMLR

- \[23\]Simon Kornblith, Mohammad Norouzi, Honglak Lee and Geoffrey Hinton
“Similarity of Neural Network Representations Revisited”, 2019
arXiv: [https://arxiv.org/abs/1905.00414](https://arxiv.org/abs/1905.00414 "")
- \[24\]Zeljko Kraljevic, Thomas Searle, Anthony Shek, Lukasz Roguski, Kawsar Noor, Daniel Bean, Aurelie Mascio, Leilei Zhu, Amos Folarin and Angus Roberts
“Multi-domain clinical natural language processing with MedCAT: the medical concept annotation toolkit”
In _Artificial intelligence in medicine_ 117Elsevier, 2021, pp. 102083

- \[25\]Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei Chang, Andrew. Dai, Jakob Uszkoreit, Quoc Le and Slav Petrov
“Natural Questions: A Benchmark for Question Answering Research”
In _Transactions of the Association for Computational Linguistics_ 7Cambridge, MA: MIT Press, 2019, pp. 452–466
DOI: [10.1162/tacl\_a\_00276](https://dx.doi.org/10.1162/tacl_a_00276 "")
- \[26\]Aarre Laakso and Garrison Cottrell
“Content and cluster analysis: Assessing representational similarity in neural systems”
In _Philosophical Psychology_ 13.1, 2000, pp. 47–76
DOI: [10.1080/09515080050002726](https://dx.doi.org/10.1080/09515080050002726 "")
- \[27\]Guillaume Lample, Alexis Conneau, Ludovic Denoyer and Marc’Aurelio Ranzato
“Unsupervised Machine Translation Using Monolingual Corpora Only”, 2018
arXiv: [https://arxiv.org/abs/1711.00043](https://arxiv.org/abs/1711.00043 "")
- \[28\]Eric Lehman, Sarthak Jain, Karl Pichotta, Yoav Goldberg and Byron Wallace
“Does BERT Pretrained on Clinical Notes Reveal Sensitive Data?”
In _Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_Online: Association for Computational Linguistics, 2021, pp. 946–959
DOI: [10.18653/v1/2021.naacl-main.73](https://dx.doi.org/10.18653/v1/2021.naacl-main.73 "")
- \[29\]Haoran Li, Mingshi Xu and Yangqiu Song
“Sentence Embedding Leaks More Information than You Expect: Generative Embedding Inversion Attack to Recover the Whole Sentence”, 2023
arXiv: [https://arxiv.org/abs/2305.03010](https://arxiv.org/abs/2305.03010 "")
- \[30\]Jiaang Li, Yova Kementchedjhieva, Constanza Fierro and Anders Søgaard
“Do Vision and Language Models Share Concepts? A Vector Space Alignment Study”
In _Transactions of the Association for Computational Linguistics_ 12Cambridge, MA: MIT Press, 2024, pp. 1232–1249
DOI: [10.1162/tacl\_a\_00698](https://dx.doi.org/10.1162/tacl_a_00698 "")
- \[31\]Yixuan Li, Jason Yosinski, Jeff Clune, Hod Lipson and John Hopcroft
“Convergent Learning: Do different neural networks learn the same representations?”, 2016
arXiv: [https://arxiv.org/abs/1511.07543](https://arxiv.org/abs/1511.07543 "")
- \[32\]Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie and Meishan Zhang
“Towards General Text Embeddings with Multi-stage Contrastive Learning”, 2023
arXiv: [https://arxiv.org/abs/2308.03281](https://arxiv.org/abs/2308.03281 "")
- \[33\]Weixin Liang, Yuhui Zhang, Yongchan Kwon, Serena Yeung and James Zou
“Mind the Gap: Understanding the Modality Gap in Multi-modal Contrastive Representation Learning”, 2022
arXiv: [https://arxiv.org/abs/2203.02053](https://arxiv.org/abs/2203.02053 "")
- \[34\]Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár and C Zitnick
“Microsoft coco: Common objects in context”
In _European conference on computer vision_, 2014, pp. 740–755
Springer

- \[35\]Haotian Liu, Chunyuan Li, Qingyang Wu and Yong Lee
“Visual Instruction Tuning”, 2023
arXiv: [https://arxiv.org/abs/2304.08485](https://arxiv.org/abs/2304.08485 "")
- \[36\]Ming-Yu Liu, Thomas Breuel and Jan Kautz
“Unsupervised Image-to-Image Translation Networks”, 2018
arXiv: [https://arxiv.org/abs/1703.00848](https://arxiv.org/abs/1703.00848 "")
- \[37\]Valentino Maiorca, Luca Moschella, Antonio Norelli, Marco Fumero, Francesco Locatello and Emanuele Rodolà
“Latent Space Translation via Semantic Alignment”, 2024
arXiv: [https://arxiv.org/abs/2311.00664](https://arxiv.org/abs/2311.00664 "")
- \[38\]Mayug Maniparambil, Raiymbek Akshulakov, Yasser Djilali, Mohamed El, Sanath Narayan, Karttikeya Mangalam and Noel O’Connor
“Do Vision and Language Encoders Represent the World Similarly?”
In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_, 2024, pp. 14334–14343

- \[39\]Deven Mistry and Ali Minai
“A Comparative Study of Sentence Embedding Models for Assessing Semantic Variation”
In _International Conference on Artificial Neural Networks_, 2023, pp. 1–12

- \[40\]Mazda Moayeri, Keivan Rezaei, Maziar Sanjabi and Soheil Feizi
“Text-To-Concept (and Back) via Cross-Model Alignment”, 2023
arXiv: [https://arxiv.org/abs/2305.06386](https://arxiv.org/abs/2305.06386 "")
- \[41\]Ron Mokady, Amir Hertz and Amit. Bermano
“ClipCap: CLIP Prefix for Image Captioning”, 2021
arXiv: [https://arxiv.org/abs/2111.09734](https://arxiv.org/abs/2111.09734 "")
- \[42\]Ari. Morcos, Maithra Raghu and Samy Bengio
“Insights on representational similarity in neural networks with canonical correlation”, 2018
arXiv: [https://arxiv.org/abs/1806.05759](https://arxiv.org/abs/1806.05759 "")
- \[43\]John. Morris, Volodymyr Kuleshov, Vitaly Shmatikov and Alexander. Rush
“Text Embeddings Reveal (Almost) As Much As Text”, 2023
arXiv: [https://arxiv.org/abs/2310.06816](https://arxiv.org/abs/2310.06816 "")
- \[44\]John. Morris, Wenting Zhao, Justin. Chiu, Vitaly Shmatikov and Alexander. Rush
“Language Model Inversion”, 2023
arXiv: [https://arxiv.org/abs/2311.13647](https://arxiv.org/abs/2311.13647 "")
- \[45\]Luca Moschella, Valentino Maiorca, Marco Fumero, Antonio Norelli, Francesco Locatello and Emanuele Rodolà
“Relative representations enable zero-shot latent space communication”, 2023
arXiv: [https://arxiv.org/abs/2209.15430](https://arxiv.org/abs/2209.15430 "")
- \[46\]Nikola Mrksic, DiarmuidÓ Séaghdha, Blaise Thomson, Milica Gasic, Lina Rojas-Barahona, Pei-Hao Su, David Vandyke, Tsung-Hsien Wen and Steve Young
“Counter-fitting Word Vectors to Linguistic Constraints”, 2016
arXiv: [https://arxiv.org/abs/1603.00892](https://arxiv.org/abs/1603.00892 "")
- \[47\]Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavoández Ábrego, Ji Ma, Vincent. Zhao, Yi Luan, Keith. Hall, Ming-Wei Chang and Yinfei Yang
“Large Dual Encoders Are Generalizable Retrievers”, 2021
arXiv: [https://arxiv.org/abs/2112.07899](https://arxiv.org/abs/2112.07899 "")
- \[48\]Antonio Norelli, Marco Fumero, Valentino Maiorca, Luca Moschella, Emanuele Rodolà and Francesco Locatello
“ASIF: Coupled Data Turns Unimodal Models to Multimodal Without Training”, 2023
arXiv: [https://arxiv.org/abs/2210.01738](https://arxiv.org/abs/2210.01738 "")
- \[49\]Gabriel Peyré, Marco Cuturi and Justin Solomon
“Gromov-Wasserstein Averaging of Kernel and Distance Matrices”
In _Proceedings of the 33rd International Conference on Machine Learning (ICML)_ 48, JMLR: Workshop and Conference Proceedings
New York, NY, USA: JMLR, 2016

- \[50\]Alec Radford, Jong Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger and Ilya Sutskever
“Learning Transferable Visual Models From Natural Language Supervision”, 2021
arXiv: [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020 "")
- \[51\]Maithra Raghu, Justin Gilmer, Jason Yosinski and Jascha Sohl-Dickstein
“SVCCA: Singular Vector Canonical Correlation Analysis for Deep Learning Dynamics and Interpretability”, 2017
arXiv: [https://arxiv.org/abs/1706.05806](https://arxiv.org/abs/1706.05806 "")
- \[52\]Sujith Ravi and Kevin Knight
“Deciphering Foreign Language”
In _Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies_Portland, Oregon, USA: Association for Computational Linguistics, 2011, pp. 12–21
URL: [https://aclanthology.org/P11-1002/](https://aclanthology.org/P11-1002/ "")
- \[53\]Divya Saxena and Jiannong Cao
“Generative Adversarial Networks (GANs): Challenges, Solutions, and Future Directions”
In _ACM Comput. Surv._ 54.3New York, NY, USA: Association for Computing Machinery, 2021
DOI: [10.1145/3446374](https://dx.doi.org/10.1145/3446374 "")
- \[54\]Dominik Schnaus, Nikita Araslanov and Daniel Cremers
“It’s a (Blind) Match! Towards Vision-Language Correspondence without Parallel Data”, 2025
arXiv: [https://arxiv.org/abs/2503.24129](https://arxiv.org/abs/2503.24129 "")
- \[55\]Congzheng Song and Ananth Raghunathan
“Information Leakage in Embedding Models”, 2020
arXiv: [https://arxiv.org/abs/2004.00053](https://arxiv.org/abs/2004.00053 "")
- \[56\]Shezheng Song, Xiaopeng Li, Shasha Li, Shan Zhao, Jie Yu, Jun Ma, Xiaoguang Mao and Weimin Zhang
“How to Bridge the Gap between Modalities: A Comprehensive Survey on Multimodal Large Language Model”, 2023
arXiv: [https://arxiv.org/abs/2311.07594](https://arxiv.org/abs/2311.07594 "")
- \[57\]Yingtao Tian and Jesse Engel
“Latent translation: Crossing modalities by bridging generative models”
In _arXiv preprint arXiv:1902.08261_, 2019

- \[58\]Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder and Furu Wei
“Text Embeddings by Weakly-Supervised Contrastive Pre-training”, 2024
arXiv: [https://arxiv.org/abs/2212.03533](https://arxiv.org/abs/2212.03533 "")
- \[59\]Liwei Wang, Lunjia Hu, Jiayuan Gu, Yue Wu, Zhiqiang Hu, Kun He and John Hopcroft
“Towards Understanding Learning Representations: To What Extent Do Different Neural Networks Learn the Same Representation”, 2018
arXiv: [https://arxiv.org/abs/1810.11750](https://arxiv.org/abs/1810.11750 "")
- \[60\]Wenhai Wang, Zhe Chen, Xiaokang Chen, Jiannan Wu, Xizhou Zhu, Gang Zeng, Ping Luo, Tong Lu, Jie Zhou, Yu Qiao and Jifeng Dai
“VisionLLM: Large Language Model is also an Open-Ended Decoder for Vision-Centric Tasks”, 2023
arXiv: [https://arxiv.org/abs/2305.11175](https://arxiv.org/abs/2305.11175 "")
- \[61\]Christopher Wolfram and Aaron Schein
“Layers at similar depths generate similar activations across llm architectures”
In _arXiv preprint arXiv:2504.08775_, 2025

- \[62\]Chao Xing, Dong Wang, Chao Liu and Yiye Lin
“Normalized Word Embedding and Orthogonal Transform for Bilingual Word Translation”
In _Proceedings of the 2015 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_Denver, Colorado: Association for Computational Linguistics, 2015, pp. 1006–1011
DOI: [10.3115/v1/N15-1104](https://dx.doi.org/10.3115/v1/N15-1104 "")
- \[63\]Hiroaki Yamagiwa, Momose Oyama and Hidetoshi Shimodaira
“Discovering Universal Geometry in Embeddings with ICA”, 2023
arXiv: [https://arxiv.org/abs/2305.13175](https://arxiv.org/abs/2305.13175 "")
- \[64\]Zhen Yang, Wei Chen, Feng Wang and Bo Xu
“Unsupervised Neural Machine Translation with Weight Sharing”, 2018
arXiv: [https://arxiv.org/abs/1804.09057](https://arxiv.org/abs/1804.09057 "")
- \[65\]Jinsung Yoon and Sercan Arik
“Embedding-Converter: A Unified Framework for Cross-Model Embedding Transformation”, 2025
URL: [https://openreview.net/forum?id=ga9PAnFsAt](https://openreview.net/forum?id=ga9PAnFsAt "")
- \[66\]Collin Zhang, John. Morris and Vitaly Shmatikov
“Extracting Prompts by Inverting LLM Outputs”, 2024
arXiv: [https://arxiv.org/abs/2405.15012](https://arxiv.org/abs/2405.15012 "")
- \[67\]Collin Zhang, John. Morris and Vitaly Shmatikov
“Universal Zero-shot Embedding Inversion”, 2025
arXiv: [https://arxiv.org/abs/2504.00147](https://arxiv.org/abs/2504.00147 "")
- \[68\]Dun Zhang, Jiacheng Li, Ziyang Zeng and Fulong Wang
“Jasper and Stella: distillation of SOTA embedding models”, 2025
arXiv: [https://arxiv.org/abs/2412.19048](https://arxiv.org/abs/2412.19048 "")
- \[69\]Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang, Dayiheng Liu, Junyang Lin, Fei Huang and Jingren Zhou
“Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models”
In _arXiv preprint arXiv:2506.05176_, 2025

- \[70\]Jun-Yan Zhu, Taesung Park, Phillip Isola and Alexei. Efros
“Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks”, 2020
arXiv: [https://arxiv.org/abs/1703.10593](https://arxiv.org/abs/1703.10593 "")

## Appendix A Compute

Our training and evaluation were conducted using diverse compute environments, including both local and cloud GPU clusters. Experiments were done on NVIDIA 2080Ti, L4, A40, and A100 GPUs, listed in order of increasing computational capacity.

For our final results, we trained 25 vec2vec models fully and 30 models partially (see [AppendixE](https://arxiv.org/html/2505.12540v4#A5 "Appendix E Initialization robustness by model backbone ‣ Harnessing the Universal Geometry of Embeddings")). The full models’ training durations usually ranged from 1 to 7 days, depending on the specific GPU and model pair (which affected convergence rates). Partial convergence was stopped after 2 days. Due to the size of Qwen, our (qwen, gte) ablation was trained for 20 days on an A100. Taking a conservative estimate of the average training time, this amounted to approximately 176 GPU days (24 models ×\\times 4 days / model + 30 models ×\\times 2 days / model + 1 (qwen, gte) ×\\times 20 days / model).

Evaluation procedures varied by model type:

- •


The 10 main vec2vec models required ∼\\sim1 hour each for NQ, TweetTopic, and MIMIC evaluation (across GPU types), plus 30 minutes for attribute extraction on TweetTopic and MIMIC, and 1.5 hours for inversion and downstream LLM evaluation on Enron and TweetTopic. Naive baselines required ∼\\sim30 minutes each across all datasets.

- •


The 15 additional fully-trained models required 30 minutes each for NQ evaluation, with an extra 30 minutes for MS COCO evaluation of (clip, granite).

- •


Optimal transport baselines ran on CPU only, requiring ∼\\sim1 hour per dataset (three datasets for main models, one for others).


In total, our experiments consumed almost 176 GPU days for training and an additional 42 GPU hours for evaluation and analysis. An additional 45 CPU hours were required for optimal transport.

## Appendix B Oracle-aided optimal transport baseline

Let ui=M1​(di)u\_{i}=M\_{1}(d\_{i}) and vi=M2​(di)v\_{i}=M\_{2}(d\_{i}) denote embeddings of the same document did\_{i} from two different embedding models. In [Section5](https://arxiv.org/html/2505.12540v4#S5 "5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings"), we solve the optimal assignment problem:

|     |     |     |
| --- | --- | --- |
|  | π∗=arg⁡min⁡∑i=1nπ⁡cos⁡(ui,vπ⁡(i)),\\pi^{\*}=\\arg\\min\_{\\pi}\\sum\_{i=1}^{n}\\cos(u\_{i},v\_{\\pi(i)}), |  |

using four algorithms: Hungarian (linear sum assignment), Earth Mover’s Distance (EMD), Sinkhorn, Gromov-Wasserstein. For the Gromov-Wasserstein algorithm, we try both the entropic and non-entropic variants with multiple hyperparameter configurations and select the best figure. Note that the optimal transport (OT) baseline computes matchings and transports between embeddings derived from the same underlying texts, strongly favoring OT methods. Nevertheless, OT still struggles when embeddings originate from different model backbones.

Since the Hungarian algorithm produces a discrete matching, it is evaluated only using Top-1 Accuracy, while the other algorithms are evaluated across all metrics. For each experiment, the lowest-rank solver is reported in [Table2](https://arxiv.org/html/2505.12540v4#S5.T2 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings") and [Table4](https://arxiv.org/html/2505.12540v4#S5.T4 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings") (denoted by symbols in the final column). Evaluation metrics are defined as follows:

1. 1.


Top-1 Accuracy: Fraction of embeddings correctly identified as closest pairs, calculated by either selecting the maximum transported mass per embedding or applying the Hungarian algorithm directly to the transport plan PP. We report the higher accuracy between the two.

2. 2.


Mean Rank: Average rank position of the correct embedding match viv\_{i} when sorted by descending transported mass Pi​jP\_{ij} from uiu\_{i}:



|     |     |     |
| --- | --- | --- |
|  | rank​(vi)=position of ​vi​ among sorted ​Pi​j.\\text{rank}(v\_{i})=\\text{position of }v\_{i}\\text{ among sorted }P\_{ij}. |  |

3. 3.


Mean Cosine Similarity: Average cosine similarity between barycenters and true counterparts:



|     |     |     |
| --- | --- | --- |
|  | vi′=∑j=1nPi​j​vj∑j=1nPi​j,Similarity=1n​∑i=1ncos⁡(vi′,vi).v^{\\prime}\_{i}=\\frac{\\sum\_{j=1}^{n}P\_{ij}v\_{j}}{\\sum\_{j=1}^{n}P\_{ij}},\\quad\\text{Similarity}=\\frac{1}{n}\\sum\_{i=1}^{n}\\cos(v^{\\prime}\_{i},v\_{i}). |  |


## Appendix C Translating to and from Qwen

|  | vec2vec | OT Baseline |
| --- | --- | --- |
| M1M\_{1} | M2M\_{2} | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gte | qwen | 0.50 (0.0) | 0.92 | 2.28 (0.2) | 0.38 (0.0) | 0.00 | 425.28 (1.1)‡ |
| qwen | gte | 0.84 (0.0) | 0.88 | 2.49 (0.3) | 0.85 (0.0) | 0.00 | 425.07 (1.2)‡ |

Table 8: Translations between GTE and Qwen embeddings trained on NQ and evaluated on a 65536 text subset of NQ (chunked in batches of size 1024). Rank varies from 1 to 1024, thus 512 corresponds to a random ordering. Since the embedding dimensionalities are different, only the Gromov-Wasserstein‡ OT baseline is run and the naive baseline does not apply. Bold denotes best value.

As shown in [Table8](https://arxiv.org/html/2505.12540v4#A3.T8 "In Appendix C Translating to and from Qwen ‣ Harnessing the Universal Geometry of Embeddings"), vec2vec successfully translates between GTE and Qwen, significantly outperforming the optimal transport baseline in all metrics except qwen →\\to gte cosine similarity, which we hypothesize may be due to the substantial performance gap between the models—indeed, Qwen differs from GTE in architecture (dense Qwen backbone), training methodology (unsupervised + model merging techniques), size (14×\\times larger than the next largest model and 37×\\times larger than GTE), context length, and recency. Given Qwen’s size and computational cost, we only evaluated this representative pair. We leave further evaluation to future work.

## Appendix D Text-image retrieval on MS COCO

| model | R@16 ↑\\uparrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- |
| granite →\\to clip | 0.23 | 0.23 (0.0) | 233.67 (3.0) |
| clip (baseline) | 0.75 | 0.30 (0.0) | 23.20 (0.8) |

Table 9: Cross-model text-image retrieval on MS COCO: granite →\\to clip vec2vec trained on NQ (unimodal) and evaluated on MS COCO’s validation set. The rank metric varies from 1 to 5000, thus 2500 corresponds to a random ordering. Queries (captions) embedded with either Granite or CLIP. Documents (images) embedded with CLIP. Each caption has a unique image. Standard errors are shown in parentheses.

Our vec2vecs can “stitch" modalities onto unimodal models by translating to a multimodal model. To test this, we evaluated cross-modal text-image retrieval on MS COCO’s validation set (5000 examples) \[ [34](https://arxiv.org/html/2505.12540v4#bib.bibx34 "")\], translating queries (captions) embedded with Granite to retrieve documents (images) embedded with CLIP using our unimodal granite →\\to clip translator from [section4.3](https://arxiv.org/html/2505.12540v4#S4.SS3 "4.3 Evaluating information extraction ‣ 4 Experimental setup ‣ Harnessing the Universal Geometry of Embeddings"). Each caption has a unique image. We report Recall@16, cosine similarities, and Rank, with CLIP (for both documents and queries) as our baseline.

As [Table9](https://arxiv.org/html/2505.12540v4#A4.T9 "In Appendix D Text-image retrieval on MS COCO ‣ Harnessing the Universal Geometry of Embeddings") shows, translating Granite embeddings to CLIP enables non-negligible cross-model multimodal retrieval with a unimodal model for queries—despite zero multimodal training. Further evaluation of this paradigm with multimodal-specific training is a promising direction.

## Appendix E Initialization robustness by model backbone

GAN training is notoriously unstable to weight initialization \[ [53](https://arxiv.org/html/2505.12540v4#bib.bibx53 "")\]. To measure our method’s robustness, we trained fifteen e5 →\\to gte (shared backbone) and e5 →\\to gtr (cross-backbone) vec2vecs on the NQ dataset for a fixed 10 epochs.

For the translations between related models, vec2vec training was relatively stable across random seeds: 14 out of 15 seeds achieved at least 80% top-1 accuracy within a fixed epoch budget, while the remaining run reached 72%. In contrast, translation between unrelated models proved significantly less stable, with only 3 out of 15 runs achieving convergence (80% top-1 accuracy). We leave improving the seed stability of our training regime as future, valuable work.

## Appendix F Full out-of-distribution translation results

We provide baseline numbers for the experiments shown in [Table3](https://arxiv.org/html/2505.12540v4#S5.T3 "In 5 vec2vec learns to translate embeddings without any paired data ‣ Harnessing the Universal Geometry of Embeddings"), by dataset.

|  | vec2vec | Naïve Baseline | OT Baseline |
| --- | --- | --- | --- |
| E1E\_{1} | E2E\_{2} | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gra. | gtr | 0.74 (0.0) | 0.99 | 1.09 (0.1) | -0.04 (0.0) | 0.00 | 415.61 (8.2) | 0.71 (0.0) | 0.01 | 220.93 (7.1)‡ |
| gte | 0.85 (0.0) | 0.95 | 1.26 (0.1) | 0.00 (0.0) | 0.00 | 406.73 (8.2) | 0.87 (0.0) | 0.01 | 201.48 (6.6)‡ |
| ste. | 0.77 (0.0) | 0.96 | 1.11 (0.0) | 0.00 (0.0) | 0.00 | 417.27 (8.2) | 0.74 (0.0) | 0.00 | 239.36 (6.7)‡ |
| e5 | 0.83 (0.0) | 0.87 | 3.10 (0.7) | 0.02 (0.0) | 0.00 | 405.53 (8.1) | 0.87 (0.0) | 0.01 | 244.94 (7.4)‡ |
| gtr | gra. | 0.79 (0.0) | 0.98 | 2.41 (0.6) | -0.04 (0.0) | 0.00 | 411.53 (8.3) | 0.57 (0.0) | 0.01 | 398.29 (8.2)‡ |
| gte | 0.85 (0.0) | 0.96 | 1.29 (0.2) | 0.04 (0.0) | 0.00 | 392.01 (8.2) | 0.86 (0.0) | 0.01 | 259.47 (7.4)‡ |
| ste. | 0.77 (0.0) | 0.96 | 1.10 (0.0) | 0.00 (0.0) | 0.00 | 394.69 (8.3) | 0.74 (0.0) | 0.00 | 294.58 (7.4)‡ |
| e5 | 0.80 (0.0) | 0.53 | 13.38 (1.2) | 0.03 (0.0) | 0.00 | 400.85 (8.2) | 0.87 (0.0) | 0.01 | 266.04 (7.7)‡ |
| gte | gra. | 0.73 (0.0) | 0.94 | 1.33 (0.1) | 0.00 (0.0) | 0.00 | 408.81 (8.3) | 0.56 (0.0) | 0.01 | 398.16 (8.2)∗ |
| gtr | 0.71 (0.0) | 0.95 | 1.29 (0.1) | 0.04 (0.0) | 0.00 | 386.58 (8.3) | 0.71 (0.0) | 0.01 | 254.74 (7.3)‡ |
| ste. | 0.86 (0.0) | 1.00 | 1.00 (0.0) | 0.58 (0.0) | 1.00 | 1.00 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| e5 | 0.83 (0.0) | 0.91 | 1.57 (0.2) | 0.68 (0.0) | 1.00 | 1.00 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| ste. | gra. | 0.79 (0.0) | 0.99 | 1.09 (0.1) | 0.00 (0.0) | 0.00 | 418.16 (8.4) | 0.57 (0.0) | 0.00 | 399.56 (8.2)‡ |
| gtr | 0.77 (0.0) | 1.00 | 1.00 (0.0) | 0.00 (0.0) | 0.00 | 393.07 (8.1) | 0.71 (0.0) | 0.00 | 294.65 (7.4)‡ |
| gte | 0.90 (0.0) | 1.00 | 1.00 (0.0) | 0.58 (0.0) | 1.00 | 1.00 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| e5 | 0.85 (0.0) | 0.98 | 1.05 (0.0) | 0.37 (0.0) | 0.89 | 1.55 (0.1) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| e5 | gra. | 0.79 (0.0) | 0.98 | 1.08 (0.0) | 0.02 (0.0) | 0.00 | 405.75 (8.3) | 0.57 (0.0) | 0.01 | 398.34 (8.2)‡ |
| gtr | 0.67 (0.0) | 0.80 | 3.10 (0.6) | 0.03 (0.0) | 0.00 | 401.16 (8.4) | 0.71 (0.0) | 0.00 | 268.28 (7.6)‡ |
| gte | 0.87 (0.0) | 0.99 | 1.02 (0.0) | 0.68 (0.0) | 1.00 | 1.00 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| ste. | 0.75 (0.0) | 0.98 | 1.06 (0.0) | 0.37 (0.0) | 1.00 | 1.00 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |

Table 10: Out-of-distribution translations on TweetTopic (with baselines): vec2vec models trained on NQ and evaluated on the entire TweetTopic test set (800 tweets). The rank metric varies from 1 to 800, thus 400 corresponds to a random ordering. Standard errors are shown in parentheses. Symbols denote the lowest-rank solver: Earth Mover’s Distance∗ and Gromov-Wasserstein‡

|  | vec2vec | Naïve Baseline | OT Baseline |
| --- | --- | --- | --- |
| E1E\_{1} | E2E\_{2} | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow | cos⁡(⋅)\\cos(\\cdot)↑\\uparrow | T-1 ↑\\uparrow | Rank ↓\\downarrow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gra. | gtr | 0.74 (0.0) | 0.60 | 23.38 (1.6) | -0.02 (0.0) | 0.00 | 4010.00 (25.8) | 0.82 (0.0) | 0.00 | 3962.83 (26.1)† |
| gte | 0.85 (0.0) | 0.08 | 346.21 (7.8) | 0.01 (0.0) | 0.00 | 3978.35 (26.1) | 0.92 (0.0) | 0.00 | 3808.18 (25.9)† |
| ste. | 0.72 (0.0) | 0.13 | 242.23 (6.1) | -0.01 (0.0) | 0.00 | 3900.74 (26.2) | 0.86 (0.0) | 0.02 | 3780.44 (26.0)† |
| e5 | 0.84 (0.0) | 0.12 | 361.06 (8.7) | 0.02 (0.0) | 0.00 | 4024.92 (26.1) | 0.93 (0.0) | 0.00 | 3937.63 (26.2)† |
| gtr | gra. | 0.78 (0.0) | 0.51 | 35.27 (1.9) | -0.02 (0.0) | 0.00 | 4023.67 (26.1) | 0.87 (0.0) | 0.00 | 3964.83 (26.1)† |
| gte | 0.84 (0.0) | 0.12 | 279.56 (6.9) | 0.08 (0.0) | 0.00 | 4180.47 (26.2) | 0.87 (0.0) | 0.00 | 4088.97 (26.2)‡ |
| ste. | 0.72 (0.0) | 0.27 | 127.92 (4.4) | 0.00 (0.0) | 0.00 | 4296.04 (26.1) | 0.76 (0.0) | 0.00 | 4095.11 (26.1)‡ |
| e5 | 0.82 (0.0) | 0.01 | 1413.80 (18.3) | 0.09 (0.0) | 0.00 | 4064.47 (26.2) | 0.93 (0.0) | 0.00 | 4010.13 (26.1)† |
| gte | gra. | 0.73 (0.0) | 0.09 | 342.15 (7.8) | 0.01 (0.0) | 0.00 | 3946.19 (25.8) | 0.87 (0.0) | 0.00 | 3802.92 (25.9)† |
| gtr | 0.69 (0.0) | 0.12 | 256.63 (6.4) | 0.08 (0.0) | 0.00 | 4229.90 (26.2) | 0.69 (0.0) | 0.00 | 4094.02 (26.1)‡ |
| ste. | 0.85 (0.0) | 1.00 | 1.00 (0.0) | 0.56 (0.0) | 1.00 | 1.00 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| e5 | 0.86 (0.0) | 0.54 | 17.71 (0.9) | 0.69 (0.0) | 0.98 | 1.04 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| ste. | gra. | 0.77 (0.0) | 0.14 | 221.95 (5.9) | -0.01 (0.0) | 0.00 | 3951.42 (25.9) | 0.87 (0.0) | 0.01 | 3776.52 (26.0)† |
| gtr | 0.75 (0.0) | 0.56 | 17.70 (1.0) | 0.00 (0.0) | 0.00 | 4339.83 (26.2) | 0.70 (0.0) | 0.00 | 4093.61 (26.1)‡ |
| gte | 0.91 (0.0) | 1.00 | 1.00 (0.0) | 0.56 (0.0) | 1.00 | 1.00 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| e5 | 0.85 (0.0) | 0.51 | 26.33 (1.2) | 0.35 (0.0) | 0.59 | 12.68 (0.6) | 0.93 (0.0) | 1.00 | 1.00 (0.0)† |
| e5 | gra. | 0.78 (0.0) | 0.21 | 151.09 (4.6) | 0.02 (0.0) | 0.00 | 4008.10 (25.9) | 0.87 (0.0) | 0.00 | 3932.58 (26.2)† |
| gtr | 0.66 (0.0) | 0.01 | 1029.64 (14.9) | 0.09 (0.0) | 0.00 | 4032.85 (26.2) | 0.82 (0.0) | 0.00 | 4010.06 (26.1)† |
| gte | 0.87 (0.0) | 0.60 | 32.59 (2.6) | 0.69 (0.0) | 0.98 | 1.09 (0.0) | 1.00 (0.0) | 1.00 | 1.00 (0.0)∗ |
| ste. | 0.75 (0.0) | 0.46 | 32.12 (1.4) | 0.35 (0.0) | 0.86 | 2.49 (0.1) | 0.86 (0.0) | 1.00 | 1.01 (0.0)† |

Table 11: Out-of-distribution translations on MIMIC (with baselines): vec2vec models trained on NQ and evaluated on an 8192-record subset of MIMIC. The rank metric varies from 1 to 8192, thus 4096 corresponds to a random ordering. Standard errors are shown in parentheses. Symbols denote the lowest-rank solver: Earth Mover’s Distance∗, Sinkhorn† and Gromov-Wasserstein‡

## Appendix G Zero-shot inversion on TweetTopic

![Refer to caption](https://arxiv.org/html/2505.12540v4/tweettopic_heatmap.png)Figure 7: Leakage of information via inversion. Trained on NQ and evaluated on a 50-tweet subset of the TweetTopic dataset. Cells denote judge accuracy.

We replicate [Figure5](https://arxiv.org/html/2505.12540v4#S6.F5 "In 6 Using vec2vec translations to extract information ‣ Harnessing the Universal Geometry of Embeddings") on the TweetTopic dataset in [Figure7](https://arxiv.org/html/2505.12540v4#A7.F7 "In Appendix G Zero-shot inversion on TweetTopic ‣ Harnessing the Universal Geometry of Embeddings"), extracting information given only translated embeddings of tweets. We achieve non-negligible leakage for all model pairs.

## Appendix H Prompt for measuring information extraction

[Figures5](https://arxiv.org/html/2505.12540v4#S6.F5 "In 6 Using vec2vec translations to extract information ‣ Harnessing the Universal Geometry of Embeddings") and [7](https://arxiv.org/html/2505.12540v4#A7.F7 "Figure 7 ‣ Appendix G Zero-shot inversion on TweetTopic ‣ Harnessing the Universal Geometry of Embeddings") utilize an LLM judge to determine whether the approximate inversion (using \[ [67](https://arxiv.org/html/2505.12540v4#bib.bibx67 "")\]) of a translated email embedding leaks information about the original email. [Figure8](https://arxiv.org/html/2505.12540v4#A8.F8 "In Appendix H Prompt for measuring information extraction ‣ Harnessing the Universal Geometry of Embeddings") shows our prompt to the GPT-4o judge:

Original email: {ground\_truth}Reconstructed email: {generation}.Does the reconstructed email leak any information about the original email?Answer with only ‘yes’ or ‘no’.Figure 8: The prompt given to the LLM judge.