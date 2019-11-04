# psd-xhtml

A program to export data from a PSDs layers to generate HTML.

## Installation and Requirements

Requires Python 3.6+

Install the dependency packages [psd-tools](https://github.com/psd-tools/psd-tools), [requests](https://github.com/psf/requests) and [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html).

``` terminal
    cd psd-xhtml/
    pip install -r requirements.txt
```

## How do i run this

Run the following inside a terminal

``` terminal
    python main.py
```

There's some files in `example/` you can use, just move the `modules.json` in to the parent directory.

## How does it work

The program uses [psd-tools](https://github.com/psd-tools/psd-tools) to read photoshops COM API, the layer names are read which correspond to the `modules.json`, `key` (html module name) and `value` (raw html).

Example; If the PSD layer name is `TEXT_01` this will requests the value of key `TEXT_01` from `modules.json` which will return the html `...<h1>TEXT_01</h1>...`

The text is also parsed from the PSD and inserted/replace in the HTML

## PSD requirements

The photoshop file must include;

- An Artboard, with `Mobile` in the name
