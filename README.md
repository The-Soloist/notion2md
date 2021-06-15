# Notion Markdown Exporter

[English](README/README.md) | [中文](README.md)

## Upgrade

1. 添加了对导出database的支持

## Usage 

在`/path/to/notion2md`路径下添加config.ini

```
[notion]
token_v2 = token
```
运行
```sh
❯ python main.py [url]
```
```sh
❯ python main.py
Enter Notion Page Url: https://www.notion.so/your_page_id
```

## TODO

- [ ] 修复导出时出现重复的内容

## Reference

[How To Find Your Notion v2 Token — Red Gregory](https://www.redgregory.com/notion/2020/6/15/9zuzav95gwzwewdu1dspweqbv481s5)