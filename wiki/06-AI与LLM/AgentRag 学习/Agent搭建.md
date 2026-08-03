<h2>Agent 搭建</h2><h2>一、AI Agent 核心概念</h2><h3>1.1 Agent 的历史脉络</h3><p>AI Agent 并不是大语言模型的专属概念。它的思想根源可以追溯到 20 世纪 50 年代的符号主义 AI：</p><figure class="table"><table><thead><tr><th>时期</th><th>范式</th><th>核心思想</th><th>代表</th></tr></thead><tbody><tr><td>1950s-1980s</td><td>符号推理 Agent</td><td>基于逻辑和知识库进行符号操作</td><td>专家系统、SOAR</td></tr><tr><td>1980s-2000s</td><td>反应式 Agent</td><td>基于感知-动作规则对环境做出反应</td><td>行为树、有限状态机</td></tr><tr><td>1990s-2010s</td><td>BDI Agent</td><td>基于信念(Belief)-欲望(Desire)-意图(Intention)模型推理</td><td>PRS、Jason</td></tr><tr><td>2010s</td><td>强化学习 Agent</td><td>通过环境交互和奖励信号学习策略</td><td>DQN、AlphaGo</td></tr><tr><td>2022-至今</td><td>LLM Agent</td><td>以语言模型为核心推理引擎，通过自然语言与环境交互</td><td>AutoGPT、LangGraph Agent</td></tr></tbody></table></figure><p><strong>关键转折</strong>：LLM Agent 的核心突破在于用自然语言作为"思维语言"——Agent 的推理过程不再需要形式逻辑或结构化规则，而是利用了 LLM 在预训练中习得的常识推理能力。</p><h3>1.2 什么是 LLM Agent</h3><p>LLM Agent 是一个以语言模型为核心推理引擎、通过工具调用与环境交互的智能系统。它与传统 Chain 的本质区别在于：</p><figure class="table"><table><thead><tr><th>维度</th><th>Chain</th><th>Agent</th></tr></thead><tbody><tr><td><strong>控制流</strong></td><td>预定义、确定性</td><td>动态、由 LLM 自主决定</td></tr><tr><td><strong>工具使用</strong></td><td>无或固定</td><td>灵活选择、动态调用</td></tr><tr><td><strong>决策能力</strong></td><td>无</td><td>每步都需做出决策</td></tr><tr><td><strong>适应性</strong></td><td>无</td><td>可根据中间结果调整策略</td></tr><tr><td><strong>复杂度</strong></td><td>低</td><td>高（需要循环、路由、错误处理）</td></tr></tbody></table></figure><h3>1.3 Agent 的数学定义</h3><p>可以将 Agent 形式化为一个函数：</p><pre><code class="language-text-x-trilium-auto">Agent(input, state_t, tools) → (action, state_{t+1})

