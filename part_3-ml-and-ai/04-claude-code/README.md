# Claude Code

##  Installation and first steps

1. Log into [Claude chat](https://claude.ai/login)

1. Install into WSL using:

    ```bash
    $ curl -fsSL https://claude.ai/install.sh | bash
    Setting up Claude Code...

    ✔ Claude Code successfully installed!

    Version: 2.1.76

    Location: ~/.local/bin/claude


    Next: Run claude --help to get started

    ✅ Installation complete!
    ```

## Claude Code Quickstart

https://code.claude.com/docs/en/overview

`Claude.md` is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists.

| Command | What it does | Example |
| :------ | :----------- | :------ |
| `claude`  | Start interactive mode | `claude` |
| `claude "task"`  | Run a one-time task | `claude "fix the build error"` |
| `claude -p "query"`  | Run one-off query, then exit | `claude -p "explain this function"` |
| `/clear` | Clear conversation history within interactive mode | `/clear` |
| `/help` | Show available commands | `/help` |
| `exit` | Exit Claude Code | `exit` |
| `claude -r` | Resume a previous conversation | `claude -r` |


## How Claude Code works
> https://code.claude.com/docs/en/how-claude-code-works

Claude Code is an agentic assistant that runs in your terminal. It excels at coding, but it can help with anything you can do from the command line: writing docs, running builds, searching files, researching topics, etc.

### The agentic loop

When you give Claude a task it works through three phases:
1. Gather context
1. Take action
1. Verify results

![Agentic loop](pics/001_agentic-loop.svg)

These phases blend together.

Claude uses tools throughout, whether searching files to understand your code, editing to make changes, or running tests to check its work.

The loop adapts to what you ask:
+ a question about the codebase might only need context gathering.
+ a bug fix might require multiple cycles through the agentic loop.

You can interrupt at any point to steer Claude in a different direction, provide additional context, or ask it to try a different approach.

The agentic loop is powered by:
+ **models** that reason.
+ **tools** that act.

#### Models

Claude Code uses Claude models to understand your code and reason about tasks.

Multiple models are available:
+ Sonnet handles most coding tasks well.
+ Opus provides stronger reasoning for complex architectural decisions.

You can switch between models using:

```bash
# when in interactive mode
❯ /model opus
  ⎿  Set model to Opus 4.6
```

Or when using the command line:

```bash
$ claude --model {name}
```

#### Tools

Tools are what make Claude Code agentic. With tools, Claude can act: read your code, edit files, run commands, search the web, and interact with external services. Each *tool use* returns information that feeds back into the loop, informing Claude's next decision.

The built-in tools generally fall into the following categories, each representing a different kind of agency:

| Category | What Claude can do |
| :------- | :----------------- |
| File operations | Read files, edit code, create new files, rename and reorganize. |
| Search | Find files by pattern, search content with regex, explore codebases. |
| Execution | Run shell commands, start servers, run tests, use git. |
| Web | Search the web, fetch documentation, look up error messages. |
| Code intelligence | See type errors and warnings after edits, jump to definitions, find references. |

Claude also has tools for spawning subagents, asking you questions, and other orchestration tasks.

Claude chooses which tools to use based on your prompt and what Claude learns along the way.

For example, when you say "fix the failing tests", Claude will:

1. Run the test suite to see what's failing.
1. Read the error output.
1. Search for the relevant source files.
1. Read those files to understand the code.
1. Edit the files to fix the issue.
1. Run the tests again to verify.

##### Extending the base capabilities

You can extend what Claude knows with:
+ skills
+ connect to external services with MCP
+ automate workflows with hooks
+ offload tasks to subagents

These extensions form a layer on top of the core agentic loop.

### What Claude can access

When you ran `claude` in a directory, Claude Code gains access to:
+ Your project: files in your dir and subdirs, plus files everywhere with your permission.
+ Your terminal: any command you can run from the command line, Claude can too (build tools, git, package managers, system utilities, scripts).
+ Your git state: current branch, uncommitted changes, recent commit history.
+ You `CLAUDE.md`: An md file where you store project-specific instructions, conventions, and cntext that Claude should be aware for every session.
+ Auto memory: learning Claude saves automatically as you work, like project patterns, preferences, etc.
+ Extensions you configure: MCP servers for external services, skills for workflows, subagents for delegated work, and Claude in Chrome for browser interaction.

### Environments and interfaces

#### Execution environments

Claude Code runs in three environments, each with different tradeoffs for where your code executes.

| Environment | Where code runs | Use case |
| :---------- | :-------------- | :------- |
| Local | Your machine | Default. Full access to your file, tools, and environment. |
| Cloud | Anthropic-managed VMs | Offload tasks, work on repos you don't have locally. |
| Remote Control | Your machine, controlled from a browser. | Use the web UI while keeping everything local. |

#### Interfaces

You can access Claude code through:
+ The terminal
+ The desktop app
+ IDE extensions
+ claude.ai/code
+ Remote Control
+ Slack
+ CI/CD pipelines.

The underlying agentic loop is identical.

### Work with sessions

Claude Code saves your conversation locally as you work with it. Each message, tool use, and result is stored, which enables:
+ rewinding sessions
+ resuming sessions
+ forking sessions

It also snapshots the affected files so you can revert if needed.

Sessions are independent though. Each new session starts with a fresh context window, without the conversation history from previous sessions.

However, Claude persists automatically learnings across session using auto memory, and you can add your own persistent instructions in `CLAUDE.md`.

#### Work across branches

Each Claude Code conversation is a session tied to your current directory. When you resume, you only see sessions from that dir.

Claude sees your current branch's files. When you switch branches, Claude sees the new branch's files, but your conversation history stays the same.

Since sessions are tied to directories, you can run parallel Claude sessions by using git worktrees, which create separate directories for individual branches.

#### Resume or fork sessions

You can resume a session with `claude --continue` or `claude --resume`. You'll pick up where you left off using the same sessionID and your full conversation history will be restored. You'll need to re-approve session-scoped permissions.

You can also branch off and try a different approach without affecting the original session using the `claude --continue --fork-session`. This will create a new sessionID, while preserving the conversation history up to that point. Session-scoped permissions won't be inherited either.

![Resume and fork](pics/002_resume_and_fork.svg)

While you can open the same session in multiple terminals, the conversation will become *jumbled*. For parallel work, `--fork-session` is recommended.

#### The context window

Claude's context window holds:
+ your conversation history
+ file contents
+ command outputs
+ `CLAUDEmd` contents
+ loaded skills
+ system instructions

Claude compacts the context automatically, but as the context grows, information from the early stages of the conversation might get lost. You should place persistent rules/information in `CLAUDE.md` to prevent those from being lost.

You can use `/context` to see what's using space.

When context window needs to be compacted, Claude Code clears older tool outputs first, then summarizes the conversation if needed.

To control what's preserved during compaction, you can add a "Compact Instructions" section to `CLAUDE.md` or run the `/compact` command giving some directions:

```bash
/compact focus on the API changes
```

##### Managing the context with skills and subagents

Beyond compaction you can use other features to control what gets into the context:

+ Skills: these load on demand. Claude sees skill descriptions at session start, but the full content is only loaded when a skill is used. For skills you invoke manually, set `disable-model-invocation: true` to keep descriptions out of context until you need them.

+ Subagents: these get their own fresh context, completely separate from your main conversation. When done, they return a summary. Subagents are instrumental in long sessions.

### Stay safe with checkpoints and permissions

+ Checkpoints: let you undo file changes
+ Permissions: control what Claude can do without asking.

#### Undo changes with checkpoints

Every file edit is reversible. You just need to press ESC twice to rewind to a previous state, or ask Claude to undo.

Checkpoints are local to your session, and separate from git. Obviously, actions on remote systems like DBs can't be checkpointed (that's why Claude asks for permission before running commands with external side effects).

