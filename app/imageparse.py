import base64
from openai import OpenAI
import json


class ImageParse:
    """
    ref to image input: https://platform.openai.com/docs/guides/vision
    """

    def __init__(self,image) -> None:
        self._client = OpenAI()
        self._base64_image=base64.b64encode(image.read()).decode('utf-8')
       

    def parse(self):
        response = self._client.chat.completions.create(
            model="gpt-4o",
            messages= [
                {"role": "system", "content": "The meter_number is a printed serial number"},
                {"role": "system", "content": "The counting number is a six digit number separated by line delimiter"},
                {"role": "system", "content": "each digit of the counting_number is printed on top of a rotating wheel"},
                {"role": "system", "content": "The required_response is a json format including meter_number counting_number"},
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "Analyze the image and give me the required_response"
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{self._base64_image}"
                    }
                    }
                ]
                }
            ],
            max_tokens=300
        )
        answer = response.choices[0].message.content
        try:
            ret_json=answer.split('json')[1].split('}')[0]+'}'
            self._readings=json.loads(ret_json)
            self._ok=True
        except:
            self._ok=False

    def isOK(self):
        return self._ok
    
    def getReadings(self):
        return self._readings
    
    def save(self):
        return self._base64_image



