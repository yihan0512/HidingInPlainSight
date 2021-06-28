import os

# from hmmlearn.hmm import GMMHMM
# from hmmlearn import hmm
import numpy as np

from .hmmutils.utils import load_data, hmm_forward, NUM_WORKERS

import glob
import pickle
from tqdm import tqdm
from multiprocessing import Pool


def inference_HMM(data_dir, model_name, win_size, feature_choice='time'):
    os.chdir('/home/cspl/Documents/projects/HidingInPlainSight/AdvSideChannel_tcas/SideChannelDetector/')
    # load test dataset
    test_data = load_data(data_dir, feature_choice=feature_choice, win_size=win_size)

    # load the model
    checkpoint = glob.glob(os.path.join(model_name, 'best_val_snapshot*'))[0]
    with open(checkpoint, 'rb') as handle:
        models = pickle.load(handle)

    pool = Pool(NUM_WORKERS)

    samples = []
    for key, value in test_data.items():
        for signal in value:
            samples.append([signal, key])
    
    jobs = []
    for sample in samples:
        job = pool.apply_async(hmm_forward, (models, sample[0], sample[1]))
        jobs.append(job)
        
    outputs = []
    for job in tqdm(jobs):
        output = job.get()
        outputs.append(output)
    

    scores = []
    labels = []
    predicted = []
    for output in outputs:
        scores.append(max(output[0].values()))
        labels.append(output[1])
        predicted.append(max(output[0], key=output[0].get))

    return np.array(scores), labels, predicted