#### Control what Claude can do

Press shift+tab to cycle through permission modes:
+ Default: Claude asks before file edits and shell commands.
+ Auto-accept edits: Claude edits files without asking, still asks for commands.
+ Plan mode: Claude used read-only tools only, creating a plan that you can approve before execution.

You can allow specific commands (e.g., `uv run pytest`, `git status`) in `.claude/settings.json`

### Tips for working effectively with Claude Code

#### Ask Claude Code for help

You can ask Claude Code to teach you how to use it asking questions like "how do I set up hooks?" or "what's the best way to structure my CLAUDE.md".

Additionally, there are built-in commands to guide you through the setup:

+ `/init`: walks you through creating a CLAUDE.md for your project.
+ `/agents`: helps you configure custom subagents.
+ `/doctor`: diagnoses common issues with your installation.

#### It's a conversation

Claude Code is conversational. You don't need perfect prompts. With Claude Code it's better to start with something you want and then refine.

#### Interrupt and steer

You can interrupt Claude at any point. If Claude is going down a wrong path, type your correction and press Enter. This will cause Claude to stop and adjust its approach based on your input. You don't have to wait for it to finish or start over.

#### Be specific upfront

Be precise in your initial prompt:
+ reference specific files
+ mention constraints
+ point to example patterns

