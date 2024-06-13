# TabSQLify: Enhancing Reasoning Capabilities of LLMs Through Table Decomposition

## Method Overview 

<image src="/method.jpg"/>

## Abstract 

Abstract Table reasoning is a challenging task that requires understanding both natural language questions and structured tabular data. Large language models (LLMs) have shown impressive capabilities in natural language understanding and generation, but they often struggle with large tables due to their limited input length. In this paper, we propose TabSQLify, a novel method that leverages text-to-SQL generation to decompose tables into smaller and relevant sub-tables, containing only essential information for answering questions or verifying statements, before performing the reasoning task. In our comprehensive evaluation on four challenging datasets, our approach demonstrates comparable or superior performance compared to prevailing methods reliant on full tables as input. Moreover, our method can reduce the input context length significantly, making it more scalable and efficient for large scale table reasoning applications. Our method performs remarkably well on the WikiTQ benchmark, achieving an accuracy of 64.7%. Additionally, on the TabFact benchmark, it achieves a high accuracy of 79.5%. These results surpass other LLM-based baseline models on gpt-3.5-turbo (chatgpt). TabSQLify can reduce the table size significantly alleviating the computational load on LLMs when handling large tables without compromising performance.


## Code 



## Citation

If you want to cite our papers, please use:

```bibtex
@inproceedings{nahid2024tabsqlify,
title={Tab{SQL}ify: Enhancing Reasoning Capabilities of {LLM}s Through Table Decomposition},
author={Md Mahadi Hasan Nahid and Davood Rafiei},
booktitle={2024 Annual Conference of the North American Chapter of the Association for Computational Linguistics},
year={2024},
url={https://openreview.net/forum?id=nmX0MjIs2H}
}
```
