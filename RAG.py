import os
from flask import Flask
from flask_restx import Resource, Api, fields
from dotenv import load_dotenv
import chromadb
from openai import AzureOpenAI
load_dotenv()
storage_path=os.getenv("STORAGE_PATH")
chroma_client = chromadb.PersistentClient(path=storage_path)
load_dotenv()
client = AzureOpenAI(
  api_key = os.getenv("AZURE_API_KEY"),  
  api_version = os.getenv('AZURE_API_VERSION'),
  azure_endpoint =os.getenv('AZURE_API_BASE_PATH')
)

def get_embeddings(text_chunks):
    embeddings = []
    for chunk in text_chunks:
        response = client.embeddings.create(
            input=chunk,
            model="text-embed-ada-east-us2" 
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

collection = chroma_client.get_collection(
    name="pdf_embeddings"
)

app = Flask(__name__)
api = Api(app)

question_model = api.model('Question', {
    'question': fields.String(required=True, description='Ask the question')
})

def answer_question(question, top_chunks):
    context = '\n\n'.join([' '.join(chunk) for chunk in top_chunks])
    prompt = [
        {
            "role": "system",
            "content": f"Assistant is an intelligent chatbot designed to help users. Only answer questions using the context below and if you're not sure of an answer, you can say 'I don't know'.\n\nContext:\n{context}"
        },
        {
            "role": "user",
            "content": question
        }
    ]
    
    response = client.chat.completions.create(
        messages=prompt,
        max_tokens=150,
        model="aoai-gpt-35-4k-genai"
    )
    return response.choices[0].message.content.strip()


@api.route('/qna')
class QnA(Resource):

    @api.expect(question_model)
    def post(self):

        data = api.payload
        question = data.get("question")
        top_n = 3

  
        query_embedding = get_embeddings([question])[0]

  
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_n
        )

        top_chunks = [result for result in results['documents']]
        
        answer = answer_question(question, top_chunks)

        return {'Answer': answer}

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)