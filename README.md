# The picture that tastes of one ingredient

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-orange)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
[![entry](https://img.shields.io/badge/entry-entry.png-gold)](entry.png)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

One picture of food, built on a single ingredient: **honey**.

A macro close-up fills the whole frame with golden honeycomb, thick honey
dripping from the top edge in glossy streams, and a shining pool of honey
along the bottom. Warm amber light, no text, nothing to distract from the
one ingredient you can almost taste.

## Bounty

[The picture that tastes of one ingredient](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
— the program writes one image to `/output/entry.png`; an AI judge compares
entries two at a time and ranks them by how delicious the food looks.

## Reproduce

```sh
python3 generate.py   # renders entry.png (1024x1024 PNG, deterministic)
node main.ts          # copies entry.png to /output/entry.png
```

`main.ts` uses only the Node 22 standard library and needs no network.
`generate.py` uses Pillow locally to render the picture; the finished
`entry.png` is committed in this repository, so the entry point only copies
it — the grader sandbox never needs Pillow.

## License

MIT — see [LICENSE](LICENSE).
