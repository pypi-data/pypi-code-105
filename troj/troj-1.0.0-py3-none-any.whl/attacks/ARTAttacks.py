from art.attacks.evasion import FastGradientMethod
from ..metrics import true_min_pert
import numpy as np


class LpAttack:
    def __init__(self, model, attack, use_model_preds=False, **attkwargs):
        """
        Makes a classifier L^p attacker instance from an ART evasion attack.

        :param model: TrojClassifier class instance.
        :param attack: an undeclared instance of an ART evasion attack i.e art.evasion.pgd
        :param attkwargs: keyword arguments for the attack
        """
        self.model = model
        attack_dict = {}
        att_name = "attack"
        attack_dict[att_name] = attack(model, **attkwargs)
        self.attack_dict = attack_dict
        self.use_model_preds = use_model_preds

    def generate(self, x, y):
        """
        Generates adversarial examples from the sample and label arrays.

        :param x: inputs
        :param y: labels, either true labels or original unperturbed model labels.
        :return: adversarial examples with minimal perturbation, adversarial losses, adversarial predictions
        """
        generated_examples = []
        model_adv_losses = []
        model_adv_preds = []
        # For each attack method in the attack dictionary, generate adversarial examples, then compute the loss
        # and the class predictions.
        for attacker in list(self.attack_dict.values()):
            adv_x = attacker.generate(x, y)
            if len(y.shape) == 1:
                adv_losses, adv_preds = self.model.ComputeLoss(adv_x, y)
                if self.use_model_preds == True:
                    true_losses, true_preds = self.model.ComputeLoss(x, y)
            else:
                adv_losses, adv_preds = self.model.ComputeLoss(
                    adv_x, np.squeeze(y, axis=1)
                )
                if self.use_model_preds == True:
                    true_losses, true_preds = self.model.ComputeLoss(
                        x, np.squeeze(y, axis=1)
                    )
            model_adv_losses.append(adv_losses)
            generated_examples.append(adv_x)
            model_adv_preds.append(adv_preds)
        # reshape arrays so that they each have shape [batch_size, num_attacks, *]
        generated_examples = np.stack(generated_examples)
        generated_examples = np.swapaxes(generated_examples, 0, 1)

        model_adv_losses = np.stack(model_adv_losses)
        model_adv_losses = np.swapaxes(model_adv_losses, 0, 1)

        model_adv_preds = np.stack(model_adv_preds)
        model_adv_preds = np.swapaxes(model_adv_preds, 0, 1)

        # Whether or not to compute the perturbations quickly, or in such a way as to minimize
        # the perturbation that flips the label.
        if self.use_model_preds == True:
            labels = true_preds
        else:
            labels = y
        output, preds, losses = true_min_pert(
            labels, model_adv_preds, x, generated_examples, model_adv_losses
        )

        return output, preds, losses
