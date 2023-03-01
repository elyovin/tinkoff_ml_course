import typing
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas import DataFrame


def create_subplots(
        df: DataFrame,
        group_column: str,
        operate_column: str,
        is_numeric: bool = False,
        subplot_graph: go = go.Bar,
        subplot_titles: typing.List[str] = None,
        **agg_funcs: typing.Callable) -> typing.Tuple[go.Figure, DataFrame]:
    """
    Creates a plotly figure with multiple subplots to compare
    the results of two or more aggregation functions.
    The figure contains a separate subplot for each
    aggregation function specified in the **agg_funcs parameter.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame.
    group_column : str
        The name of the column to group by.
    operate_column : str
        The name of the column to apply the aggregation functions to.
    is_numeric : bool
        Whether `group_column` has numeric values
        by default False.
    subplot_graph: plotly.graph_objects, optional
        Graph object for plot drawing
        by default plotly.graph_object.Bar.
    subplot_titles : List of str, optional
        A list of strings to be used as the subplot titles,
        by default None.
    **agg_funcs : Callable
        Keyword arguments specifying the aggregation functions
        to apply to the `operate_column` for each group.

    Returns:
    --------
    fig : go.Figure
        The resulting plotly figure object.
    operated_df : pd.DataFrame
        The DataFrame resulting from applying `agg_funcs` to `operate_column`.
    """

    # Compute the results for each group
    # using the specified aggregation functions
    operated_df = (
        df
        .groupby(group_column)[operate_column]
        .agg(**agg_funcs)
        .reset_index()
    )

    # Create subplot for each aggregation function
    fig = make_subplots(
        rows=len(agg_funcs),
        cols=1,
        subplot_titles=subplot_titles
    )

    # Add a trace for each aggregation function
    for i, func_name in enumerate(agg_funcs.keys()):
        # Sort the results by the current aggregation function
        operated_df_by_func = operated_df
        if not is_numeric:
            operated_df_by_func = operated_df.sort_values(by=func_name,
                                                          ascending=False)
        # Add a bar chart trace for the current aggregation function
        fig.add_trace(
            subplot_graph(
                x=operated_df_by_func[group_column],
                y=operated_df_by_func[func_name]
            ),
            row=i+1,
            col=1
        )

        # Set subplot axis titles
        fig.update_xaxes(title_text=group_column, row=i+1, col=1)
        fig.update_yaxes(
            title_text=f'{func_name.lower().capitalize()} {operate_column.lower()}',
            row=i+1, col=1
        )

    return fig, operated_df
