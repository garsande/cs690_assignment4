asked ChatGPT to implement reflexion.py and provided below details along with tests/test_reflexion.py to use for testing and verification

# judge(workspace) runs the acceptance tests against one workspace.
#   - report = run_unittests(workspace, tests_dir=JUDGE_DIR, timeout=TEST_TIMEOUT_SECONDS,
#                            pattern=JUDGE_PATTERN)
#   - If it timed out: return (False, f"FAILED: the acceptance tests did not finish within "
#                                     f"{TEST_TIMEOUT_SECONDS} seconds.")
#   - Otherwise return (report.ok, format_report(report)).
def judge(workspace: Path) -> tuple[bool, str]:
    raise NotImplementedError("Part 4: write judge in agent/reflexion.py")


# write_lesson(provider, task, history, report) asks the model why the attempt failed.
#   - prompt = LESSON_PROMPT.format(task=task, actions=summarize_actions(history), report=report)
#   - turn = provider.complete(LESSON_SYSTEM, prompt)
#   - The lesson is turn.text on one line: " ".join(turn.text.split()), cut to its first
#     600 characters.
#   - Return (lesson, turn.input_tokens, turn.output_tokens). Let AIError propagate.
def write_lesson(provider: Any, task: str, history: list[dict[str, Any]], report: str) -> tuple[str, int, int]:
    raise NotImplementedError("Part 4: write write_lesson in agent/reflexion.py")


# reflexion(...) runs up to max_attempts attempts and returns a ReflexionResult.
#   For attempt = 1, 2, ... max_attempts:
#     1. notes = the text of notes_path (or "" if the file does not exist), read fresh
#        at the start of every attempt.
#     2. result = run_agent(task, provider=..., toolbox=..., approve=..., trace=...,
#                           limits=limits, notes=notes, attempt=attempt)
#        If result.status is "error", stop now: return passed False, with result.reason
#        as the report. (A broken provider is not a reason to try again.)
#     3. passed, report = judge(toolbox.workspace), then trace.judge(attempt=..., passed=..., report=...).
#        If passed, return ReflexionResult(True, attempt, runs, lessons, report).
#     4. Otherwise write a lesson with write_lesson(provider, task, result.history, report).
#        If that raises AIError, stop and return passed False.
#        Append one line to notes_path:  f"- Lesson from {trace.run}, attempt {attempt}: {lesson}\n"
#        (start a new line first if the file does not end with one), add the lesson to
#        the list, and write trace.lesson(attempt=..., text=lesson, input_tokens=..., output_tokens=...).
#   After the last attempt fails, return ReflexionResult(False, max_attempts, runs, lessons, report).
#   `runs` is the list of every RunResult, in order.
def reflexion(
    task: str,
    *,
    provider: Any,
    toolbox: Any,
    approve: Approver,
    trace: TraceWriter,
    notes_path: Path,
    limits: Limits = Limits(),
    max_attempts: int = 2,
) -> ReflexionResult:
    raise NotImplementedError("Part 4: write reflexion in agent/reflexion.py")

