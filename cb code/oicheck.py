from openai import OpenAI

client = OpenAI(api_key="sk-proj-4MgKpChcrmcg8Tkzq4wtT3BlbkFJzGClb2YgbDUOM3oXSpIX")

assistant = client.beta.assistants.create(
    name="Legal Documents Analyser and Support Assistant (LegalEase)",
    instructions="You are an expert legal analyst. Use your knowledge base to answer questions about the given legal statements.",
    model="gpt-4-turbo",
    tools=[{"type": "file_search"}],
)

vector_store = client.beta.vector_stores.create(name="Legal Documents")

filepath = "uploads/rental_agreement_template.pdf"
# Ready the files for upload to OpenAI
file_paths = [filepath]
file_streams = [open(path, "rb") for path in file_paths]

# Upload the files, add them to the vector store, and poll the status of the file batch
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

# Update the assistant with the vector store
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# Upload the user-provided file to OpenAI
message_file = client.files.create(file=open(filepath, "rb"), purpose="assistants")

# Create a chatbot loop to interact in the terminal
try:
    while True:
        user_input = input("Ask a legal question about the document (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Read the document that has been provided to you in your knowledge carefully that is the legal document on basis of which questions are being asked, so read that before you answer this or continue the conversation from before" + user_input,
                    "attachments": [{"file_id": message_file.id, "tools": [{"type": "file_search"}]}],
                }
            ]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        for message in messages:
            if message.role == "system":
                print("Assistant is thinking ...")
            elif message.role == "assistant":
                print("Assistant:", message.content[0].text.value)

finally:
    # Close all file streams
    for f in file_streams:
        f.close()

