❯ Use the a4-tools MCP server: call its run_tests tool, then its read_file tool on discounts.py, and tell me why the failing test fails. Do not change any files.

  Called a4-tools 2 times

test_lowercase_code_works fails because the code lookup in apply_discount is case-sensitive. 1 of the 4 tests fails, with this error:

ValueError: unknown code: save10

Cause: the keys in CODES are all uppercase ("SAVE10", "WELCOME5"), and discounts.py:16 checks the input exactly as it was given:

if code not in CODES:
    raise ValueError(f"unknown code: {code}")

Nothing normalizes code first, so "save10" doesn't match "SAVE10", and line 17 raises the error. The test name and error message suggest it expects lowercase codes to work like their uppercase versions. I only read discounts.py, so I haven't seen the test's exact assertion.

Likely fix (not applied): normalize the code before the lookup, for example with code = code.upper() before line 16. The empty-string check on line 14 would still work.

Separate bug: last_day is unpacked on line 18 but never used, and neither is today. Expired codes are therefore still accepted, even though the comment on line 5 says each code has a last day. This isn't causing the failure, and the other three tests pass despite it.

No files were changed.

✻ Worked for 12s · done 11:32 AM