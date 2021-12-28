# -*- coding: utf-8 -*-
# file: augment.py
# time: 2021/12/20
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os
import tqdm

from findfile import find_cwd_files, find_cwd_dirs

from pyabsa import APCCheckpointManager
from pyabsa.functional.dataset import detect_dataset, DatasetItem


def nlpaug_augment(dataset: DatasetItem):
    for f in find_cwd_files('.augment'):
        os.remove(f)
    import nlpaug.augmenter.word as naw

    checkpoint = max(find_cwd_dirs('fast_lcf_bert_{}'.format(dataset.dataset_name)))
    sent_classifier = APCCheckpointManager.get_sentiment_classifier(checkpoint=checkpoint,
                                                                    auto_device=True,  # Use CUDA if available
                                                                    )

    augmenter = naw.ContextualWordEmbsAug(
        # model_path='microsoft/deberta-v3-base', action="insert")
        model_path='roberta-base', action="substitute", device='cuda')
    dataset_files = detect_dataset(dataset, 'apc')
    valid_sets = dataset_files['valid']

    for valid_set in valid_sets:
        if '.augment' in valid_set:
            continue
        print('processing {}'.format(valid_set))
        augmentations = []
        fin = open(valid_set, encoding='utf8', mode='r', newline='\r\n')
        lines = fin.readlines()
        fin.close()
        for i in tqdm.tqdm(range(0, len(lines), 3), postfix='Augmenting...'):
            try:
                lines[i] = lines[i].strip()
                lines[i + 1] = lines[i + 1].strip()
                lines[i + 2] = lines[i + 2].strip()

                augs = augmenter.augment(lines[i].replace('$T$', '%%'), n=10, num_thread=os.cpu_count())

                for text in augs + [lines[i]]:
                    if '$ * $' in text:
                        _text = text.replace('$ * $', '[ASP]{}[ASP] '.format(lines[i + 1]), 1) + ' !sent! {}'.format(lines[i + 2])
                    elif '$*$' in text:
                        _text = text.replace('$*$', '[ASP]{}[ASP] '.format(lines[i + 1])) + ' !sent! {}'.format(lines[i + 2])
                    elif '$-$' in text:
                        _text = text.replace('$-$', '[ASP]{}[ASP] '.format(lines[i + 1])) + ' !sent! {}'.format(lines[i + 2])
                    elif '%%' in text:
                        _text = text.replace('%%', '[ASP]{}[ASP] '.format(lines[i + 1])) + ' !sent! {}'.format(lines[i + 2])
                    else:
                        continue
                    results = sent_classifier.infer(_text, print_result=False)
                    if results[0]['ref_check'][0] != 'Correct':
                        augmentations.extend(
                            [text.replace('%%', '$T$').replace('$*$', '$T$').replace('$-$', '$T$').replace('$ * $', '$T$'), lines[i + 1], lines[i + 2]]
                        )

            except Exception as e:
                print('Exception:{}, {}'.format(e, lines[i]))

        fout = open(valid_set.replace('Valid', 'train').replace('valid', 'train') + '.augment', encoding='utf8', mode='w')

        for line in augmentations:
            fout.write(line + '\n')
        fout.close()
    del sent_classifier
    del augmenter


def text_attack_augment(dataset: DatasetItem):
    for f in find_cwd_files('.augment'):
        os.remove(f)
    from textattack.augmentation import CheckListAugmenter
    # Alter default values if desired
    augmenter = CheckListAugmenter(pct_words_to_swap=0.3, transformations_per_example=10)

    checkpoint = max(find_cwd_dirs('fast_lcf_bert_{}'.format(dataset.dataset_name)))
    sent_classifier = APCCheckpointManager.get_sentiment_classifier(checkpoint=checkpoint,
                                                                    auto_device=True,  # Use CUDA if available
                                                                    )


    dataset_files = detect_dataset(dataset, 'apc')
    valid_sets = dataset_files['valid']

    for valid_set in valid_sets:
        if '.augment' in valid_set:
            continue
        print('processing {}'.format(valid_set))
        augmentations = []
        fin = open(valid_set, encoding='utf8', mode='r', newline='\r\n')
        lines = fin.readlines()
        fin.close()
        for i in tqdm.tqdm(range(0, len(lines), 3), postfix='Augmenting...'):
            try:
                lines[i] = lines[i].strip()
                lines[i + 1] = lines[i + 1].strip()
                lines[i + 2] = lines[i + 2].strip()

                augs = augmenter.augment(lines[i].replace('$T$', '%%'))

                for text in augs + [lines[i]]:
                    if '$ * $' in text:
                        _text = text.replace('$ * $', '[ASP]{}[ASP] '.format(lines[i + 1])) + ' !sent! {}'.format(lines[i + 2])
                    elif '$*$' in text:
                        _text = text.replace('$*$', '[ASP]{}[ASP] '.format(lines[i + 1])) + ' !sent! {}'.format(lines[i + 2])
                    elif '$-$' in text:
                        _text = text.replace('$-$', '[ASP]{}[ASP] '.format(lines[i + 1])) + ' !sent! {}'.format(lines[i + 2])
                    elif '%%' in text:
                        _text = text.replace('%%', '[ASP]{}[ASP] '.format(lines[i + 1])) + ' !sent! {}'.format(lines[i + 2])
                    else:
                        continue
                    results = sent_classifier.infer(_text, print_result=False)
                    if results[0]['ref_check'][0] != 'Correct':
                        augmentations.extend(
                            [text.replace('%%', '$T$').replace('$*$', '$T$').replace('$-$', '$T$').replace('$ * $', '$T$'), lines[i + 1], lines[i + 2]]
                        )

            except Exception as e:
                print('Exception:{}, {}'.format(e, lines[i]))

        fout = open(valid_set.replace('Valid', 'train').replace('valid', 'train') + '.augment', encoding='utf8', mode='w')

        for line in augmentations:
            fout.write(line + '\n')
        fout.close()
    del sent_classifier
    del augmenter

# if __name__ == '__main__':
#     for valid_set in detect_dataset(ABSADatasetList.SemEval, 'apc')['test']:
#         if '.augment' in valid_set:
#             continue
#         print('processing {}'.format(valid_set))
#         test_set = []
#         fin = open(valid_set, encoding='utf8', mode='r', newline='\r\n')
#         lines = fin.readlines()
#         fin.close()
#         for i in tqdm.tqdm(range(0, len(lines), 3)):
#
#                 lines[i] = lines[i].strip()
#                 lines[i + 1] = lines[i + 1].strip()
#                 lines[i + 2] = lines[i + 2].strip()
#
#                 test_set.append([lines[i], lines[i + 1], lines[i + 2]])
#
#         fout1 = open(valid_set, encoding='utf8', mode='w')
#         fout2 = open(valid_set + '.re-split', encoding='utf8', mode='w')
#
#         random.shuffle(test_set)
#
#         set1 = test_set[:len(test_set) // 2]
#         set2 = test_set[len(test_set) // 2:]
#
#         for case in set1:
#             for line in case:
#                 fout1.write(line + '\n')
#
#         for case in set2:
#             for line in case:
#                 fout2.write(line + '\n')
