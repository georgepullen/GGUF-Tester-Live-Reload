# GGML Testing Script
For tweaking model and completion parameters with a live reload functionality.

## Setup
* ```pip install -r requirements.txt```
* Add the path to your ggml model and tweak the settings in ```inference.json```

## Note
#### The ```n_ctx``` parameter will limit token output even when ```max_tokens``` is set to a higher value 