其中：
  action ∈ {FINAL_ANSWER(text), TOOL_CALL(name, params)}
  state_t 为当前状态（消息历史、中间结果等）</code></pre><p>Agent 在每一步中自主决定：</p><ol><li data-list-item-id="efef4498dab40d5c1489028512879daff">是否已经有足够信息给出最终答案（<code spellcheck="false">FINAL_ANSWER</code>）</li><li data-list-item-id="e9ee41695e1b7f80a87989ed75264ed13">还是需要调用某个工具获取更多信息（<code spellcheck="false">TOOL_CALL</code>）</li></ol><p>这个决策-执行循环持续进行，直到 Agent 决定终止。</p><hr><h2>二、ReAct 模式</h2><h3>2.1 ReAct 的历史与理论基础</h3><p>ReAct（Reasoning + Acting）由 Yao 等人于 2022 年在《ReAct: Synergizing Reasoning and Acting in Language Models》论文中提出。这篇论文的关键贡献是证明了<strong>推理和行动可以相互增强</strong>：</p><ul><li data-list-item-id="e9319fb567be059037b3699d2b4882ab0"><strong>推理指导行动</strong>：通过思考"我需要知道什么"来决定调用哪个工具</li><li data-list-item-id="e97f3f09b0362fa01a780d630678b0708"><strong>行动反馈推理</strong>：工具返回的结果更新了状态，促使下一轮推理更准确</li></ul><p>论文的实验表明，ReAct 在 HotpotQA（多跳推理）和 Fever（事实验证）任务上显著优于纯 CoT（Chain-of-Thought）和纯 Act-only 方法，同时减少了幻觉——因为外部工具提供了可验证的事实依据。</p><h3>2.2 ReAct 循环的深层原理</h3><pre><code class="language-text-x-trilium-auto">Thought → Action → Observation → Thought → Action → ... → Final Answer</code></pre><p><strong>为什么这个循环有效？</strong></p><p>关键在于 LLM 的"上下文学习"（In-Context Learning）能力。当 LLM 在自己的上下文中看到之前的 Thought-Action-Observation 序列后，它能：</p><ol><li data-list-item-id="ef8fc98a35f87036e6e350d5699765b67"><strong>从观察中提取关键信息</strong>：解析工具返回结果中有用的部分</li><li data-list-item-id="e89ded993870afe2c998375815e716855"><strong>检测信息缺口</strong>：判断当前信息是否足以回答问题</li><li data-list-item-id="e67d85e1953a78fe4b2a8b2e7fa0ea624"><strong>调整搜索方向</strong>：如果当前工具没返回有用信息，换一个工具或参数</li></ol><p>这本质上是将 LLM 作为一个<strong>隐式的世界模型</strong>来使用——它通过自然语言在上下文中维护了对任务状态的认知。</p><h3>2.3 ReAct 循环流程序列图</h3><pre><code class="language-text-x-trilium-auto">迭代 1:
  [用户] "北京今天多少度？"
  [Agent Thought] 我需要查询北京的实时天气
  [Agent Action] → get_weather(city="北京")
  [Observation] "北京 25°C，晴"
  
迭代 2:
  [Agent Thought] 已获得天气数据，可以给出答案
  [Agent Action] → FINAL_ANSWER: "北京今天 25°C，晴天"</code></pre><h3>2.4 LangGraph 实现 ReAct Agent</h3><h4>方式一：使用 create_agent（高层 API）</h4><pre><code class="language-text-x-python">from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4o",
    tools=[search_tool, calculator_tool, weather_tool],
    prompt="你是一个有用的助手，可以使用工具来回答问题。",
    checkpointer=MemorySaver(),
)
result = agent.invoke({"messages": [{"role": "user", "content": "北京今天多少度？"}]})</code></pre><h4>方式二：手动构建 StateGraph（深入理解底层机制）</h4><pre><code class="language-text-x-python">from langgraph.graph import StateGraph, START, END
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model
from typing import Literal, Annotated, TypedDict
import operator

# 1. 定义工具
from langchain.tools import tool

@tool
def add(a: int, b: int) -&gt; int:
    """Add two numbers"""
    return a + b

@tool
def multiply(a: int, b: int) -&gt; int:
    """Multiply two numbers"""
    return a * b

tools = [add, multiply]
tools_by_name = {t.name: t for t in tools}

# 2. 初始化模型并绑定工具
# bind_tools 将工具定义转为 JSON Schema 注入到 system message 中
model = init_chat_model("gpt-4o", temperature=0)
model_with_tools = model.bind_tools(tools)

# 3. 定义状态
# 使用 Annotated + operator.add 确保消息列表在节点间自动追加而非覆盖
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# 4. LLM 调用节点 —— Agent 的"思考"环节
def llm_call(state: AgentState):
    response = model_with_tools.invoke(
        [SystemMessage(content="你是一个数学助手。")] + state["messages"]
    )
    return {"messages": [response]}

# 5. 工具执行节点 —— Agent 的"行动"环节
def tool_node(state: AgentState):
    last_message = state["messages"][-1]
    results = []
    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        results.append(ToolMessage(
            content=str(observation),
            tool_call_id=tool_call["id"]
        ))
    return {"messages": results}

# 6. 路由判断 —— 决定继续循环还是终止
def should_continue(state: AgentState) -&gt; Literal["tool_node", END]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END

# 7. 构建有向循环图
builder = StateGraph(AgentState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, {
    "tool_node": "tool_node", END: END
})
builder.add_edge("tool_node", "llm_call")  # 工具结果返回 LLM

agent = builder.compile()

