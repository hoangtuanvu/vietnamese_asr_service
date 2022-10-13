import io
from typing import Union
import torch
import soundfile as sf
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


class ASRModel():
    def __init__(self,
                 pretrained_token: str = "app/pretrained_models/snapshots/69e9000591623e5a4fc2f502407860bcdc0de0b2/",
                 pretrained_asr: str = "app/pretrained_models/snapshots/69e9000591623e5a4fc2f502407860bcdc0de0b2/"):
        """Loads pretrained Vietnamese tokenizer and asr based-model.

        Args:
            pretrained_token (str, optional): Path to the pretrained tokenizer. Defaults to "./pretrained_models".
            pretrained_asr (str, optional): Path to the pretrained asr model. Defaults to "./pretrained_models".
        """
        super().__init__()

        self.processor = self.load_processor(pretrained_token)
        self.asr_model = self.load_model(pretrained_asr)

    @staticmethod
    def load_processor(pretrained_token):
        return Wav2Vec2Processor.from_pretrained(pretrained_token)

    @staticmethod
    def load_model(pretrained_asr):
        return Wav2Vec2ForCTC.from_pretrained(pretrained_asr)

    def infer(self, audio: Union[bytes, str]) -> str:
        """Transform audio in both bytes or string format (audio path) 
        to text.

        Args:
            audio (Union[bytes, str]): raw audio in both formats

        Returns:
            _type_(str): transformed text
        """
        if isinstance(audio, str):
            speech_np, _ = sf.read(audio)
        else:
            speech_np, _ = sf.read(io.BytesIO(audio))

        # tokenize with batchsize = 1
        input_values = self.processor(speech_np,
                                      return_tensors="pt",
                                      padding="longest").input_values

        # retrieve logits
        logits = self.asr_model(input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)

        return transcription[0]


if __name__ == "__main__":
    # Do some testing cases
    model = ASRModel()
    text = model.infer('./audio_samples/t1_0001-00010.wav')

    print(text)
