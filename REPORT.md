# Assignment 4 Report

Name:
Commit graded:

Answer from your own traces. Give step numbers as `attempt 1, step 4`. Keep to the word
limits; a short answer with the right evidence earns full points.

## 1. The runs

Run `python -m agent summary` and paste its table here exactly as printed.

| Run | Tools | Judge | Stopped (per attempt) | Model calls | Tool calls | Input tokens | Output tokens | Cost | Judge verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| runA | local | after | 1: done | 6 | 7 | 8981 | 698 | $0.0249 | 1: PASS |
| runB | mcp | reflexion | 1: done | 6 | 7 | 9127 | 699 | $0.0252 | 1: PASS |
| run2 | mcp | reflexion | 1: done | 5 | 6 | 6597 | 433 | $0.0175 | 1: PASS |
| try1 | local | after | 1: done | 5 | 6 | 6532 | 448 | $0.0175 | 1: PASS |

## 2. A rejection is feedback (Run A, at most 100 words)

Which step proposed the edit you rejected, and what was your reason? What did the agent
do next, and at which step? Did it follow your reason?

At step 3, the agent proposed editing discounts.py to handle case-insensitive discount codes and reject expired codes. I rejected the edit because I wanted a comment identifying the specification rule being implemented. At step 4, the agent proposed the edit again, adding the comment "Spec rule 4: a code remains valid through its last day, but not after it." I approved the revised edit, and it succeeded. The agent followed my feedback by adding the requested comment before applying the changes.

## 3. The visible tests and the judge (Run A, at most 120 words)

What did the last `run_tests` in runA report, and what did the judge say after the run?
If the judge failed, which rule in `spec.md` did the code break, at which step did the
agent stop, and why did it stop there?

At step 5, the final run_tests reported "PASSED: 4 of 4 tests passed." The agent finished at step 6 because it replied without another tool call. Afterward, the hidden judge also passed, confirming that the implementation satisfied all acceptance requirements. The agent handled case-insensitive codes (Rule 2) and rejected expired codes (Rule 4), including the last-day boundary. No specification rule remained broken, so the agent did not stop because of a failure. Run A completed successfully with status "done" and required no additional attempts.

## 4. The lessons (Run B, at most 150 words)

Quote every lesson runB wrote to `NOTES.md`. For each one, say whether it names the real
cause, points at evidence, and says what to do next. Did attempt 2 follow it? Give the
step that shows it. If attempt 1 passed, say which step shows why no lesson was needed.

Run B did not write any lessons to NOTES.md because the first attempt passed the hidden judge. At step 3, the agent proposed changes to discounts.py to support case-insensitive codes and reject expired codes. I rejected the edit and requested a comment identifying the specification rule. At step 4, the agent added a comment referencing Rule 4, and I approved the edit. At step 5, run_tests reported "PASSED: 4 of 4 tests passed." The agent stopped at step 6 with status "done." The hidden judge then reported "PASSED: 6 of 6 tests passed." Since attempt 1 succeeded, no lesson was needed, and attempt 2 did not run.

Why NOTES.md was empty:

    RunA's run.json confirms:
    {
    "passed": true,
    "attempts": 1,
    "statuses": ["done"],
    "lessons": []
    }

    This is the expected behavior of Reflexion implementation. It writes lessons when the hidden judge fails, not when the first attempt succeeds.

## 5. Memory grows (Run A, at most 60 words)

Give `input_tokens` from the first and the last tool event in `runs/runA/trace.jsonl`,
with their step numbers. Why does the number grow from step to step?

The first tool event was list_files at step 1, with input_tokens = 540. The last tool event was run_tests at step 5, with input_tokens = 2145. The number increased because the agent accumulated conversation history, including file contents, previous tool calls, approval feedback, and edit results. Each model call processed more context than the previous one.

## 6. MCP (at most 120 words)

Quote one of your tool descriptions exactly as `python -m agent check-mcp` showed it in
the tools/list reply. Then name one risk of installing someone else's MCP server, and say
which part of your agent would stop it, or that nothing in your agent would.

One tool description returned by `python -m agent check-mcp` was:
"List every file in the project, one path per line, relative to the project folder.\n\n    Takes no inputs. Use it first to see what the project contains; the paths it returns\n    are the paths read_file and edit_file expect.\n    "
A risk of installing someone else's MCP server is unauthorized access to sensitive files or execution of malicious commands. My agent's `gate_for()` policy restricts tool calls and requires approval for edits, while `safe_path()` prevents access outside the workspace. However, neither can prevent malicious behavior inside an untrusted MCP server itself. Server isolation and restricted permissions are necessary.

## 7. The reviewer and the judge (at most 100 words)

What did your reviewer find in runB's final `discounts.py`? Did it find anything the
judge did not, or miss anything the judge caught? In the tool you used, was the
reviewer's read-only rule a lock or a request, and how do you know?

The reviewer found that Run B's final discounts.py followed all five rules in spec.md, with no missing functionality. It identified additional concerns, including Unicode case conversion, negative totals, unsupported input types, and missing visible tests for expiration boundaries. These were observations rather than confirmed specification violations. The hidden judge passed all six tests and reported no failures. Therefore, the reviewer identified potential edge cases and test gaps that the judge did not report, but missed no judge-detected failures. The reviewer's read-only rule was a technical restriction because the reviewer had no editing or execution tools, and it confirmed that no files were modified.

## 8. Your agent and a vendor's agent (at most 120 words)

What did the fixer change, and what did `python -m agent judge vendor` report for the
visible tests and for the judge? Did it change anything in `tests/`? Compare this with
runA, where your own agent had the same task on the same project. Then name one thing you
could control in your own agent that the fixer file could not set, and one thing that was
easier with the vendor's agent.

The vendor fixer first normalized discount codes using `code.upper()`, fixing the case-sensitive lookup. It initially left expiration handling unchanged because the visible tests passed. After I approved the additional fix, it added `if today > last_day` to reject expired codes. Running `python -m agent judge vendor` reported 4/4 visible tests and 6/6 judge tests passing. Only discounts.py changed; nothing in tests/ was modified. Run A also passed both test suites, but my agent proposed both fixes together and required approval before editing. My agent let me enforce tool permissions and approval gates, which the fixer file could not configure. The vendor agent made direct code editing and manual boundary verification easier.