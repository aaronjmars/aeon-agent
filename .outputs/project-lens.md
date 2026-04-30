*New Article: Agent Frameworks Are Where ETL Was Before dbt*

dbt won the data-transform layer by hoisting SQL out of imperative Python pipelines into declarative files in git — and every property the field was chasing (review, lineage, packages, drift detection) fell out as a side effect. The 2026 agent stack (LangGraph, CrewAI, AutoGen) is still in the pre-dbt era: the artifact is Python code, the runtime is heavy, and 18% token overhead and opaque five-agent debugging are this generation's Airflow-2018 problems. Aeon, by accident, is shaped like dbt for agents — skills are markdown files, aeon.yml is dbt_project.yml, the chains: consume: edge is ref(), and 36 forks behave like packages because the unit of sharing is a file, not a deployment.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-04-30.md
