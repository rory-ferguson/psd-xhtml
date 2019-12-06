# psd-xhtml

A program to export data from a PSDs layers to generate HTML.

## Installation and Requirements

This program will not run without a `modules.json` of your html modules. You can generate a `json` file using this [json_generator](https://github.com/Constuelo/json_generator) script.

Requires atleast Python 3.6

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

## How does it work

The program uses the [psd-tools](https://github.com/psd-tools/psd-tools) library to read Photoshops COM API.
The layer names are read which correspond to the `modules.json`, `key` (the html module name) and `value` (raw html).

``` json
    {
        "TEXT_01": "<h1>TEXT_01</h1>"
    }
```

Here's an example; If the PSD layer name is `TEXT_01` this will request the value of key `TEXT_01` from `modules.json` which will return the html `...<h1>TEXT_01</h1>...`

The text is also parsed from the PSD and replaced in the HTML.

## PSD requirements

The photoshop file must include;

- An Artboard, with `Mobile` in the name
