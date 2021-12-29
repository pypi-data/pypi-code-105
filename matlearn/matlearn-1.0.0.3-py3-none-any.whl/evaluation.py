import numpy as np

def regularization(w, type='L2', alpha=.00001, jac=False):
    """Used to set a penalty the model. 

    Args:
        w (Array): Weight matrix.
        type (str, optional): Choose between L1 and L2 Regularization. Defaults to 'L2'.
        alpha ([Float,integer], optional): Alpha hyperparameter. Used to Adjust the importance of the penalty. Defaults to .00001
        jac (bool, optional): If True, Jacobian version of regularization will be returned. Defaults to False.

    Raises:
        ValueError: if invalid value is provided as "type". only [L1, L2] is supported.

    Returns:
        Float
    """
    type = type.upper()
    if type == 'L2':
        if not jac:
            if w.ndim > 1:
                return alpha * (w.T @ w)[0, 0]
            return alpha * np.sum(np.square(w))
        return alpha * w
    elif type == 'L1':
        return alpha * np.sum(np.abs(w))
    else:
        raise ValueError(f"{type} is not supported. only [L1, L2] is supported.")



class Loss:
    """Contains Loss functions for machine learning models.
    List of loss functions currently available: {Mean sqaured error, binary cross entropy, cross entropy}
    """
    @classmethod
    def _use_app_loss(cls, app_loss):

        if app_loss == 'mse':
            return cls.mse
        elif app_loss == 'binary_cross_entropy':
            return cls.binary_cross_entropy
        elif app_loss == 'multi_class_cross_entropy':
            return cls.multi_class_cross_entropy

    @staticmethod
    def mse(p, y,vectorized=True):
        """Mean Squared Error loss function.

        Args:
            p (Array): Predicted value.
            y (Array): Target value.
            vectorized (bool, optional): If True, vectorized version of MSE is used. Defaults to True.

        Returns:
            float
        """
        dls = np.average((np.square(p - y)))
        if vectorized:
            dls = 1/len(y) * ((p - y).T @ (p - y))[0, 0]
        return dls

    @staticmethod
    def binary_cross_entropy(p, y):
        """binary cross entropy loss function for binary classification.

        Args:
            p (Array): Predicted value.
            y (Array): Target value.

        Returns:
            Float
        """
        return np.average((-y * np.log(p))-((1-y)*np.log(1 - p)))

    @staticmethod
    def multi_class_cross_entropy(p, y):
        """Cross entropy loss function for binary or multiclass classification.

        Args:
            p (Array): Predicted value.
            y (Array): Target value.

        Returns:
            Float
        """
        m = y.shape[0] 
        return  np.average(-y * np.log(p[range(m),y]))


