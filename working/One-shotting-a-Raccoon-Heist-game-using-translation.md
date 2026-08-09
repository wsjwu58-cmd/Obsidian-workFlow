---
created: 2026-08-09
updated: 2026-08-09
title: 用 Claude Fable 5 一次做出《Raccoon Heist》游戏
sourceUrl: https://simonwillison.net/2026/Aug/5/raccoon-heist/
sourceAuthor: Simon Willison
translatedAt: 2026-08-09
sources: [references/articles.md 待处理队列]
tags: [AI Agent, Claude, vibe coding, 游戏开发, 提示词工程, type/翻译]
---

# 用 Claude Fable 5 一次做出《Raccoon Heist》游戏

> 2022 年我用 GPT-3 生成了一个游戏概念、用 DALL-E 画了张概念「美术」；今天，在四周年之际，我让 Claude Fable 5 仅凭那条推文的内容做出一整款游戏。它干得相当不错！

2022 年，我在[一条推文](https://twitter.com/simonw/status/1555626060384911360)里贴出过 GPT-3 生成的游戏概念截图，以及用 DALL-E 创作的概念「美术」。今天，在这条推文四周年之际，我决定看看 Claude Fable 5（运行在 [Claude Code for web](https://code.claude.com/docs/en/claude-code-on-the-web) 中）能否仅凭那条推文的内容，把整款游戏做出来。结果它干得相当不错！

你可以[在这里试玩这款游戏](https://simonw.github.io/raccoon-heist/)。这是 [GitHub 仓库](https://github.com/simonw/raccoon-heist/)，还有一个短视频演示：

（视频演示：你的浏览器不支持 HTML5 video，可到原文页面查看）

### 我是怎么做的

这是 [2022 年 8 月 5 日那条推文](https://twitter.com/simonw/status/1555626060384911360)：

![Simon Willison @simonw - 新爱好：用 GPT-3 和 DALL-E 的组合在 60 秒内原型化视频游戏。这就是「Raccoon Heist」。两张图——左边是 GPT-3 playground 的截图，提示词见下。右边是一张明显由 DALL-E 生成的近乎等距视角的 3D 电脑游戏画面：两只浣熊正沿一条街道偷偷溜过，经过一栋未来主义风格的大楼，看起来想偷点东西。](https://static.simonwillison.net/static/2026/raccoon-heist-tweet.webp)

我当年给 GPT-3 的提示词是：

> `Write a detailed product description of a computer game where a team of raccoons go on heists.`

那是文本补全（text completion）的时代——你让 GPT-3 补全剩下的文本。它补全道：

> 在《Raccoon Heist》中，你和你的偷窃浣熊团队将执行一系列大胆的劫案。从抢银行到偷无价之宝的艺术品，对你的毛茸茸团队来说，没有办不到的事。你需要运用你的智慧与技能躲避警察，带着赃物全身而退。激动人心的玩法加上迷人的角色阵容，《Raccoon Heist》是任何想找一场轻松愉快冒险的人的不二之选。

我给 DALL-E 的提示词则非常简短：

> `Screenshot from a video game where a team of raccoons go on a heist`

今天的实验是：我能不能把这些截图丢给 Fable 5，附上一段让它写一款游戏的提示词，然后放手不管，最后拿到一款能玩的成品游戏？

### 为 GitHub Pages 配置 Claude Code for web

Claude Code for web 一个让人沮丧的地方是：它还在工作的时候，你很难实时预览它正在做的东西。

我一直在用 GitHub Pages 绕过这个限制，发现效果非常好。

我的流程是：

1. 在 [https://github.com/new](https://github.com/new) 为项目新建一个仓库——公开或私有都行，这个技巧对两者同样有效。
2. 打开一个 Claude Code for web 会话，在 Claude iPhone 应用、桌面应用或浏览器 [https://claude.ai/code](https://claude.ai/code) 里都行。
3. 告诉 Claude 要做什么，并鼓励它尽快提交一个 `index.html` 页面。这会创建一个类似 `claude/3d-raccoon-heist-game-50n293` 的分支。
4. 进入仓库的 Settings -> Pages 区域（我的情况是 `github.com/simonw/raccoon-heist/settings/pages`），选择「Deploy from a branch」，选中那个分支，点保存。

就这么简单！每次 push 后大约 30 秒，最新内容就会出现在 `yourname.github.io/your-repo/`。

如果你对私有仓库这么做，任何能猜到仓库名的人都能看到发布的内容。我自己不太担心这一点。

### 给 Fable 5 的提示词

下面是我给 Fable 5 的提示词（写在手机上的备忘录应用里——整个项目都是在手机上进行的）。我随提示词附上了原推文中的两张图片。

> 在浏览器里把这款 3D 游戏做出来。
>
> 这个仓库配置为托管静态文件，所以请确保有一个 index.html 加载其他所有内容。
>
> 确保它对移动端友好（触控操作，在小屏幕上表现良好）。
>
> 你有一个 OpenAI API key，可以访问他们的图像生成模型 API，用它们为你的 3D 模型生成贴图。文档在这里：https://developers.openai.com/api/docs/guides/image-generation - 使用 gpt-image-2
>
> 独立工作——不要让我做任何进一步的设计决定。确保游戏有趣、带点惊喜、有良好的浣熊劫案氛围，并且视觉上赏心悦目。
>
> 尽可能频繁地提交并推送，这样我就能预览你的进度——先从一个带标题画面的 index.html 开始，然后在此基础上继续构建。
>
> 边工作边把进展写进 notes.md 文件，并把对它的修改包含进每一次提交。

我没有做任何技术选型。我（正确地）猜它大概会用 [Three.js](https://threejs.org/)——基于以往的经验。

给 Claude 一个 OpenAI key 的效果出乎意料地好，正好补上它能力的缺口——这次我们需要某种生成图片来当贴图的方式。Fable 非常擅长给图像生成器写提示词！

我说「独立工作——不要让我做任何进一步的设计决定」，是因为我想看看它能否在不需要我任何进一步输入的情况下，产出一款完整可玩的游戏。

我还说了「尽可能频繁地提交并推送，这样我就能预览你的进度」。当你在 Claude iPhone 应用里使用 Claude Code 时，你会给它一个 GitHub 仓库，它在分支上工作。告诉它「尽可能频繁推送」，提交就会立刻开始落进那个分支。

我喜欢要一份 `notes.md` 作为一点额外风味——这是[那份最终文件](https://github.com/simonw/raccoon-heist/blob/main/notes.md)，以及它加入那条狗时写的记录：

> 新的升级：从第 3 夜起，院子里会有一只巡逻的护卫犬——一只低多边形棕色猎犬，戴着红色尖刺项圈，尾巴摇来摇去。它会在随机地点之间游荡，12 个单位内闻到你的气味就会追踪你（视线完全无关——全靠鼻子，头顶会显示 👃 并且会吠叫）。如果你拉开 17 个单位的距离，它就会放弃。被抓提示现在按来源区分：守卫 / 车灯 / 猎犬。已用自动化测试验证 游荡 → 追踪 → 被抓 的流程。

### 回顾对话记录

你可以访问 [Claude Code 共享会话](https://claude.ai/code/session_01NUBoCfnhGETcCDyEUPS8jp)，我还用我的 [claude-code-transcripts](https://github.com/simonw/claude-code-transcripts) 工具导出了一份我自己的 HTML 版本，[可以在这里找到](https://simonw.github.io/raccoon-heist/transcript/page-001.html)。

Fable 先做了一个 index 页面，[内置了一份](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-13-304Z) Three.js 副本，然后写了自己的 [gen_textures.py 脚本](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-55-49-064Z)（[副本在这里](https://github.com/simonw/raccoon-heist/blob/main/gen_textures.py)）。

它生成了贴图，并[抽查](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T14-59-07-900Z)确认效果没问题。它给垃圾桶生成的 [metal.jpg](https://github.com/simonw/raccoon-heist/blob/main/textures/metal.jpg) 长这样，不过我并不觉得它在游戏里被用对了地方：

![一张深蓝灰色铆接金属面板的游戏纹理图集：左上角是带把手的圆形舱门，中间是瓦楞波纹板，左下角是素面圆形板，顶部和底部是平坦的带状条。没有可见文字。](https://raw.githubusercontent.com/simonw/raccoon-heist/refs/heads/main/textures/metal.jpg)

然后它搭出了游戏的第一版，接着[决定](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-04-51-625Z)用 Playwright 在「预装的 Chromium」里做冒烟测试。这意味着它可以给自己的作品截图，然后[亲自过目](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-05-53-823Z)。它分别对桌面和移动宽度的页面做了这件事，然后注意到[移动宽度下浣熊不可见](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-09-33-406Z)，于是[修复了它](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-14-39-180Z)：

> 浣熊、垃圾箱藏身处和两个队友浣熊在移动端现在完全可见了。提交这个关键修复。

它决定做一个标题画面，用这个 [gen_title.py](https://github.com/simonw/raccoon-heist/blob/main/gen_title.py) 脚本[做了出来](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-15-02-574Z)。这是它给 `gpt-image-2` 用的提示词：

> `Video game key art, low-poly 3D render style, moody nighttime scene: a cute low-poly raccoon wearing a tiny black burglar mask sneaking on its hind legs carrying a glowing gold coin, next to a tipped-over metal trash can, suburban house with warm glowing windows in the background, deep blue night, full moon, fireflies, cinematic rim lighting, charming heist caper mood. No text, no words, no logos.`

（中文：游戏主视觉，低多边形 3D 渲染风格，阴郁的夜景：一只戴着小小黑色强盗面罩的可爱低多边形浣熊，用后腿蹑手蹑脚地走，叼着一枚发光的金币，旁边是一个被掀翻的金属垃圾桶，背景是亮着暖光窗户的郊区房屋，深蓝夜空、满月、萤火虫、电影感轮廓光，迷人的劫案片氛围。不要文字、不要单词、不要 logo。）

生成的图片（Claude [觉得它「美极了」](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-16-42-176Z)）——不过我注意到，它在桌面端显示时会被裁掉，只剩上面三分之一，浣熊都不见了！

![一只拿着金币的多边形浣熊，旁边是翻倒的垃圾桶，背景是房子和月亮。](https://static.simonwillison.net/static/2026/raccoon-heist-title.jpeg)

然后是我最喜欢的一处改动：它[加了一条狗](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-23-00-850Z)：

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

接着用 Playwright 对它做了一[轮测试](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-09-230Z)，包括[另一张截图](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-24-33-559Z)。

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

![游戏截图。第 3 夜，浣熊在画面中间和狗撞在一起。一条消息显示「Busted! The Guard shooed you off!（被抓了！守卫把你赶走了！）」屏幕边缘泛着红色。](https://static.simonwillison.net/static/2026/shot-dog.png)

它又做了几处微调，然后[宣布完工](https://simonw.github.io/raccoon-heist/transcript/page-001.html#msg-2026-08-05T15-29-13-245Z)：

> **Raccoon Heist 已构建、测试并推送** —— 分支 `claude/3d-raccoon-heist-game-50n293` 上 7 次提交，全部通过桌面、竖屏手机、横屏手机视口下的 Playwright 自动化通关验证。
>
> **游戏内容：** 你是一只戴着面罩的浣熊，从团队的垃圾箱藏身点溜出来，进入一条月光下的尽端路（cul-de-sac）。捡起金币、宝石、戒指、甜甜圈和鱼（它们会可见地叠在你的背上并拖慢你的速度），然后在黎明前蹒跚回家把它们存进仓库。每过一夜，目标和热度都会提高：第 1 夜有一个扫着手电筒的守卫，第 2 夜有两个，第 3 夜加了一条完全无视视线的嗅觉追踪猎犬。一辆警车用车灯扫过街道，房主会随机从窗户探出头来，海鸥会时不时俯冲轰炸你没收好的战利品，披萨片会触发 6 秒的速度狂热（FRENZY），还有一台稀有的金色电视，如果你能把它拖回家，就值 120 分。胜利段位：TRASH PANDA ⭐（垃圾熊猫）→ CAT BURGLAR ⭐⭐（入室窃贼）→ MASTER OF DISGUISE ⭐⭐⭐（伪装大师），最佳记录保存在 localStorage 里。
>
> **实现方式：** 内置 Three.js（无 CDN）、程序化生成的低多边形角色，以及一段程序化生成的 WebAudio 配乐（鬼祟的行走贝斯爵士乐加全部音效——零音频文件）。全部七张地面/墙壁贴图和标题画面主视觉都由 gpt-image-2 生成并作为静态资源提交，所以部署后的游戏不做任何 API 调用。移动端有动态触控摇杆（出现在你手指触碰的位置）外加 DASH 冲刺按钮；桌面端用 WASD/方向键和空格。
>
> **测试抓到了两个值得一提的真实 bug：** canvas 在任何真机上都会以 2 倍尺寸渲染（一个 `cssText` 赋值把 Three.js 的内联尺寸设置清掉了——桌面端 DPR-1 测试完全掩盖了这个问题）；胜利画面的星级评分 div 继承了标题画面的全屏 `.stars` CSS，悄悄吞掉了「下一夜」按钮的每次点击。两个都已修复并做了回归测试；拾取、存款、追逐/被抓、黎明、夜晚推进、失败/重试流程也都测过了。
>
> `notes.md` 里有完整的构建日志。游戏已经部署在该分支上——只需托管仓库根目录并打开 `index.html`。

### 这游戏好玩吗？

它是一个令人印象深刻的起点，但不是一款_好_游戏。

你操控浣熊在院子里移动、收集物品——甜甜圈、鱼、金币、宝石——同时躲避打着手电筒的守卫，后期关卡还要躲一条狗。你的携带容量有限，装满后得先去垃圾箱卸货。捡起一片披萨会获得临时加速。

完全没有团队机制——垃圾箱旁边有两只静止不动的浣熊，但它们纯粹是装饰。

随着关卡推进，难度会稍微上升——第 3 关引入的狗是最有意思的新机制——但这游戏非常、非常容易通关。它也挺无聊：每个夜晚时长固定，你可以把物品全捡完，然后只能干等着天亮。

我对实现本身印象深刻。它是完整的 3D，有垃圾桶，手电筒的光照锥很好玩，视觉风格也算自洽。它能在移动端运行。音乐（按 Claude 的说法是「程序化生成的 WebAudio 配乐（鬼祟的行走贝斯爵士乐加全部音效——零音频文件）」）很简单，但感觉刚刚好。

作为一款完成的游戏项目，它平庸。但作为从单条提示词出发的起点，我觉得它非常令人印象深刻。

我已经用氛围编码（vibe coding）做过不少游戏了。从玩法角度看，它们全都让人大失所望——事实证明，设计出_好玩_的游戏依然是人类独有的天赋，而且需要的技巧和经验，远比 Claude 或我能带来的多得多。

话虽如此，我强烈推荐把游戏开发小项目当作探索 agent 能力的方式。它好玩、低风险，适合尝试新东西。如果你坚持得够久，说不定还能做出点值得一玩的东西！

**2026 年 8 月 7 日更新：** 我把同样的提示词丢给了运行 GPT-5.6 Sol Ultra 的 OpenAI Codex Desktop，得到了[明显更好的结果](https://simonwillison.net/2026/Aug/7/moonlight-mayhem/)——GPT-5.6 Sol 抓住了「一队浣熊去干一票」的重点，做了一款你必须在一座博物馆里救出两位队友、然后叠罗汉偷走金沙丁鱼（Golden Sardine）的游戏。
