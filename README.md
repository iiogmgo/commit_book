### HOW TO USE

1. Extracting log data

```shell
git log --pretty=format:'%h::%s::%ad::%an::' --shortstat --no-merges --date=short --author={sample@gmail.com} | paste - - - > {repo}_{name_with_hypen}_log.txt
```

2. Modifying config data

```python
CSS_FILE = 'sample_css.css'
PAGES = [{
    'name': 'name', 'repos': ['repo'], 'comments': [{'author': 'iiogmgo', 'message': 'comments for you!'}]
}]
```

3. Make commit book

```shell
python commit.py
```
