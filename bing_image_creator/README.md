# Usage Examples: Bing Image Creator
```bash
pip install git+https://github.com/meap158/bing_image_creator_dalle3_batch
```

---
## From Another File (as a package):
```python
import os
from bing_image_creator import BingImageCreator

prompt = "a giant fish in the cloud, realistic"
cookie = os.environ["bing_cookie"]

image_creator = BingImageCreator(prompt,
                                 save_folder=".",
                                 cookie_value=cookie)
image_creator.run()
```

---
## From Command Line

#### *Single Prompt Example*:
```bash
bing_image_creator "a giant fish in the cloud, realistic" --cookie_value <your_cookie_value> --save_folder .
```

#### *Multiple Prompts Example*:
```bash
bing_image_creator "prompt 1" "prompt 2" --cookie_value <your_cookie_value> --save_folder .
```
