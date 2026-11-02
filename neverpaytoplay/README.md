# neverpaytoplay.co.uk

A one-page static site. No framework, no build step at request time, and
**no Tailwind CDN** — the stylesheet is compiled to `assets/style.css` and
served as an ordinary file.

## Files

```
neverpaytoplay/
  index.html              the page
  src/input.css           Tailwind source (edit this, not style.css)
  assets/style.css        the built stylesheet (generated — do not hand-edit)
  assets/never-pay-to-play.svg   header illustration, also the social card
```

## Rebuilding the CSS

Any time `index.html` changes, classes it uses must be compiled in. From the
repository root:

```bash
npx @tailwindcss/cli -i ./neverpaytoplay/src/input.css -o ./neverpaytoplay/assets/style.css --minify
```

`src/input.css` begins with `@import "tailwindcss" source(none);` followed by an
explicit `@source "../index.html";`. The `source(none)` matters: without it,
Tailwind walks the whole repository, picks up every Flask template in the app
next door, and the stylesheet comes out around 208 KB instead of 29 KB.

## Deploying

Upload the whole `neverpaytoplay/` folder's contents to the web root of
neverpaytoplay.co.uk. It is static — any host will do, including a CDN or an
S3 bucket. There is nothing to install and nothing to run.

Keep the paths relative as they are (`assets/style.css`), so the site works
from a subfolder or a staging URL without editing.

## Things worth knowing

- The animations respect `prefers-reduced-motion`; anyone who has asked their
  device for less movement gets a still page.
- Outbound links point at quizmondo.com, its contact page, and the longer
  position piece at `/never-pay-to-play`. If those move, they are the only
  links to update.
- The claims about advertising on Quizmondo — human review, no profiling,
  viewable impressions — describe how the ad system on the main site actually
  works. If that changes, this page has to change with it.
- There are deliberately no audience figures anywhere. Add real ones before
  sending this to a media buyer; invented ones do not survive the first
  question.
