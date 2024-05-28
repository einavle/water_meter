import base64
from openai import OpenAI
import json
import io
from PIL import Image
import base64


class ImageParse:
    """
    ref to image input: https://platform.openai.com/docs/guides/vision
    """

    def __init__(self,image) -> None:
        self._client = OpenAI()
        self._base64_image=self.convertImage(image)
       

    def parse(self):
        """
         Some prompt instructions and definitions of what to encode from the image and the structure of the response.
        """
        response = self._client.chat.completions.create(
            model="gpt-4o",
            messages= [
                {"role": "system", "content": "The meter_number is a printed serial number"},
                {"role": "system", "content": "The counting_number is a six digit number separated by line delimiter"},
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
    
    def resizeImage(self,f):
        img = Image.open(f)
        img = img.resize((300, 300))
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
    
    def convertImage(self,f):
        return base64.b64encode(f.read()).decode('utf-8')



