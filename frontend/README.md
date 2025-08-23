## Deploying the Streamlit App to Cloud Run

This document describes how to deploy the Streamlit application to Google Cloud Run using Google Cloud Build.

### Prerequisites

1.  **Google Cloud SDK:** Make sure you have the `gcloud` command-line tool installed and configured on your machine. You can find installation instructions [here](https://cloud.google.com/sdk/docs/install).

2.  **Enable APIs:** Ensure the following APIs are enabled for your Google Cloud project:
    *   Cloud Build API
    *   Cloud Run API
    *   Container Registry API

### Deployment Steps

1.  **Navigate to the project root directory:**

    ```bash
    cd /path/to/your/project/root
    ```

2.  **Run the Cloud Build command:**

    To trigger a build, run the following command from the root directory of the project. This command uses the `cloudbuild.yaml` file to build and deploy the application. You can override the default values for `_PROJECT_ID`, `_SERVICE_NAME`, and `_REGION` by providing them as substitutions.

    ```bash
    gcloud builds submit --config cloudbuild.yaml \
      --substitutions=_PROJECT_ID=your-gcp-project-id,_SERVICE_NAME=your-cloud-run-service-name,_REGION=your-gcp-region
    ```

    Replace the following placeholders:

    *   `your-gcp-project-id`: Your Google Cloud project ID.
    *   `your-cloud-run-service-name`: The name you want to give your Cloud Run service (e.g., `market-mirror-frontend`).
    *   `your-gcp-region`: The Google Cloud region where you want to deploy your service (e.g., `us-central1`).

    If you want to use the default values defined in the `cloudbuild.yaml` file, you can omit the `--substitutions` flag:

    ```bash
    gcloud builds submit
    ```

### Accessing the Deployed Application

Once the Cloud Build pipeline is complete, your Streamlit application will be deployed to Cloud Run. You can find the URL of your application in the output of the `gcloud builds submit` command or by navigating to the Cloud Run section of the Google Cloud Console.