Example:
> The checkout flow is broken for users with expired cards.<br>Check src/payments/ for the issue, especially token refresh.<br>Write a failing test first, then fix it.

#### Give Claude something to verify against

Claude performs better when it can check its own work. Include test cases, paste screenshots of expected UI, or define the output you want:

Example:
> Implement validate_email. Test cases: "user@example.com" → true, "invalid" → false, "user@.com" → false. Run the tests after.

#### Explore before implementing

For complex problems, separate research from coding. Use plan mode (shift+tab twice) to analyze the codebase first:

> Read src/auth/ and understand how we handle sessions.<br>Then create a plan for adding OAuth support.

Then review the plan, refine it through conversation, then let Claude implement.

This two-phase approach produces better results than jumping straight to code.

#### Delegate, don't dictate

Think of Claude Code as a capable colleague: give context and direction, and let Claude Code figure out the details.

> The checkout flow is broken for users with expired cards.<br>The relevant code is in src/payments/. Can you investigate and fix it?

## Extend Claude Code

This section helps you understand when to use CLAUDE.md, skills, subagents, hooks, MCP, and plugins.

Claude Code combines a model that reasons about your code with built-in tools for file operations, search, execution, and web access. The built-in tools cover most coding tasks.

The extension layer lets you customize what Claude knows, connect it to externsal services, and automate workflows.

### Overview

Claude Code extensions plug into different parts of the agentic loop:

![Claude Code](pics/001_agentic-loop.svg)

+ **`CLAUDE.md`**: adds persistent context Claude sees in every session.
+ **Skills**: add reusable knowledge and invocable workflows.
+ **MCP**: connects Claude to external services and tools
+ **Subagents**: run their own loops in isolated context, returning summaries.
+ **Agent teams**: coordinate multiple independent sessions with shared tasks and peer-to-peer messaging.
+ **Hooks**: run outside the loop entirely as deterministic scripts.
+ **Plugins and marketplaces**: package and distribute these features.

| NOTE: |
| :---- |
| **Skills** are the most flexible extension. A skill is an MD file containing knowledge, workflows, or instructions. You can invoke skills with a command such as `/deploy`, or Claude can load them automatically when relevant. Skills can run in your current conversation or in an isolated context via subagents. |

### Match features to your goal

Features range from:
+ always-on context that Claude sees every session
+ to on-demand capabilities you or Claude can invoke
+ to background automation that runs on specific events

It's important to understand the sweet spot for each extension point:

| Feature | What it does | When to use it | Example |
| :------ | :----------- | :------------- | :------ |
| **CLAUDE.md** | Persistent context loaded in every conversation | Project conventions, like "always do X" rules | "Use uv and not pip for project management"<br>"Run tests before committing" |
| **Skill** | Instructions, knowledge, and workflows Claude can use | Reusable content, reference docs, repeatable tasks | `/deploy` runs your deployment checklist<br>API docs skill with endpoint patterns |
| **Subagent** | Isolated execution context that returns summarized results | Context isolation, parallel tasks, specialized workers | Research tasks that reads many files but returns only key findings |
| **Agent teams** | Coordinate multiple independent Claude Code sessions | Parallel research, new feature development, debugging with competing hypotheses | Spawn reviewers to check security, performance, and tests simultaneously |
| **MCP** | Connect to external services | External data or actions | Query your database<br>Post to Slack<br>Control a browser |
| **Hook** | Deterministic script that runs on events | Predictable automation, no LLM involved | Run Ruff after every file edit |

Plugins are the packaging layer. A plugin bundles skills, hooks, subagents, and MCP servers into a single installatable unit. Plugin skills are namespaced (like `/my-plugin:review`) so multiple plugins can coexist. Use plugins when you want to reuse the same setup across multiple repositories or distribute to others via a marketplace.

### Compare similar features

#### Skills vs. Subagents

Skills and subagents solve different problems:
+ Skills are reusable content you can load into any context
+ Subagents are isolated workers that run separately from your main conversation

| Aspect | Skill | Subagent |
| :----- | :---- | :------- |
| What it is | Reusable instructions, knowledge, or workflows | Isolated worker with its own context |
| Key benefit | Share content across contexts | Context isolation. Work happens separately, only summary returns |
| Best for | Reference material, invocable workflows | Tasks that read many files, parallel work, specialized workers |

Skills can be reference or action: Reference skills provide knowledge Claude uses throughout your session (like your API style guide). Action skills tell Claude to do something specific (like `/deploy` to run your deployment workflow).

Subagents: useful when you need context isolation or when your context window is getting full. The subagent might read dozens of files or run extensive searches, but your main conversation only receives a summary. Also useful when when you don't need the intermediate work to remain visible. Custom subagents can have their own instructions and can preload skills.

A subagent can preload skills (using the `skills:` field). A skill can run in isolated context using `context: fork`.

#### CLAUDE.md vs. Skill

Both store instructions, but they load differently and serve different purposes.

| Aspect | CLAUDE.md | Skill |
| :----- | :-------- | :---- |
| Loads | Every session, automatically | On demand |
| Can include files | Yes, with `@path` imports | Yes, with `@path` imports |
| Can trigger workflows | No | Yes, with `/<name>` |
| Best for | "Always do X" rules | Reference material, invocable workflows |

CLAUDE.md: coding conventions, build commands, project structure, "never do X" or "always do Y" rules that Claude should always know.

Skills: if it's a reference material Claude needs sometimes (API docs, style guides) or a workflow you trigger with `/<name>` (e.g., `/deploy`, `/review`, `/release`).

Rule of thumb: Keep CLAUDE.md under 200 lines as it is loaded into every session. If it's growing beyond that, move reference content to skills or split into `.claude/rules/` files.

#### CLAUDE.md vs. Rules vs. SKills

All three store instructions, but they load differently:

| Aspect | CLAUDE.md | .claude/rules/ | Skill |
| :----- | :-------- | :------------- | :---- |
| Loads | Every session, automatically | Every session, or when matching files are opened | On demand, when invoked or when relevant |
| Scope | Whole project | Can be scoped to file paths | Task-specific |
| Best for | Core conventions and build commands | Language-specific or directory-specific guidelines | Reference material, repeatable workflows |

CLAUDE.md: use for instructions every session needs: build commands, test conventions, project architecture.

Rules: use to keep CLAUDE.md focused. Rules with `paths` only load hwn claud works with matching files, saving context.

Skills: for content Claude only needs sometimes, like API documentation or a deployment checklist you trigger with `/<name>`.

#### Subagent vs. Agent team

Both are used to parallelize work, but they're architecturally different:
+ Subagents: run inside your session and report results back to your main context.
+ Agent teams: independent of Claude Code sessions; can communicate with each other.