# 8. 调用
result = agent.invoke(
    {"messages": [HumanMessage(content="3乘以4再加5等于多少？")]}
)
for m in result["messages"]:
    m.pretty_print()</code></pre><h3>2.5 工具调用（Tool Calling）的底层机制</h3><p><strong>bind_tools 到底做了什么？</strong></p><p><code spellcheck="false">model.bind_tools(tools)</code> 将每个工具的定义转换为 JSON Schema 格式，注入到 API 请求的 <code spellcheck="false">tools</code> 参数中：</p><pre><code class="language-text-x-trilium-auto">{
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "获取指定城市的天气信息",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {"type": "string", "description": "城市名称"}
        },
        "required": ["city"]
      }
    }
  }]
}</code></pre><p>当 LLM 决定调用工具时，它的输出不是普通文本，而是结构化的 tool_call 对象：</p><pre><code class="language-text-x-trilium-auto">{
  "role": "assistant",
  "content": null,
  "tool_calls": [{
    "id": "call_abc123",
    "type": "function",
    "function": {
      "name": "get_weather",
      "arguments": "{\"city\": \"北京\"}"
    }
  }]
}</code></pre><p><strong>LLM 如何学会调用工具？</strong> 模型在微调阶段被训练了"在看到特定工具描述后输出结构化调用"的能力。这不是 prompt engineering 的结果，而是模型参数中内化的功能。</p><h3>2.6 ReAct 的优缺点</h3><figure class="table"><table><thead><tr><th>优点</th><th>缺点</th></tr></thead><tbody><tr><td>灵活适应不确定任务</td><td>可能进入死循环（无限调用同一工具）</td></tr><tr><td>推理过程完全可解释（可在 UI 展示 Thought）</td><td>复杂任务效率低（每步都需调用 LLM）</td></tr><tr><td>适合交互式探索任务</td><td>缺乏全局规划（只考虑下一步，不考虑全局最优）</td></tr><tr><td>工具使用直观</td><td>Token 消耗大（每轮循环都在积累上下文）</td></tr><tr><td>出错后可以自我纠正</td><td>对长任务容易迷失方向（上下文漂移）</td></tr></tbody></table></figure><hr><h2>三、Plan-and-Execute 模式</h2><h3>3.1 理论基础：分层任务分解</h3><p>Plan-and-Execute 模式借鉴了 AI 规划理论中的 **HTN（Hierarchical Task Network）**思想——将高层目标逐步分解为可直接执行的原语操作。与 ReAct 的"走一步看一步"不同，Plan-Execute 先做全局规划再执行。</p><pre><code class="language-text-x-trilium-auto">用户任务 → Planner（全局分解为步骤序列）→ Executor（逐步执行）→ 结果汇总</code></pre><p><strong>Plan-Execute vs ReAct 的本质区别</strong>：</p><figure class="table"><table><thead><tr><th>维度</th><th>ReAct</th><th>Plan-Execute</th></tr></thead><tbody><tr><td><strong>规划粒度</strong></td><td>每步规划下一步</td><td>一次性规划全部</td></tr><tr><td><strong>适用任务</strong></td><td>探索式（{不确定性高}）</td><td>确定性（步骤可预知）</td></tr><tr><td><strong>容错性</strong></td><td>高（每步可纠偏）</td><td>低（依赖计划质量）</td></tr><tr><td><strong>效率</strong></td><td>低（频繁 LLM 调用）</td><td>高（规划一次，执行 N 步）</td></tr><tr><td><strong>可中断性</strong></td><td>差</td><td>好（可在步骤间中断）</td></tr></tbody></table></figure><h3>3.2 实现示例</h3><pre><code class="language-text-x-python">from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
import operator
import json

class PlanStep(TypedDict):
    step: int
    description: str
    tool: str
    status: str  # pending, in_progress, completed

class PlanExecuteState(TypedDict):
    task: str
    plan: list[PlanStep]
    current_step: int
    results: Annotated[list, operator.add]
    messages: list

def planner(state: PlanExecuteState):
    """全局规划：将任务分解为步骤序列"""
    prompt = f"""你是一个任务规划专家。将以下任务拆解为可独立执行的步骤。
    每个步骤必须明确使用的工具。

    任务: {state["task"]}

    以 JSON 格式返回：{{"steps": [{{"step": 1, "description": "...", "tool": "..."}}]}}"""
    
    response = llm.invoke(prompt)
    plan = json.loads(response.content)["steps"]
    return {"plan": plan, "current_step": 0, "results": []}

