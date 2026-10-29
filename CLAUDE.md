# Working on Quizmondo

## Several Claude sessions share this one checkout

There are no worktrees. Every session works in this same folder, on the same
branch, against the same git index. Another session may be editing files while
you are, and its changes appear in your `git status` looking exactly like your
own.

Two deploys have already gone out by accident this way: a push sends the whole
branch, so it carries every commit on it, including commits somebody else made
and was not finished with.

### Staging

1. **`git add <explicit paths>` only.** Name the files you changed, one by one.
2. **Never `git add -A`, `git add .`, `git add -u`, or `git commit -a`.**
3. **`git status --short` before you commit.** Anything in there you did not
   write belongs to another session. Leave it alone and say so.
4. Stage and commit in the same command, so there is no window where your
   files sit staged for somebody else's commit to collect.

### Pushing

**A push to `main` deploys the live site.** Treat it as a release, not a save.

1. **Never push unless Trevor has asked for it in this conversation.** His
   approval of an earlier push is not approval of the next one.
2. **Before pushing, run `git log --oneline origin/main..HEAD`.** If there are
   commits there that are not yours, you are about to deploy another session's
   work. Stop and tell Trevor instead.
3. Never `git stash`, `git reset --hard`, or switch branches. Other sessions
   have uncommitted work in this folder.

### Commits

Commit in logical batches with a message that says what changed and why. If
you fixed something, say what the bug actually was.

## Testing

**Never run tests or scripts against `instance/sitebuilder.sqlite`.** It is the
real database, with real player and duel rows. Take a copy first, using
sqlite's backup API rather than a file copy, because the database is in WAL
mode and a plain copy of a live WAL database comes out corrupt:

```python
src = sqlite3.connect('file:instance/sitebuilder.sqlite?mode=ro', uri=True)
dst = sqlite3.connect('scratch/copy.sqlite')
with dst:
    src.backup(dst)
```

Then point the app at the copy with `APP_DATABASE_URL`. Never delete player or
duel rows.

## Tailwind

`app/static/css/tailwind.min.css` is a **purged build**. A class that appears
in no template does not exist in the CSS, so a class you have just written in
a template will do nothing on the live site until the file is rebuilt:

```bash
npx @tailwindcss/cli -i ./src/input.css -o ./app/static/css/tailwind.min.css --minify
```

Rebuild it after every batch of template edits, and commit it with them. It is
a shared build artifact, so expect to see it modified when you did not touch
it; the output is a superset of what every session needs, so that is harmless.

## Mini games

`app/static/js/games-fx.js` is the shared engine (`window.QMG`) behind every
game in `app/templates/themes/quizhub/games/`. Prefer adding to it over
copying code into a game.

Games draw their **own on-screen keyboard** (`QMG.keyboard`,
`QMG.attachKeyboard`) rather than using the device keyboard. On a phone the
system keyboard covers half the screen, and iOS zooms the page in on any input
whose text is under 16px. Do not reintroduce a text input into a game board.

Boards that are dragged or tapped need `QMG.boardGestures`, which sets
`touch-action: none`. Without it a phone scrolls the page instead of playing
the game; `preventDefault` on a pointer event cannot stop that on its own.

Every game must be playable with a thumb at 375px wide, and must not scroll
sideways.
