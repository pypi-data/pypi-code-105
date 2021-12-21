from trojai.attacks.VisionAttacksPytorch import *
from trojai.corruptions.Transformations import transform_dict
from trojai.corruptions import corruption_class_builder

att_dict = {'FGSM':GenericFGSM, 'MomentumPGD':MomentumPGD, 'AdaptivePGD':AdaptivePGD, 'EoT':EoTPytorch}
corrupt_dict = {'GaussianNoise':corruption_class_builder('gaussian_noise'), 'ImpulseNoise':corruption_class_builder('impulse_noise'),
                'ShotNoise':corruption_class_builder('shot_noise'), 'DefocusBlur':corruption_class_builder('defocus_blur'),
                'GlassBlur':corruption_class_builder('glass_blur'), 'MotionBlur':corruption_class_builder('motion_blur'),
                'ZoomBlur':corruption_class_builder('zoom_blur'), 'GaussianBlur':corruption_class_builder('gaussian_blur'),
                'Snow':corruption_class_builder('snow'), 'Frost':corruption_class_builder('frost'), 'Fog':corruption_class_builder('fog'),
                'Brightness':corruption_class_builder('brightness'), 'Contrast':corruption_class_builder('contrast'), 'ElasticTransform':corruption_class_builder('elastic_transform'),
                'Pixelate':corruption_class_builder('pixelate'), 'JPEGCompress':corruption_class_builder('jpeg_compress'), 'SpeckleNoise':corruption_class_builder('speckle_noise'),
                'Spatter':corruption_class_builder('spatter'), 'Saturate':corruption_class_builder('saturate')
                }

transformation_dict = {**transform_dict, **corrupt_dict}




def BuildAttack(model, attack_params):
    '''
    Builds an attack from a model and a dictionary containing the name of the attack as the key and the value as a dictionary
    with keyword arguments.

    :param model:
    :param attack_params:
    :return:
    '''
    if list(attack_params.keys())[0] in att_dict:
        attack = att_dict[list(attack_params.keys())[0]](model, **list(attack_params.values())[0])
    elif list(attack_params.keys())[0] in transformation_dict:
        attack = TransformationAttackWrapper(model, attack_params)
    return attack


