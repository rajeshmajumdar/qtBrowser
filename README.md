# qt Browser Engine
Goal is to make a bare minimum browser-engine with minimal dependencies in python3.

## Install
```bash
$ python3 browser.py <url|empty>
```

## Roadmap
- [x] Support `http://`, `https://` & `file://` scheme.
- [x] Create a hashmap from the html.
- [x] Open a default html when executed without url.
- [x] Open local files.
- [ ] Support for entities i.e. `&lt;` & `&gt;`.
- [ ] Support for `view:source//<url>`.
- [ ] Add support for encodings.
- [ ] Handle redirects.
- [ ] Handle HTTP errors properly.
- [ ] Caching.
