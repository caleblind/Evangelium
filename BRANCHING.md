### Git Documentation: Branching and Process

#### Creating a New Branch

Before starting work on a new issue, create a new branch specifically for that issue. Follow the branch naming convention:

```
GH-####_Your-Descriptive-Branch-Name-Here
```

- **GH-####**: Replace with the GitHub issue number.
- **Descriptive-Branch-Name**: Clearly describe the feature or task.

Example: `GH-101_Fix-Login-Bug`

This naming convention links the issue to the branch, making it easy to track the feature in pull requests.

#### Branching: What, When, and How

Branching allows you to isolate work on specific features. Always create a new branch for each feature or bug fix to keep changes organized.

##### Creating a New Branch

1. **Sync changes**: First, fetch the latest updates from the repository.
   ```bash
   git fetch
   ```
2. **Create and switch to your new branch**:
   ```bash
   git switch -c <GH-####_Your-Descriptive-Branch-Name-Here>
   ```
   You are now in your new branch and ready to make changes.

##### Switching Branches

To view or work on another branch:
```bash
git switch <Branch-Name>
```
This switches without creating a new branch.

#### After Switching or Creating a Branch

- Make changes **only related to the feature** of the current branch.
- Example: If on `GH-123_Add-A-Login-Page`, don't add unrelated features like party mode. Instead, create a new branch (`GH-124_Add-Party-Mode`) for that task.

#### Committing Changes

Once changes are functional:
1. Stage changes:
   ```bash
   git add .
   ```
2. Commit your work:
   ```bash
   git commit -m "Clear commit message describing changes."
   ```

Keep commits clean, and aim for a functional state in each commit.

### Managing Upstream and Remote in Git

#### Setting the Upstream Branch

Once you've created your branch, you'll want to set the upstream to easily push changes and sync with the remote repository. Use the following command to set the upstream branch:

```bash
git push --set-upstream origin <GH-####_Your-Descriptive-Branch-Name-Here>
```

This command pushes the branch to the remote repository and links your local branch to the remote, allowing you to use `git push` and `git pull` without specifying the remote/branch name each time.

#### Pushing Changes to Remote

Once upstream is set, simply push your changes:

```bash
git push
```

If you haven't set upstream yet, you'll need to specify the branch:

```bash
git push origin <Branch-Name>
```

#### Pulling Changes from Remote

If someone else has updated the branch and you want to sync with the latest changes:

```bash
git pull
```

This command pulls the latest changes from the remote branch you're tracking (as long as upstream is set).
