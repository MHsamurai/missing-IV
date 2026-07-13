# Shadow variable literature search

多変量欠測、項目無回答、self-censoring、および shadow variable に関する追加文献を保存するフォルダです。

## Search record

- Database: Web of Science
- Search date: 2026-07-13
- Exported bibliography: `savedrecs.bib`
- Search query:

```text
(( ALL=(
    "multivariate missing data" OR
    "incomplete multivariate data" OR
    "multivariate nonignorable*" OR
    "multiple outcome*" OR
    "vector-valued outcome*" OR
    "item nonresponse" OR
    "nonmonotone missing*" OR
    "multiple missing indicator*" OR
    "missingness pattern*"
)) AND ALL=(
    "shadow variable*" OR
    "nonresponse instrument*" OR
    "self-censoring" OR
    "no self-censoring" OR
    "itemwise conditionally independent nonresponse" OR
    "ICIN model"
)) AND ALL=(
    identif* OR completeness OR estimat*
)
```

## File policy

- `savedrecs.bib` is the Web of Science BibTeX export and is tracked by Git.
- Article PDFs are local research resources and remain excluded from Git by the repository-wide `*.pdf` rule.
