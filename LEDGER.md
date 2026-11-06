# Provenance Ledger

Write one entry per reviewable change or experiment, when the work is done. Use exactly
the schema in HANDOUT.md. Put the prompts you typed into AI tools in `prompts/` and name
the file in the entry's `prompts` field.

For a run, most of the entry comes straight from its trace: what the agent did and in
what order, the commands that checked it, and the result. You add what only you know:
how you reviewed it, what you rejected, and what is still uncertain.

## Worked example (not graded; leave it here and add your entries under "My entries")

This shows the level of detail expected. The commit SHAs, dates, steps and numbers are
made up, and so is the practice run.

```
## Entry 2
artifact:  agent/loop.py, run_agent, at commit 9c3a71e
tool:      Claude Code, model Claude Sonnet 5.5, 2026-11-01
prompts:   asked for the loop body from the comment above run_agent;
           prompts/loop-01.md
review:    read every line against the comment. It returned as soon as is_stuck was
           true, which skipped the tool results for the other calls in the same turn;
           moved the stuck check after the for loop as the comment says. Rejected its
           suggestion to import a framework's message classes; kept the dicts from
           core.py
checks:    pytest tests/test_loop.py: 9 passed
evidence:  HANDOUT Part 3; the comment above run_agent, steps 4 and 5
risk:      no test of mine has three tool calls in one turn

## Entry 4
artifact:  runs/try1, a practice run, agent code at commit 4b9e2d1
tool:      my agent (python -m agent run try1), anthropic claude-haiku-5-5, 2026-11-02
prompts:   the default task and BASE_SYSTEM in agent/loop.py; prompts/try1-task.md
review:    read every event in trace.jsonl. At attempt 1, steps 4 and 6, the model
           copied old_text with the read_file line numbers, and edit_file refused both
           times. At step 7 it made an edit that changed nothing the tests check, and
           at step 8 the stuck rule stopped it. I approved the step 7 edit without
           reading it closely
checks:    python -m agent check-trace try1: complete
evidence:  HANDOUT Part 1 (tool descriptions) and Part 2 (is_stuck)
risk:      one practice run; a better description may still not stop the copying
dataset:   fixture/ at commit 4b9e2d1, task "Make the tests pass."
result:    stopped stuck after 8 model calls, 14,880 input tokens, about $0.002;
           runs/try1/trace.jsonl
changed:   wrote "copy it without the line numbers" into the read_file and edit_file
           descriptions, and read every diff before approving
```

## My entries

artifact:  agent/tools.py, safe_path, read_file, edit_file, format_report, run_tests, at commit 5036a692d557d5bfbc5bb4c230383c0574f3375c
tool:      ChatGPT, model GPT-6, 2026-11-06
prompts:   prompts/tools-01.md
review:    reviewed the implementations against the function comments and
           test expectations. Checked path validation, line limits,
           exact text replacement, error messages, and test reporting.
           Fixed missing imports and file placement issues during testing.
           Kept the given functions and TOOLS list unchanged.
checks:    pytest tests/test_tools.py -v passed
evidence:  comments and docstring rules in agent/tools.py;
           tests/test_tools.py
risk:      full test suite has not been verified; additional edge cases
           may remain untested


artifact:  agent/policy.py, gate_for, budget_stop, is_stuck, at commit 5036a692d557d5bfbc5bb4c230383c0574f3375c
tool:      ChatGPT, model GPT-6, 2026-11-06
prompts:   prompts/policy-01.md
review:    reviewed the implementations against the function comments and
           test expectations. Checked tool permissions, approval requirements,
           denial of edits to tests/, budget limits, and repeated test failures.
           Verified path normalization and step-budget priority.
           Kept the given GATES dictionary and TESTS_RULE unchanged.
checks:    pytest tests/test_policy.py -v passed
evidence:  comments and policy rules in agent/policy.py;
           tests/test_policy.py: passed
risk:      full test suite has not been verified; additional edge cases

artifact:  agent/reflexion.py, judge, write_lesson, reflexion, at commit 5036a692d557d5bfbc5bb4c230383c0574f3375c
tool:      ChatGPT, model GPT-6, 2026-11-06
prompts:   prompts/reflexion-01.md
review:    reviewed the implementations against the function comments and
           test expectations. Checked acceptance test execution, timeout
           handling, lesson generation, and retry behavior. Verified that
           lessons are normalized, limited to 600 characters, and appended
           to NOTES.md for subsequent attempts. Checked that provider errors
           stop execution and successful acceptance tests end the loop.
           Kept JUDGE_PATTERN, LESSON_SYSTEM, and LESSON_PROMPT unchanged.
checks:    python -m py_compile reflexion.py: passed
           pytest tests/test_reflexion.py -v: not yet verified
evidence:  HANDOUT Part 4; comments above judge, write_lesson,
           and reflexion in agent/reflexion.py; tests/test_reflexion.py:  passed
risk:      full integration tests have not been verified; edge cases
           involving provider failures, note persistence, and repeated
           attempts may remain untested.
           involving path normalization and budget boundaries may remain untested.

artifact:  agent/loop.py, build_system_prompt, run_agent, at commit 5036a692d557d5bfbc5bb4c230383c0574f3375c
tool:      ChatGPT, model GPT-6, 2026-11-06
prompts:   prompts/loop-01.md
review:    reviewed the implementations against the function comments and
           test expectations. Checked system prompt construction, model
           calls, tool execution, approval handling, and stop conditions.
           Verified that denied tools never execute and rejected edits
           return feedback to the model. Ensured all tool results in a
           turn are processed before checking the stuck condition.
           Kept BASE_SYSTEM and NOTES_HEADER unchanged and avoided
           using an agent framework.
checks:    python -m py_compile loop.py: passed
           pytest tests/test_loop.py -v: passed
evidence:  comments above build_system_prompt and
           run_agent in agent/loop.py; tests/test_loop.py
risk:      integration with the complete project has not been verified;
           additional cases involving multiple tool calls in one turn
           may remain untested.

artifact:  server.py, mcp, main, at commit 5036a692d557d5bfbc5bb4c230383c0574f3375c
tool:      ChatGPT, model GPT-6, 2026-11-06
prompts:   prompts/server-01.md
review:    reviewed the implementation against the Part 5 instructions
           and test expectations. Checked MCPServer initialization,
           registration of all four tools, command-line argument
           parsing, workspace configuration, and stdio transport.
           Verified that importing server.py does not start the server.
           Preserved the existing imports and main entry point.
checks:    python -m py_compile server.py: passed
           pytest tests/test_server.py -v: passed
evidence:  requirements in server.py;
           tests/test_server.py
risk:      MCP client integration has not been verified in the complete
           project environment; tool registration and error propagation
           require confirmation through integration tests.

