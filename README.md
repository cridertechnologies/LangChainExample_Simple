# Querying custom data

The `upload.py` file can be used to upload the vectorized data to Pinecone. You will need to create a `.env` file with the following format:

```txt
OPENAI_API_KEY=<your_key_here>
PINECONE_API_KEY=<your_key_here>
PINECONE_ENVIRONMENT=<add_here>
PINECONE_INDEX_NAME=<index_name_here>
```

You can find your OpenAI API key by creating an account with them and [going here](https://platform.openai.com/account/api-keys). Visit the [Pinecone console](https://app.pinecone.io) for the other information.

Both require you to create accounts, but Pinecone offers a small but free tier. OpenAI does charge, but if you're just learning then it will be relatively cheap (I spent less than $1 working on this example).

# Need help?

We would love to have a conversation and see how you can best utilize Large-Language-Models like ChatGPT on your own data. Feel free to [reach out](https://cridertechnologies.com) with any questions!