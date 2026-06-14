# Agent Instructions

- To run and test Python code, use `devcontainer exec --workspace-folder . python -c "<python code>"`.
- When invoking multiple tasks from a task.md, use a subagent for each task implementation
- Each task, when completed, gets it's own git commit
- Each task, when completed, must be verified
