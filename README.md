# psd-xhtml

A program to export data from a PSD files layers to generate HTML.

## Installation and Requirements

Requires Python 3.6+

Install the dependency packages [psd-tools](https://github.com/psd-tools/psd-tools), [requests](https://github.com/psf/requests) and [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html).

``` terminal
    cd psd-xhtml/
    pip install -r requirements.txt
```

## How does it work

``` terminal
    python main.py
```

The email modules are located as json data inside `modules.json`

To generate the json file use the [json_generator](https://github.com/Constuelo/json_generator)

### Simple

The program uses [psd-tools](https://github.com/psd-tools/psd-tools) to read photoshops COM API, the layer names are read which correspond to the `modules.json`, `key` (html module name) and `value` (raw html).

Example; If the PSD layer name is `TEXT_01` this will requests the value of key `TEXT_01` from `modules.json` which will return the html `...<h1>TEXT_01</h1>...`

The text is also parsed from the PSD and inserted/replace in the HTML

### Advanced

To use the dynamic text module, include a layer in the PSD called `DYNAMIC_TEXT`, include typelayers named (HEADER_01, HEADER_02, HEADER_03) and spacers (SPACER_X), change X to the height of the spacer (SPACER_20, SPACER_5).

## PSD requirements

The photoshop file must include;

- Artboards
