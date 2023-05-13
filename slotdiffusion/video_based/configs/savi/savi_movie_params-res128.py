from nerv.training import BaseParams


class SlotAttentionParams(BaseParams):
    project = 'SlotAttention-Diffusion'

    # training settings
    gpus = 1
    max_epochs = 30
    save_interval = 0.25
    eval_interval = 1
    save_epoch_end = True
    n_samples = 8  # visualization after each epoch

    # optimizer settings
    # Adam optimizer, Cosine decay with Warmup
    optimizer = 'Adam'
    lr = 1e-4
    weight_decay = 0.0
    clip_grad = 0.05  # SA paper doesn't say any clipping?
    warmup_steps_pct = 0.025  # SA paper uses 10k steps over 500k total steps

    # data settings
    movi_level = 'e'
    dataset = 'movi'
    data_root = './data/MOVi'
    n_sample_frames = 3  # follow STEVE, SAVi uses 6
    frame_offset = 1  # no offset
    video_len = 24
    load_mask = True
    train_batch_size = 32 // gpus
    val_batch_size = train_batch_size * 2
    num_workers = 8

    # model configs
    model = 'SAVi'
    resolution = (128, 128)
    input_frames = n_sample_frames

    # Slot Attention
    slot_size = 192
    slot_dict = dict(
        # 11-23 objects on MOVi-E
        num_slots=15,
        slot_size=slot_size,
        slot_mlp_size=slot_size * 2,
        num_iterations=2,
    )

    # CNN Encoder
    enc_dict = dict(
        resnet='resnet18',
        use_layer4=False,  # True will downsample img by 8, False is 4
        # will use GN
        enc_out_channels=slot_size,
        replace_stride_with_dilation=[False, False, False],
    )

    # CNN Decoder
    # larger dec (ch=128) just doesn't work, i.e. training diverges
    dec_dict = dict(
        dec_channels=(slot_size, 64, 64, 64, 64),
        dec_resolution=(8, 8),
        dec_ks=5,
        dec_norm='',
    )

    # Predictor
    pred_dict = dict(
        pred_type='transformer',
        pred_rnn=False,
        pred_norm_first=True,
        pred_num_layers=2,
        pred_num_heads=4,
        pred_ffn_dim=slot_size * 4,
        pred_sg_every=None,
    )

    # loss configs
    loss_dict = dict(use_img_recon_loss=True, )

    img_recon_loss_w = 1.  # slots image reconstruction loss weight