| Aspect | Subagent | Agent team |
| :----- | :------- | :--------- |
| Context | Own context window; results return to the caller | Own context window; fully independent |
| Communication | Reports results back to the main agent only | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Best for | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| Token cost | Lower: results summarized back to main context | Higher: each teammate is a separate Claude instance |

Subagents: when you need quick, focused worker (e.g., research a question, verify a claim, review a file). The subagent does the work and returns a summary. Your main conversation stays clean.

Use an agent team: when teammates need to share findings, challenge each other, and coordinate independently. Agent teams are best for research with competing hypotheses, parallel code review, and new feature development where each teammate owns a separate piece.

The transition point from subagent to agent team is when you're hitting context limit with subagents.

| NOTE: |
| :---- |
| As of March 19, 2026, team agents are experimental. |

#### MCP vs. Skill

MCP connects Claude Code to external services. Skills extends what Claude knows, including how to use those services effectively.

| Aspect | MCP | Skill |
| :----- | :------- | :--------- |
| What it is | Protocol for connecting to external services | Knowledge, workflows, and reference material |
| Provides | Tools and data access | Knowledge, workflows, reference material... |
| Examples | Slack integration, database queries, browser control | Code review checklist, deploy workflow, API style guide |

MCP: gives Claude the ability to interact with external systems. Without MCP, Claude can't query your DB or post to Slack.

Skills: give Claude knowledge about how to use those tools effectively, plus workflows you can trigger with `/<name>`. A skill might include your DB schema and query patterns, or a `/post-to-slack` workflow with your team's message formatting rules.

Example: an MCP server connects Claude to your DB. A skill teaches Claude your data model, common query patterns, and which tables to use for different tasks.

### Undersing features layers

Features can be define at multiple levels: user-wide, per-project, via plugins, or through managed policies. You can also nest CLAUDE.md files in subdirs or place skills in specific packages of a monorepo. When the same features exists at multiple levels they layer according to these rules:

+ CLAUDE.md files are additive: all levels contribute to Claude's context simultaneously. Files from your working dir and above load at launch; subdirs load as you work in them. When instructions conflict, Claude uses judgement to reconcile them, with more specific instructions taking precedence.

+ Skills and subagents override by name: when the same name exists at multiple levels, one definition wins based on managed > user > project for skills; managed > CLI flag > project > user > plugin for subagents. Plugin skills are namespaced to avoid conflicts.

+ MCP servers override by name and local > project > user.

+ Hooks merge: all registered hooks fire for their matching events regardless fo source.

### Combine features

Each type of extension solves a different problem. Real setups combine them based on your needs.

For example, you might use CLAUDE.md for your project conventions, a skill for your deployment workflow, MCP to connect to your DB, and a hook to run linting after every edit.

+ CLAUDE.md: handles always-on context
+ Skills: handled on-demand knowledge and workflows
+ MCP: handles external connections
+ Subagents: handles isolation from your main context
+ Hooks: handles automation without LLMs

| Pattern | How it works | Example |
| :------ | :----------- | :------ |
| Skill + MCP | MCP provides the connection; a skill teaches Claude how to use it well | MCP connects to your DB, a skill documents your schema and query patterns |
| Skill + Subagent | A skill spawns subagents for parallel work | `/audit` skill triggers security, performance, and style subagents that work in isolated contexts |
| CLAUDE.md + Skills | CLAUDE.md holds always-on rules; skills hold reference material loaded on demand | CLAUDE.md says "Follow our API conventions" and a skill contains the full API style guide |
| Hook + MCP | A hook triggers external actions through MCP | Post-edit hook sends a Slack notification when Claude modifies critical files |

### Understanding context costs

Every feature you add consumes some of Claude's context. Too much can fill up your context window, and what's worse, add noise that will make Claude less effective: skills may not trigger correctly, Claude may lose track of conventions, etc.

