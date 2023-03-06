## I found myself waiting a long time for the train to arrive, so I made a Streamlit app to track train arrival times

This project is inspired by the great works of CommutersTakeAction, a Chicago local public transit activist group.
[CommutersTakeAction](https://linktr.ee/commuterstakeaction)

My streamlit app for tracking [Blueline Arrivals](https://kollerbud-cta-gcp-appapp-95pnfi.streamlit.app/).

<div>
    <img alt="Version" src="https://img.shields.io/badge/Project Number-1-orange.svg?cacheSeconds=2592000" />
</div>

App URL: <https://kollerbud-cta-gcp-appapp-95pnfi.streamlit.app/>

## Data Pipeline

## Data Pipeline Flowchart

## Tech stack & Cloud Services
* API: [CTA_API](https://www.transitchicago.com/developers/)
* Scheduler: [Cloud Scheduler](https://cloud.google.com/scheduler)
* Serverless Container: [Cloud Run](https://cloud.google.com/run)
* Data warehouse: [Bigquery](https://cloud.google.com/bigquery)
* Visualization: [Streamlit](https://docs.streamlit.io/)
* CI/CD: Github-Actions/gcloud CLI
* local deployment:
    * Container: docker
    * testing: pytest
