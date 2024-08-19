from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/Sanket-Kathrotiya/Electricity-Demand-Prediction.git",
        entrypoint="2-Orchestration/orchestrate.py:main_flow",
    ).deploy(
        name="Electricity Demand Prediction Deployment",
        work_pool_name="zoompool",
        cron="0 1 * * *",
    )