| Feature | When it loads | What loads | Context cost |
| :------ | :------------ | :--------- | :----------- |
| CLAUDE.md | Session start | Full content | Every request |
| Skills | Session start + when used | Descriptions at start, full content when used | Low (descriptions every request, unless you use `disable-model-invocation: true`) |
| MCP servers | Sessions start | All tool definitions and schemas | Every request |
| Subagents | When spawned | Fresh context with specified skills | Isolated from main session |
| Hooks | On trigger | Nothing (runs externally) | Zero, unless hook returns additional context |

## How Claude remembers your project

Each Claude Code session begins with a fresh context window.

There are two mechanisms that carry knowledge across sessions:
+ CLAUDE.md: instructions you write to give Claude persistent context.
+ Auto memory: notes Claude writes itself based on your corrections and preferences.

### CLAUDE.md vs. auto memory

CLAUDE.md and auto memory are two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration.

As a best practice, the more specific and concise your instructions, the more consistently Claude follows them.

|      | CLAUDE.md | Auto memory |
| :--- | :-------- | :---------- |
| Who writes it | You | Claude |
| What it contains | Instructions and rules | Learnings and patterns |
| Scope | Project, user, or org | Per working tree |
| Loaded into | Every session | Every session (first 200 lines) |
| Use for | Coding standards, workflows, project architecture | Build commands, debugging insights, preferences Claude discovers |

Note that subagetns can also maintain their own auto memory.

### CLAUDE.md files

CLAUDE.md files are md files that give Claude persistent instructions for a project, your personal workflow, or your entire organization. You write these files in plain text; Claude reads them at the start of every session.

#### Choose where to put CLAUDE.md files

CLAUDE.md files can live in several locations, each with a different scope. More specific locations take precedence over broader ones.

| Scope | Location | Purpose | Use case examples | Shared with |
| :---- | :------- | :------ | :---------------- | :---------- |
| Managed policy | `/etc/claude-code/CLAUDE.md`<br>`C:\Program Files\ClaudeCode\CLAUDE.md`<br>`/Library/Application Support/ClaudeCode/CLAUDE.md` | Organization-wide instructions managed by IT/DevOps | Company coding standards, security policies, compliance requirements | All users in the org |
| Project instructions | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions for the project | Project architecture, coding standards, common workflows | Team members via source control |
| User instructions | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Code styling preferences, personal tooling shortcuts | Just you (all projects) |

CLAUDE.md files in the directory hierarchy above the working directory are loaded in full at launch. CLAUDE.md files in subdirs load on demand when Claude reads files in those directories.

For large projects, you can break instructions into topic-specific files using project rules, which lets you scope instructions to specific file types or subdirectories.

#### Set up a project CLAUDE.md

A project CLAUDE.md can be stored in either:
+ `./CLAUDE.md`
+ `./.claude/CLAUDE.md`

Create this file and add instructions that apply to anyone working on the project: build and test commands, coding standards, architectural decisions, naming conventions, and common workflows.

These instructions will be shared with your engineering team through version control, so focus on project-level standards rather than personal preferences.

You can run `/init` to generate a starting `CLAUDE.md` automatically. Claude will analyze your codebase and create a file with build commands, test instructions, and project conventions. If a CLAUDE.md already exists, Claude will suggest improvements instead of overwriting it.

You can set `CLAUDE_CODE_NEW_INIT=true` to enable an interactive multi-phase flow in which `/init` will ask you about the different artifacts to set up:
+ `CLAUDE.md`
+ skills
+ hooks

##### Write effective instructions

CLAUDE.md are loaded into the context window at the start of every session, consuming tokens along your conversation. Specific, concise, well-structured instructions work best.

| NOTE: |
| :---- |
| CLAUDE.md is context, not deterministic enforced configuration. |

**Size**: target less than 200 lines. If you need more lines, split them using imports or `.claude/rules/` files.

**Structure**: use MD headers and bullets to group related instructions.

**Specificity**: write instructions that are concrete enough to verify
+ "Use 2-space indentation" is better than "Format code properly"
+ "Run uv run pytest" is better than "Test your changes"
+ "Path operations live in `routers/` is better than "Keep files organized"

