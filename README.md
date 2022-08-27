# Miro CQRS generator

## Setup

### Miro

Follow this tutorial create an Miro app to get the token access.

- https://developers.miro.com/docs/try-out-the-rest-api-in-less-than-3-minutes

### Python

```bash
$ brew install poetry
$ poetry install
$ poetry shell
```

## Usage

### 1. Config the ENV

```bash
$ export BOARD_ID=<your_board_id>
$ export BEARER_TOKEN=<your_miro_app_token>
```

### 2. Run

```bash
$ python miro_cqrs/generator.py          
```
