## Topics

Close

01. [Analytics](https://www.infoworld.com/analytics/)
02. [Artificial Intelligence](https://www.infoworld.com/artificial-intelligence/)
03. [Careers](https://www.infoworld.com/careers/)
04. [Cloud Computing](https://www.infoworld.com/cloud-computing/)
05. [Data Management](https://www.infoworld.com/data-management/)
06. [Databases](https://www.infoworld.com/database/)
07. [Development Tools](https://www.infoworld.com/development-tools/)
08. [Devops](https://www.infoworld.com/devops/)
09. [Emerging Technology](https://www.infoworld.com/emerging-technology/)
10. [Enterprise Buyer’s Guides](https://www.infoworld.com/enterprise-buyers-guide/)
11. [Generative AI](https://www.infoworld.com/generative-ai/)
12. [IT Leadership](https://www.infoworld.com/it-leadership/)
13. [Java](https://www.infoworld.com/java/)
14. [JavaScript](https://www.infoworld.com/javascript/)
15. [Microsoft .NET](https://www.infoworld.com/microsoft-net/)
16. [Open Source](https://www.infoworld.com/open-source/)
17. [Programming Languages](https://www.infoworld.com/programming-languages/)
18. [Python](https://www.infoworld.com/python/)
19. [Security](https://www.infoworld.com/security/)
20. [Software Development](https://www.infoworld.com/software-development/)
21. [Technology Industry](https://www.infoworld.com/technology-business/)

by [Prasanth Aby Thomas](https://www.infoworld.com/profile/prasanth-aby-thomas/)

# Meta launches Muse Code for complex software work with persistent AI agents

news

Aug 6, 20264 mins

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

[Artificial Intelligence](https://www.infoworld.com/artificial-intelligence/)[Development Tools](https://www.infoworld.com/development-tools/)[Software Development](https://www.infoworld.com/software-development/)

by [Prasanth Aby Thomas](https://www.infoworld.com/profile/prasanth-aby-thomas/)

Prasanth Aby Thomas is a freelance technology journalist who specializes in semiconductors, security, AI, and EVs. His work has appeared in DigiTimes Asia and asmag.com, among other publications.

Earlier in his career, Prasanth was a correspondent for Reuters covering the energy sector. Prior to that, he was a correspondent for International Business Times UK covering Asian and European markets and macroeconomic developments.

He holds a Master's degree in international journalism from Bournemouth University, a Master's degree in visual communication from Loyola College, a Bachelor's degree in English from Mahatma Gandhi University, and studied Chinese language at National Taiwan University.

## More from this author

- [news\\
**Google ADK flaws reveal what happens when AI agents trust the wrong message** \\
Aug 4, 2026 5 mins](https://www.infoworld.com/article/4204919/google-adk-flaws-reveal-what-happens-when-ai-agents-trust-the-wrong-message-2.html)
- [news\\
**Anthropic rejects open-weight AI bans, calls for China chip controls and safety tests** \\
Jul 28, 2026 5 mins](https://www.infoworld.com/article/4202193/anthropic-rejects-open-weight-ai-bans-calls-for-china-chip-controls-and-safety-tests-2.html)
- [news\\
**Thinking Machines Lab offers enterprises a US alternative in open-weight AI** \\
Jul 16, 2026 5 mins](https://www.infoworld.com/article/4197743/thinking-machines-offers-enterprises-a-us-alternative-in-open-weight-ai.html)
- [news\\
**SpaceXAI launches Grok 4.5, touts lower coding-task costs than AI rivals** \\
Jul 9, 2026 5 mins](https://www.infoworld.com/article/4194895/spacexai-launches-grok-4-5-touts-lower-coding-task-costs-than-ai-rivals.html)
- [news\\
**Argo CD flaw shows why GitOps infrastructure should be treated as tier zero** \\
Jul 2, 2026 4 mins](https://www.infoworld.com/article/4192199/argo-cd-flaw-shows-why-gitops-infrastructure-should-be-treated-as-tier-zero-2.html)
- [news\\
**Anthropic accuses Alibaba of using 25,000 fake accounts to scrape Claude AI** \\
Jun 25, 2026 4 mins](https://www.infoworld.com/article/4189342/anthropic-accuses-alibaba-of-using-25000-fake-accounts-to-scrape-claude-ai.html)
- [news\\
**OpenAI rolls out AI-led push to fix open-source software flaws** \\
Jun 23, 2026 5 mins](https://www.infoworld.com/article/4188325/openai-rolls-out-ai-led-push-to-fix-open-source-software-flaws-2.html)
- [news\\
**France’s OVHcloud bets on frontier AI as Europe seeks alternatives to US models** \\
Jun 18, 2026 4 mins](https://www.infoworld.com/article/4186756/frances-ovhcloud-bets-on-frontier-ai-as-europe-seeks-alternatives-to-us-models-2.html)

## Show me more

PopularArticlesVideos

[news\\
\\
**Moonshot’s Kimi AI model has also escaped from a test environment** \\
\\
By Maxwell Cooter\\
\\
Aug 7, 20262 mins\\
\\
Artificial IntelligenceSecurity\\
\\
![Image](https://www.infoworld.com/wp-content/uploads/2026/08/4206787-0-72458200-1786114400-shutterstock_2295737281-100963189-orig.jpg?quality=50&strip=all&w=375)](https://www.infoworld.com/article/4206787/moonshots-kimi-ai-model-has-also-escaped-from-a-test-environment-2.html)

[news\\
\\
**Snowflake attacker pleads guilty to hack of 165 companies’ data** \\
\\
By Maxwell Cooter\\
\\
Aug 7, 20262 mins\\
\\
CyberattacksCybercrimeData Breach\\
\\
![Image](https://www.infoworld.com/wp-content/uploads/2026/08/4206755-0-51911700-1786109128-shutterstock_559515940-100961501-orig.jpg?quality=50&strip=all&w=375)](https://www.infoworld.com/article/4206755/snowflake-attacker-pleads-guilty-to-hack-of-165-companies-data-2.html)

[news\\
\\
**DeepMind founder ascends to singular AI role at Google** \\
\\
By Maxwell Cooter\\
\\
Aug 7, 20262 mins\\
\\
Artificial Intelligence\\
\\
![Image](https://www.infoworld.com/wp-content/uploads/2026/08/4206728-0-17956000-1786106972-shutterstock_2336779245.jpg?quality=50&strip=all&w=375)](https://www.infoworld.com/article/4206728/deepmind-founder-ascends-to-singular-ai-role-at-google-2.html)

[video\\
\\
**AI trends that need more attention** \\
\\
Aug 4, 20265 mins\\
\\
Python\\
\\
![Image](https://www.infoworld.com/wp-content/uploads/2026/08/4205130-0-81560300-1785861578-youtube-thumbnail-kUGzdL2OpyQ.jpg?quality=50&strip=all&w=444)](https://www.infoworld.com/video/4205130/ai-trends-that-need-more-attention.html)

[video\\
\\
**Who's leaving GitHub and why** \\
\\
Jul 29, 20267 mins\\
\\
Python\\
\\
![Image](https://www.infoworld.com/wp-content/uploads/2026/07/4202965-0-61481400-1785343003-youtube-thumbnail-TkT-To8u2Eo.jpg?quality=50&strip=all&w=444)](https://www.infoworld.com/video/4202965/whos-leaving-github-and-why.html)

[video\\
\\
**Typst, the programming language for documents** \\
\\
Jul 23, 20267 mins\\
\\
Python\\
\\
![Image](https://www.infoworld.com/wp-content/uploads/2026/07/4200709-0-60659500-1784814917-youtube-thumbnail-Mp2fgP0Kr5g.jpg?quality=50&strip=all&w=444)](https://www.infoworld.com/video/4200709/typst-the-programming-language-for-documents.html)

Notice Message App

X

![Infoworld logo](https://b2b-contenthub.com/wp-content/uploads/2024/07/infoworld-logo-black.svg)

## Information about cookies

We use essential cookies to make this site work. You may disable these by changing your browser settings but this may effect how the website functions. All other cookies require your consent including cookies from our trusted 108 [partners](https://cmpv2.infoworld.com/index.html?hasCsp=true&message_id=1497676&consentUUID=null&consent_origin=https%3A%2F%2Fcmpv2.infoworld.com%2Fconsent%2Ftcfv2&preload_message=true&version=v1#). Types of personal data processed include, but are not limited to, unique identifiers and browsing behaviour. You can get more information about cookies and how we collect and process personal data by going to our [cookie](https://foundryco.com/cookie-policy/) and [privacy policies](https://foundryco.com/privacy-policy/). We use your data for the following purposes:

Precise geolocation data, and identification through device scanning

Precise geolocation and information about device characteristics can be used.

Store and/or access information on a device

Cookies, device or similar online identifiers (e.g. login-based identifiers, randomly assigned identifiers, network based identifiers) together with other information (e.g. browser type and information, language, screen size, supported technologies etc.) can be stored or read on your device to recognise it each time it connects to an app or to a website, for one or several of the purposes presented here.

Personalised advertising and content, advertising and content measurement, audience research and services development

Advertising and content can be personalised based on your profile. Your activity on this service can be used to build or improve a profile about you for personalised advertising and content. Advertising and content performance can be measured. Reports can be generated based on your activity and those of others. Your activity on this service can help develop and improve products and services.

Social Media

Social Media cookies and pixels including Facebook, Twitter and LinkedIn

Analytics Storage

Enables storage (such as cookies) related to analytics (e.g. visit duration).

You have the right to withdraw consent at any time and you can do this by clicking Privacy Settings or Member Preferences located at the bottom of every page. To see your options please click the button below.

Reject AllOptionsI Agree