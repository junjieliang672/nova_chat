# How to use litellm to host a ollama model

1. Install `litellm` from the `requirements.txt` file.
1. Download the ollama model from the mac machine by running `ollama run orca2`. This by default will download the 7b version of orca2.
1. Run the following to host the ollama model `litellm --model orca2`. Wait a bit and you will see a url for the hosted model.
1. To use the model, in any llm application, whenever it asks for `base_url`, provide the url obtained from the previous step. Whenever it asks for `api_key`, use `null` or `anything`.

