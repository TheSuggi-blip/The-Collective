# collective-index -- Search The-Collective

Hybrid file retrieval over the `The-Collective` repository. It combines
semantic search (embedding model in `config.yaml`) with BM25 keyword search,
merges both rankings with Reciprocal Rank Fusion (RRF), reorders the first
fused chunks with a reranker when `reranker.enabled` is set, and returns one
best chunk per file. Markdown files are indexed; the logs are not.

Gold questions measure the search results. They never influence live ranking.

## Commands

Run from the repository root (`/srv/collective/the-collective`) with the
search tools' own Python:

```bash
/opt/search/venv/bin/python collective-index/query.py --check-freshness
/opt/search/venv/bin/python collective-index/query.py "<question>" --top-k 20
/opt/search/venv/bin/python collective-index/index.py --check
/opt/search/venv/bin/python collective-index/eval.py --validate-only
/opt/search/venv/bin/python collective-index/eval.py --verbose
/opt/search/venv/bin/python collective-index/eval.py --baseline <earlier eval-results.json>
/opt/search/venv/bin/python collective-index/eval.py --rerank on|off
/opt/search/venv/bin/python collective-index/self-test.py
```

The watcher owns index builds: once a minute it checks the index against
the repository and rebuilds what changed. Do not run `index.py --force`
unless recovering a diagnosed corrupt index or changing the embedding model.

## Files

- `index.py`: incremental/full index builder and freshness check.
- `query.py`: dense + BM25 + RRF retrieval. BM25 matches lowercase words;
  punctuation and Markdown marks separate words. The reranker scores the
  first `reranker.top_k` fused chunks on their full text through the embed
  service; without its answer the fused order is returned.
- `eval.py`: relevance-set validation; Top-1/3/5, Recall, MRR, nDCG and
  seconds per query; question-by-question comparison with an earlier run;
  `--rerank on|off` overrides the config for one run.
- `gold-queries.yaml`: curated questions and relevant repository files.
- `self-test.py`: package contract and regression tests.
- `config.yaml`: model, chunking, fusion, reranker, and data-path settings.

## Embed Service

`index.py` and `query.py` ask the embed service named by the environment
variable `BRAIN_EMBED_URL` (default `http://127.0.0.1:8099/embed`) for
embeddings; the same service reranks. Without it they load the embedding
model in-process and return results in fused order.

## Data and Evaluation

Index data lives in the folder named by `index.data_dir` in `config.yaml`
(`/srv/collective/index`), outside git. Gold entries use `gold_files`
because one question can have more than one relevant file. Every target
must exist, be nonempty, and appear in the index.

Refresh relevance judgments when the corpus grows materially.

Agents open the top 3-5 files, so Top-1/3/5 and MRR decide a search change;
Recall@20 only guards against losing files. To test a change, keep the
`eval-results.json` of the old state and run `eval.py --baseline <that file>`
on the same gold set. It prints the MRR difference with its 95% interval:
`clear gain` and `clear loss` are real; `no clear difference` means this gold
set cannot tell the two states apart.
