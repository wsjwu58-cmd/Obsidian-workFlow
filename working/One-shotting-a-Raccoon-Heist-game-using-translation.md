---
created: 2026-10-03
updated: 2026-10-03
title: 用 Claude Fable 5 一次性生成《浣熊劫案》游戏
sourceUrl: https://simonwillison.net/2026/Aug/5/raccoon-heist/
sourceAuthor: Simon Willison
translatedAt: 2026-10-03
sources: [references/articles.md 待处理队列]
tags: [Claude Code, Claude Fable 5, 一次性提示, One-shot, 游戏开发, Three.js, Playwright, gpt-image-2, GPT-5.6 Sol, 编码智能体, vibe coding, type/翻译]
---

# 用 Claude Fable 5 一次性生成《浣熊劫案》游戏

> [simonwillison.net](https://simonwillison.net/2026/Aug/5/raccoon-heist/)｜分类：AI / 编码智能体
> 作者：Simon Willison
> 发布：2026-08-05 19:42（页面标注）
> 原文：https://simonwillison.net/2026/Aug/5/raccoon-heist/

2022 年，我曾[在推特上](https://twitter.com/simonw/status/1555626060384911360)发过几张截图——一个由 GPT-3 生成的游戏概念，以及一些用 DALL-E 创作的"概念图"。今天，在那条推文的四周年之际，我决定看看 Claude Fable 5（运行在 [Claude Code for web](https://code.claude.com/docs/en/claude-code-on-the-web) 里）能否仅凭那条推文的内容，把整个游戏做出来。它完成得相当不错！

你可以[在这里玩到这款游戏](https://simonw.github.io/raccoon-heist/)。这是 [GitHub 仓库](https://github.com/simonw/raccoon-heist/)，还有一段简短的视频演示：

你的浏览器不支持 HTML5 视频。

#### 我是如何构建它的 [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#how-i-built-this)

这就是那条 2022 年 8 月 5 日的[推文](https://twitter.com/simonw/status/1555626060384911360)：

![Simon Willison @simonw - 新爱好：用 GPT-3 和 DALL-E 的组合，在 60 秒内做游戏原型。这是"Raccoon Heist"。两张图——第一张是 GPT-3 playground 的截图，提示词见下。右侧是一张明显由 DALL-E 生成的、近似等距视角的 3D 电脑游戏画面：两只浣熊沿着街道潜行，经过一栋充满未来感的建筑，看起来像是想偷点什么。](https://static.simonwillison.net/static/2026/raccoon-heist-tweet.webp)

我当时的 GPT-3 提示词是：

> `Write a detailed product description of a computer game where a team of raccoons go on heists.`

（中文：写一段详细的电脑游戏产品描述：一队浣熊去实施一系列抢劫。）

那还是在文本补全（text completion）的时代——你让 GPT-3 把后面的文本补全出来。它补全出的是：

> In "Raccoon Heist", you and your team of thieving raccoons are tasked with pulling off a series of daring heists. From robbing banks to stealing priceless art, no job is too big or too small for your furry crew. You'll need to use your wits and your skills to avoid the police and make a clean getaway with the loot. With exciting gameplay and a charming cast of characters, "Raccoon Heist" is the perfect game for anyone looking for a light-hearted caper.

（中文：在《浣熊劫案》中，你和你那队神偷浣熊要完成一连串大胆的抢劫。从抢银行到盗取无价艺术品，对你这支毛茸茸的团队来说，没有什么活儿是太大或太小的。你需要用机智和技能避开警察，带着战利品干净利落地逃走。凭借刺激的玩法和一群迷人的角色，《浣熊劫案》是所有想体验轻松愉快劫案故事的玩家的完美之选。）

我给 DALL-E 的提示词很短：

> `Screenshot from a video game where a team of raccoons go on a heist`

（中文：一张电子游戏截图，一队浣熊正在实施抢劫。）

今天的实验是：我能不能把这些截图连同一条"写个游戏"的提示词一起丢给 Fable 5，然后放手不管，最后得到一个能跑的游戏？

#### 让 Claude Code for web 用上 GitHub Pages [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#setting-claude-code-for-web-up-to-use-github-pages)

Claude Code for web 有一个让人头疼的地方：它还在干活的时候，你很难测试它正在做的东西。

我一直在用 GitHub Pages 绕开这个限制，发现效果非常好。

我的流程如下：

1. 在 [https://github.com/new](https://github.com/new) 为项目新建一个仓库——公开或私有都行，这个技巧对两者同样有效。
2. 在 Claude 的 iPhone 或桌面应用，或者浏览器里的 [https://claude.ai/code](https://claude.ai/code) 中开启一个 Claude Code for web 会话。
3. 告诉 Claude 要做什么，并鼓励它尽快提交一个 `index.html` 页面。这会创建一个名字类似 `claude/3d-raccoon-heist-game-50n293` 的分支。
4. 进入该仓库的 Settings -> Pages 区域（在我的例子里是 `github.com/simonw/raccoon-heist/settings/pages`），选择"Deploy from a branch"，选中那个分支名，然后点 Save。

就这么简单！每次 push 之后大约 30 秒内，最新内容就会出现在 `yourname.github.io/your-repo/` 上。

如果你用私有仓库这么做，任何能猜出仓库名的人都能看到已发布的内容。我自己倒不太在意这一点。

#### Fable 5 的提示词 [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#the-fable-5-prompt)

以下是我给 Fable 5 的提示词（写在我手机的备忘录应用里——整个项目都是在移动端完成的）。我随提示词附上了原推文里的两张图片。

> `Build this 3D game, for the browser.`
>
> `This repo is configured to serve static files so make sure there is an index.html that loads everything else.`
>
> `Make sure it is mobile-friendly (touch controls, works well on small screens).`
>
> `You have an OpenAI API key and access to their image generation model APIs, use that for textures to use with your 3D models. Docs here: https://developers.openai.com/api/docs/guides/image-generation - use gpt-image-2`
>
> `Work independently - do not ask me to make any further design decisions. Make sure the game is fun, a little surprising, has good raccoon heist vibes, and is visually pleasing.`
>
> `Commit and push as often as possible so I can preview your work - start with an index.html that presents a title screen, then build from there.`
>
> `Append to a notes.md file as you work, including your changes to that as part of every commit.`

（中文：把这款 3D 游戏做出来，面向浏览器。／这个仓库配置为提供静态文件，所以要确保有一个 index.html 来加载其他所有内容。／确保它对移动端友好（触摸控制，在小屏幕上也能良好运行）。／你有一个 OpenAI API key，以及对他们图像生成模型 API 的访问权限，用它来生成 3D 模型要用的贴图。文档在此：https://developers.openai.com/api/docs/guides/image-generation —— 用 gpt-image-2。／独立工作——不要再问我做任何进一步的设计决策。确保游戏好玩、带点小惊喜、有好的浣熊劫案氛围，并且视觉上赏心悦目。／尽可能频繁地 commit 和 push，这样我就能预览你的成果——先从呈现标题画面的 index.html 开始，再在此基础上继续构建。／在工作的过程中不断往 notes.md 文件里追加内容，并把对它的改动包含进每一次 commit 中。）

我没有做任何技术选型。基于此前的实验，我（正确地）假设它很可能会用 [Three.js](https://threejs.org/)。

事实证明，给 Claude 访问 OpenAI key 的权限，能很好地补齐它能力上的短板——在这个例子里，我们需要某种方式来生成用作贴图的图像。Fable 非常擅长给图像生成器写提示词！

我说"独立工作——不要再问我做任何进一步的设计决策"，是因为我想看看它能否在我完全不介入的情况下，产出一个完整、能跑的游戏。

我还说了"尽可能频繁地 commit 和 push，这样我就能预览你的成果"。当你在 Claude iPhone 应用里使用 Claude Code 时，你给它一个 GitHub 仓库，它就在某个分支里工作。让它"尽可能频繁地 push"，意味着 commit 会立刻开始落到那个分支上。

我喜欢加一点额外的"风味"——让它写 `notes.md`。这是[那个最终文件](https://github.com/simonw/raccoon-heist/blob/main/notes.md)，以及它在加入狗时写下的记录：

> New escalation: from night 3 the yards get a patrolling guard dog — a low-poly brown hound with a spiked red collar and a wagging tail. It wanders between random spots, and within 12 units it catches your scent and tracks you by smell (line of sight is irrelevant — it's all nose, shown by a 👃 over its head and barking). It gives up if you open a 17-unit gap. Getting caught messages are now source-specific: guard / headlights / hound. Verified wander → track → caught with an automated test.

（中文：新的升级：从第 3 夜开始，院子里会出现一只巡逻的护卫犬——一只低模的棕色猎犬，戴着带尖刺的红色项圈，尾巴还会摇。它在随机地点之间游荡，一旦进入 12 个单位内就会嗅到你的气味，并靠嗅觉追踪你（视线无关紧要——全靠鼻子，头顶会显示一个 👃 并伴随吠叫）。如果你拉开 17 个单位的距离，它就会放弃。被抓住的提示信息现在按来源区分：守卫 / 车灯 / 猎犬。用自动化测试验证了"游荡 → 追踪 → 抓住"的流程。）

#### 回顾会话记录 [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#reviewing-the-transcript)

你可以访问[这份 Claude Code 共享会话](https://claude.ai/code/session_01NUBoCfnhGETcCDyEUPS8jp)，另外我还用我的 [claude-code-transcripts](https://github.com/simonw/claude-code-transcripts) 工具导出了自己的 HTML 版本，你可以[在这里看到](https://simonw.github.io/raccoon-heist/transcript/page-001.html)。

Fable 先是做了一个 index 页面，[引入了一份](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-13-304Z) Three.js 的 vendored 副本，然后写了自己的 [gen\_textures.py 脚本](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-49-064Z)（[副本在此](https://github.com/simonw/raccoon-heist/blob/main/gen_textures.py)）。

它生成了这些贴图，并[抽查确认](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-59-07-900Z)它们看起来没问题。它为垃圾桶生成的 [metal.jpg 文件](https://github.com/simonw/raccoon-heist/blob/main/textures/metal.jpg)长这样——不过我觉得它在游戏里应用得并不完全正确：

![一张游戏贴图集：深蓝灰色的铆钉金属面板，左上有一个带把手的圆形舱门，中间是带肋的波纹面板，左下是一块素圆盘，顶部和底部是平整的条带。没有可见文字。](https://raw.githubusercontent.com/simonw/raccoon-heist/refs/heads/main/textures/metal.jpg)

接着它做出了游戏的第一个基础版本，然后[决定](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-04-51-625Z)用 Playwright 在"预装的 Chromium 里做冒烟测试"。这意味着它可以给自己的作品截图并[亲眼检查](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-05-53-823Z)。它分别针对页面的桌面宽度和移动端宽度做了这件事，随后发现[浣熊在移动端宽度下不可见](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-09-33-406Z)，于是[修好了这个问题](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-14-39-180Z)：

> The raccoon, dumpster hideout, and both crew raccoons are now perfectly visible on mobile. Committing this critical fix.

（中文：浣熊、垃圾箱藏身处，以及两名同伙浣熊现在在移动端都完全可见了。提交这个关键修复。）

它决定生成一个标题画面，并[用这个](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-15-02-574Z) [gen\_title.py](https://github.com/simonw/raccoon-heist/blob/main/gen_title.py) 脚本来完成。以下是它为这个标题画面使用的 `gpt-image-2` 提示词：

> `Video game key art, low-poly 3D render style, moody nighttime scene: a cute low-poly raccoon wearing a tiny black burglar mask sneaking on its hind legs carrying a glowing gold coin, next to a tipped-over metal trash can, suburban house with warm glowing windows in the background, deep blue night, full moon, fireflies, cinematic rim lighting, charming heist caper mood. No text, no words, no logos.`

（中文：电子游戏主视觉，低多边形 3D 渲染风格，氛围感夜景：一只可爱的低模浣熊戴着小小的黑色窃贼面罩，用后腿直立潜行，抱着一枚发光的金币，旁边是一个翻倒的金属垃圾桶，背景是郊区房屋、窗户透着暖光，深蓝色的夜，满月，萤火虫，电影感的轮廓光，迷人的劫案冒险氛围。不要文字、不要词语、不要标志。）

以及生成出来的图像（Claude [认为它"美极了"](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-16-42-176Z)）——不过我要指出，在桌面端显示时，它会被裁剪得只剩上三分之一，浣熊都没了！

![多边形浣熊抱着金币，旁边是一个翻倒的垃圾桶，背景是一栋房子和月亮。](https://static.simonwillison.net/static/2026/raccoon-heist-title.jpeg)

然后是我最喜欢的一处改动：它[加入了那只狗](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-23-00-850Z)：

```
export function makeDog() {
  const g = new THREE.Group();
  const BROWN = 0x8a6440, DARK = 0x5e4128;
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.42, 10, 8), M(BROWN));
  body.scale.set(0.9, 0.8, 1.5);
  body.position.y = 0.55;
  body.castShadow = true;
  g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 10, 8), M(BROWN));
  head.position.set(0, 0.85, 0.62);
  g.add(head);
  const snout = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 6), M(DARK));
  snout.scale.set(0.9, 0.7, 1.3);
  snout.position.set(0, 0.76, 0.9);
  g.add(snout);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.06, 6, 6), M(BLACK));
  nose.position.set(0, 0.78, 1.08);
  g.add(nose);
  for (const s of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 6), M(DARK));
    ear.scale.set(0.7, 1.3, 0.5);
    ear.position.set(0.2 * s, 1.08, 0.55);
    g.add(ear);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.05, 6, 6), M(0x1a1a1a, { emissive: 0x331111 }));
    eye.position.set(0.13 * s, 0.92, 0.86);
    g.add(eye);
  }
  const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.09, 0.5, 6), M(DARK));
  tail.position.set(0, 0.8, -0.62);
  tail.rotation.x = 0.8;
  g.add(tail);
  // spiked collar
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.05, 6, 12), M(0xc0392b));
  collar.position.set(0, 0.78, 0.5);
  collar.rotation.x = Math.PI / 2.4;
  g.add(collar);
  const legGeo = new THREE.CylinderGeometry(0.07, 0.09, 0.34, 6);
  const legs = [];
  for (const [x, z] of [[-0.22, 0.35], [0.22, 0.35], [-0.22, -0.35], [0.22, -0.35]]) {
    const leg = new THREE.Mesh(legGeo, M(DARK));
    leg.position.set(x, 0.17, z);
    g.add(leg);
    legs.push(leg);
  }
  let phase = Math.random() * 10;
  return {
    group: g,
    animate(dt, speed) {
      phase += dt * (3 + speed * 10);
      const amp = Math.min(0.6, 0.1 + speed * 0.6);
      legs[0].rotation.x = Math.sin(phase) * amp;
      legs[3].rotation.x = Math.sin(phase) * amp;
      legs[1].rotation.x = -Math.sin(phase) * amp;
      legs[2].rotation.x = -Math.sin(phase) * amp;
      tail.rotation.z = Math.sin(phase * 1.5) * 0.4;
      body.position.y = 0.55 + Math.abs(Math.sin(phase)) * 0.04 * (0.3 + speed);
    },
  };
}
```

并对它做了[一轮测试](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-09-230Z)（用的是 Playwright），还包括[另一张截图](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-33-559Z)。

```
  // walk near the dog
  await page.evaluate(() => { const d = window.__rh.dog; window.__rh.teleport(d.x + 6, d.z); });
  await page.waitForTimeout(2000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state, player: window.__rh.debug().player }));
  console.log('after approach:', info);
  await page.waitForTimeout(3000);
  info = await page.evaluate(() => JSON.stringify({ dog: window.__rh.dog, state: window.__rh.state }));
  console.log('after chase:', info);
  await page.screenshot({ path: __dirname + '/shot-dog.png' });
```

![游戏截图。第 3 夜，浣熊在画面中央与狗交叠。一条消息显示"Busted! The Guard shooed you off!"（被抓住了！守卫把你赶走了！）屏幕边缘泛着红色。](https://static.simonwillison.net/static/2026/shot-dog.png)

它又做了一些调整，然后[宣布完工](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-29-13-245Z)：

> **Raccoon Heist is built, tested, and pushed** — 7 commits on `claude/3d-raccoon-heist-game-50n293`, all verified with automated Playwright playthroughs on desktop, portrait-phone, and landscape-phone viewports.
>
> **The game:** You're a masked raccoon sneaking out of your crew's dumpster hideout into a moonlit cul-de-sac. Grab coins, gems, rings, donuts, and fish (they visibly stack on your back and slow you down), then waddle home and bank them before dawn. Each night raises the goal and the heat: night 1 has one flashlight-sweeping guard, night 2 has two, night 3 adds a scent-tracking hound that ignores line-of-sight entirely. A police cruiser sweeps the street with headlights, homeowners randomly peek out of windows, a seagull periodically dive-bombs your unclaimed loot, pizza slices trigger a 6-second speed FRENZY, and a rare golden TV is worth 120 points if you can haul its weight home. Win ranks: TRASH PANDA ⭐ → CAT BURGLAR ⭐⭐ → MASTER OF DISGUISE ⭐⭐⭐, with your best run saved to localStorage.
>
> **How it's built:** Vendored Three.js (no CDN), procedural low-poly characters, and a procedural WebAudio soundtrack (sneaky walking-bass jazz plus all sound effects — zero audio files). All seven ground/wall textures and the title-screen hero art were generated with gpt-image-2 and committed as static assets, so the deployed game makes no API calls. Mobile gets a dynamic touch joystick (appears wherever you touch) plus a DASH button; desktop uses WASD/arrows and Space.
>
> **Testing caught two real bugs worth mentioning:** the canvas rendered at 2× size on any real phone (a `cssText` assignment was wiping Three.js's inline sizing — desktop DPR-1 tests masked it completely), and the win screen's star-rating div inherited the title screen's full-screen `.stars` CSS and silently swallowed every tap on the "next night" button. Both are fixed and regression-tested, along with pickup, banking, chase/caught, dawn, night progression, and lose/retry flows.
>
> `notes.md` has the full build log. The game is live on the branch — just serve the repo root and open `index.html`.

（中文：**《浣熊劫案》已构建、测试并推送**——在 `claude/3d-raccoon-heist-game-50n293` 上有 7 个 commit，全部通过自动化 Playwright 试玩验证，覆盖桌面、竖屏手机和横屏手机三种视口。

**游戏内容：** 你是一只戴着面罩的浣熊，从你们团伙的垃圾箱藏身处溜出来，进入月光下的死胡同。捡金币、宝石、戒指、甜甜圈和鱼（它们会明显地堆在你背上，并让你变慢），然后摇摇摆摆地走回家，在天亮前把它们存起来。每一夜都会提高目标数和危险度：第 1 夜有一名用手电筒扫射的守卫，第 2 夜有两名，第 3 夜增加了一只完全无视视线的嗅迹猎犬。一辆警车用车灯扫过街道，房主会随机从窗户探出头来，一只海鸥会定时俯冲轰炸你尚未收走的战利品，披萨块会触发 6 秒的加速 FRENZY（狂暴），还有一台稀有的金色电视，如果你能把它扛回家就值 120 分。胜利等级：TRASH PANDA ⭐ → CAT BURGLAR ⭐⭐ → MASTER OF DISGUISE ⭐⭐⭐，你最好的一局会保存到 localStorage。

**构建方式：** 以内联（vendored）副本方式引入 Three.js（不用 CDN），程序化生成的低模角色，以及一段程序化生成的 WebAudio 配乐（鬼祟的行走贝斯爵士乐加上所有音效——零音频文件）。全部七张地面/墙面贴图以及标题画面的主视觉都用 gpt-image-2 生成，并作为静态资源提交，所以部署后的游戏不会调用任何 API。移动端有动态触摸摇杆（在你触摸的任何位置出现）外加一个 DASH 按钮；桌面端用 WASD/方向键和空格键。

**测试抓出了两个值得一提的真实 bug：** 在任何真实手机上，画布都会以 2 倍尺寸渲染（一处 `cssText` 赋值把 Three.js 的内联尺寸设置抹掉了——桌面端 DPR-1 的测试完全掩盖了这个问题）；以及胜利画面的星级评分 div 继承了标题画面全屏的 `.stars` CSS，静默吞掉了对"下一夜"按钮的每一次点击。两者都已修复并做了回归测试，与拾取、存钱、追逐/被抓、天亮、夜晚推进、失败/重试流程一起。

`notes.md` 里有完整的构建日志。游戏已经在那个分支上线——只要把仓库根目录作为静态服务打开 `index.html` 即可。）

#### 这游戏到底好不好玩？ [\#](https://simonwillison.net/2026/Aug/5/raccoon-heist/\#is-the-game-any-good-)

它是一个令人印象深刻的起点，但并不是一款*好*游戏。

你在一个院子里操控浣熊四处收集物品——甜甜圈、鱼、金币、珠宝——同时要躲避拿着手电筒的守卫，以及在后几关出现的狗。你的负重上限有限，一旦满载就得把东西放到垃圾箱那里。如果你捡起一块披萨，会获得一段临时加速。

完全没有任何团队机制——垃圾箱旁边另外还有两只静止不动的浣熊，但它们纯粹是装饰。

随着关卡推进，它会稍微更有挑战性——第 3 关引入的狗是最有趣的新机制——但它非常非常好通关。而且它也相当无聊——每一夜的时长是固定的，你把所有物品收完之后，就只能干等天亮，无事可做。

它的实现让我印象深刻。它是完全 3D 的，有垃圾桶，手电筒的光锥很好玩，整体视觉风格也相当统一。它在移动端能跑。音乐（据 Claude 说，是"一段程序化生成的 WebAudio 配乐（鬼祟的行走贝斯爵士乐加上所有音效——零音频文件）"）很简单，但感觉差不多刚刚好。

作为一个完成的游戏项目，它很平庸。但作为从一个单条提示词出发的起点，我觉得它非常令人印象深刻。

我现在已经靠 vibe coding 做过不少游戏了。从玩法的角度看，它们全都令人深感失望——事实证明，设计出真正*好玩*的游戏仍然是一项人类独有的特质，而且它所需的技巧和经验，远超 Claude 或我能拿得出来的水平。

话虽如此，我强烈推荐把游戏开发项目当作探索智能体能力的一种方式，随手折腾一番。它是一种有趣、低风险的尝鲜方式。如果你坚持得够久，说不定还能做出点值得一玩的东西！

**2026 年 8 月 7 日更新**：我把同样的提示词交给了运行 GPT-5.6 Sol Ultra 的 OpenAI Codex Desktop，得到了一个[明显更好的结果](https://simonwillison.net/2026/Aug/7/moonlight-mayhem/)——GPT-5.6 Sol 抓住了"一队浣熊去抢劫"这一要点的重要性，做出的游戏里你必须先在博物馆里救出两名同伙，然后踩在它们身上叠罗汉去偷走"金沙丁鱼"（Golden Sardine）。

发布于 [2026 年 8 月 5 日](https://simonwillison.net/2026/Aug/5/)晚上 7:42 · 在 [Mastodon](https://fedi.simonwillison.net/@simon)、[Bluesky](https://bsky.app/profile/simonwillison.net)、[Twitter](https://twitter.com/simonw) 上关注我，或[订阅我的通讯](https://simonwillison.net/about/#subscribe)
