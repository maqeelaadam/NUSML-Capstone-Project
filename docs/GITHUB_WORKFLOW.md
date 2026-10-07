# GitHub and import workflow

The existing destination is https://github.com/maqeelaadam/NUSML-Capstone-Project. Keep capstone changes in this project folder rather than committing unrelated assignments from its parent folder.

## Continue the existing repository

Clone the repository or open the local Git copy in GitHub Desktop. The setup history is a framework; continue committing real task work incrementally. Review changed files before each commit and use a specific message. Push after completing a coherent task. Use the supplied task and pull request templates if helpful.

## Import the local framework into a new empty repository

The companion ZIP contains project files and the raw dataset, without Git metadata. Extract it, add the folder to GitHub Desktop, and create a repository there. Publish it under the desired account and name. For a command-line workflow:

```bash
git init -b main
git add .
git commit -m "Initial capstone framework"
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Create the new GitHub destination empty, without a README, licence or gitignore, before pushing. `data/raw` is ignored, so the raw CSV in the ZIP is not uploaded by these commands. Include data attribution and retain the import instructions.

A companion Git bundle preserves the GitHub framework's commit history. To use it:

```bash
git clone /path/to/NUSML-Capstone-Project.bundle NUSML-Capstone-Project
git -C NUSML-Capstone-Project remote set-url origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git -C NUSML-Capstone-Project push -u origin main
```

Only use this new-destination procedure for an empty repository. A ZIP is a file backup; GitHub's website importer expects a Git source URL rather than a ZIP or local bundle.

## Before course submission

- Confirm all required deliverables and actual task commits are present.
- Review tracked files for credentials and unnecessary files.
- Verify the repository URL. For a public repository, check grader access without login. For a private repository, invite the grader using their verified GitHub username and confirm acceptance.
- Ensure figures, required sample logs, reports, dashboard and MLflow evidence are tracked or reproducibly accessible.
- Submit the repository URL through Canvas yourself. No invitations or submissions are sent by this framework.

Reference: [GitHub's local-code import guide](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).
