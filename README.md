# qt Browser
A simple terminal based browser.

## Install
```bash
$ pip3 install -r requirements.txt
$ python3 browser.py <url|empty>
```

## Dependencies
- `curses`
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
- [x] ~~Basic GUI (using Tkinter for this).~~
- [x] ~~Text-wrap and Scrolling.~~
- [ ] ~~Make browser resizable.~~
- [ ] ~~Add the zoom-in and zoom-out feature.~~
- [x] Add a basic TUI.
- [x] Handle bad URLs.
- [ ] Add maximum redirect limits.
- [ ] Handle HTTP errors properly.
- [ ] Caching.
- [ ] Add support for emojis.