def executor(state: PlanExecuteState):
    """逐步执行：每次执行当前步骤"""
    step = state["plan"][state["current_step"]]
    result = execute_step(step, state["results"])
    step["status"] = "completed"
    return {
        "results": [result],
        "current_step": state["current_step"] + 1
    }

def summarizer(state: PlanExecuteState):
    """汇总所有步骤结果，生成最终输出"""
    summary_prompt = f"汇总以下步骤结果：\n{state['results']}\n生成最终回答。"
    response = llm.invoke(summary_prompt)
    return {"messages": [response]}

def should_execute(state: PlanExecuteState) -&gt; Literal["executor", "summarizer"]:
    if state["current_step"] &lt; len(state["plan"]):
        return "executor"
    return "summarizer"

builder = StateGraph(PlanExecuteState)
builder.add_node("planner", planner)
builder.add_node("executor", executor)
builder.add_node("summarizer", summarizer)
builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_conditional_edges("executor", should_execute, {
    "executor": "executor", "summarizer": "summarizer"
})
builder.add_edge("summarizer", END)

plan_execute_agent = builder.compile()</code></pre><h3>3.3 Replan（重新规划）</h3><p>纯 Plan-Execute 的重大缺陷是：如果某步执行失败，后续步骤可能全部无效。Replan 变体在执行过程中监控结果质量，必要时重新触发规划器生成新计划。</p><hr><h2>四、其他重要 Agent 范式</h2><h3>4.1 Self-Refine（自我反思）</h3><p><strong>理论基础</strong>：LLM 具有"自我批评"能力——给模型机会审视自己的输出，通常能发现并修正错误。</p><pre><code class="language-text-x-trilium-auto">生成回答 → 自我检查（反馈: "这段回答不完整，缺少...") → 改进回答 → ... → 最终回答</code></pre><p><strong>适用场景</strong>：写作、代码生成、翻译等可以迭代优化的任务。</p><p><strong>关键论文</strong>：Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback" (2023)</p><h3>4.2 Tree-of-Thoughts（思维树）</h3><p><strong>理论基础</strong>：将推理过程建模为树状搜索，使用 BFS/DFS 探索多条推理路径。每步生成多个候选"下一步思路"，LLM 对每个候选评分，选择最有前景的路径继续探索。</p><p>适用于需要创造性思维或"灵光一现"的任务——包括数学证明、创意写作构思、谜题解决。</p><p><strong>关键论文</strong>：Yao et al., "Tree of Thoughts: Deliberate Problem Solving with LLMs" (2023)</p><h3>4.3 Reflexion</h3><p>Reflexion 在 ReAct 基础上增加了"长期记忆"机制——将失败的经验（为什么上次做错了）存储为文本记忆，在后续类似任务中注入到 prompt 中以避免重复犯同样的错误。</p><h3>4.4 范式对比总结</h3><figure class="table"><table><thead><tr><th>范式</th><th>推理方式</th><th>执行方式</th><th>记忆</th><th>最佳场景</th></tr></thead><tbody><tr><td><strong>ReAct</strong></td><td>逐步推理</td><td>逐步执行</td><td>上下文内</td><td>探索式交互</td></tr><tr><td><strong>Plan-Execute</strong></td><td>全局规划</td><td>按计划执行</td><td>无</td><td>多步骤确定性任务</td></tr><tr><td><strong>Self-Refine</strong></td><td>迭代反馈</td><td>迭代改进</td><td>无</td><td>内容生成</td></tr><tr><td><strong>ToT</strong></td><td>树状搜索</td><td>最佳路径执行</td><td>无</td><td>创造性推理</td></tr><tr><td><strong>Reflexion</strong></td><td>逐步+反思</td><td>逐步执行</td><td>长期记忆</td><td>需要经验的重复任务</td></tr></tbody></table></figure><hr><h2>五、LangGraph 深度解析</h2><h3>5.1 设计哲学</h3><p>LangGraph 的核心抽象是基于<strong>有向图</strong>的计算模型。与传统的 DAG 流水线不同，LangGraph 支持循环边，使其天然适合 Agent 的循环推理模式。</p><p><strong>为什么选择图而非链？</strong></p><p>Chain（如 LangChain 的 LCEL）是线性的：A → B → C → D。它适合确定性流水线（如 RAG），但无法表达"如果 A 产生 X 去 B，产生 Y 去 C，然后都回到 A"的循环逻辑。Agent 的核心特征是循环决策，这恰好是图模型的优势。</p><h3>5.2 核心概念</h3><figure class="table"><table><thead><tr><th>概念</th><th>类型</th><th>说明</th></tr></thead><tbody><tr><td><strong>StateGraph</strong></td><td>容器</td><td>有状态图，定义 Agent 的工作流拓扑结构</td></tr><tr><td><strong>Node</strong></td><td>节点</td><td>图中的执行单元，接收 State 返回 State 的更新</td></tr><tr><td><strong>Edge</strong></td><td>边</td><td>确定性的数据流路径（A 之后永远是 B）</td></tr><tr><td><strong>Conditional Edge</strong></td><td>边</td><td>分支路由（A 之后根据条件去 B 或 C 或 D）</td></tr><tr><td><strong>State</strong></td><td>数据</td><td>图的状态对象，通过 Reducer 函数在各节点间传递和合并</td></tr><tr><td><strong>Checkpointer</strong></td><td>持久化</td><td>在每个 Superstep 后保存状态快照</td></tr><tr><td><strong>Store</strong></td><td>持久化</td><td>长期记忆存储（跨会话、跨线程）</td></tr><tr><td><strong>Superstep</strong></td><td>执行概念</td><td>一次从当前节点到下一个节点（或 END）的执行为一个 Superstep</td></tr></tbody></table></figure><h3>5.3 持久执行（Durable Execution）</h3><p>LangGraph 的持久执行机制是其与传统工作流引擎的关键区别：</p><pre><code class="language-text-x-trilium-auto">节点A 执行 → 保存检查点到 Checkpointer
节点B 执行 → 保存检查点到 Checkpointer
节点B 中断（崩溃/人工暂停）
--- 恢复后 ---
从节点B 的检查点恢复 → 继续执行节点C</code></pre><p><strong>三种持久化模式</strong>：</p><figure class="table"><table><thead><tr><th>模式</th><th>行为</th><th>适用场景</th></tr></thead><tbody><tr><td><code spellcheck="false">async</code>（默认）</td><td>后台异步写检查点，不阻塞执行</td><td>高吞吐，允许少量数据丢失</td></tr><tr><td><code spellcheck="false">sync</code></td><td>同步写检查点，阻塞执行直到持久化完成</td><td>金融等不允许任何丢失的场景</td></tr><tr><td><code spellcheck="false">exit</code></td><td>仅在图完全结束时写一次检查点</td><td>不需要中间恢复的场景</td></tr></tbody></table></figure><h3>5.4 状态设计原理</h3><pre><code class="language-text-x-python">from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
import operator

