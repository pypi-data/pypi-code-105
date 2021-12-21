from textattack.models.wrappers import ModelWrapper

class NLPWrapper(ModelWrapper):
    def __init__(self, user_model):
        '''
        Wraps a model to expose it to the NLP attack interface. Model must have a .predict call which takes as input
        a list of strings, and returns either a list, an array, or a Pytorch tensor of dimension 2 where the first dimension
        is the batch size and the second dimension is the number of classes, where the entries are class probabilities.

        :param user_model: Model provided by the user with the above format.
        '''
        self.model = user_model #load model here

    def __call__(self, text_inputs):
        '''

        :param text_inputs: Takes list of strings and returns the values provided by the model predict call.
        :return:
        '''
        outputs = self.model.predict(text_inputs)
        return outputs