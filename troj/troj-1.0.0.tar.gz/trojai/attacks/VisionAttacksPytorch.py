import torch
import random
from trojai.corruptions import TorchCorrupt
import trojai.corruptions.Transformations
import numpy as np
from abc import ABC, abstractmethod

class AbstractVisionAttack(ABC):
    '''
    Abstract base class for all vision attacks.

    '''
    @abstractmethod
    def generate(self, x, y):
        pass

class GenericFGSM(AbstractVisionAttack):
    def __init__(self, model, epsilon=0.1, alpha=0.03, num_iter=25, loss_kwarg_dict={}):
        '''

        :param model: an instance of a model.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param num_iter: Number of steps

        '''
        #TODO allow user to pick certain losses from the model loss dictionary to maximize.
        assert hasattr(model, 'compute_loss')
        assert hasattr(model, 'predict')
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.num_iter = num_iter
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''

        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial loss and final loss)

        :return: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True

        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val)>0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict)
                    loss.backward(retain_graph=True)
                    delta.data = (delta + x.shape[0] * self.alpha * delta.grad.data).clamp(-self.epsilon, self.epsilon)
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts


class MomentumPGD(AbstractVisionAttack):
    def __init__(self, model, epsilon=0.1, alpha=0.03, beta=0.99, num_iter=25, loss_kwarg_dict={}):
        '''
        PGD with momentum.

        :param model: an instance of a generic model.
        :param epsilon: Maximum allowable perturbation.
        :param beta: Momentum constant.
        :param alpha: Step size
        :param num_iter: Number of steps

        '''
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.beta = beta
        self.num_iter = num_iter
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''

        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial loss and final loss)

        :return: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True

        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val)>0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                prev_delta = 0
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict)
                    loss.backward(retain_graph=True)
                    delta.data = (self.beta*(delta + x.shape[0] * self.alpha * delta.grad.data)+(1-self.beta)*prev_delta).clamp(-self.epsilon, self.epsilon)
                    prev_delta = delta.grad.data
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts


class AdaptivePGD(AbstractVisionAttack):
    def __init__(self, model, epsilon=0.1, alpha=0.03, beta=0.99, reduction_thresh=0.5, reduction_rate=2, patience=5, num_iter=25, loss_kwarg_dict={}):
        '''
        PGD with momentum and adaptive step size.

        :param model: an instance of a PytorchObjectDetector object.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param beta: Momentum constant.
        :param reduction_thresh: If the difference between the previous loss and the newest loss is less than the threshhold,
        the stepsize alpha is reduced by 1/reduction_rate.
        :param reduction_rate: The denominator of the reduction value.
        :param patience: Number of iterations to wait before reducing,
        :param num_iter: Number of steps

        '''
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.beta = beta
        self.reduction_thresh = reduction_thresh
        self.reduction_rate = reduction_rate
        self.num_iter = num_iter
        self.patience = patience
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''

        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial loss and final loss)

        :return: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True

        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            wait = 0
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val) > 0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                prev_loss = init_loss
                reduct = 1
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                prev_delta = 0
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict)
                    loss.backward(retain_graph=True)
                    delta.data = (self.beta * (delta + x.shape[0] * (self.alpha / reduct) * delta.grad.data) + (
                                1 - self.beta) * prev_delta).clamp(-self.epsilon, self.epsilon)
                    prev_delta = delta.grad.data
                    cur_loss = loss.item()
                    if cur_loss - prev_loss < self.reduction_thresh:
                        wait += 1
                        if wait>=self.patience:
                            reduct = reduct * self.reduction_rate
                    else:
                        wait=0
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts


class EoTPytorch(AbstractVisionAttack):
    def __init__(self, model, augmentation_dict, num_queries, device=None):
        #TODO can we make this faster
        '''
        Runs a version of an Expectation over Transformation attack.

        :param model: Model of generic type.
        :param augmentation_dict: A dictionary containing augmentation names, where the values are lists contain allowable severity values.
        :param num_queries: How many times to randomly apply transformations to each sample.
        :param mode:
        '''
        self.model=model
        self.augmentations = augmentation_dict
        self.num_queries = num_queries
        self.device = device
        if device is None:
            self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        #TODO in generic output parser block perturbation norms for certain attacks

    def GenerateCorruptions(self, x, y):
        '''
        Generates num_queries corrupted versions of x by randomly sampling from the augmentation dict.

        :param x: Input tensor
        :param y: Label dict
        :return: List of corrupted tensors, and list of corresponding labels.
        '''
        augs_list = list(self.augmentations.keys())
        ims_list = []
        labels_list = []
        corruption_info = []
        for i in range(self.num_queries):
            augment = random.choice(augs_list)
            severity = random.choice(self.augmentations[augment])
            corrupted = TorchCorrupt(x, severity, augment)
            ims_list.append(corrupted.to(self.device))
            labels_list.append(y)
            corruption_info.append((augment, severity))
        return ims_list, labels_list, corruption_info

    def corruption_losses(self,X,Y):
        '''
        Computes loss on individual corrupt samples. Used to find the strongest transformation on a given sample, and the
        expected loss.

        :param X: List of corrupted versions of a sample.
        :param Y: Set of labels for the sample.
        :return: the losses on the set X.
        '''
        losses = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            loss = self.model.compute_loss([x], [y], grad=False).detach().cpu().numpy()
            losses.append(loss)
        return losses

    def loss_parser(self, corr_losses):
        '''
        Parses the output of corruption_losses.

        :param corr_losses: Corruption losses returned by corruption_losses
        :return: the mean loss over the transformations, the max loss, and the argument for the max loss.
        '''
        mean_loss = np.mean(corr_losses)
        max_loss_arg = np.argmax(corr_losses)
        max_loss = corr_losses[max_loss_arg]
        return mean_loss, max_loss, max_loss_arg

    def generate(self, X, Y,):
        #TODO note that loss_dicts can return any information about a sample
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            loss_dict = {}
            x = X[idx]
            y = Y[idx]
            corrupt_ims, labels, info = self.GenerateCorruptions(x,y)
            init_loss = self.model.compute_loss([x], [y], grad=False)
            corrupt_losses = self.corruption_losses(corrupt_ims, labels)
            mean, max_, max_arg = self.loss_parser(corrupt_losses)
            adv_X.append(corrupt_ims[max_arg])
            loss_dict['initial_loss'] = init_loss.item()
            loss_dict['EoT_loss'] = mean
            loss_dict['max_loss'] = max_
            loss_dict['max_corruption'] = info[max_arg][0]
            loss_dict['max_corruption_svserity'] = info[max_arg][1]
            loss_dicts.append(loss_dict)
        return adv_X, loss_dicts


