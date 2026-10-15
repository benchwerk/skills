# Suite

Generic developer-workflow skills written by benchwerk on 2026-10-08 as the crowd and the overlap pairs of the skill-management tests.
Each follows the same pattern: a description that names the situation and what the skill is not for, then a short numbered procedure and a few rules.

Measured on Claude Code 2.1.286, Sonnet 5.5 (1M window), one run each, 2026-10-08:
- all 15 load (15 of 15 appear in the session's skill list);
- the 15 listing entries together add 1,165 tokens to the empty session (19,242 to 20,407);
- one skill alone (`changelog-entry`) adds 76 tokens to the listing and 420 more when invoked.

| Skill | Description (chars) | Body (chars) | Overlap partner |
| :-- | --: | --: | :-- |
| `api-error-check` | 240 | 889 | `api-versioning-check` |
| `api-versioning-check` | 213 | 939 | `api-error-check` |
| `bash-script-safety-review` | 236 | 945 | `shell-portability-check` |
| `changelog-entry` | 218 | 1085 | `release-notes-from-log` |
| `commit-message-format` | 193 | 892 | `pull-request-description` |
| `csv-cleaning-plan` | 212 | 995 | - |
| `html-accessibility-audit` | 239 | 1118 | `html-seo-audit` |
| `html-seo-audit` | 238 | 841 | `html-accessibility-audit` |
| `meeting-notes-summary` | 216 | 654 | - |
| `pull-request-description` | 193 | 805 | `commit-message-format` |
| `python-docstrings` | 163 | 881 | - |
| `release-notes-from-log` | 229 | 830 | `changelog-entry` |
| `shell-portability-check` | 236 | 873 | `bash-script-safety-review` |
| `sql-migration-review` | 209 | 1083 | `sql-query-tuning` |
| `sql-query-tuning` | 186 | 990 | `sql-migration-review` |

The bodies are short (650 to 1,120 characters); the median body of the 138 popular skills in the main study is 8,085.5 characters, so these cost much less to invoke than a typical popular skill.
