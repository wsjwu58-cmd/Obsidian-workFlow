---
created: 2026-08-17
updated: 2026-08-17
title: 我给 Claude Code 立了一份 AGENTS.md 契约，从此不再当保姆
sourceUrl: https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m
sourceAuthor: DaymondHyper（dev.to）
translatedAt: 2026-08-17
sources: [references/articles.md 待处理队列]
tags: [Claude Code, AGENTS.md, 提示词工程, 智能体工作流, 工程纪律, type/翻译]
---

# 我给 Claude Code 立了一份 AGENTS.md 契约，从此不再当保姆

> dev.to：DaymondHyper（2026-08-09 发布）| 原文：https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m

Claude Code 太听话了，而这正是问题所在。当没有任何东西告诉它「工程纪律长什么样」时，它就会自己编一个看起来合理的版本：把类型优雅地降级成 `any`、写只断言实现细节的测试（这样无论代码好坏都能通过）、用静默的 `catch (e) {}` 吞掉你本应听到的失败。我花了几个月，一次一次地手动纠正这些编辑。最终的解法不是更好的提示词，而是一份契约。

## 问题是它太听话了（The problem is that it listens）

Claude Code 是我用过的最听话的指令执行者，而这正是问题所在。给它一个含糊的需求，它不会卡住，而是会猜。它选择最快的那条看似合理的路径，而这条路径独自走下去通常是小小的降级：这里把类型放宽成 `any`，那里写一个只断言代码现状的测试，再来一个空的 catch 块悄悄吞掉本该大声报错的异常。

这一切都不是恶意。这是当没人告诉它「完成是什么样」时，一个非常积极、非常快的助手会做的事。你也不可能一直站在旁边纠正它的每一个回复——花钱雇一个需要像实习生一样盯着的 agent 毫无意义。真正的问题在于：如何在「看似合理」与「正确」之间划出界限，并让这条界限在每一个任务、每一个会话、每一个工具上都持续生效。

## AGENTS.md 是契约，不是愿望清单（AGENTS.md is a contract, not a wish list）

我和所有人一样，从 `CLAUDE.md` 开始——一份描述项目的散文式文件。它有帮助，但读起来像文档。Claude Code 扫一眼，吸收其中的「氛围」，一旦遇到没有覆盖到的情况，就又回到它自己编造「貌似合理工程」的老路上。

转折发生在我把所有内容搬进 `AGENTS.md`、并且不再像给同事留便条那样写作的时候。Claude Code 会先读 `AGENTS.md`，其他 agent 也会尊重它，于是纪律随仓库一起流动，而不是寄居在某个工具的提示词里。更重要的是，我开始像写契约一样写它。愿望清单会说「写好测试」；契约则会规定「好」是什么意思、测试写得不好会怎样、以及工作持续失败时该怎么办。具体、编号、可检验。这个差别占了收益的大头。

## 契约骨架（The contract skeleton）

我的契约有 8 条基线规则、一架 6 级验证阶梯，外加一套失败协议。任何变更都要爬完这架阶梯才算完成，其中第 1 到 3 级没有商量余地。下面是它的形状（精简到真正起作用的部分）：

```markdown
# AGENTS.md

## Baseline Rules

1. Never widen a type to `any` to make a check pass. Fix the check.
2. A test that cannot fail is not a test. Delete it and write one that can.
3. No silent `catch (e) {}`. Handle it, rethrow it, or log it with context.
4. Prefer the codebase's existing patterns over new abstractions.
5. A change that compiles but is not verified does not exist.
6. Public APIs get tests before they get callers.
7. If a rule conflicts with a deadline, the deadline loses.
8. When in doubt, ask. Guessing is the expensive path.

## Verification Ladder

Rungs 1-3 are mandatory for every change:

1. Does it compile?
2. Does the changed behavior actually work?
3. Does it break anything adjacent?
4. Does it follow this codebase's conventions?
5. Does it hold at the boundaries: empty, null, huge, concurrent?
6. Is the result observable in production?

## Failure Protocol

- First failure: fix it and re-verify. Normal day.
- Second failure: stop and re-derive. Your mental model of the system is wrong.
- Third failure: stop, revert to last known good, and document what happened.
```

