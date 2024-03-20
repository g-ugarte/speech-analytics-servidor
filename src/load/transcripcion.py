import torch
import os
import pandas as pd
import numpy as np
os.environ['CURL_CA_BUNDLE']=''
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, pipeline

class Transcripcion():
    def __init__(self, ruta_export):
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.type = torch.float16 if torch.cuda.is_available() else torch.float32

        self.task = "automatic-speech-recognition"
        
        try:
            self.processor =  AutoProcessor.from_pretrained(f"{ruta_export}/processor-transcript")
            print("Procesador cargado.")
        except Exception as e:
            print(e)
        
        try:
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(f"{ruta_export}/model-transcript", torch_dtype=self.type, low_cpu_mem_usage=True, use_safetensors=True)
            print("Procesador cargado.")
        except Exception as e:
            print(e)

        try:
            self.model.to(self.device)
            print("Modelo cargado a dispotivo CPU/GPU")
        except Exception as e:
            print(e)

        try:
            self.pipeline = pipeline(self.task, 
                tokenizer=self.processor.tokenizer, 
                model=self.model, 
                feature_extractor=self.processor.feature_extractor,
                max_new_tokens=128,
                chunk_length_s=30,
                batch_size=16,
                return_timestamps=True,
                torch_dtype=self.type,
                device=self.device
            )
            print("Flujo de transcripción creado.")
        except Exception as e:
            print(e)

    def transcribir(self, ruta_audio: str, idioma:str='spanish'):
        return self.pipeline(ruta_audio, generate_kwargs={'language': idioma})