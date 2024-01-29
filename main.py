
from PIL import Image
import base64
import io
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
from typing import Union
from fastapi import FastAPI, UploadFile
import uvicorn
from langchain.schema import HumanMessage
from langchain_community.chat_models import BedrockChat
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator




app = FastAPI()
# app = Flask(__name__)
def process_image_with_cpu_model(image):
    processor = BlipProcessor.from_pretrained("./model")
    model = BlipForConditionalGeneration.from_pretrained("./model")
    # raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    answer = processor.decode(out[0], skip_special_tokens=True)
    
    return answer

chat = BedrockChat(model_id="anthropic.claude-instant-v1", model_kwargs={"temperature": 0.1})

# Define your desired data structure.
class tags(BaseModel):
    #id: str = Field(description="pictures_id")
    tags: List[str] = Field(description="pictures_tags")
    # You can add custom validation logic easily with Pydantic.


def output_tags(sum) :
# And a query intented to prompt a language model to populate the data structure.
    tags_query = "extract the main word in sentence"+sum
# Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=tags)
    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | chat | parser
    return chain.invoke({"query": tags_query})

@app.post("/upload")
async def create_upload_file(file: UploadFile):
    try:
        print("test")
        # image_data = request.form['image'].split(',')[1]
        image_data = await file.read()
        print("Received image data:", image_data)
        image = Image.open(io.BytesIO(image_data))
        # image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        result_caption = process_image_with_cpu_model(image)
        answer= output_tags(result_caption)
        return answer
    except Exception as e:
        print("Error:", str(e))
        return str(e)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port = 8000)