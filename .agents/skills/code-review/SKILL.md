# Code Review

## Purpose
Perform a read-only review before merge.

## Trigger
Use when the user asks for review, risk assessment, or pre-merge inspection.

## Checklist
- Correctness
- Security
- Edge cases
- Architecture drift
- Unnecessary complexity
- Test coverage
- Backward compatibility

## Output
Findings first, ordered by severity:
- File and line reference
- Impact
- Suggested fix

Then include:
- Open questions
- Test gaps
- Short summary

## Constraints
- Review only unless the user asks for fixes.
- Prioritize concrete bugs over style comments.