**Consistency**: If two rules contradict, Claude may pick one arbitrarily. Review your CLAUDE.md files in subdirectories and `.claude/rules/` periodically to remove outdated or conflicting instructions. In monorepos use `claudeMdExcludes` to skip CLAUDE.md files that might not be relevant to you.

##### Import additional files

CLAUDE.md can import additional files using `@path/to/import`. These will be expanded and loaded into context at launch alongside the CLAUDE.md that references them.

```markdown
See @README for project overview and @package.json for available npm commands for this project.

# Additional instructions
- git workflow @docs/git-instructions.md
```

For personal preferences you don't want to check in, import a file from your home directory. That way, the import will land in the context, but the file will stay in your machine:

```markdown
# Individual preferences
- @/.claude/my-project-instructions.md
```

##### How CLAUDE.md files load

Claude Code reads CLAUDE.md files walking up the dir tree from your current directory, checking each directory along the way.

If you run Claude Code in `foo/bar/`, it will load both: `foo/bar/CLAUDE.md` and `foo/CLAUDE.md`.

Claude also discovers CLAUDE.md files in subdirs. These will be loaded only when Claude reads files in those subdirectories.

To load CLAUDE.md files from additional directories that you enable with the `--add-dir` flag (typically used to give Claude access to additional dirs outside of your main working dir) use:

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

#### Organize rules with `.claude/rules/`

For big projects, you can organize instructions into multiple files using the `.claude/rules/` directory. This keeps instructions modular and easier for teams to maintain. Rules can also be scoped to specific file paths so they only load into context when Claude works with matching files, and therefore saving context space.

To set up rules, place MD files in your `.claude/rules/` directory. Each file should cover one topic with a descriptive filename like `testing.md` or `api-design.md`. The files will be discovered recursively, you can organize them into directories:

```
your-project/
├── CLAUDE.md
└── rules/
    ├── backend/
    │   ├── api-design.md
    │   ├── code-style.md
    │   ├── security.md
    │   └── testing.md
    └── frontend/
        ├── code-style.md
        ├── security.md
        ├── testing.md
        └── widget-libraries.md
```

#### Path-specific rules

Rules can be scoped to specific files using YAML frontmatter with the `paths` field. These conditional rules only apply when Claude is working with the files matching the specified patterns:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

Rules without `paths` will be loaded unconditionally and will apply to all files. Otherwise, path-scoped rules will be triggered when Claude reads files matching the given pattern, not on every tool use.

| Pattern | Matches |
| :------ | :------ |
| **/*.ts | All TypeScript files in any dir |
| src/**/* | All files under src/ |
| *.md | Markdown files in the project root |
| src/components/*.tsx | All *.tsx file in that specific directory |


You can specify multiple patterns and use brace expansion:

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Sharing rules across projects with symlinks

The `.claude/rules` directory supports symlinks, so you can maintain a shared set of rules and link them into multiple projects. Symlinks are resolved and loaded normally, and circular symlinks are detected and handled gracefully:

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ls -s ~/company-standards/security.md .claude/rules/security.md
```

#### User level rules

Personal rules in `~/.claude/rules/` apply to every project in your machine. Use them for preferences that aren't project specific.

```
~/.claude/rules/
├── preferences.md    # Your personal coding preferences
└── workflows.md      # Your preferred workflows
```

#### Manage CLAUDE.md for large teams

For organizations deploying Claude Code across teams, you can centralize instructions and control which CLAUDE.md files are loaded.

##### Deploy organization wide CLAUDE.md

Organizations can deploy a centrally managed CLAUDE.md that applies to all users on a machine. This file cannot be excluded by individual settings.

1. You must create the file at the managed policy locations:
  + macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
  + Linux and WSL: `/etc/claude-code/CLAUDE.md`
  + Windows: `C:\Program Files\ClaudeCode\Claude.md`

1. Deploy with your configuration management system.

#### Exclude specific CLAUDE.md files

In large monorepos, ancestor CLAUDE.md files may contain instructions that aren't relevant to you.

You can fix that using `claudeMdExcludes` in `.claude/settings.local.json`:

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

| NOTE: |
| :---- |
| Managed policy CLAUDE.md files cannot be excluded. |

### Auto Memory

Auto memory lets Claude accumulate knowledge across sessions without you writing anythings. Claude saves notes for itself as it works: build commands, debugging insights, architecture notes, code style preferences, and workflow habits.

| NOTE: |
| :---- |
| Auto memory requires Claude Code v2.1.59 or later (see `claude --version`). |

#### Enabling or disabling auto memory

Auto memory is on by defaults, but you can toggle it using `/memory` in a session, or using the `automMemoryEnabled` in your project settings:

```json
{
  "autoMemoryEnabled": false
}
```

#### Storage location

Each project gets its own memory directory at `~/.claude/projects/{project}/memory`. The `{project}` path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside any git repo, the project root is used instead.

| NOTE: |
| :---- |
| The default location can be customized with the `autoMemoryDirectory` project setting. |

The directory contains a `MEMORY.md` entrypoint and optional topic files:

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

#### How it works

The first 200 lines of `MEMORY.md` are loaded at the start of every conversations. Content beyond 200 lines is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files.

Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.

Claude reads and writes memory files during your session (you'll see "Writing memory" or "Recalled memory" messages).

#### Audit and edit your memory

Auto memory files are plain markdown you can edit or delete at any time. You can inspect them using `/memory` to browse and open memory files from within a session.

### View and edit with `/memory`

The `/memory` command lists all CLAUDE.md and rules files loaded in your current session, lets you toggle auto memory on and off, and provides a link to open the auto memory folder. Select any file to open it into your editor.

When you ask Claude to remember something like "always use uv, not pip" or "remember that the API tests require a local REDIS instance", Claude saves it to auto memory. To add instructions to CLAUDE.md, ask Claude directly like "add this to CLAUDE.md", or edit the file yourself.

### Troubleshooting memory issues

#### Claude isn't following my CLAUDE.md

CLAUDE.md is delivered as a user message after the system prompt, not as part as the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance.

To debug:
+ run `/memory`
+ Check the CLAUDE.md is in a location that gets loaded for your session.
+ Make instructions more specific (e.g., "use 2-space indentation" rather than "format code nicely").
+ Look for conflicting instructions across CLAUDE.md files.

#### I don't wknow auto auto memory is saved

Run `/memory` and inspect.

#### My CLAUDE.md is too large

Files over 200 lines consume more context and may reduce adherence. Move detailed content into separate files referenced with `@path` imports, or split instructions across `.claude/rules/` files.

#### Instructions seem lost after `/compact`

CLAUDE.md fully survives compaction.

## Common workflows

This section covers several practical workflows for everyday development.

### Understanding new codebases

Start with a high-level overview:

```
give me an overview of this codebase
```

Then dive deeper into specific components:

+ explain the main architecture patterns used here
+ what are the key data models
+ how is authentication handled
+ ...

### Find relevant code

When you need to locate code related to a specific feature or functionality:

+ Ask Claude to find relevant files: find the files that handle user authentication.
+ Get context of how components interact: how do these authentication files work together?
+ Understand the execution flow: trace the login process from frontend to database.

### Fix bugs efficiently

+ share the error with Claude: I'm seeing an error when I run npm test
+ ask for fix recommendations: suggest a few ways to fix the @ts-ignore in user.ts
+ apply the fix: update user.tx to add the null check you suggested

### Refactor code

+ Identify legacy code for refactoring: find deprecated API usage in our codebase.

+ Get refactoring recommendations: suggest how to refactor utils.js to use modern JavaScript features.

+ Apply the changes safely: refactor utils.js to use ES2024 features while maintaining the same behavior.

+ Verify the refactoring: run tests for the refactored code.

### Using specialized subagents in your workflow

Some workflows involve the use of specialized AI subagents to handle specific tasks more efficiently.

+ view available subagents: `/agents`
+ use subagents automatically: review my recent code changes for security issues

    This will trigger the automatic delegation of tasks to specialized agents.