# Regression fixtures

`legacy_results.json` contains 54 expected results obtained from the original
TUI implementation before its removal: 18 chests × seeds 1, 19, 888, each with
30 starting chests. The original implementation was executed independently of
the current simulation engine. Fixed Advice of Valks wrappers were flattened
in that reference implementation to match the intended terminal-item behavior.

Each record stores the English chest ID, seed, basket quantity, terminal
inventory, total opened count and Cron-equivalent value. The fixture is test
data, not the application's catalog.

Do not regenerate it from the current engine just to make a failing test pass.
Changes require an intentional content/rules revision and an independently
reviewed expected result.