class AgentState(TypedDict):
    # 使用 add_messages reducer：新消息追加到列表末尾
    messages: Annotated[list, add_messages]
    
    # 使用 operator.add reducer：列表合并
    intermediate_steps: Annotated[list, operator.add]
    
    # 无 Annotated = 默认覆盖行为：每次节点返回都会覆盖
    tool_call_count: int
    phase: str</code></pre><p><strong>Reducer 机制</strong>是 LangGraph 状态管理的关键创新。每个字段可以定义独立的数据合并策略：</p><ul><li data-list-item-id="e084703fc6e84c355d226f61ea4a7b3aa"><code spellcheck="false">Annotated[list, add_messages]</code> → 新消息<strong>追加</strong></li><li data-list-item-id="e33146633a569c22841155ef377c113d5"><code spellcheck="false">Annotated[list, operator.add]</code> → 两个列表<strong>拼接</strong></li><li data-list-item-id="e54fc3a48a0897f351f996dadf80c6104">无 Annotated → <strong>覆盖</strong>（新值替换旧值）</li></ul><h3>5.5 节点粒度设计的权衡</h3><pre><code class="language-text-x-trilium-auto">粗粒度节点（合并多个操作）:
  优点：代码简洁，检查点少
  缺点：失败后重跑更多工作，不透明

细粒度节点（每个操作单独节点）:
  优点：失败后重跑少，可观测性高，可独立配置重试策略
  缺点：图结构更复杂，检查点更多</code></pre><p><strong>推荐原则</strong>：对外部服务调用（API、数据库）、LLM 调用、关键决策点使用独立节点。</p><h3>5.6 容错与重试机制</h3><pre><code class="language-text-x-python">from langgraph.errors import NodeError
