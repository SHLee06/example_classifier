
from allennlp.data import Instance
from allennlp.common.util import JsonDict
from allennlp.predictors import Predictor
from typing import List
from overrides import overrides
import json
from ..utils import LABEL_TO_INDEX


@Predictor.register('example_predictor')
class ExamplePredictor(Predictor):
    @overrides
    def predict_json(self, inputs: JsonDict) -> str:
        probs = self.predict_probs(inputs)
        return {'text': inputs['text'], 'probs': probs}

    def predict_probs(self, inputs: JsonDict):
        """
        Args:
            inputs: a dictionary containing two keys
                (1) word (optional)
                (2) definition: need to be tokenized

        Returns:
            def_embeds: definition embeddings, a list consists of 300 floating points
        """
        instance = self._json_to_instance(inputs)
        output_dict = self.predict_instance(instance)
        probs = output_dict['probs'][LABEL_TO_INDEX['positive']]
        return probs

    @overrides
    def predict_batch_json(self, inputs: List[JsonDict]) -> List[str]:
        instances = self._batch_json_to_instances(inputs)
        output_dicts = self.predict_batch_instance(instances)
        results = []
        for inp, od in zip(inputs, output_dicts):
            results.append({'text': inp['text'], 'probs': od['probs'][0]})
        return results

    @overrides
    def _batch_json_to_instances(self, json_dicts: List[JsonDict]) -> List[Instance]:
        instances = []
        for json_dict in json_dicts:
            instances.append(self._json_to_instance(json_dict))
        return instances

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        text = json_dict['text']
        return self._dataset_reader.example_to_instance(text=text, label=None)

    @overrides
    def dump_line(self, outputs: JsonDict) -> str:
        return json.dumps(outputs) + '\n'