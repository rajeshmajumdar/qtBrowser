# qt Browser Engine
Goal is to make a bare minimum browser-engine with minimal dependencies in python3.

## Install
```bash
$ pip3 install -r requirements.txt
$ python3 browser.py <url|empty>
```

## Dependencies
- `tkinter`
- `io`
- `socket`
- `ssl`
- `typing`

## Roadmap
- [x] Support `http://`, `https://` & `file://` scheme.
- [x] Create a hashmap from the html.
- [x] Open a default html when executed without url.
- [x] Open local files.
- [x] Support for entities i.e. `&lt;` & `&gt;`.
- [x] Support for `view-source:<url>`.
- [x] Add support for compression.
- [x] Add support for `Transfer-Encoding: chunked`.
- [x] Handle redirects.
- [x] Basic GUI (using Tkinter for this).
- [x] Text-wrap and Scrolling.
- [ ] Add maximum redirect limits.
- [ ] Handle HTTP errors properly.
- [ ] Caching.
