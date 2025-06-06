from sentence_transformers import SentenceTransformer, util
from ollama import chat
from pydantic import BaseModel

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# get similarity between two topics with score between 1 - 10
def get_similarity_score(x: str, y: str):
  
  emb1 = model.encode(x, convert_to_tensor=True)
  emb2 = model.encode(y, convert_to_tensor=True)

  # Cosine similarity ranges from -1 to 1
  cosine_sim = util.cos_sim(emb1, emb2).item()

  def rescale_similarity(cosine_score):
    return round(((cosine_score + 1) / 2) * 9 + 1, 2)

  return rescale_similarity(cosine_sim)


# q&a class
class QuestionAnswer(BaseModel):
  question: str
  correct_answer: str
  wrong_answer_1: str
  wrong_answer_2: str
  website_link: str

def get_question_answer(topic, info):
  response = chat(
    messages=[
      {
        'role': 'user',
        'content': (f'Give me a verifiable factual question, 2 incorrect but possible answers, '
                    f'and 1 correct answer about {topic} specifically on {info}. Include '
                    f'a valid website link that still works so I can verify the fact.'
                    )
      }
    ],
    model='phi',
    format=QuestionAnswer.model_json_schema(),
  )

  qa_obj = QuestionAnswer.model_validate_json(response.message.content)
  return qa_obj