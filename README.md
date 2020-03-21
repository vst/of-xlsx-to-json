# Convert .xlsx to .json

![GitHub release (latest by date)](https://img.shields.io/github/v/release/vst/of-xlsx-to-json)

This repository provides an OpenFAAS function to convert uploaded `.xlsx` files to `JSON`.

## Deploy

Use `-a`, `--gateway` and `--image` if required, but essentially:

```
faas-cli template pull stack
faas up
```

Alternatively, you can use it in your own stack by including the
function definition as follows:

``` yaml
  my-xlsx-to-json-converter:
    image: vehbisinan/of-xlsx-to-json
```

The resulting stack file should look like this:

``` yaml
provider:
  name: openfaas
  gateway: https://your.openfaas.gateway.com

functions:
  your-function:
    lang: dockerfile
    handler: ./your-function
    image: your-function:latest
  my-xlsx-to-json-converter:
    image: vehbisinan/of-xlsx-to-json
```

## Usage

``` sh
curl -F file=@/tmp/sample.xlsx http://localhost:8000/ | jq .
```

Note that `jq` is just for pretty printing.