from langgraph.types import Command, RetryPolicy
from langgraph.graph import StateGraph, START

class State(TypedDict):
    status: str

def charge_payment(state: State) -&gt; State:
    raise RuntimeError("payment timeout")

def payment_error_handler(state: State, error: NodeError) -&gt; Command:
    """Saga 补偿模式：支付失败后取消预留"""
    return Command(
        update={"status": f"compensated: {error.error}"},
        goto="rollback",
    )

graph = (
    StateGraph(State)
    .add_node(
        "charge_payment",
        charge_payment,
        retry_policy=RetryPolicy(max_attempts=3, retry_on=ConnectionError),
        error_handler=payment_error_handler,
    )
    .add_node("rollback", rollback_node)
    .add_edge(START, "charge_payment")
    .add_edge("charge_payment", "rollback")
    .compile()
)</code></pre><h3>5.7 时间旅行（Time Travel）</h3><p>LangGraph 支持从历史检查点重放执行——对于调试和"撤销-重做"功能非常有用。</p><pre><code class="language-text-x-python"># 获取检查点历史
history = list(graph.get_state_history(config))

# 找到"写笑话之前"的检查点
before_joke = next(s for s in history if s.next == ("write_joke",))

# 从该点重新执行
replay_result = graph.invoke(None, before_joke.config)</code></pre><h3>5.8 子图与 Agent 组合</h3><pre><code class="language-text-x-python">from langgraph.graph import StateGraph, MessagesState

def create_sub_agent(model, *, name, tools, prompt, checkpointer=None):
    """包装子 Agent 为独立子图，确保命名空间隔离"""
    agent = create_agent(
        model=model, name=name,
        tools=tools, prompt=prompt,
        checkpointer=checkpointer,
    )
    return (
        StateGraph(MessagesState)
        .add_node(name, agent)
        .add_edge("__start__", name)
        .compile()
    )</code></pre><p><strong>命名空间隔离的重要性</strong>：多个子 Agent 在同一个线程中运行时，如果没有命名空间隔离，它们的内部状态（消息历史）会相互污染。每个被 <code spellcheck="false">StateGraph</code> 包装的子 Agent 自动获得独立的检查点命名空间。</p><h3>5.9 流式输出</h3><pre><code class="language-text-x-python"># 消息级流式：每当产生新消息就输出（适合聊天 UI）
for message, metadata in graph.astream(
    input={"messages": [{"role": "user", "content": "你好"}]},
    stream_mode="messages",
):
    print(message.content, end="")

# 值级流式：每个节点执行完毕输出完整状态（适合调试）
for chunk in graph.astream(
    input={"messages": [{"role": "user", "content": "3+5等于多少？"}]},
    stream_mode="values",
):
    print(chunk)</code></pre><h3>5.10 Human-in-the-Loop（人机协作）</h3><pre><code class="language-text-x-python">from langgraph.types import interrupt

def approval_node(state: AgentState):
    """在关键操作前暂停，等待人类审批"""
    action = state["pending_action"]
    approval = interrupt(f"是否确认执行 {action}？(yes/no)")
    if approval.lower() != "yes":
        return {"messages": ["操作已取消"]}
    return execute_action(action)

