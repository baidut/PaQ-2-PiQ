from ..learner import * # IqaLearner
# from ..labels import TestImages



class RoIPoolLearner(IqaLearner):
    def __init__(self, data: DataBunch, model: nn.Module, weight=None, **learn_kwargs):
        super().__init__(data, model, **learn_kwargs)

        if weight is not None:
            self.loss_func.weight = weight

    # def predict_quality_map(self, blk_size, img_size, **kwargs):
    #     self.model.input_block_rois(blk_size, img_size)
    #     self.get_preds(**kwargs)

    def get_quality_maps(self):
        # TODO predict in batch (according to data.batch_size)
        # get_qmaps
        """
        save all quality maps to quality maps folder
        =======================================
        im = open_image('/media/zq/Seagate/data/TestImages/Noisy Lady.png') #
        learn = e['Pool1RoIModel']
        learn.data = TestImages()
        t, a = learn.predict_quality_map(im, [[8,8]])
        print(a)
        print(t[0].data[0])  # image score
        # im
        plt.savefig('foo.png', bbox_inches='tight')
        :return:
        """
        # cannot do it in parallel (GPU)
        # only generate on valid set
        # must be data, inner_df only contain train samples and it's shuffled
        # must be loaded, since we need to call data.one_item

        # use learn.data.valid_ds with df.fn_col, no need
        # this will not load the database
        # only load the dataframe
        df = self.data.df[self.data.df.is_valid]  #.reset_index()
        #for file in df[self.data.fn_col]
            # img = open_image(self.data.path/self.data.folder/file)

        # _, ax = plt.subplots()
        fig, (ax1, ax2) = plt.subplots(2)
        names = df[self.data.fn_col].tolist()
        for n in range(len(self.data.valid_ds)):  # add progress bar
            sample = self.data.valid_ds[n][0]
            qmap = self.predict_quality_map(sample)
            qmap.show(ax=ax2)
            ax1.imshow(sample)
            dir = self.data.path/'quality_maps'/self.data.folder
            filename = str(dir/names[n]).split('.')[-2] + '.jpg'
            dir = filename.rsplit('/', 1)[0]  # 'data/CLIVE/quality_maps/Images/trainingImages/t1.jpg'
            if not os.path.exists(dir):
                os.makedirs(dir)
            plt.savefig(filename, bbox_inches='tight')

    def predict_quality_map(self, sample, blk_size=None):
        """

        :param sample: fastai.vision.image.Image  open_image()
        :param blk_size:
        :return:

        if you simply wanna quality map matrix:

        sample = open_image('img.jpg')
        self.model.input_block_rois(blk_size, [sample.shape[-2], sample.shape[-1]])
        t = self.predict(sample)
        """

        if blk_size is None:
            blk_size = [[32, 32]]  #[[8, 8]]

        if not isinstance(blk_size[0], list):
            blk_size = [blk_size]
        # input_block_rois(self, blk_size=None, img_size=[1, 1], batch_size=1, include_image=True):
        # [8, 8] #  [5, 5]
        cuda = self.data.device.type == 'cuda'
        self.model.input_block_rois(blk_size, [sample.shape[-2], sample.shape[-1]], cuda=cuda)  # self.data.img_raw_size
        # [768, 1024] [8, 8] is too big learn.data.batch_size

        # predict will first convert image to a batch according to learn.data
        # TODO backup self.data
        # this is very inefficient
        # data = self.data
        # self.data = TestImages()
        t = self.predict(sample)
        # self.data = data

        a = t[0].data[1:].reshape(blk_size[0])  # TODO only allow one blk size

        # convert sample to PIL image
        # image = PIL_Image.fromarray((255 * image2np(sample.px)).astype(np.uint8))
        return QualityMap(a, sample, t[0].data[0])

    # valid on 1 image score and 3 patch scores
    def valid_on(self, db=None, kind="scatter", idx=0, suffixes='', **kwargs):
        # TODO won't affect self.data
        # from IPython.display import display
        if db is None:
            db = self.data

        # TODO this is not consistent, use db.idx instead
        if not isinstance(db, list):
            db = [db]

        if not isinstance(idx, list):
            idx = [idx for _ in range(len(db))]

        if not isinstance(suffixes, list):
            suffixes = [suffixes for _ in range(len(db))]

        records = []
        n = 0
        for data in db:
            self.data = data
            #print(data.name)
            # self.jointplot(xlim=(0, 100), ylim=(0, 100))  # get_preds requires setting data
            # save to csv files
            csv_file = self.path / ('valid@' + data.name + suffixes[n] + '.csv')
            if os.path.isfile(csv_file):
                df = pd.read_csv(csv_file)
                output = df['output'].tolist()
                target = df['target'].tolist()
            else:
                preds = self.get_preds()
                n_output = self.data.c  # only consider image score
                # no need since metric will take care of it
                output = preds[0].flatten().numpy()[idx[n]::n_output]
                target = preds[1].flatten().numpy()[idx[n]::n_output]

                df = pd.DataFrame({'output': output, 'target': target})
                df.to_csv(csv_file, index=False)

            result = {metric.name: metric.fn(output, target)[0] for metric in self.metrics}
            records.append(result)
            #print(result)
            # sns.jointplot(output, target, kind=kind, xlim=(0, 100), ylim=(0, 100), **kwargs).set_axis_labels("output",
            #                                                                                                  "target").annotate(
            #     stats.pearsonr)
            n += 1
        """
        for data in db:
            self.callbacks = []   # TODO
            res = self.validate(data.valid_dl)
            # res = self.validate()
            # print(res)
            columns = ['valid loss'] + [metric.__name__ for metric in self.metrics]
            # df = pd.DataFrame(dict(zip(columns, res)), index=[self.model.__name__]).transpose()
            records.append(dict(zip(columns, res)))
        """
        # joinplot will clear the output, so do jointplot first
        return pd.DataFrame(records, index=[data.name + suffix for data, suffix in zip(db, suffixes)])

    # predict on database (cached) get numpy predictions
    def get_np_preds(self, on=None, cache=True):
        """
            generate according to output (image/patch1/...)
            output = preds[0]
            target = preds[1]
        :param on:
        :return:
        """
        if on is None:
            on = self.data

        idx_col = on.label_idx
        # if we don't flatten it, then we cannot store it.
        # so we need to only get the valid output
        # rois_learner gives three output csv

        # if on.c == 1:  # only output 1   call this will load the database
        #     return super().get_np_preds(on)

        suffixes = ['', '_patch_1', '_patch_2', '_patch_3']
        csv_file = self.path / ('valid@' + on.name + suffixes[idx_col] + '.csv')
        if os.path.isfile(csv_file) and cache:
            df = pd.read_csv(csv_file)
            output = df['output'].tolist()
            target = df['target'].tolist()
        else:
            current_data = self.data
            self.data = on
            preds = self.get_preds()
            self.data = current_data

            output = preds[0].flatten().numpy()
            target = preds[1].flatten().numpy()
            """
            preds is a list [output_tensor, target_tensor]
            torch.Size([8073, 4])
            """
            # we already loaded the data, so feel free to call data.c
            if cache:
                if on.c == 4:
                    for n in [0, 1, 2, 3]:
                        df = pd.DataFrame({'output': output[n::on.c], 'target': target[n::on.c]})
                        csv_file = self.path / ('valid@' + on.name + suffixes[n] + '.csv')
                        df.to_csv(csv_file, index=False)
                elif on.c == 1:
                    df = pd.DataFrame({'output': output, 'target': target})
                    df.to_csv(csv_file, index=False)
                else:
                    raise NotImplementedError

            output = output[idx_col::on.c]
            target = target[idx_col::on.c]

        return output, target
