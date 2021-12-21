from ..attacks.ARTAttacks import LpAttack
from ..metrics.metric_utils import compute_Lp_distance
from ..evaluators import RobustnessEvaluatorBase, AbstractEvaluationCallback
from trojai.attacks.VisionAttacksPytorch import AbstractVisionAttack
import numpy as np

#TODO make the robustness evaluation classes work with the base evaluator class

class ClassifierRobustnessEvaluator:
    def __init__(
        self, classifier, attack, attack_name, attkwargs={}, use_model_preds=False
    ):
        """
        The simple robustness evaluator class. Should be used to form a baseline.

        :param classifier: TrojClassifier/ART Classifier instance
        :param attack: undeclared ART evasion class, or declared Troj attack.
        :param attack_name: Name for logging
        :param **attkwargs: keyword arguments for attack.
        """
        self.atk_meta = attkwargs
        self.classifier = classifier
        if issubclass(type(attack), AbstractVisionAttack):
            self.attacker = attack
        else:
            self.attacker = LpAttack(self.classifier, attack, use_model_preds, **attkwargs)
        self.atk_meta["name"] = attack_name

    def attack(self, data, target, index, device=None):
        """
        Runs the attack.

        :param data: Input data
        :param target: Target labels
        :param index: Index of samples in dataframe
        :param device: If using Pytorch, one can specify the device.
        :return: A dictionary containing the minimum perturbation, the loss, adversarial loss, prediction, and adversarial
        prediction for each sample, along with a list of indices for the logging function.
        """

        # send data and target to cpu, convert to numpy
        data = np.ascontiguousarray(data.astype(np.float32))
        test_loss, preds = self.classifier.ComputeLoss(data, target)
        preds = np.argmax(preds, axis=1)
        #check if attack is a Troj vision attack. This is used to support transformation based attacks.
        if issubclass(type(self.attacker), AbstractVisionAttack):
            adv_x, loss_dicts = self.attacker.generate(data, target)
            #Currently hardcoded for transformation attacks
            adv_loss = np.asarray([loss_dicts[i]['transformed_loss'][0] for i in range(len(loss_dicts))])
            adv_preds = self.classifier.predict(adv_x)
            adv_x = np.asarray(adv_x)
        else:
            adv_x, adv_preds, adv_loss = self.attacker.generate(data, target)
        # adv_loss, adv_preds = self.classifier.ComputeLoss(adv_x, target)
        perturbation = compute_Lp_distance(data, adv_x)
        adv_pred = np.argmax(adv_preds, axis=1)
        # generate the adversarial image using the data numpy array and label numpy array
        out_dict = {
            "Linf_perts": perturbation,
            "Loss": test_loss,
            "Adversarial_Loss": adv_loss,
            "prediction": preds,
            "Adversarial_prediction": adv_pred,
        }
        return (index, out_dict)


class ModelPredictionsCallback(AbstractEvaluationCallback):
    def __init__(self, classifier, return_probs=True):
        '''
        Builds a simple callback for evaluating the predictions of a classifier.


        :param classifier: an instance of a Troj classifier.
        :param return_probs: Whether to return probabilities or hard predictions.
        '''
        self.classifier = classifier
        self.return_probs = return_probs

    def run_on_batch(self, data, target, index):
        '''

        :param data: Array of samples.
        :param target: Array of labels.
        :param index: Indices in dataframe.
        :return: Indices and predictions.
        '''
        outs_dict = {}
        data = np.ascontiguousarray(data.astype(np.float32))
        test_loss, preds = self.classifier.ComputeLoss(data, target)
        hard_preds = np.argmax(preds, axis=1)
        outs_dict['Loss'] = test_loss
        outs_dict['Preds'] = hard_preds
        if self.return_probs == True:
            outs_dict['pred_probs'] = preds.tolist()
        return (index,outs_dict)


def classification_adversarial_evaluator_builder(classifier, attack, attack_name, attkwargs, use_model_preds=False):
    '''

    :param classifier: A troj classifier
    :param attack: An uninstantiated ART attack.
    :param attack_name: The name of the attack for logging.
    :param attkwargs: Any keyword arguments when intializing the attack.
    :param use_model_preds: Whether to use the true labels or the clean model predictions.
    :return: An evaluator which uses the specified attack.
    '''
    call = ClassifierRobustnessEvaluator(classifier, attack, attack_name, attkwargs, use_model_preds)
    evaluator = RobustnessEvaluatorBase(None, [call.attack], [{}])
    return evaluator