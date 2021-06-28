import os
import glob
import torch

import json

class CheckpointWriter:
    def __init__(self, checkpoint_dir, model_specs):
        self.checkpoint_dir = checkpoint_dir
        if not os.path.exists(self.checkpoint_dir):
            os.mkdir(self.checkpoint_dir)
        
        # write down model specs as a json file
        with open(os.path.join(self.checkpoint_dir, 'model.json'), 'w+') as fp:
            json.dump(model_specs, fp, indent=2)


    def load(self, model, optimizer):
        # check if best checkpoint exists
        best_checkpoint_name = glob.glob(os.path.join(self.checkpoint_dir, 'best_val_snapshot*'))
        if best_checkpoint_name:
            checkpoint = torch.load(best_checkpoint_name[0])
            model.load_state_dict(checkpoint['model_state_dict'])
            # optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            ep = checkpoint['epoch']
            loss = checkpoint['loss']
            print('Resuming from previous training session with epoch: {}, loss: {:.4f}'.format(ep, loss))
        return model, optimizer

    def save(self, model, optimizer, accuracy_val, loss_val, epoch, loss):
        snapshot_path = os.path.join(self.checkpoint_dir, 'best_val_snapshot' + '_valacc_{}_valloss_{}_model.ckpt'.format(accuracy_val, loss_val))
        torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'loss': loss,
                    }, snapshot_path)
        for f in glob.glob(os.path.join(self.checkpoint_dir, 'best_val_snapshot*')):
            if f != snapshot_path:
                os.remove(f)