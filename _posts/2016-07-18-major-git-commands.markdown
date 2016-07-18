---
published: true
title: Major GIT commands
layout: post
---

[Git] is a version control system that is used for software development and other version control tasks developed by Linus Torvalds in 2005. As a distributed revision control system it is aimed at speed, data integrity, support for distributed and non-linear workflows.


### git config
 Sets configuration values for your user name, email, gpg key, preferred diff algorithm, file formats and more.

### git branch -a
Lists existing branches, including remote branches.

### git branch -d [branch-name]
Deletes the specified branch

### git push origin --delete [branch-name]
Deletes the specified branch from remote

### git stash
Temporarily stores all modified tracked files

### git stash list
Lists all stashed changesets

### git stash pop
Restores the most recently stashed files

### git stash drop
Discards the most recently stashed changeset

### git reset [commit]
Undoes all commits afer [commit], preserving changes locally

### git reset --hard [commit]
Discards all history and changes back to the specified commit

### git show
Shows information about a git object.

### git grep
Lets you search through your trees of content for words and phrases. Example: git grep "www.google.com" -- *.js

[Git]: https://git-scm.com/