## 失败协议（The failure protocol）

这是人们问得最多的部分，也是最省时间的部分。Claude Code 迭代很快，也会乐此不疲地在错误假设上烧 token。它会重读同一个文件、换一种方式尝试同一个修复，然后满怀信心地告诉你为什么这次一定行。如果没有刹车踏板，那就是把钱和耐心扔进无底洞。

三次尝试，这就是整套协议。第一次失败：修复并重新验证，平常的一天。第二次失败：停下来重新推导，因为到这时出错的已经不是打字，而是模型对系统的心理模型。第三次失败：停下，回退到最近可用版本，并记录发生了什么。回退很重要：它让系统回到已知的地面，而不是更糟的地面；记录则意味着下一个会话从教训开始，而不是重复它。

「三次即止」这一条规则，比文件里其他任何内容都更帮我避免了浪费。在错误假设上死磕是最昂贵的失败模式，而这套协议让它在结构上变得不可能。

## 工作流各归各文件（Workflows get their own files）

基线规则是底线，但项目里的大多数任务都有固定的形态：功能开发、缺陷修复、代码评审。这些形态不是契约，而是流程——按顺序排列、关卡之间的步骤。所以它们放在独立的工作流文件里，任务开始时，agent 会被指到对应的那个文件。

分开存放很重要，因为工作流是顺序的，而契约不是。工作流如果埋在系统提示词里，会被扫一眼略过；放在自己的文件里，就会被照做。当 Claude Code 开始做功能时，它会打开功能工作流，而那个文件的第一个要求是：用两句话说明这次变更的契约——它做什么、刻意不做什么。单单这一步就消除了惊人程度的漂移。

```markdown
# Feature Workflow

1. State the contract for this feature in two sentences: what it does, what it deliberately doesn't.
2. Find the closest existing pattern in this codebase and follow it.
3. Write the behavior-proving test first. Watch it fail.
4. Implement the smallest change that makes it pass.
5. Climb the verification ladder. Rungs 1-3 are mandatory.
6. If the design fights you at rungs 4-5, stop and re-derive before writing more code.
7. Report back: what you changed, what you tested, what you left untested.
```

## 验证行为，而非实现（Tests that prove behavior, not implementation）

验证阶梯的第 2 级才是纪律真正落地的地方，因为这里是 Claude Code 默认直觉的葬身之地。如果没人管，它会写断言实现细节的测试——这些测试永远不会失败，因为它们只检查代码能跑，不检查代码对不对。

```typescript
// Asserts the mechanism, not the behavior. Passes even when the feature is broken.
test("addItem stores the item", () => {
  const cart = new Cart();
  cart.addItem({ name: "sword", price: 45 });
  expect(cart.items.length).toBe(1); // still passes if the total is never charged
});

// Asserts the behavior. Fails when the feature is broken.
test("addItem charges the full price of what was added", () => {
  const cart = new Cart();
  cart.addItem({ name: "sword", price: 45 });
  cart.addItem({ name: "shield", price: 30 });
  expect(cart.total()).toBe(75);
});
```

我用一条规则来评判任何测试：删掉实现，测试应当失败。如果它不失败，那它从来就没在测任何东西。行为验证测试是那种「有人弄坏功能时就会挂掉」的测试，也只有这类测试才值得花钱让 Claude Code 去写。

这一切并不会让 Claude Code 变得神奇。还是同一个模型、同样的推理。变化在于：它读到的第一个文件现在把纪律描述为流程而不是偏好；流程说停，它就停。你仍然要评审它的工作，只是少得多。

免费样例：完整 AGENTS.md 契约，外加 TypeScript、安全与测试规则：https://github.com/DaymondHyper/agentforge

完整包：功能、缺陷修复与评审工作流，模板，以及 24 个规则文件，一次性 $29：https://dedyclan.gumroad.com/l/agentforge

仅限发布周：结账时输入 LAUNCH50，该包半价。
