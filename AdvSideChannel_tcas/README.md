# compile program
- in `firmware/simpleserial-main/`
    - `sh windows_make_asm.sh main`
    - `sh windows_make_binary.sh main`
    - `sh windows_make_upload.sh main`

## collect data
in `SideChannelTesting/`: `sh collect_data.sh` (data will be stored in `train/` and `test/`)

## detectors training and validation
in `SideChannelDetector/`:
- training
    - for BiLSTM: `ipython train_BiLSTM.py -- -b 128 --lr 0.0003 --training ../SideChannelTesting/train --testing ../SideChannelTesting/test/ -l CHECKPOINT_NAME -e 1000 --hs 128 --nl 2 -i 8 -f FEATURE_CHOICE`   \
    - for BiRNN: `ipython train_BiLSTM.py -- -b 128 --lr 0.0003 --training ../SideChannelTesting/train --testing ../SideChannelTesting/test/ -l CHECKPOINT_NAME -e 1000 --hs 128 --nl 2 -i 8 -f FEATURE_CHOICE` \
    - for HMM: `python train_HMM.py --n-components 30 -l hmm_fft -f fft --training ../SideChannelTesting/train --testing ../SideChannelTesting/test/` 
    - flags: \

            `-b`: batch size \ 
            `--lr`: initial learning rate \ 
            `--training/testing`: data dir for training and testing \ 
            `-l`: saving checkpoint dir \
            `-e`: number of epochs \ 
            `--hs`: hidden size \
            `--nl`: number of layers \
            `-i`: size

- validation
    - in the root dir: `python validate_detectors.py --collect True --model MODEL --checkpoint CHECKPOINT_DIR`

## run the attack
- same device attack
    - in root dir: 
        - `python evading_bilstm.py --malware MALWARE --checkpoint CHECKPOINT_DIR -e EPOCHS`
        - `python evading_birnn.py --malware MALWARE --checkpoint CHECKPOINT_DIR -e EPOCHS`
        - `python evading_hmm.py --malware MALWARE --checkpoint CHECKPOINT_DIR -e EPOCHS`
    - the results are stored in `results/MODEL/FEATURE/MALWARE.txt`
- cross device attack
    - in root dir: `python cross_device.py --model MODEL --checkpoint CHECPOINT_DIR --malware MALWARE`
- cross model attack
    - in root dir: `python cross_model.py --model MODEL --target-model TARGET_MODEL --checkpoint CHECPOINT_DIR --malware MALWARE`

## adversarial training 
- make sure top 10 evading samples are generated for all the malware samples
- collect adversarial signals: 
    - (under `SideChannelTesting/`) `python collect_adv_data.py --feature FEATURE`
    - collected data will be stored in `SideChannelTesting/adv_FEATURE/`
- prepare dataset for adversarial training: 
    - (under `SideChannelTesting/`) `python train_test_split.py --source adv_FEATURE`
- train with adversarial examples (AE): 
    - (under `SideChannelDetector`) `ipython train_BiLSTMAdv.py -- -b 128 --lr 0.0003 --training ../SideChannelTesting/dataset_adv_time/train --testing ../SideChannelTesting/dataset_adv_time/test/ -l bilstm_time_adv -e 1000 --hs 128 --nl 2 -i 8 -f time` 
- attack AE-augmented detectors: 
    - (under root dir) `python evading_bilstmadv.py --malware MALWARE --checkpoint CHECKPOINT_DIR`