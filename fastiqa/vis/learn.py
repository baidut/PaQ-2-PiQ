from ..learner import *

def clickable_scatter(x, y, xlabel, ylabel, xlim, ylim, func):
    import plotly.offline as py
    py.init_notebook_mode(connected=False)
    import plotly.graph_objects as go

    fig = go.FigureWidget([go.Scatter(x=x, y=y, mode='markers')])
    N = len(x)
    scatter = fig.data[0]
    colors = ['#a3a7e4'] * N
    scatter.marker.color = colors
    scatter.marker.size = [10] * N
    fig.layout.hovermode = 'closest'

    # create our callback function
    def update_point(trace, points, selector):
        c = list(scatter.marker.color)
        s = list(scatter.marker.size)

        for i in points.point_inds:
            c[i] = '#bae2be'
            s[i] = 20
            with fig.batch_update():
                scatter.marker.color = c
                scatter.marker.size = s
                func(i)

    scatter.on_click(update_point)
    # https://plot.ly/python/axes/#setting-the-range-of-axes-manually
    fig.update_xaxes(range=xlim)
    fig.update_yaxes(range=ylim)
    # https://plot.ly/python/figure-labels/
    fig.update_layout(
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text=xlabel
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=ylabel
            )
        ),
        autosize=False,
        width=500,
        height=500
    )
    return fig



# learn.jointplot(ylim=None)
def jointplot(self, kind="scatter", xlim=(0, 100), ylim=(0, 100), **kwargs):
    output, target = self.get_np_preds()  # TODO note here only output 1 scores
    if kind is 'plotly': #TODO, use html instead #40
        def func(i):
            row = df.iloc[i]
            print(row['name'])
            # https://docs.fast.ai/vision.image.html#ImageBBox.create
            img = open_image(self.data.path / self.data.folder / row['name'])
            img.show(figsize=(6, 6), title=row['name'])

        df = self.data.df
        if self.data.valid_pct is 1:
            pass
        elif self.data.valid_pct is None:
            df = df[df['is_valid']]
        else: raise NotImplementedError

        #x = df['niqe'].array
        #y = df['mos'].array
        return clickable_scatter(output, target, 'output', 'target', xlim, ylim, func)
    else:
        import seaborn as sns
        sns.set(style="white", color_codes=True)
        g = sns.jointplot(output, target,
                          kind=kind, xlim=xlim, ylim=ylim, **kwargs)
        return g.set_axis_labels("output", "target").annotate(stats.pearsonr)

IqaLearner.jointplot = jointplot
