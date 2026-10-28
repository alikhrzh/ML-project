# Deploy NU Club Finder on Streamlit Community Cloud

The repository already has the expected root-level entrypoint (`app.py`) and
dependency file (`requirements.txt`). The recommended deployment target is
Streamlit Community Cloud because it runs the existing interface directly.

## Before deployment

1. Run `python -m unittest discover -s tests` locally.
2. Run `streamlit run app.py` and confirm that the model downloads complete.
3. Push the reviewed commit to a public GitHub branch.
4. Do not configure `NU_CLUB_ANALYTICS_URL` unless the destination is owned and
   documented by the project. Search sharing remains opt-in in the interface.

## Community Cloud settings

1. Open <https://share.streamlit.io> and select **Create app**.
2. Choose repository `alikhrzh/ML-project` and the reviewed branch.
3. Set the entrypoint to `app.py`.
4. In advanced settings, select Python 3.11 to match `runtime.txt`.
5. Deploy and wait for the initial model downloads to finish.

If the build exceeds the platform's resource limits, remove unused heavyweight
dependencies first, then consider a smaller embedding/translation path. Do not
claim the deployment is public until its URL opens in a signed-out browser.

## Verification checklist

- English and Russian queries both return five club cards.
- Interest filters change the ranking.
- Social links open the expected club pages.
- The app loads in a signed-out browser without an authentication redirect.
- The final public URL replaces `[TODO: public demo URL]` in the README and
  profile README.

Official references:

- <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy>
- <https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies>
