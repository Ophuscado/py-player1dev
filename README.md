# Player1 Development Framework

## About

A framework for perfectionists to build at light speed. Powered by Flet (Flutter) and FastAPI.

## Attributions

This project has influence from many sources. You can find a quasi-complete list of attributions in the file [`ATTRIBUTIONS.md`.](https://github.com/Ophuscado/py-player1dev/blob/main/ATTRIBUTIONS.md)

## Contributions

Please read
[`CONTRIBUTIONS.md`](https://github.com/Ophuscado/py-player1dev/blob/main/CONTRIBUTIONS.md) before submitting a pull request. For security reports, please follow our
[responsible disclosure policy.](https://ophuscado.com/security)

## Documentation

### Installation

```
pip install player1dev
```

### Usage

There is a full working example in the `example/` directory.

#### Client

The client is a Flet application, which brings Flutter to Python. You can run it with the following command:

```
flet example/client.py
```

Add your own views to `example/views/` and extend the file `example/client.py` to build your own truly cross-platform client application.

#### Server

The server is a FastAPI application, also capable of server side rendering markdown files with custom styles and templates. You can run it with the following command:

```
uvicorn example.main:app --reload --port 8000
```

Add your own pages to `example/content/` and extend the file `example/server.py` to build your own server application.

## License

Copyright (c) 2020-2023, Ophuscado LLC.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
