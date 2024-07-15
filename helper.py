import pathlib as pl

import pandas as pd
import plotly.express as px

import data


def load_all(data_path="data"):
    data_pl = pl.Path(data_path)
    data_pl_path = list(data_pl.glob("*.csv"))
    data = {f.stem: pd.read_csv(f) for f in data_pl_path}
    assert len(data) == 20
    return data


def custom_sort_key(item):
    try:
        # Try to compare the item directly
        return (0, item)
    except TypeError:
        # If there's a TypeError, convert to string for comparison
        return (1, str(item))


def get_merge_keys(keys1, keys2):
    """find common keys between the current and next df"""
    common_keys = list(set(keys1) & set(keys2))
    return common_keys if common_keys else keys1


def join_data(
    select_data_list,
    data_dict=data.data_dict,
    fixed_order=True,
    merge_keys=data.merge_keys,
    desired_join_order=data.desired_join_order,
):
    if len(select_data_list) == 0:
        pass

    if len(select_data_list) == 1:
        return data_dict[select_data_list[0]]

    if fixed_order:
        # if we have multiple datasets selected,
        # we need to join them

        # map the select_data_list to order in desired list
        order_dict = {item: idx for idx, item in enumerate(desired_join_order)}

        data_list = sorted(
            select_data_list,
            key=lambda itm: order_dict.get(itm, len(desired_join_order)),
        )
    else:
        # don't change the order of the input list
        data_list = select_data_list

    # start with first dataframe in the join order
    merged_df = data_dict[data_list[0]]
    current_keys = merge_keys[data_list[0]]

    # merge the DataFrames in the specified order
    # print("*" * 80)
    # print("\n\n")

    for key in data_list[1:]:
        # print("*" * 80)
        # print(f"merging df by key name: {key}")
        next_df = data_dict[key]
        next_keys = merge_keys[key]
        # print(f"current keys: {current_keys}")
        # print(f"next keys: {next_keys}")

        merge_keys_to_use = get_merge_keys(current_keys, next_keys)
        # print(f"merge keys to use: {merge_keys_to_use}")
        # print(f"Merge keys to use: {merge_keys_to_use}")

        merged_df = merged_df.merge(next_df, on=merge_keys_to_use, how="inner")
        current_keys = next_keys  # update current keys for the next iteration
        # print(f"new current keys: {current_keys}")

    return merged_df


def px_missing(df, col_name):
    data = df[col_name]

    missing_proportion = data.isnull().mean()
    missing_df = pd.DataFrame(
        {"column": [data.name], "proportion": [missing_proportion]}
    )

    fig = px.bar(
        missing_df,
        x="proportion",
        y="column",
        orientation="h",
        color="proportion",
        color_continuous_scale="Reds",
    )

    # Customize the layout to remove additional elements and axis labels
    fig.update_layout(
        title=None,
        xaxis=dict(
            range=[0, 1],
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            title=None,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            title=None,
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig
