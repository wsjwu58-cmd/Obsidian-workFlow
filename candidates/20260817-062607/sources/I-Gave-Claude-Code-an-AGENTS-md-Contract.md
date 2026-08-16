# I Gave Claude Code an AGENTS.md Contract and Stopped Babysitting It

- **作者：** DaymondHyper（dev.to 用户 daymondhyper）
- **来源：** https://dev.to/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m
- **发布：** 2026-08-09T07:11:55Z（dev.to）
- **标签：** ai / productivity / claude / testing
- **性质：** 博客短文（正文 Markdown 约 7.7KB；讲如何用 AGENTS.md 写「契约」而非「愿望清单」，约束 Claude Code 的工程纪律；文末附付费产品推广）
- **抓取：** 2026-08-17（dev.to API `api.dev.to/api/articles/daymondhyper/i-gave-claude-code-an-agentsmd-contract-and-stopped-babysitting-it-53m` 的 body_markdown，已与页面 HTML 交叉核对一致）

---

Claude Code follows instructions too well, and that's the whole problem. When nothing tells it what engineering discipline looks like, it invents a plausible version: graceful degradation into `any`, tests that assert implementation details so they pass no matter what, silent `catch (e) {}` blocks eating the failures you needed to hear about. I spent months working around this one edit at a time. The fix wasn't a better prompt. It was a contract.

## The problem is that it listens

Claude Code is the best instruction follower I've used, and that's the whole problem. Give it an ambiguous ask and it doesn't stall, it guesses. It picks the fastest plausible path, and on its own that path is usually a small degradation: a type widened to `any` here, a test that only asserts what the code already does there, an empty catch block quietly swallowing the error that should have been loud.

None of this is malice. It's what a very eager, very fast assistant does when nobody has told it what done looks like. And you can't just stand over it and correct every response, there's no point paying for an agent you have to supervise like an intern. The real question is how you draw the line between plausible and correct, and make it stick across every task, every session, every tool.

## AGENTS.md is a contract, not a wish list

I started with CLAUDE.md, like everyone does, a prose file describing the project. It helped, but it read like documentation. Claude Code skimmed it, absorbed the vibes, and when a situation wasn't covered it went right back to inventing plausible engineering.

The shift came when I moved everything into AGENTS.md and stopped writing like I was leaving notes for a colleague. Claude Code reads AGENTS.md first, and other agents respect it too, so the discipline travels with the repo instead of living inside one tool's prompt. More importantly, I started writing it like a contract. A wish list says "write good tests." A contract says what good means, what happens when a test is bad, and what to do when the work keeps failing. Specific, numbered, testable. That difference is most of the win.

## The contract skeleton

Mine has eight baseline rules, a six-rung verification ladder, and a failure protocol. Every change has to climb the ladder before it counts as done, and rungs one through three are non-negotiable. Here's the shape of it, trimmed to the parts that do the actual work:

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

## The failure protocol

This is the part people ask me about most, and it's the part that saves the most time. Claude Code iterates fast and burns tokens happily grinding on a broken hypothesis. It will re-read the same file, try the same fix a different way, and tell you with total confidence why this time it will work. Without a brake pedal, that's money and patience going down a hole.

Three attempts, that's the whole protocol. First failure, fix and re-verify, a normal day. Second failure, stop and re-derive, because by then the model's mental model of the system is wrong, not its typing. Third failure, stop, revert to last known good, and document. The revert matters: it puts the system back on known ground instead of worse ground, and the documentation means the next session starts from the lesson instead of repeating it.

That one rule, stop after three, has saved me more wasted work than anything else in the file. Grinding on a broken hypothesis is the expensive failure mode, and the protocol makes it structurally impossible.

## Workflows get their own files

Baseline rules are the floor, but most tasks in a project follow a shape: feature, bugfix, review. Those shapes aren't contracts, they're procedures, steps in order with gates between them. So they live in separate workflow files, and the agent gets pointed at the right one when a task starts.

Keeping them separate matters because a workflow is sequential and the contract is not. Buried in a system prompt, a workflow gets skimmed. In its own file, it gets followed. When Claude Code starts a feature, it opens the feature workflow, and the first thing that file asks for is a two-sentence contract for the change. That single step kills a surprising amount of drift.

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

## Tests that prove behavior, not implementation

Rung two of the ladder is where the discipline actually lands, because it's where Claude Code's default instincts go to die. Left alone, it writes tests that assert implementation details, tests that can't fail because they only check that the code runs, not that it's right.

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

Here's the rule I use to judge any test: delete the implementation and the test should fail. If it doesn't, it was never testing anything. Behavior-proving tests are the ones that break when someone breaks the feature, and those are the only tests worth paying Claude Code to write.

None of this makes Claude Code magic. It's the same model doing the same reasoning. What changed is that the first file it reads now describes discipline as a procedure instead of a preference, and when the procedure says stop, it stops. You still review its work, just a lot less of it.

Free sample with the full AGENTS.md contract, plus TypeScript, security, and testing rules: https://github.com/DaymondHyper/agentforge

Full pack with feature, bugfix, and review workflows, templates, and 24 rule files for a one-time $29: https://dedyclan.gumroad.com/l/agentforge

Only during launch week: enter LAUNCH50 at checkout and the pack is half price.