# 在 approval_node 之前自动暂停
graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["approval_node"]
)</code></pre><hr><h2>六、Agent 开发实践</h2><h3>6.1 Agent vs Chain 决策指南</h3><figure class="table"><table><thead><tr><th>场景</th><th>选择</th><th>原因</th></tr></thead><tbody><tr><td>固定流程</td><td>Chain</td><td>无决策需求，确定性流水线更简单可靠</td></tr><tr><td>多轮交互 + 工具</td><td>Agent</td><td>需要动态决策何时使用哪个工具</td></tr><tr><td>简单文档问答</td><td>Chain (RAG)</td><td>RAG 流程固定，用户意图明确</td></tr><tr><td>复杂多步推理</td><td>Agent</td><td>需要多轮工具调用和信息整合</td></tr><tr><td>需要不确定次数循环</td><td>Agent</td><td>Chain 无法表达循环</td></tr></tbody></table></figure><h3>6.2 Agent 开发最佳实践</h3><ol><li data-list-item-id="e3c9edd8df48f2422073f61ea3bffefb3"><strong>渐进式构建</strong>：先用 Chain 验证核心流程，确认需要动态决策后再升级为 Agent</li><li data-list-item-id="ec5677366fa1a7474cab6cd2cbb0fcae4"><strong>工具描述即接口协议</strong>：LLM 完全依赖工具描述来决策调用，模糊描述 = 错误调用</li><li data-list-item-id="e3355dd32e008895a9846ae92e232dfbf"><strong>循环上限</strong>：设置 <code spellcheck="false">max_iterations=5~10</code>，防止死循环消耗大量 Token</li><li data-list-item-id="e8603dcce65d2f714d8a644159a9e2e12"><strong>完整日志</strong>：记录每一步的 Thought/Action/Observation，方便审计和调试</li><li data-list-item-id="e4cab2a3ac5a94e6cb79ee332af8b51a5"><strong>错误优雅降级</strong>：捕获工具异常，返回有意义的错误信息（而非 traceback）给 LLM</li><li data-list-item-id="eecf313fcd05039dae2efc39c5f52bd31"><strong>流式设计</strong>：实时展示推理过程，提升用户信任感和体验</li><li data-list-item-id="e89590ae63278a897acbda014eb478531"><strong>A/B 测试 System Prompt</strong>：不同的系统指令对 Agent 行为影响巨大</li></ol><h3>6.3 常见问题诊断</h3><figure class="table"><table><thead><tr><th>症状</th><th>可能原因</th><th>治疗方案</th></tr></thead><tbody><tr><td>死循环</td><td>LLM 找不到正确答案，不断试同一工具</td><td>设置 max_iterations，添加"如果三次调用同一工具无进展则换个策略"的Prompt</td></tr><tr><td>工具参数错误</td><td>工具描述不清楚，或参数名歧义</td><td>使用 Pydantic schema + Field(description=...) 明确每个参数</td></tr><tr><td>调用不存在的工具</td><td>幻觉</td><td>在 System Prompt 中明确"你只能使用以下工具"</td></tr><tr><td>过早终止</td><td>LLM 过于"保守"</td><td>Prompt 中添加"如果你不确定，请多调用一次工具确认"</td></tr><tr><td>Token 爆炸</td><td>历史消息过长</td><td>实现滑动窗口或摘要压缩</td></tr><tr><td>多轮后"遗忘"任务</td><td>上下文漂移</td><td>定期重述当前目标（"我们正在尝试解决..."）</td></tr></tbody></table></figure><hr><h2>七、Agent 安全与可控性</h2><h3>7.1 工具沙箱化</h3><p>所有 Agent 调用的工具都应该在受限环境中执行。核心原则是"最小权限原则"：</p><ul><li data-list-item-id="e9803115e1a56b6d720cf8d5f44c812ae">网络工具：限制域名白名单、超时时间</li><li data-list-item-id="e2484909374a4033f219a2a3e966b6ccc">文件工具：限制可访问的目录范围</li><li data-list-item-id="e36f31cf48febd0bd037cd6fa70267376">数据库工具：使用只读账号，限制返回行数</li><li data-list-item-id="eddb79dde07dc0e5e849f14eaa3b587f6">代码执行工具：在 Docker 容器或沙箱中执行</li></ul><h3>7.2 权限分级</h3><pre><code class="language-text-x-trilium-auto">Level 0: 只读工具（搜索、查询、读取）—— 无需确认
Level 1: 非破坏性写入（保存草稿、创建标签）—— 需要告知用户
Level 2: 破坏性操作（删除、发送、付费）—— 需要人类明确确认</code></pre><h3>7.3 Human-in-the-Loop 的三种模式</h3><figure class="table"><table><thead><tr><th>模式</th><th>说明</th><th>适用场景</th></tr></thead><tbody><tr><td><code spellcheck="false">interrupt_before</code></td><td>在指定节点前自动暂停</td><td>高风险操作（如发送邮件前）</td></tr><tr><td><code spellcheck="false">interrupt_after</code></td><td>在指定节点后自动暂停</td><td>审查结果（如生成内容后人工审核）</td></tr><tr><td>动态中断</td><td>程序代码中调用 <code spellcheck="false">interrupt()</code></td><td>根据运行时条件决定是否暂停</td></tr></tbody></table></figure>

## 相关条目
- [[MCP协议与工具调用]]
- [[RAG处理优化]]
- [[多智能体与记忆机制]]
- [[langgraph4j-study-notes-01-core]]
- [[面试]]
