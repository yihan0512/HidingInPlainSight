import os
import glob
import pickle
import json

import ipdb

class CheckpointWriter:
    def __init__(self, checkpoint_dir, model_specs):
        self.checkpoint_dir = checkpoint_dir
        if not os.path.exists(self.checkpoint_dir):
            os.mkdir(self.checkpoint_dir)
        
        # write down model specs as a json file
        with open(os.path.join(self.checkpoint_dir, 'model.json'), 'w+') as fp:
            json.dump(model_specs, fp, indent=2)

    # def load(self, model, optimizer):
    #     # check if best checkpoint exists
    #     best_checkpoint_name = glob.glob(os.path.join(self.checkpoint_dir, 'best_val_snapshot*'))
    #     if best_checkpoint_name:
    #         checkpoint = torch.load(best_checkpoint_name[0])
    #         model.load_state_dict(checkpoint['model_state_dict'])
    #         # optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    #         ep = checkpoint['epoch']
    #         loss = checkpoint['loss']
    #         print('Resuming from previous training session with epoch: {}, loss: {:.4f}'.format(ep, loss))
    #     return model, optimizer

    def save(self, model, accuracy_val, likelihood_val):
        # remove existing checkpoint
        for f in glob.glob(os.path.join(self.checkpoint_dir, 'best_val_snapshot*')):
            os.remove(f)

        # save to new checkpoint
        snapshot_path = os.path.join(self.checkpoint_dir, 'best_val_snapshot_valacc_{}_vallike_{}_model.ckpt'.format(accuracy_val, likelihood_val))
        # snapshot_path = os.path.join(self.checkpoint_dir, 'best_val_snapshot.ckpt')
        with open(snapshot_path, 'wb') as handle:
            pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('checkpoint saved to {}'.format(snapshot_path))