# Commit Instructions

Write clear, concise Git commit messages that describe **what changed and why**.

* Do not use Conventional Commit prefixes or tags such as `fix:`, `feat:`, `[fix]`, or `[feature]`.
* Start with a short, specific summary of the change.
* Write the summary as an imperative sentence, such as `Update authentication handling for expired tokens.`
* Keep the first line focused and able to stand on its own in Git history.
* Follow the summary with a blank line when additional explanation is needed.
* In the body, explain the motivation, problem being solved, or important implementation context.
* Include relevant limitations, tradeoffs, follow-up considerations, issue references, or design context when useful.
* Prefer specific descriptions over vague messages such as `Fix bug`, `Update code`, `Add changes`, or `Cleanup`.
* Describe the resulting change, not the act of making the change.
* Keep the message proportional to the change; small changes may require only a clear summary.
* Ensure the final commit message accurately reflects the complete diff.

<!-- 
Reference: 
- https://google.github.io/eng-practices/review/developer/cl-descriptions.html
- https://www.reddit.com/r/git/comments/1vvt8r7/stop_using_conventional_commits/
 -->