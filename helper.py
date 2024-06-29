import pathlib as pl

import pandas as pd

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
    for key in data_list[1:]:
        next_df = data_dict[key]
        next_keys = merge_keys[key]
        # print(f"current keys: {current_keys}")
        # print(f"next keys: {next_keys}")

        merge_keys_to_use = get_merge_keys(current_keys, next_keys)
        # print(f"merge keys to use: {merge_keys_to_use}")

        merged_df = merged_df.merge(next_df, on=merge_keys_to_use, how="inner")
        current_keys = (
            # TODO: there's a bug here where i get when_x and when_y if demo is listed in fixed
            merge_keys_to_use  # update current keys for the next iteration
        )

    return merged_df