class TransformationAttackWrapper(AbstractVisionAttack):
    def __init__(self, model, transformation , device=None):
        '''
        Wraps image transformations into an attack.

        :param model:
        :param transformation: Either a dictionary containing a single transformation name as the key with the value
        being a set of keyword arguments. Or, a transformation which takes in an input tensor and returns an input tensor.
        '''
        self.model = model
        if type(transformation)==dict:
            self.transform = self.build_transformation(transformation)
        else:
            self.transform = transformation
        self.device = device

    def build_transformation(self, t_dict):
        '''
        Builds transformation from the appropriate dictionary.

        :param t_dict:
        :return:
        '''
        name = list(t_dict.keys())
        transform = trojai.corruptions.Transformations.transform_dict[name](t_dict[name])
        return transform


    def generate(self, X, Y):
        '''

        :param X: List of input samples
        :param Y: List of labels
        :return: list of transformed samples and loss dictionaries.
        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            loss_dict = {}
            x = X[idx]
            y = Y[idx]
            transformed = self.transform(x)
            if self.device !=None:
                transformed = transformed.to(self.device)
            if hasattr(self.model, 'ComputeLoss'):
                init_loss = self.model.ComputeLoss(np.asarray([x]), np.asarray([y]))
                transformed_loss = self.model.ComputeLoss(np.asarray([transformed]), np.asarray([y]))

            else:
                init_loss = self.model.compute_loss([x], [y], grad=False)
                transformed_loss = self.model.compute_loss([transformed], [y], grad=False)
            adv_X.append(transformed)
            loss_dict['initial_loss'] = init_loss
            loss_dict['transformed_loss'] = transformed_loss
            loss_dicts.append(loss_dict)
        return adv_X, loss_dicts


class BasicCWStyle(AbstractVisionAttack):
    def __init__(self, model, epsilon=0.1, alpha=0.03, tradeoff=0.5, num_iter=25, p=2, loss_kwarg_dict = {}):
        '''
        A simplified version of the Carlini-Wagner attack generalized for generic models. Normally a beam/binary
        search is carried out over the tradeoff parameter to find the minimum perturbation which would cause a misclassification,
        however since these attacks are meant for generic models, we cannot directly perform this beam search, so we take the tradeoff as a fixed parameter.
        However, it still will work  for finding adversarial examples with a lower perturbation while still achieving a high loss.

        :param model:
        :param epsilon:
        :param alpha:
        :param tradeoff:
        :param num_iter:
        :param p:
        :param loss_kwarg_dict:
        '''
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.tradeoff = tradeoff
        self.num_iter = num_iter
        self.p = p
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''

        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial loss and final loss)
        :return: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True
        '''

        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val) > 0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict) - self.tradeoff*torch.norm(delta, p=self.p)
                    loss.backward(retain_graph=True)
                    delta.data = (delta + x.shape[0] * self.alpha * delta.grad.data).clamp(-self.epsilon, self.epsilon)
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
            return adv_X, loss_dicts



class AdaptiveCWStyle(AbstractVisionAttack):
    def __init__(self, model, epsilon=0.1, alpha=0.03, beta=0.99, reduction_thresh=0.5, reduction_rate=2, patience=5, num_iter=25, tradeoff=0.1, p=2, loss_kwarg_dict={}):
        '''
        A simplified version of the Carlini-Wagner attack generalized for generic models, which has an adaptive step size and momentum. Normally a beam/binary
        search is carried out over the tradeoff parameter to find the minimum perturbation which would cause a misclassification,
        however since these attacks are meant for generic models, we cannot directly perform this beam search, so we take the tradeoff as a fixed parameter.
        However, it still will work  for finding adversarial examples with a lower perturbation while still achieving a high loss.

        :param model: an instance of a model.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param beta: Momentum constant.
        :param reduction_thresh: If the difference between the previous loss and the newest loss is less than the threshhold,
        the stepsize alpha is reduced by 1/reduction_rate.
        :param reduction_rate: The denominator of the reduction value.
        :param patience: Number of iterations to wait before reducing,
        :param num_iter: Number of steps

        '''
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.beta = beta
        self.reduction_thresh = reduction_thresh
        self.reduction_rate = reduction_rate
        self.num_iter = num_iter
        self.patience = patience
        self.tradeoff = tradeoff
        self.p = p
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''

        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial loss and final loss)

        :return: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True

        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            wait = 0
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val) > 0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                prev_loss = init_loss
                reduct = 1
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                prev_delta = 0
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict) - self.tradeoff*torch.norm(delta, p=self.p)
                    loss.backward(retain_graph=True)
                    delta.data = (self.beta * (delta + x.shape[0] * (self.alpha / reduct) * delta.grad.data) + (
                                1 - self.beta) * prev_delta).clamp(-self.epsilon, self.epsilon)
                    prev_delta = delta.grad.data
                    cur_loss = loss.item()
                    if cur_loss - prev_loss < self.reduction_thresh:
                        wait += 1
                        if wait>=self.patience:
                            reduct = reduct * self.reduction_rate
                    else:
                        wait=0
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts